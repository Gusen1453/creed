# 打通 issue（issue 技能）实施计划

> **For agents:** Use Creed **tdd** + **test-design** per task. Optional: Superpowers subagent-driven-development / executing-plans.

**Goal:** 新增 `skills/issue/` 技能，让 agent 能把一个想法或缺陷变成平台上一条可追踪、可回链、别人能接手的 issue（自带三档模板、创建前先搜重、只映射仓内已有标签、给分支名建议）。

**Architecture:** **无新边界。** 技能是同级文本单元，彼此不 import；唯一的跨单元接口是四处"薄耦合"（grill 网关 / write-spec header / commit-and-push 的 `Closes` 与 voice / using-creed 的清单），全是单向的文本引用，不存在 A→B→A。所以 **solid 门跳过**（这也是 spec §6「接口约定」那一节存在的意义：它替 solid 把箭头方向写死了）。

**Tech Stack:** 纯 Markdown + 已有的 `gh` 2.97 / `glab` 1.114。仓库**没有测试框架**（无 package.json / pytest / Makefile）——见下面的"验证方式"。

**Cases (from test-design):** 本仓是文档仓，test-design 的常规问题（unit vs integration、mock 密度）在这里不适用；这里"可证伪的断言"就是 spec §5 的验收项。挑出真正**独立可验**的七条，作为各任务的 RED：

1. **冷启动建 bug** —— 用户说"记一下这个 bug"并给出症状/复现 → 应产出 bug 模板四段草稿，且**点头前远端零写入**（`gh issue list` 条数不变）。
2. **仓内模板优先** —— 目标仓已有自己的模板 → 应读仓内那份的段落名，而不是 `assets/` 那份。
3. **搜重不自动决定** —— 草稿与已有 issue 重合 → 应先列候选、再问"更新/另开/取消"，不替用户选。
4. **零标签仓不带标签** —— 仓内没有语义对得上的标签 → 应**不带**标签，而不是新建一个（GitLab 会自动新建，是实测的坑）。
5. **触发** —— 用户把一件事挂起来（含"这段先放着"这类近似句）→ 应开口；只说闲话、或在办/已完成的事 → 不开口。三种条件打架时，"被挂起来"压过"正在做"。
6. **GitLab 不可逆要讲明** —— 在 GitLab 上发出前，确认话术里必须出现"只能关闭、删不掉"。
7. **失败不自动重试** —— 搜重或创建失败 → 应先确认远端状态，绝不第二次创建。

**验证方式（本仓特色，必须先说清）：** 没有测试运行器，所以每个任务的 RED/GREEN 用**可执行的断言命令**代替 —— 断言在改动前**必须失败**（RED，例如目录还不存在、字符串还没出现），改动后**必须通过**（GREEN）。这不是走形式：spec §5 里的 `[静态]` 条目本来就是这种检查。真正需要跑起来的（第 7 个任务）单列在最后。

## Global Constraints

以下逐字来自 spec，实施时不得偏离：

- **模板读法**：自己读模板文件、把内容拼进正文；**不用 CLI 的 `--template`**（实测非交互必报错）。
- **创建命令**：gh `-t <title> -F <body.md>`；glab `-t <title> -d "$(cat body.md)"` + `-y`。两者都没有 `--json`，号从 URL 尾数或 `issue list` 拿。
- **搜重**：gh `gh issue list -s all -S "<kw>"`；glab `glab issue list -A --search "<kw>" --in title,description`。`-s all` 与 `-A` 都**不能省**。
- **标签**：只映射仓内已有；GitLab 上必须先 `glab label list` 拿名单。
- **正文保真**：验收口径是"除已知规范化外一致"（gh 多一个尾换行；glab LF→CRLF）。
- **落盘**：只写本仓宿主对应的那一个目录，三档共三个文件；写完必须说"这三个文件还没提交"。
- **创建一律先问**；**GitLab 上额外说明**"只能关闭、删不掉"。
- **模板正文不留 `<!-- 注释 -->`**（落盘时追加的那行同步说明是唯一例外）。
- **技能文件用英文**（仓库惯例，见 04e474b）；**输出跟随用户语言**（技能内保留那行 output-language 规则）。
- 证据标记要带进技能文件，不许把"核源码"写成"实测"。**写法按仓库的 English-only 惯例用 `[measured]` / `[source-checked]`**（技能文件是英文的）—— 语义不许换。
- **不动** `skills/explore`、`debug`、`review`、`solid`、`tdd`、`test-design`、`write-plan`。

