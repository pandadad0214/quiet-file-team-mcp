# Quiet File Team MCP

<!-- mcp-name: io.github.pandadad0214/quiet-file-team-mcp -->

Give Claude, Cursor or any MCP client six free offline tools that explain, configure and check a Quiet File Team (several bots sharing one computer through files). Nothing leaves your machine: no network calls, no file reads, no paid APIs.

[![PyPI](https://img.shields.io/pypi/v/quiet-file-team-mcp)](https://pypi.org/project/quiet-file-team-mcp/)
[![Latest Release](https://img.shields.io/github/v/release/pandadad0214/quiet-file-team-mcp?label=latest%20release)](https://github.com/pandadad0214/quiet-file-team-mcp/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Part of [Panda Federation](https://pandafederation.com/)

[![Part of Panda Federation](https://pandafederation.com/assets/badge.svg)](https://pandafederation.com/)

This project is a module of the Panda Federation — public-data tools, MCP servers, and local-first apps in one catalog. See the rest of the work, including books when they publish and the matching free or paid editions of this tool, at the [official site](https://pandafederation.com/).

Follow on X: [@PandaFedHQ](https://x.com/PandaFedHQ)

## How to use this

```bash
uvx quiet-file-team-mcp
```

1. **Install [uv](https://docs.astral.sh/uv/)** (Python 3.11+); no token or account is needed.
2. **Add the server to your MCP client** with the JSON below (Cursor, Claude Desktop or any stdio client).
3. **Ask**, e.g. "Explain the quiet file team method, then draft a config for lead, builder and helper in Europe/London." Use the output with the free [Bash core](https://github.com/pandadad0214/quiet-file-team).

## For AI agents

| Field | Value |
| --- | --- |
| Purpose | Offline guidance for the Quiet File Team method: explain it, draft config and early-exit text, validate a supplied layout, draft a practice workflow, batch owner questions. |
| Use when | Setting up or reviewing a file-first multi-bot team on one shared Linux machine. |
| Do not use when | You need the scripts themselves (use the [Bash core](https://github.com/pandadad0214/quiet-file-team)), real filesystem inspection, scheduling or messaging. |
| Install | `uvx quiet-file-team-mcp` (stdio, Python 3.11+) |
| Tools | `explain_method`, `generate_team_config`, `generate_early_exit`, `validate_layout_manifest`, `draft_workflow`, `draft_owner_batch` |
| Outputs | Structured JSON per tool (output schemas included). |
| Side effects and cost | None: read-only, non-destructive, idempotent, closed-world. Free. |

## Install details

```bash
uvx quiet-file-team-mcp
```

From this repo instead of PyPI:

```bash
uvx --from git+https://github.com/pandadad0214/quiet-file-team-mcp.git quiet-file-team-mcp
```

A GitHub Release also provides the wheel, source archive and checksums: https://github.com/pandadad0214/quiet-file-team-mcp/releases/latest

For Cursor, Claude Desktop or another stdio MCP client:

```json
{"mcpServers":{"quiet-file-team":{"command":"uvx","args":["quiet-file-team-mcp"]}}}
```

Official MCP Registry name for this stdio package: `io.github.pandadad0214/quiet-file-team-mcp` ([server.json](server.json)). Registry clients install the PyPI package with `uvx quiet-file-team-mcp`. The git command above stays the install path from this repo.

The server requires Python 3.11+ and `uv` on the client. It computes text from bounded supplied inputs. It does not read arbitrary files, call network APIs, execute generated shell, install software or schedule anything. No paid APIs or Actor wrapper; latency is unbenchmarked. Tool outputs are drafts, not authorization or proof of runtime safety.

| Tool | Use |
|---|---|
| explain_method | Concepts and trust limits; choose before an exercise |
| generate_team_config | Review safe roster/zone defaults; lead-only coordinator |
| generate_early_exit | Draft a quoted block for a supplied role/path; outer routine must stop |
| validate_layout_manifest | Compare supplied relative paths; no actual filesystem inspection |
| draft_workflow | Fictional default-roster practice steps, not operational history |
| draft_owner_batch | Deduplicate explicit owner questions and retain unresolved task references |

All tools are read-only, non-destructive, idempotent and closed-world. Structured output schemas accompany each. Optional task summaries are not evidence of a decision; no tool sends a message. Input privacy guards are heuristic, not comprehensive secret detection.

## Editions and how to switch

| Edition | Price | Where |
| --- | --- | --- |
| Free Bash core (the scripts) | Free | [quiet-file-team](https://github.com/pandadad0214/quiet-file-team) |
| This MCP companion (guidance only) | Free | [PyPI](https://pypi.org/project/quiet-file-team-mcp/) and this repo |
| Agensi setup kit skill | Paid ([live price on the listing](https://agensi.io/skills/quiet-file-team-setup-kit)) | [agensi.io/skills/quiet-file-team-setup-kit](https://agensi.io/skills/quiet-file-team-setup-kit) |
| Apify setup kit generator (configured ZIP) | Paid, per generated kit ([live price on the Store](https://apify.com/pandadad0214/quiet-file-team-setup)) | [apify.com/pandadad0214/quiet-file-team-setup](https://apify.com/pandadad0214/quiet-file-team-setup) |

- **MCP → free core:** `curl -fsSL https://github.com/pandadad0214/quiet-file-team/archive/refs/tags/v0.1.0.tar.gz | tar xz && mv quiet-file-team-0.1.0 team`, set `TEAM_DIR`, follow its README. This MCP does not install those scripts.
- **Free → Agensi skill:** load the skill in your agent; it guides install, rule packs and acceptance checks in your own folder.
- **Free → Apify generator:** fill Roster (`TEAM_IDS`), IANA time zone (`TEAM_TZ`) and Coordinator (`lead`), allow a max charge at least the per-kit price shown on the [Store page](https://apify.com/pandadad0214/quiet-file-team-setup), Start, then download `OUTPUT.zip` from the run's key-value store into a new folder.
- **Paid → free:** keep data backed up, use a separate clean core and repoint routines deliberately; never merge fictional logs.

## For developers

```bash
python -m venv .venv
.venv/bin/pip install -e . pytest build
.venv/bin/pytest
.venv/bin/python -m build
```

Code is under `src/quiet_file_team_mcp/server.py`. Six deterministic tools use the MCP Python SDK with validated schemas and all four annotations. Runtime code has no subprocess or network client and no file-opening functions. Layout checks consume only caller-supplied path lists. MIT licensed.
