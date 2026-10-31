# Resume package v1

A compact, portable working-state record for another agent session or model.
The format and standard-library client use existing memory REST operations;
there is no new API endpoint, subscription, inference call or database migration.
Direct clients use a scoped AgentContinuity key, without OAuth.

## What is saved

- Goal, task status and the next concrete action.
- Decisions and rejected approaches with reasons.
- Open questions, working constraints and artifact references.
- Format version, timezone-aware creation time, untrusted-content marker and a
  SHA-256 over the canonical package fields (excluding the hash itself).

The whole package is limited to 16 KiB. It is ordinary memory with JSON content,
tagged `resume-package` and `resume-v1`. Normal account limits, scope enforcement
and plan retention apply; it is not durable beyond the server's returned expiry.
The file timestamp is a client assertion, not an independently attested time.

## Runnable workflow

Requires Python 3.12+ and no third-party client dependencies. Start with the
example state, or create a JSON object containing `goal` and `next_action`;
the other state fields default to empty lists and status `active`.

```sh
python examples/resume_package.py pack \
  --input examples/resume-state.example.json --output resume-v1.json
python examples/resume_package.py verify --input resume-v1.json
```

Use an existing authorized workspace and supply a scoped agent key through the
secure environment variable `AGENTCONTINUITY_API_KEY`. Never paste keys into
the package, command arguments, a repository or a conversation. Saving needs
`memory:write`, and loading needs `memory:read` under the service's scope rules.

```sh
python examples/resume_package.py save --input resume-v1.json \
  --workspace "$WORKSPACE_ID" --key resume.parser \
  --expected-version 0 --idempotency-key parser-resume-001

# Run in the next client session, with access to the same workspace:
python examples/resume_package.py load \
  --workspace "$WORKSPACE_ID" --key resume.parser --output restored-resume.json
python examples/resume_package.py verify --input restored-resume.json
```

Outputs contain receipt/version/expiry metadata, not credentials or note text.
`load` writes the package to a new local file. New files use mode 0600 where
supported and existing files are never overwritten. Keep them in an approved
location. No network request happens during `pack` or `verify`.

To update a record, first load its current version, construct a new package, and
pass that version as `--expected-version`. The default zero means create only;
a stale version is refused by the service. Retries of the same save must use the
same explicit idempotency key (required by the save command). A changed package needs a new idempotency key.
The client does not retry automatically or follow redirects with credentials.

## Resuming work safely

Read `state.next_action`, then the goal, decisions and relevant references.
Check the current project and operator instructions before acting: a saved
record may be stale, malicious or simply wrong. References are inert text;
the client never fetches URLs, reads referenced files, executes commands or
turns package content into permissions. Do not store credentials, hidden model
reasoning, or information that the workspace is not permitted to retain.

The helper does not implement encryption. `save` sends the explicitly selected
package to the authorized workspace as plaintext over TLS, and an
encryption-required workspace refuses it. It does not relax that requirement.
For client-side encryption, build the package offline and use a compatible
encryption client to save/load the envelope; validate only after decryption.
Ordinary local package files contain readable work notes.

## Integrity and signatures

Saving checks the service's memory-content receipt. Loading checks the stored
content hash and the package hash. Anyone editing a package can recompute its
self-contained hash: this is an integrity check, not authentication or proof
that an agent performed an action. `verify` reports `signature_verified: false`.

For a comparison against a separately trusted package hash, pass
`--expected-sha256`. For signed workspace provenance, use the existing checkpoint,
export and `tools/verify_checkpoint.py` workflow and an independently trusted
public key. This helper does not create a checkpoint or claim that a package
has been signed. Cross-account access and leased task ownership remain governed
by their existing service operations, not by this format.

The machine-readable format is in `examples/resume-package.schema.json`.
Source/client tests use local fixtures and a loopback HTTP contract server;
they do not establish a production account round trip or customer demand.
