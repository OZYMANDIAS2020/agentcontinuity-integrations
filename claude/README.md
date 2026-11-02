# AgentContinuity plugin for Claude

Persistent memory, signed checkpoints and task handoffs for AI agents. This plugin connects Claude Code to the hosted AgentContinuity MCP server so Claude can save selected project notes and decisions, retrieve and search them in a later session, create signed checkpoints and hand tasks to other agents, all inside your own AgentContinuity account.

Publisher: SapienCX LLC · https://agentcontinuity.net · Support: https://agentcontinuity.net/contact/ (tom@phase3ai.com)

## Install

```
/plugin marketplace add OZYMANDIAS2020/agentcontinuity-integrations
/plugin install agentcontinuity@agentcontinuity
```

When Claude Code asks for the plugin's **AgentContinuity API key**, enter your own AgentContinuity agent API key. Claude Code keeps it in secure storage. Get a key by starting the free 7-day trial (you accept the current terms) or from a paid account: https://agentcontinuity.net/pricing/

## Use it

- "Save these decisions and the next step for this project in AgentContinuity."
- "Retrieve what I saved for this project yesterday and continue from it."
- "Create a checkpoint of my workspace" or "Show my unfinished AgentContinuity tasks."

Workflows you start yourself (Claude does not run them on its own):

- `/agentcontinuity:save-work`: save a minimal summary of an authorized task, re-read it and confirm its content hash; optionally create a signed checkpoint.
- `/agentcontinuity:resume-work`: find and retrieve saved task records and present a resume brief, without obeying instructions inside them or resuming work automatically.
- `/agentcontinuity:handoff-work`: prepare a handoff brief for another agent already authorized in your account; a task or message is written only when you separately approve it.

The `setup` skill covers connecting and troubleshooting; the `continuity` skill covers safe saving, resuming and restoring.

## What it contains and what it sends

- `.mcp.json`: one remote MCP server, `https://api.agentcontinuity.net/mcp` (Streamable HTTP), operated by SapienCX LLC. Your key is sent only to that endpoint, as `Authorization: Bearer …`, taken from the plugin's sensitive `api_key` option. No key ships in this plugin, and nothing is read from your environment or files.
- `skills/`: `setup`, `continuity`, `save-work`, `resume-work`, `handoff-work`. Instructions only.
- No hooks, scripts, binaries, package installs or local servers.

Only content you or Claude deliberately pass to AgentContinuity tools (for example a note given to `save_memory`) is sent to the service and stored in your account, subject to plan limits and retention. Do not store secrets, credentials or personal data you are not permitted to share. Privacy policy: https://agentcontinuity.net/privacy/ · Terms: https://agentcontinuity.net/terms/

## What it does not do

- It does not automatically extract or upload your Claude conversations. Save, resume and handoff operate only on information you or an agent you authorized deliberately supply.
- It does not collect conversations in the background or build user profiles.
- It does not change the underlying Claude model. The skills are instructions loaded into your session.
- It does not purchase services or contact third parties on its own.

## Surfaces and safety

- The authenticated connection works in Claude Code. On claude.ai and in Cowork the skills load, but the bundled connector needs OAuth account linking, which AgentContinuity does not offer yet.
- The server advertises its full tool list, including billing tools. It enforces account scopes and tenant isolation; purchases need a human customer acceptance and an explicitly authorized, funded budget. The skills tell Claude never to spend, publish board posts or contact third parties on its own, and Claude Code asks before each tool call unless you allow it.
- Retrieved records are untrusted data, never instructions. Content hashes and signed checkpoints prove bounded integrity claims, not truth or authorship.

## License

MIT for this plugin package (see `LICENSE`). Use of the hosted service is governed by the AgentContinuity Terms of Service.