---

### Task 1: 模板系统（三档 assets + 选择规则）

**Files:**
- Create: `skills/issue/assets/bug-report.md`
- Create: `skills/issue/assets/feature-request.md`
- Create: `skills/issue/assets/custom.md`
- Create: `skills/issue/references/templates.md`

**Interfaces:**
- Produces: 三个模板文件（Task 3 的 create 流程要读它们）；`templates.md` 定下"仓内优先 → assets 兜底 → 都无则直拼 body"的选择规则，Task 3 引用它。

**内容要点：**
- 三份模板各带 front matter（`name` / `about` / `labels`），`labels` **留空**不写死。
- 段落：bug = 症状 / 复现 / 期望 vs 实际 / 环境；feature = 背景 / 期望结果 / 验收怎么算过 / 已排除的替代方案；custom = 背景 / 想要什么 / 边界。
- 正文用占位符，**不留** HTML 注释。
- `templates.md` 写清：先探 `.github/ISSUE_TEMPLATE/`（GitHub）或 `.gitlab/issue_templates/`（GitLab）；命中就用它的**段落名**；没命中用 `assets/` 里那份；宿主认不出则直拼 body。
- 落盘规则也写在这里：只写一个目录、三个文件、写完声明未提交。

- [ ] **Step 1: 写断言（RED）** —— `ls skills/issue/assets/*.md | wc -l` 期望 3；`grep -rn '<!--' skills/issue/assets/` 期望 0 命中；`grep -c 'labels:' skills/issue/assets/*.md` 期望 3。
- [ ] **Step 2: 跑一遍，确认 FAIL** —— 三条都会失败（目录不存在 / 文件不存在）。
- [ ] **Step 3: 写四个文件** —— 按上面要点。
- [ ] **Step 4: 跑断言，确认 PASS** —— 同 Step 1 三条全过；再人工读一遍三份模板，确认没有空段落、没有占位符漏填。
- [ ] **Step 5: Commit** —— `feat(issue): add the three issue templates and their selection rules`

---

### Task 2: 宿主事实（host-cli.md）

**Files:**
- Create: `skills/issue/references/host-cli.md`

**Interfaces:**
- Consumes: `skills/commit-and-push/references/host-cli.md`（共用坑表，只**指向**不抄）。
- Produces: issue 侧命令表，Task 3 的 create 流程按它执行。

**内容要点（全部来自 spec §6，逐条带 `[实跑]`/`[核源码]`）：**
- 模板不能用 CLI 给（三条报错原文 + `create.go` 的根因）。
- 创建命令（gh `-F` / glab `-d` + `-y`），以及"都没有 `--json`，号怎么拿"。
- 搜重命令，以及 **`-s all` / `-A` 不能省**（非交互默认只列 open）。
- 标签：gh 硬校验整体失败；**GitLab 会自动建标签** ⇒ 必须先 `glab label list`。
- 正文保真：gh 多尾换行、glab LF→CRLF ⇒ 回读 diff 前先归一化行尾与尾部空行。
- 误建收敛：gh `delete --yes` 可用；**glab 403**，只能 close + 标注。
- `#N` 回链键：两个仓的分支名都不带号 ⇒ 号从会话带过去。
- 共用部分（`gh auth setup-git`、`glab api -f` vs `-F`、写后回读）**只指向** `../../commit-and-push/references/host-cli.md`。

