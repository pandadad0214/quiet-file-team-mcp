import asyncio
import subprocess
import sys

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import ValidationError

from quiet_file_team_mcp.server import (
    REQUIRED,
    OwnerItem,
    draft_owner_batch,
    draft_workflow,
    explain_method,
    generate_early_exit,
    generate_team_config,
    mcp,
    validate_layout_manifest,
)


def test_explain():
    for topic in ["overview", "idle", "durability", "trust"]:
        r = explain_method(topic)
        assert r.principles and r.limits and r.free_core.startswith("https://github.com/")


def test_config():
    r = generate_team_config(["lead", "writer"], "America/Phoenix")
    assert "${TEAM_IDS:-lead writer}" in r.config_text
    assert "${TEAM_TZ:-America/Phoenix}" in r.config_text
    for ids in (["lead", "lead"], ["helper"], ["lead", "x;false"], ["lead", "a" * 25], []):
        with pytest.raises(ValueError):
            generate_team_config(ids)
    with pytest.raises(ValueError):
        generate_team_config(["lead"], "Invalid/Zone")
    with pytest.raises(ValueError):
        generate_team_config(["lead", "builder"], coordinator="builder")
    with pytest.raises(ValueError):
        generate_team_config(["lead"], "$(false)")


def test_early_exit():
    r = generate_early_exit("helper", "/tmp/sample folder'quote", ["lead", "helper"])
    assert "NO WORK" in r.block
    syntax = subprocess.run(["bash", "-n"], input=r.block, text=True, capture_output=True)
    assert syntax.returncode == 0
    for path in ("relative", "/tmp/../x", "/", "/tmp/line\nexit"):
        with pytest.raises(ValueError):
            generate_early_exit("helper", path, ["lead", "helper"])
    with pytest.raises(ValueError):
        generate_early_exit("builder", "/tmp/x", ["lead", "helper"])


def test_manifest():
    assert validate_layout_manifest(list(REQUIRED)).complete
    r = validate_layout_manifest(["task.sh"])
    assert not r.complete and "team.conf" in r.missing
    for paths in (["../etc/passwd"], ["/etc/passwd"], ["a/../b"], ["./x"], ["a\\b"], ["x"] * 501, ["a\nx"], ["a//b"]):
        with pytest.raises(ValueError):
            validate_layout_manifest(paths)


def test_workflow():
    r = draft_workflow("Sort a sample list")
    assert "Fictional" in r.scenario and "NO WORK" in " ".join(r.steps)
    assert r.acceptance and r.warnings
    for text in ["example https://invalid.test", "password value", "a\nline", "1234567", ""]:
        with pytest.raises(ValueError):
            draft_workflow(text)


def test_batch():
    items = [
        OwnerItem(task_id="T0001", summary="Demo order", question="Choose demo order?"),
        OwnerItem(task_id="T0002", summary="Demo order", question="choose demo order?"),
        OwnerItem(task_id="T0003", summary="Missing evidence"),
        OwnerItem(task_id="T0004", summary="Second decision", question="Pick a demo color?"),
    ]
    r = draft_owner_batch(items, 1)
    assert r.questions[0].task_ids == ["T0001", "T0002"]
    assert r.unresolved_task_ids == ["T0003", "T0004"]
    with pytest.raises(ValidationError):
        OwnerItem(task_id="../file", summary="Demo")
    with pytest.raises(ValueError):
        draft_owner_batch([OwnerItem(task_id="T0001", summary="api key value")])


def test_schemas_annotations_and_six_tools():
    tools = asyncio.run(mcp.list_tools())
    assert len(tools) == 6
    for tool in tools:
        assert tool.outputSchema
        assert tool.annotations.readOnlyHint is True
        assert tool.annotations.destructiveHint is False
        assert tool.annotations.idempotentHint is True
        assert tool.annotations.openWorldHint is False
        for word in ("unlike", "Free", "latency", "Returns"):
            assert word in tool.description
        if tool.name == "draft_owner_batch":
            lowered = tool.description.lower()
            assert "send_message" not in lowered
            assert "send messages" not in lowered
            assert "message sent" not in lowered
        for field, schema in tool.inputSchema["properties"].items():
            assert schema.get("description"), (tool.name, field)


def test_stdio_protocol_all_six():
    async def check():
        params = StdioServerParameters(command=sys.executable, args=["-m", "quiet_file_team_mcp"])
        async with stdio_client(params) as (reader, writer), ClientSession(reader, writer) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert len(tools.tools) == 6
            cases = {
                "explain_method": {},
                "generate_team_config": {"roster": ["lead", "builder", "helper"]},
                "generate_early_exit": {"role": "helper", "team_dir": "/tmp/sample", "roster": ["lead", "helper"]},
                "validate_layout_manifest": {"paths": list(REQUIRED)},
                "draft_workflow": {},
                "draft_owner_batch": {
                    "items": [{"task_id": "T0001", "summary": "Demo question", "question": "Choose demo order?"}]
                },
            }
            for name, arguments in cases.items():
                result = await session.call_tool(name, arguments)
                assert not result.isError, (name, result)
                assert result.structuredContent
            result = await session.call_tool("generate_team_config", {"roster": ["lead"], "coordinator": "builder"})
            assert result.isError
            result = await session.call_tool("draft_owner_batch", {"items": [], "max_questions": 0})
            assert result.isError
            result = await session.call_tool("explain_method", {"topic": "unsupported"})
            assert result.isError

    asyncio.run(check())
