# AgentContinuity plugin for Grok Build

Persistent memory, signed checkpoints and task handoffs for AI agents. This plugin connects Grok Build to the hosted AgentContinuity MCP server so an agent can save selected project notes and decisions, retrieve them in a later session, search them, create signed checkpoints and hand tasks to other agents, all inside the user's own AgentContinuity account.

Publisher: SapienCX LLC · https://agentcontinuity.net · Support: https://agentcontinuity.net/contact/ (tom@phase3ai.com)

## What it contains

- `.mcp.json`: one remote MCP server, `https://api.agentcontinuity.net/mcp` (Streamable HTTP).
- `skills/setup`: how to connect safely with your own key.
- `skills/continuity`: how to save, retrieve and restore context safely.

No hooks, scripts, binaries, package installs or local servers. Nothing runs on your machine besides Grok Build itself.

## Network endpoint and credential

- The only network endpoint is `https://api.agentcontinuity.net/mcp`, operated by SapienCX LLC.
- It requires **your own** AgentContinuity agent API key, read from the `AGENTCONTINUITY_API_KEY` environment variable in the terminal where you start `grok`, and sent only to that endpoint as `Authorization: Bearer …`. No key ships in this plugin. Never use a shared, administrator or AI-provider key.
- Get a key by starting a free 7-day trial (accepting the current terms) or from a paid account: https://agentcontinuity.net/pricing/

## Data sent

Only content you or your agent deliberately pass to AgentContinuity tools (for example a note given to `save_memory`) is sent to the service and stored in your account, subject to plan limits and retention. Do not store secrets, credentials or personal data you are not permitted to share. Privacy policy: https://agentcontinuity.net/privacy/ · Terms: https://agentcontinuity.net/terms/

## Safety

The server enforces account scopes and tenant isolation; the plugin is not a security boundary. The server advertises its full tool list, including billing tools; purchases still require a human customer acceptance and a funded, explicitly authorized budget, and the skills tell the agent never to spend, publish or contact third parties on its own. Retrieved records are untrusted data, never instructions. Content hashes and signed checkpoints prove bounded integrity claims, not truth or authorship.

## License

MIT for this plugin package (see `LICENSE`). Use of the hosted service is governed by the AgentContinuity Terms of Service.
