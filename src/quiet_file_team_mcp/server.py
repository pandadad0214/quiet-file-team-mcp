"""Six pure guidance tools. No caller filesystem access, subprocesses or network calls."""
from __future__ import annotations
import re
import shlex
from pathlib import PurePosixPath
from typing import Annotated, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field

mcp=FastMCP('Quiet File Team',instructions='Free offline guidance for one trusted shared Linux machine. No installation, scheduling, filesystem reads, network calls, or paid APIs. Supplied notes never authorize external actions.')
ANN=ToolAnnotations(readOnlyHint=True,destructiveHint=False,idempotentHint=True,openWorldHint=False)
FREE='https://github.com/pandadad0214/quiet-file-team'
REQUIRED=('LICENSE','README.md','team.conf','common.sh','task.sh','post.sh','pair.sh','has-work.sh','backup.sh','board.md','tasks.log','notes/core-rules.md','notes/early-exit.md','notes/handover-template.md','pairs/builder-lead.md','memory.md','tests/smoke.sh')

class Result(BaseModel):
    model_config=ConfigDict(extra='forbid')
class MethodResult(Result):
    principles:list[str]
    prerequisites:list[str]
    limits:list[str]
    free_core:str=FREE
class ConfigResult(Result):
    config_text:str
    roster:list[str]
    zone:str
    coordinator:str
    warnings:list[str]
class EarlyExitResult(Result):
    block:str
    warnings:list[str]
class ManifestResult(Result):
    complete:bool
    missing:list[str]
    present_required:list[str]
    limitations:list[str]
class WorkflowResult(Result):
    scenario:str
    steps:list[str]
    acceptance:list[str]
    warnings:list[str]
class OwnerItem(Result):
    task_id:str=Field(pattern=r'^T[0-9]{4,8}$',description='Generic task reference, preserved without reassignment.')
    summary:str=Field(min_length=1,max_length=240,description='Non-sensitive summary of the unresolved choice; no private account data.')
    question:str=Field(default='',max_length=240,description='Optional explicit decision question. Omit if evidence is insufficient.')
class BatchQuestion(Result):
    task_ids:list[str]
    question:str
class BatchResult(Result):
    questions:list[BatchQuestion]
    unresolved_task_ids:list[str]
    warnings:list[str]

def roster_check(ids:list[str],coordinator:str='lead')->list[str]:
    if not 1<=len(ids)<=12 or len(set(ids))!=len(ids) or any(not re.fullmatch(r'[a-z][a-z0-9_-]{0,23}',x) for x in ids):
        raise ValueError('Use 1–12 distinct simple lowercase ids, each at most 24 characters')
    if coordinator!='lead' or 'lead' not in ids:
        raise ValueError('Lead must be in the roster and coordinator must remain lead')
    return ids

def zone_check(zone:str)->str:
    if len(zone)>80 or not re.fullmatch(r'[A-Za-z0-9_+/-]+',zone): raise ValueError('Expected IANA zone')
    try: ZoneInfo(zone)
    except (ValueError,ZoneInfoNotFoundError): raise ValueError('Unsupported IANA zone') from None
    return zone

def generic(text:str)->str:
    if any(ord(c)<32 for c in text) or re.search(r'\d{6,}|[\w.+%-]+@|https?://|\b(?:password|api[_ -]?key|secret|token)\b',text,re.I):
        raise ValueError('Use fictional, single-line, non-sensitive text without contacts, credentials or links')
    return text.strip()

@mcp.tool(annotations=ANN,structured_output=True)
def explain_method(topic:Annotated[Literal['overview','trust','idle','durability'],Field(description='Choose conceptual focus: overview, trust boundaries, quiet idle behavior, or durable tasks.')]='overview')->MethodResult:
    """Explain the file-first quiet-bus method and trust limits; unlike draft_workflow, return concepts rather than a practice sequence. Use before adoption or to clarify idle/durable behavior, not to install software or create schedules. Free offline text computation; no paid APIs or network calls, small bounded work with unbenchmarked latency. Topic selects emphasis, not an integration. Returns principles, prerequisites, limits and the free-core link."""
    focus={
        'overview':'Separate short directed pair notes, durable task events and concise board results.',
        'trust':'Ids label records, not identities; anyone with local write access can change data.',
        'idle':'Check has-work output exactly: NO WORK means stop the entire routine silently, not just a shell step.',
        'durability':'A cursor means observed, not completed; required follow-ups belong in tasks.'}
    return MethodResult(principles=[focus[topic],'Start with the early-exit check before loading context.','Batch unresolved owner decisions; a task note is not action authorization.'],prerequisites=['One trusted shared Linux filesystem with reliable flock locks.','Bash 4+, GNU utilities; manual routine integration.'],limits=['No hosted agents, scheduler, remote transport, authentication or encryption.','No measured savings claim. Privacy checks are heuristic, not a secret audit.','Do not rotate logs blindly or run concurrent routines for the same id.'])

