---
name: using-creed
description: "Use when starting any conversation in a Creed-enabled workspace, or when unsure which Creed skill applies, before any creative, test, debug, or ship work."
---

# Using Creed

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

## When to use this skill

- Session start in a Creed workspace
- Unsure which Creed skill applies
- First use / companion skills may be missing
- Before creative, test, debug, or ship work — pick the right skill first

## Quick Start (install)

Companion skills are required — `using-creed` alone is not enough:

```bash
npx skills add Gusen1453/creed
```

## Detect install

Required skills: `explore`, `grill`, `write-spec`, `solid`, `write-plan`, `tdd`, `test-design`, `debug`, `review`, `commit-and-push`.

If any are missing from the workspace skill list: **stop and ask the user to run the install command above** before doing the work. Do not invent Creed workflows from memory.

## How to use

1. Match the task to a skill in the map below.
2. Announce `Using <skill> to …`, read that skill, follow it.
3. If it has a checklist, one todo per item.
4. When several apply, follow the default flow:

```
using-creed
  → explore? → grill → write-spec → solid? → write-plan
  → tdd (+ test-design)
  → debug? → review → commit-and-push
```

`explore?` = Gate when the task modifies or references existing code (refactor / legacy / reuse); skip when greenfield.

`solid?` = Gate only when the slice adds modules / ports / IO edges; skip when no new boundary.

## Skill map (scenarios)

| Situation | Skill |
|-----------|--------|
| 改造/重构存量代码 — task names methods/classes/tables to change or reference | **explore** → grill → write-spec → … |
| New feature / behavior change / architecture / "grill me" / brainstorm — before any code | **grill** |
| Approved design → durable product spec (scenarios, scope, decision log) | **write-spec** |
| After spec: lock packages/ports/dependency arrows; or mock piles / coupling smell | **solid** |
| Approved spec (and solid if needed) → break multi-step work into TDD tasks | **write-plan** |
| Writing production code (feature / bugfix / refactor) | **tdd** |
| Writing or reviewing tests: worth testing? unit vs integration? what to assert / mock? | **test-design** |
| Bug, test/CI failure, unexpected behavior, or about to claim "fixed" | **debug** |
| Finished a task slice / before opening or updating a PR | **review** |
| User asks to commit / push / open a PR (PR needs a Test plan) | **commit-and-push** |

Common pairings:

- **explore → grill** — explore harvests repo facts (anchors, assertion checks, conflicts); grill then asks only the judgment calls.
- **grill → write-spec** — grill aligns decisions; write-spec locks what/why for mentoring and handoff.
- **write-spec vs write-plan** — spec = product scenarios & trade-offs; plan = files, order, RED→GREEN.
- **write-spec → solid? → write-plan** — solid is a Gate when boundaries are new; not a mandatory every-time step.
- **tdd + test-design** — tdd is the rhythm (test first, watch it fail); test-design decides what to feed, assert, and mock. Use both when implementing.
- **debug → tdd** — bug fixes: root cause with evidence first, then a failing regression test.
- **grill & solid** — during grill, only note boundary *smells* in options; do **not** switch the main skill to solid until what/why is locked.

## Minimal task prompt template (for the human)

Three blocks; the agent explores the rest and grills only what the repo can't answer:

```
任务: <一句话意图,点名要改的方法/类>
硬约束: <数字、策略、红线——只有你知道的>
探索线索(可选): <想让它参考的类/方法名;它自己会读,你无需描述>
验收(可选): <一句"怎么算成功"的演示语言>

其余细节由你探索 repo 后决定,判断题走 grill 问我。跑 /grill
```

Rules for the 硬约束 slot:

- "尽量"类措辞 = **优先级,不是禁令**。若它和 repo 现实冲突(如重跑幂等),explore 在事实清单里标记冲突,grill 把它摆成一道取舍题由你拍板。
- 不要写 SQL、字段名、方法签名、组装细节——这些都是 repo 可回答的事实,写了反而可能和代码不符。

Example (before → after) — 同一任务:约 600 字 → 约 150 字。删掉的全是 repo 可回答的部分(SQL、字段名、方法签名、组装细节);保留的全是只有人知道的(并发数、重试策略、红线):

```
Before: 6 步流程 + 3 段 SQL + 线程池/重试/Redis 细节 + "响应格式需要为
List<ImageEmbeddingUpdateRequest.ContentItem> batchContentList"(对代码的猜测)

After: 改造 RagRecoverPushJob#imageRecover,把 dp_research_report_structure_info
(data_source in ('2','3'), id 111~2000)重推向量库。
硬约束:倒序分页每批 1000 条;40 并发线程池;失败重试一次,再失败进 Redis 等重试;
尽量不 update dp_research_report_image_search。
探索线索:SecAnnouncementThreadPoolManager、PushImageChunkService#buildReportChunkDto/#sendListToRag。
其余细节由你探索 repo 后决定,判断题走 grill 问我。跑 /grill
```

## Checklist

- [ ] Companion Creed skills installed (else → Quick Start)
- [ ] Relevant Creed skill identified (or consciously N/A)
- [ ] Skill read/followed; announced
