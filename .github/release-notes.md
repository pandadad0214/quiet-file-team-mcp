**Install** from [PyPI](https://pypi.org/project/quiet-file-team-mcp/) (needs [uv](https://docs.astral.sh/uv/); no token or account):

```bash
uvx quiet-file-team-mcp@{{VERSION}}
```

- **Cursor / Claude / VS Code:** command `uvx`, args `["quiet-file-team-mcp"]`.
- Official MCP Registry name: `io.github.pandadad0214/quiet-file-team-mcp`.

### Changed
- `draft_owner_batch` still only drafts and deduplicates owner questions on the local machine. Its description and warning no longer say "send messages" or "message sent," which a scanner had read as an external-sink capability. The tool name is unchanged, so existing clients keep working. It does not contact anyone or deliver anything.
- No behavior change.

Full docs: [README](https://github.com/pandadad0214/quiet-file-team-mcp#readme).