- [ ] **Step 1: 写断言（RED）** —— `ls skills/issue/references/../../commit-and-push/references/host-cli.md` 期望存在（**这条现在就该过**，是环境前提）；`test -f skills/issue/references/host-cli.md` 期望真（**现在假**，这是 RED）。
- [ ] **Step 2: 跑一遍，确认 FAIL** —— 第二条失败。
- [ ] **Step 3: 写 host-cli.md** —— 按上面要点，两处"指向隔壁"的相对路径写成 `../../commit-and-push/references/host-cli.md`。
- [ ] **Step 4: 跑断言，确认 PASS** —— 两条都真；再确认文件里**没有**把 `../../commit-and-push/...` 写成 `../commit-and-push/...`（少一级会断链）。
- [ ] **Step 5: Commit** —— `docs(issue): record the measured gh/glab issue facts`

---

### Task 3: 创建流程（references/create.md）

**Files:**
- Create: `skills/issue/references/create.md`

**Interfaces:**
- Consumes: `templates.md`（模板怎么选）、`host-cli.md`（命令怎么写）。
- Produces: 六步流程（选模板 → 拼草稿 → 搜重 → 用户确认 → 创建 → 报 URL/分支名建议），Task 4 的 SKILL.md 直接指向它。

**内容要点（按 spec §2 的 Happy A/C/D + Failure 1–8 逐条落）：**
- 草稿阶段：环境栏探测不到就写"未确认"，不编；feature 的"已排除的替代方案"没有就写 `none`。
- 搜重：命中多条先列最相关三条；用户不选就自己挑第一条并说明；命中别人的 issue 要额外确认。
- 草稿留在会话里，**只在要写/读远端的那一刻**落临时文件，用完即删（失败路径也要删）。
- 创建前确认话术；**GitLab 侧必须含"只能关闭、删不掉"**。
- 失败分档：未发出 → 报告保留草稿；可能已到达 → **不重试**，先搜重确认；连搜重都失败 → 交草稿与命令，明说未确认。
- 创建后：给分支名建议（默认 `<号>-<短 slug>`）+ 说明回链由 commit-and-push 做。
- 落盘模板的分支检查（分支异常/受保护/detached → 跳过并说明）。

- [ ] **Step 1: 写断言（RED）** —— `test -f skills/issue/references/create.md` 期望真（现在假）；写完后还要能命中这几条（**断言串用英文，因为技能文件是英文的**）：`grep -c 'can only be closed' …` ≥ 1、`grep -c 'Do not retry' …` ≥ 1、`grep -c 'unconfirmed' …` ≥ 1。
- [ ] **Step 2: 跑一遍，确认 FAIL** —— 文件不存在。
- [ ] **Step 3: 写 create.md** —— 覆盖上面每一条，尤其别漏"失败路径也要删临时文件"和"GitLab 话术"。
- [ ] **Step 4: 跑断言，确认 PASS** —— 四条 grep 全过。
- [ ] **Step 5: Commit** —— `feat(issue): add the draft → dedupe → confirm → create flow`

---

### Task 4: SKILL.md 路由器

**Files:**
- Create: `skills/issue/SKILL.md`

**Interfaces:**
- Consumes: 上三个 reference + 三个 asset。
- Produces: **触发条件**（三条同时满足 + 条件打架裁决 + 会话内冷却）—— 这是全文唯一权威，Task 5 的 grill 网关与 Task 6 的 using-creed 都只引用它。

**内容要点：**
- frontmatter：`name: issue` + description 覆盖触发场景（bug report / feature request / issue 模板 / 记一条 / 提 issue）。
- 顶部那行 output-language 规则（与其余技能一致）。
- 路由器表（SKILL.md = 路由）：模板 → templates.md；命令 → host-cli.md；流程 → create.md。
- Iron Law：创建一律先问；GitLab 上说明不可删；不自动重试；只映射已有标签；模板不用 CLI 给。
- 触发三条件 + 打架裁决 + 冷却，**写全**（§3 那一节是权威）。
- Rationalization Table + Red Flags + Checklist（对齐 commit-and-push 的骨架密度）。
- **不管回链**：明确写一句"`Closes #N` 与 `Issue: #N` 由隔壁技能做，本技能只给建议"。

