# Quiet File Team MCP

Six free offline guidance tools for a file-first quiet team on one trusted shared Linux machine.

## Install / Use

```bash
uvx --from git+https://github.com/pandadad0214/quiet-file-team-mcp.git@v0.1.0 quiet-file-team-mcp
```

A GitHub Release also provides the wheel, source archive and checksums: https://github.com/pandadad0214/quiet-file-team-mcp/releases/latest

For Cursor, Claude Desktop or another stdio MCP client:

```json
{"mcpServers":{"quiet-file-team":{"command":"uvx","args":["--from","git+https://github.com/pandadad0214/quiet-file-team-mcp.git@v0.1.0","quiet-file-team-mcp"]}}}
```

The server requires Python 3.11+ and `uv` on the client. It computes text from bounded supplied inputs. It does not read arbitrary files, call network APIs, execute generated shell, install software or schedule anything. No paid APIs or Actor wrapper; latency is unbenchmarked. Tool outputs are drafts, not authorization or proof of runtime safety. No PyPI package is claimed.

| Tool | Use |
|---|---|
| explain_method | Concepts and trust limits; choose before an exercise |
| generate_team_config | Review safe roster/zone defaults; lead-only coordinator |
| generate_early_exit | Draft a quoted block for a supplied role/path; outer routine must stop |
| validate_layout_manifest | Compare supplied relative paths; no actual filesystem inspection |
| draft_workflow | Fictional default-roster practice steps, not operational history |
| draft_owner_batch | Deduplicate explicit owner questions and retain unresolved task references |

All tools are read-only, non-destructive, idempotent and closed-world. Structured output schemas accompany each. Optional task summaries are not evidence of a decision; no tool sends a message. Input privacy guards are heuristic, not comprehensive secret detection.

## Free core / editions

The usable free Bash core is https://github.com/pandadad0214/quiet-file-team. To install it: `git clone https://github.com/pandadad0214/quiet-file-team.git`, set TEAM_DIR to the checkout, follow its README and smoke test in a disposable copy. This guidance MCP does not replace or install those scripts.

A paid setup kit is planned but not for sale yet; there is no paid listing asserted here. The free path needs no purchase. If switching to free-only from optional guidance, keep current data backed up, use a separate clean core and repoint routines deliberately; never merge fictional logs.

## For developers

```bash
python -m venv .venv
.venv/bin/pip install -e . pytest build
.venv/bin/pytest
.venv/bin/python -m build
```

Code is under `src/quiet_file_team_mcp/server.py`. Six deterministic tools use the MCP Python SDK with validated schemas and all four annotations. Runtime code has no subprocess or network client and no file-opening functions. Layout checks consume only caller-supplied path lists. MIT licensed.
