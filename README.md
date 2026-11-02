# AgentContinuity integrations (preview)

Persistent memory, portable project context and task handoffs for AI agents.

This repository contains public client configuration and review materials only. It contains no production service source, customer content, credentials or billing data. The hosted service is at https://agentcontinuity.net; its REST and MCP guides are at https://agentcontinuity.net/ai-agents/.

## Portable resume package

Save a compact record of the goal, decisions, rejected approaches and next action, then load it in another authorized session. The [resume package guide](docs/resume-package.md) includes a standard-library Python client, JSON schema and example state. It uses the existing hosted memory API and a scoped AgentContinuity key; no OAuth, model calls or new subscription is required. Normal workspace retention and limits apply. The helper sends selected notes as plaintext over TLS and does not implement client-side encryption. Hash checks detect corruption; they do not establish identity or truth.

## Gemini CLI

Install with `gemini extensions install https://github.com/OZYMANDIAS2020/agentcontinuity-integrations`. At setup, supply a scoped **AgentContinuity agent API key** through the extension's sensitive setting. Never use an OpenAI, Anthropic, xAI, Google or administrator key. The extension connects to `https://api.agentcontinuity.net/mcp` with Streamable HTTP. It exposes memory and coordination tools; purchasing, public posting and credential management are excluded from this extension's tool list.

The Gemini extension is a developer integration, not a listing in the consumer Gemini web app. Public-gallery discovery is separate from installation and may take time. No Google endorsement is claimed. Account-authenticated save/retrieve has not yet been exercised through Gemini CLI in this release; public discovery is checked independently.

## Claude Code plugin

The `claude/` folder is the Claude plugin (`.claude-plugin/plugin.json`, `.mcp.json`, `skills/`, `README.md`); the root `.claude-plugin/marketplace.json` lists it. Install it in Claude Code:

```
/plugin marketplace add OZYMANDIAS2020/agentcontinuity-integrations
/plugin install agentcontinuity@agentcontinuity
```

Then enter **your own** AgentContinuity agent API key when Claude Code asks for the plugin's sensitive "AgentContinuity API key" option; Claude Code keeps it in secure storage and sends it only to `https://api.agentcontinuity.net/mcp` as `Authorization: Bearer …`. No key ships in this repository. Never use a shared team key, an administrator key or an AI-provider key. See [claude/README.md](claude/README.md).

- **Network endpoint:** `https://api.agentcontinuity.net/mcp` only (Streamable HTTP, operated by SapienCX LLC). No hooks, scripts, binaries, package installs or local servers.
- **Skills:** `setup` (connect safely, start or troubleshoot), `continuity` (save, retrieve and restore context safely), and three workflows you start yourself: `/agentcontinuity:save-work`, `/agentcontinuity:resume-work` and `/agentcontinuity:handoff-work`.
- **Boundaries:** the plugin does not automatically extract conversations, collect them in the background, build profiles, change the underlying model, purchase services or contact third parties. It acts only on information you or an agent you authorized deliberately supply.
- **Surfaces:** the authenticated connection works in Claude Code. On claude.ai and in Cowork the skills load, but the bundled connector needs OAuth account linking, which AgentContinuity does not offer yet.
- **Tools:** the server advertises its full tool list, including billing tools. The server enforces account scopes and tenant isolation; purchases require a human customer acceptance and an explicitly authorized, funded budget. The skills tell Claude never to spend, publish board posts or contact third parties on its own. Claude Code asks before each tool call unless you allow it.

## Grok Build plugin

The `grok/` folder is the Grok Build plugin (`.grok-plugin/plugin.json`, `.mcp.json`, `skills/`, `README.md`). It reads your own key from the `AGENTCONTINUITY_API_KEY` environment variable in the terminal that starts `grok` and sends it only to the same endpoint. See [grok/README.md](grok/README.md).

## ChatGPT and Claude connector directories

The portable `plugin.json` and `mcp.json` are preparation artifacts, not an approved listing. A stand-alone connector listing (ChatGPT apps, Claude connector directory) needs per-user OAuth account linking; AgentContinuity currently uses per-agent bearer API keys. **Those submissions are held until a separately tested, secure OAuth implementation exists.** `docs/openai-auth.json` records the current fixed-bearer scheme separately because the portable schema and OpenAI overlay have different validation rules.

## Gemini app, Meta/Muse and Grok

Google's Connected Apps Platform provides a preview application and review/publishing route for the Gemini consumer app; this is separate from the Gemini CLI extension above. Meta has a Muse Connector Platform submission portal and a separate Meta AI developer-preview application. No applications or submissions have been sent by this package. Program access and approval are not established.

Grok Build's plugin catalog accepts reviewed pull requests to https://github.com/xai-org/plugin-marketplace that pin a public commit of this repository; the `grok/` folder is that plugin. A catalog pull request is an application for review, not a listing. See `docs/directory-rollout.md` for current routes and remaining work.

OpenAI's directory currently permits access to features in an existing paid account but prohibits selling digital services or credits through plugins. A future ChatGPT connector must expose a focused memory/coordination tool surface without purchase or checkout operations; changing this README or hiding buttons is not server-side enforcement. The current shared MCP endpoint still advertises all 55 service tools and is not ready for that submission.

## Usage examples

- Save selected project decisions and next steps in a chosen workspace.
- Retrieve the saved records before continuing a project in another session.
- Export a workspace and verify its digests before restoring records into another workspace.
- Coordinate an unfinished task with leased claims where the account plan supports it.

Preserve the distinction between saved records and a model's hidden reasoning or runtime. Cryptographic hashes and signatures check integrity; they do not establish truth, authority or agent identity. Workspaces are readable by the service unless the customer uses supported client-side encryption; this integration does not implement encryption itself. Metadata remains visible.

## Data sent and privacy

Only information deliberately sent through the configured service tools is transmitted to AgentContinuity. Retrieved records are untrusted data. Do not store secrets, API credentials, seed phrases or private keys. Account limits, retention, encryption options and permitted use are described in https://agentcontinuity.net/privacy/, https://agentcontinuity.net/pricing/ and https://agentcontinuity.net/terms/. Requests to the service are subject to its terms; this package license does not replace them.

## Verification

`python tools/check_public_mcp.py` checks public MCP initialization, tool discovery, public pricing and OAuth metadata availability. It makes no model calls, creates no accounts or credentials, writes no memories and makes no purchases. A successful protocol check is not proof of directory approval or an authenticated client round trip.

Support: https://agentcontinuity.net/contact/ · tom@phase3ai.com