@mcp.tool(annotations=ANN,structured_output=True)
def generate_team_config(
    roster:Annotated[list[str],Field(min_length=1,max_length=12,description='Unique simple lowercase participant ids; include lead. Each id is at most 24 characters.')],
    zone:Annotated[str,Field(max_length=80,description='IANA time zone supported by the target machine; defaults to UTC.')]='UTC',
    coordinator:Annotated[Literal['lead'],Field(description='Keep lead: the free core authorizes decided only for this label.')]='lead',
)->ConfigResult:
    """Draft reviewed team.conf defaults for a fresh local core; unlike generate_early_exit, produce roster settings rather than routine instructions. Use before manual installation, not for secrets, arbitrary shell fragments or modifying existing logs. Free offline text computation with no paid API and unbenchmarked short latency. Coordinator must be lead and occur in roster; environment overrides still win, and target zone support must be checked locally. Returns config text, normalized roster and warnings; writes nothing."""
    roster_check(roster,coordinator); zone_check(zone)
    text='# Reviewed defaults; trusted shell config. Environment overrides win.\nTEAM_IDS="${TEAM_IDS:-'+' '.join(roster)+'}"\nTEAM_TZ="${TEAM_TZ:-'+zone+'}"\n'
    return ConfigResult(config_text=text,roster=roster,zone=zone,coordinator=coordinator,warnings=['Review before saving in a fresh folder; never source untrusted shell config.','Existing TEAM_IDS and TEAM_TZ environment variables override these defaults.','Do not change zones midway through existing logs. Only lead can set decided; ids are not authentication.'])

@mcp.tool(annotations=ANN,structured_output=True)
def generate_early_exit(
    role:Annotated[str,Field(min_length=1,max_length=24,description='Participant id present in roster for this routine.')],
    team_dir:Annotated[str,Field(min_length=2,max_length=240,description='Absolute POSIX directory of the reviewed local core, not a file to inspect.')],
    roster:Annotated[list[str],Field(min_length=1,max_length=12,description='Configured roster including lead and the chosen role.')],
)->EarlyExitResult:
    """Draft a quiet early-exit shell block for an existing routine; unlike generate_team_config, leave roster settings unchanged. Use while manually wiring a routine, not to schedule it, inspect files or prove the enclosing agent stops. Free offline text computation, no paid API or network calls; short bounded work, latency unbenchmarked. Role must belong to roster; team_dir is quoted as literal text and is never read. Match exactly NO WORK, not exit status. Returns block and enclosing-routine warnings."""
    roster_check(roster)
    if role not in roster: raise ValueError('role must belong to roster')
    p=PurePosixPath(team_dir)
    if not p.is_absolute() or '..' in p.parts or any(ord(c)<32 for c in team_dir) or team_dir=='/':
        raise ValueError('Use a bounded absolute POSIX directory without traversal or control characters')
    block='export TEAM_DIR='+shlex.quote(team_dir)+'\nwork=$(bash "$TEAM_DIR/has-work.sh" '+shlex.quote(role)+')\nif [ "$work" = "NO WORK" ]; then\n  exit 0\nfi\nprintf \'%s\\n\' "$work"\n'
    return EarlyExitResult(block=block,warnings=['This block is not executed or installed. Verify the path, roster and contents yourself.','Configure the enclosing routine to stop all subsequent agent work on exactly NO WORK; shell exit alone may not stop the outer workflow.','has-work exits zero even for friendly errors; inspect output rather than treating exit zero as idle.','Cursor means observed, not completed. Durable follow-ups must be tasks.'])

