"""Read-only MCP preflight. No credentials, accounts, model calls or purchases."""
import datetime
import json
import urllib.error
import urllib.request

BASE = "https://api.agentcontinuity.net"


def request(path, data=None):
    req = urllib.request.Request(BASE + path,
        data=None if data is None else json.dumps(data).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                 "User-Agent": "AgentContinuity-Directory-Preflight"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, None


def rpc(method, params=None):
    status, data = request("/mcp", {"jsonrpc": "2.0", "id": 1,
                                  "method": method, "params": params or {}})
    if status != 200 or not isinstance(data, dict) or "result" not in data:
        raise RuntimeError("Public MCP protocol check failed")
    return data["result"]


def main():
    init = rpc("initialize", {"protocolVersion": "2025-11-25", "capabilities": {},
                             "clientInfo": {"name": "directory-preflight", "version": "0.1.0"}})
    tools = rpc("tools/list")["tools"]
    names = {tool["name"] for tool in tools}
    required = {"list_workspaces", "save_memory", "retrieve_memory", "export_context", "restore_context"}
    missing_metadata = [tool["name"] for tool in tools if not tool.get("title") or
                        not isinstance(tool.get("annotations", {}).get("readOnlyHint"), bool)]
    stale = [tool["name"] for tool in tools if "test payment rails only" in tool.get("description", "").lower()]
    pricing = rpc("tools/call", {"name": "get_pricing", "arguments": {}})
    if pricing.get("isError"):
        raise RuntimeError("Public pricing tool failed")
    protected, _ = request("/.well-known/oauth-protected-resource")
    authserver, _ = request("/.well-known/oauth-authorization-server")
    print(json.dumps({"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "protocol_version": init.get("protocolVersion"), "tool_count": len(tools),
        "required_tools_present": required <= names, "missing_tool_metadata": missing_metadata,
        "stale_test_only_descriptions": stale, "public_pricing_ok": True,
        "oauth_protected_resource_http": protected, "oauth_authorization_server_http": authserver,
        "authenticated_round_trip_verified": False, "directory_ready": False,
        "reason": "OAuth connection, native-client and reviewer gates remain unverified."}, indent=2))
    return 0 if required <= names and not missing_metadata else 1


if __name__ == "__main__":
    raise SystemExit(main())