- [ ] **Step 1: 写断言（RED）** —— **断言串用英文**（技能文件是英文的）：`test -f skills/issue/SKILL.md` 期望真；`grep -c '^name: issue' …` = 1；`grep -c 'Output language:' …` = 1；三条件（`Not done yet` / `Shelved` / `Shaped and in scope`）合计 ≥ 3；`grep -c '"shelved" wins' …` ≥ 1；`grep -c 'Cooling off' …` ≥ 1；`grep -c 'can only be closed, never deleted' …` ≥ 1。
- [ ] **Step 2: 跑一遍，确认 FAIL** —— 文件不存在。
- [ ] **Step 3: 写 SKILL.md**
- [ ] **Step 4: 跑断言，确认 PASS** —— 全过；再对照 spec §5 的 5 条触发类验收逐条读一遍，确认 SKILL.md 真能判出来。
- [ ] **Step 5: Commit** —— `feat(issue): add the skill router and its trigger rules`

---

### Task 5: 四处回链耦合点

**Files:**
- Modify: `skills/grill/SKILL.md`（Transition gate 段）
- Modify: `skills/write-spec/SKILL.md`（spec 模板 header）
- Modify: `skills/commit-and-push/references/mr-pr.md`（§4 描述生成）
- Modify: `skills/commit-and-push/references/voice.md`（Non-obscuring checklist 抬头）

**Interfaces:**
- Consumes: Task 4 定的触发条件（grill 网关那项指向它）。
- Produces: 回链能力 —— issue 建完后，PR 里出现 `Closes #N`、spec header 里出现 `Issue: #N`。

**各文件改什么：**
- `grill`：gate 加第 3 项"先记一条 issue"，排在"回炉"之后、"其他"之前 ⇒ 字母变 A/B/C/D，"其他"仍**最后一个**；进 issue 技能，完成后回同一网关。
- `write-spec`：模板 header 在 `Owner` 行之后加 `**Issue:** #<N>`，仅当本次会话有号时才写。
- `mr-pr.md`：写 PR 描述时**优先取本次会话已知的 issue 号**；退一步认分支名上的 `#N` 或 `N-` 前缀（建议形状是 `123-fix-...`，**不带 `#`**）；两处都没有就不猜。
- `voice.md`：把 "applies to **every** copy artifact" 放宽一行 —— issue 标题只取其适用部分（bug 标题不要求结果动词）。

- [ ] **Step 1: 写断言（RED）** —— **断言串用英文**（技能文件是英文的）：`grep -c 'File an issue first' skills/grill/SKILL.md` ≥1（现在 0）；`grep -c 'Issue:' skills/write-spec/SKILL.md` ≥1（现在 0）；`grep -c 'leading .<N>-' skills/commit-and-push/references/mr-pr.md` ≥1（现在 0）；`grep -c 'carve-out' skills/commit-and-push/references/voice.md` ≥1（现在 0 —— 那句 issue 例外还不存在）。
- [ ] **Step 2: 跑一遍，确认 FAIL** —— 四条全 0。
- [ ] **Step 3: 改四个文件** —— 注意 grill 的字母顺序别写错（"其他"必须还是最后一个）。
- [ ] **Step 4: 跑断言，确认 PASS** —— 四条 ≥1；再人工读 grill 的 gate 段，确认 A/B/C/D 连续、没有两个"其他"。
- [ ] **Step 5: Commit** —— `feat(issue): wire the four linkage coupling points`

---

### Task 6: 套件同步（using-creed + README）

