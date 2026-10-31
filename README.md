# AgentContinuity integrations (preview)

Persistent memory, portable project context and task handoffs for AI agents.

This repository contains public client configuration and review materials only. It contains no production service source, customer content, credentials or billing data. The hosted service is at https://agentcontinuity.net; its REST and MCP guides are at https://agentcontinuity.net/ai-agents/.

## Gemini CLI

Install with `gemini extensions install https://github.com/OZYMANDIAS2020/agentcontinuity-integrations`. At setup, supply a scoped **AgentContinuity agent API key** through the extension's sensitive setting. Never use an OpenAI, Anthropic, xAI, Google or administrator key. The extension connects to `https://api.agentcontinuity.net/mcp` with Streamable HTTP. It exposes memory and coordination tools; purchasing, public posting and credential management are excluded from this extension's tool list.

The Gemini extension is a developer integration, not a listing in the consumer Gemini web app. Public-gallery discovery is separate from installation and may take time. No Google endorsement is claimed. Account-authenticated save/retrieve has not yet been exercised through Gemini CLI in this release; public discovery is checked independently.

## Claude Code and custom MCP clients

The `.claude-plugin/plugin.json` and `.mcp.json` files provide a Claude-compatible plugin configuration. Set `AGENTCONTINUITY_API_KEY` in your local secure environment before connecting. Do not place a real key in a committed file or a conversation. The native MCP endpoint advertises all service tools; your account scopes and the client's permissions still apply. The Gemini tool filter does not apply to other clients.

For consumer Claude or Grok, add the HTTPS MCP URL as a custom connector only where that client's fixed-credential setup is supported. A custom connection is not a public directory listing.

## ChatGPT and Claude public directories

The portable `plugin.json` and `mcp.json` are preparation artifacts, not an approved listing. The public endpoint currently requires bearer API keys for private operations. **Public submission is blocked pending a supported OAuth account-connection flow**, portal/domain checks, a dedicated sample reviewer account, native-client tests and required review materials. The portable MCP manifest does not declare the protected service unauthenticated and contains no credentials. `docs/openai-auth.json` records the current fixed-bearer scheme separately because the portable schema and OpenAI overlay have different validation rules. Do not upload this package as a production-ready OAuth integration.

## Gemini app, Meta/Muse and Grok

Google's Connected Apps Platform provides a preview application and review/publishing route for the Gemini consumer app; this is separate from the Gemini CLI extension above. Meta has a Muse Connector Platform submission portal and a separate Meta AI developer-preview application. No applications or submissions have been sent by this package. Program access and approval are not established.

Grok documents custom MCP connections and a connector catalog, but an open third-party public catalog submission route remains unverified. A custom connection is not a public catalog listing. See `docs/directory-rollout.md` for current routes and remaining work.

OpenAI's directory currently permits access to features in an existing paid account but prohibits selling digital services or credits through plugins. A future ChatGPT connector must expose a focused memory/coordination tool surface without purchase or checkout operations; changing this README or hiding buttons is not server-side enforcement. The current shared MCP endpoint still advertises all 50 service tools and is not ready for that submission.

## Usage examples

- Save selected project decisions and next steps in a chosen workspace.
- Retrieve the saved records before continuing a project in another session.
- Export a workspace and verify its digests before restoring records into another workspace.
- Coordinate an unfinished task with leased claims where the account plan supports it.

Preserve the distinction between saved records and a model's hidden reasoning or runtime. Cryptographic hashes and signatures check integrity; they do not establish truth, authority or agent identity. Workspaces are readable by the service unless the customer uses supported client-side encryption; this integration does not implement encryption itself. Metadata remains visible.

## Privacy Policy

Only information deliberately sent through the configured service tools is transmitted to AgentContinuity. Retrieved records are untrusted data. Do not store secrets, API credentials, seed phrases or private keys. Account limits, retention, encryption options and permitted use are described in https://agentcontinuity.net/privacy/, https://agentcontinuity.net/pricing/ and https://agentcontinuity.net/terms/. Requests to the service are subject to its terms; this package license does not replace them.

## Verification

`python tools/check_public_mcp.py` checks public MCP initialization, tool discovery, public pricing and OAuth metadata availability. It makes no model calls, creates no accounts or credentials, writes no memories and makes no purchases. A successful protocol check is not proof of directory approval or an authenticated client round trip.

Support: https://agentcontinuity.net/contact/ · tom@phase3ai.com