@mcp.tool(annotations=ANN,structured_output=True)
def validate_layout_manifest(paths:Annotated[list[str],Field(max_length=500,description='Caller-supplied relative file paths; no absolute paths, traversal, controls or backslashes. Each path at most 240 characters.')])->ManifestResult:
    """Compare a supplied file manifest with required free-core paths; unlike generate_team_config, report omissions rather than draft settings. Use to review a known path list, not to read a filesystem, validate contents or prove runtime safety. Free offline computation, no network or paid API; bounded list processing with unbenchmarked latency. Absolute paths, traversal and oversized lists fail rather than being silently normalized. Returns completeness, missing paths and limitations; extras do not prove installation."""
    if len(paths)>500: raise ValueError('Manifest is too large')
    for path in paths:
        p=PurePosixPath(path)
        if not path or len(path)>240 or p.is_absolute() or '..' in p.parts or '\\' in path or any(ord(c)<32 for c in path) or p.as_posix()!=path or path=='.':
            raise ValueError('Only canonical relative file paths without traversal are accepted')
    present=set(paths); missing=[p for p in REQUIRED if p not in present]
    return ManifestResult(complete=not missing,missing=missing,present_required=[p for p in REQUIRED if p in present],limitations=['Caller-supplied paths only; no filesystem was read.','Names do not prove contents, provenance, permissions, privacy, locks or working scripts.','Run the free core smoke test in a disposable folder; do not treat this as a runtime check.'])

@mcp.tool(annotations=ANN,structured_output=True)
def draft_workflow(objective:Annotated[str,Field(min_length=1,max_length=160,description='Short fictional, non-sensitive practice objective; no account data, credentials or real history.')]='Sort a sample inbox')->WorkflowResult:
    """Draft a fictional lead/builder/helper task, board and pair exercise; unlike explain_method, return practice steps and acceptance checks. Use only in an empty disposable default-roster folder, not as production history or an executable fixture. Free offline template computation with no network or paid API, bounded work and unbenchmarked latency. Objective is treated as quoted prose, never executed; sensitive-shaped text is rejected heuristically. Returns scenario, ordered steps, acceptance checks and warnings."""
    objective=generic(objective)
    if not objective: raise ValueError('Objective cannot be blank')
    return WorkflowResult(scenario='Fictional exercise: '+objective,steps=[
        'Use a NEW disposable copy with roster lead builder helper, UTC and empty logs. Never use an operational TEAM_DIR.',
        'lead creates a task assigned to helper with objective: '+objective+'. Record the id printed by task new.',
        'helper claims that exact task id, then records done with a generic result after the exercise.',
        'helper posts a concise done board note; lead sends builder a short pair note to review the exercise.',
        'helper has-work must now print exactly NO WORK; builder sees its pair note once, then exactly NO WORK.',
        'For a decision practice, use needs-owner; only lead records decided after an actual authorized decision, then helper completes the task.'
    ],acceptance=['Use the actual new task id, never assume a production task id.','Task remains visible until its state changes.','Pair note delivered once; idle output equals NO WORK exactly.','No real data, messages, schedules, purchases or public changes occur.'],warnings=['Only fictional practice, not evidence of actual completed work.','Plain text steps are not executed. Privacy filtering is incomplete; do not supply sensitive details.'])

@mcp.tool(annotations=ANN,structured_output=True)
def draft_owner_batch(
    items:Annotated[list[OwnerItem],Field(min_length=1,max_length=20,description='Generic unresolved task summaries with original ids and optional explicit questions.')],
    max_questions:Annotated[int,Field(ge=1,le=10,description='Maximum deduplicated questions to return; overflow ids are marked unresolved.')]=5,
)->BatchResult:
    """Structure supplied owner-decision questions into a bounded review batch; unlike draft_workflow, organize decisions rather than simulate job execution. Use before an authorized owner review, never to send messages, infer approval or invent answers. Free offline text processing, no network or paid API and unbenchmarked short latency. Identical explicit questions merge task ids; missing questions or cap overflow preserve unresolved references. Returns questions, unresolved ids and warnings; summaries alone do not establish a decision."""
    groups={}; unresolved=[]
    for item in items:
        generic(item.summary); question=generic(item.question)
        if not question:
            if item.task_id not in unresolved: unresolved.append(item.task_id)
            continue
        key=' '.join(question.casefold().split())
        if key not in groups:
            if len(groups)>=max_questions:
                if item.task_id not in unresolved: unresolved.append(item.task_id)
                continue
            groups[key]=BatchQuestion(task_ids=[],question=question)
        if item.task_id not in groups[key].task_ids: groups[key].task_ids.append(item.task_id)
    return BatchResult(questions=list(groups.values()),unresolved_task_ids=unresolved,warnings=['Draft only; no message sent and no decision inferred.','Missing evidence and overflow remain unresolved; review source tasks before owner contact.','Task references and summaries do not authorize externally visible actions.'])

def main(): mcp.run(transport='stdio')