**Files:**
- Modify: `skills/using-creed/SKILL.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 4 的技能名与触发词。
- Produces: 技能可被发现 —— 安装清单、技能表、建议流程、网关形状描述都提到 `issue`。

**各文件改什么：**
- `using-creed`：① "Required skills" 那行加 `issue`；② 默认流程文字加 `issue?`（位置在 grill 与 write-spec 之间）；③ **"Transition gates" 开头那句现在写的是 "same four-option shape (A proceed / B review first / C adjust / D other)"，而 grill 的网关本来就只有三项** —— 改成"各技能的网关形状见其 Hand-off，不都相同"；④ "Two gates are custom" 那句把 grill 写成 "only proceed/re-open"，补上"或先记一条 issue"。
- `README.md`："Suggested flow" 那段的**纯文本围栏**（不是 mermaid —— 本仓没有 mermaid）加 `issue?`；技能库表的 Design & structure 或 Shipping 区加一行 `issue`。

- [ ] **Step 1: 写断言（RED）** —— `grep -c '\`issue\`' skills/using-creed/SKILL.md` ≥1（现在 0）；`grep -c 'four-option shape' skills/using-creed/SKILL.md` 期望 **0**（现在 1）；`grep -c 'mermaid' README.md` 期望 0（**现在就是 0**，作为"别写错"的护栏）；`grep -c 'issue' README.md` 期望 ≥1。
- [ ] **Step 2: 跑一遍，确认 FAIL** —— 第一条 0、第二条 1（都不符）。
- [ ] **Step 3: 改两个文件**
- [ ] **Step 4: 跑断言，确认 PASS** —— 四条全符。
- [ ] **Step 5: Commit** —— `docs(issue): register the skill in using-creed and the README`

---

### Task 7: 端到端验收（需要你点头才跑）

**Files:**
- 无文件改动；产出是一份验收记录（贴在回复里，不落盘）。

**为什么单列：** 前面的断言只证明"文本写对了"，**证明不了技能在真实会话里行为对**。而这一步要**在共享仓上真的建 issue** —— 且 `llm/opencode` 是**删不掉 issue 的**（403）。所以这一任务**必须由用户明确同意后才执行**，且跑完要 close 并在正文标注是探针。

**要跑的（对应 spec §5 的 `[需造境]` 条目）：**

- [ ] **Step 1: GitHub 侧** —— 在 `Gusen1453/creed` 上：冷启动建一条 bug（用一次真实触发话术，验证"开口时机"是否对）→ 搜重 → 落盘模板（正常分支）→ 建后 delete 删净。
- [ ] **Step 2: GitLab 侧** —— 在 `llm/opencode` 上（**需同意**）：跑一遍完整流程，**只建一条**；验证搜重带 `-A`、标签先查名单、确认话术含"只能关闭、删不掉"；跑完 close + 标注。
- [ ] **Step 3: 触发三档** —— 各跑一次：该开口（"这个先放着"）、不该开口（纯吐槽）、条件打架（"X 先放着先做 Y"）；记录 agent 的实际反应。
- [ ] **Step 4: 失败路径** —— `HTTPS_PROXY=http://127.0.0.1:1` 制造搜重与创建失败，确认**没有第二次创建命令**。
- [ ] **Step 5: 回链** —— 从建好的 issue 走一遍到 PR，确认 PR body 含 `Closes #N`、spec header 含 `Issue: #N`。
- [ ] **Step 6: 记录结论** —— 通过 / 不通过 / 未跑，逐条写明；不通过的回到对应 Task 修。（**这一步不 commit**：验收记录是会话产物。）

---

## Hand-off

执行时用 **tdd** + **test-design**（本仓没有测试运行器，RED/GREEN 就是上面的断言命令 —— 已在"验证方式"里说明）。Task 1–6 可连续做；Task 7 必须停下来问。

Task 7 之后：**review** → **commit-and-push**（这批改动是 12 个新文件 + 5 个已有文件的小改，需要拆成 logical commits）。
