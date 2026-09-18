# 打通 issue（issue 提交与追踪）Spec

**Status:** Draft
**Date:** 2026-09-17
**Owner:** Gusen1453

## 0. Current state（来自环境勘察）

本次是往**已有技能套件**里加能力，不是从零起。勘察到的事实：

- **Anchors（已读）**
  - `skills/commit-and-push/`：路由式骨架 —— SKILL.md 只做路由器（章节表 + Iron Law + 工作流 + Rationalization Table + Red Flags + Checklist），细节拆到 `references/{commit,mr-pr,release,host-cli,voice}.md`，逐字模板放 `assets/*.md`。`host-cli.md` 已沉淀 gh/glab 双宿主固定命令与"每个都真花过回合"的坑表。
  - `skills/grill/SKILL.md`：出口是 **Transition gate**（一处 AskUserQuestion，A 进 write-spec / B 回炉 / C 其他），明文规定"never auto-advance"。
  - `skills/write-spec/SKILL.md`：spec header 已有 `Status / Date / Owner` 字段。
  - `skills/explore`、`skills/debug`、`skills/write-plan`：确认现有技能里**没有任何** issue 相关能力（全仓 grep `issue` 只在 tdd/review 里作为普通英文词出现）。
- **Assertion check** —— 只列**结论**（证据级别 `[实跑]` = 本机真跑过 / `[核源码]` = 读源码或 `--help` 推断）。命令、报错原文、根因见 §6「宿主事实」，这里不重复。
  - **双宿主能力确实不同** ✓，且`[实跑]`两侧默认都只列 open —— 搜重必须显式带上"含已关闭"。
  - **`--template` 这条 CLI 路径用不了** ✗（关键结论）`[实跑]`。⇒ 成熟路径是自己读模板文件、填好、走 `--body-file`（gh）/ `-d`（glab）；§3 的"仓内模板优先"照此实现。
  - **搜重不会把 PR 搜进来** ✗ `[核源码]`，且`[实跑]`两侧搜索都覆盖**正文**。
  - **两侧现在都没有模板目录** ✗；creed 有 GitHub 默认标签，`llm/opencode` 标签数为 0 `[实跑]`。
  - **"标签只映射已有、绝不新建"只在 gh 上自动成立** ✗ `[实跑]` —— GitLab 会把不存在的标签直接建出来，所以那边必须先查名单。
  - **"正文逐字落地"不成立** ✗ `[实跑]` —— 两侧都有已知的换行规范化。⇒ 验收口径是"除已知规范化外一致"。
  - **Conventional Commits 管不到 issue 标题** ✗ —— 所以"套不套 `type(scope):`"是自由决策，不是事实。
- **Conflicts（约束 vs 仓库现实 → 由下文决策化解）**
  - 提 issue 是**不可逆的公开写**，而技能默认应是只读/低风险 → 对策：创建一律先问（§4「重复与更新」行）。
  - 落盘模板需要写业务仓并与**当前分支**绑定，而分支可能本身有问题（`main`/detached） → 对策：分支异常时跳过落盘，**自己读模板文件内容**（不用 CLI 的 `--template`，实测非交互走不通）或直接拼 body 发出去（§2 边界 2）。
  - 一次草稿可能在创建前就被发现与已有 issue 重复 → 对策：搜重命中即问"更新还是另开"（§2 边界 1）。
  - 草稿在**会话里**，但要发出去的正文常含多行中文、反引号、`→` —— 直接内联进命令会有引号/转义问题 → 对策：**只在用户点头、真正要读/写远端的那一刻**把正文落到临时文件，走文件通道；写完即删（§2 边界 1、边界 4）。草稿本身不预先落盘。
  - 本仓现有分支名是 `Gusen1453/work` 这类，**不带 issue 号** —— "按仓内惯例带 issue 号"在本仓并不成立 → 对策：分支名只是**建议**，默认形状 `<issue号>-<短 slug>`；仓内有自己惯例时以仓内为准（§3 In）。

## 1. One-liner（board slide）

把"想法/缺陷"变成**平台上一条可追踪、可回链、别人能接手的 issue**：技能自带 bug/feature/custom 三档可行动模板、创建前先搜重、只映射仓内已有标签、给你一个分支名建议；主路径是 `grill → issue → write-spec`，同时支持"刚发现个 bug，当场记一条"的冷启动；代价是每次创建都多一次确认，且 agent 主动开口的窗口设得偏窄（只认"用户把这件事挂起来了"）。

## 2. User scenarios（source of truth）

### Happy path A —— 冷启动：刚发现一个 bug
- **Who:** 用户，正用着自己维护的产品，撞上一个可复现的毛病。
- **When:** 还没打算动手修，只想别忘、别丢。
- **Does:** 说"记一下这个 bug / 提个 issue"，用日常话讲症状和复现路径。
- **Sees:** agent **不**先 grill（这就是用户自己定的边界），直接按 bug 模板把话填成一份草稿（症状 / 复现 / 期望 vs 实际 / 环境；环境栏探测不到就写"未确认"，不编），先给**搜重结果**（同类 issue 命中就摊出来；命中多条时先把最相关的三条列出，再问选哪条比对），草稿完整贴出并问"发这条？"；用户点头后才发；发完给 issue URL + 分支名建议 + 一段"回链交给 commit-and-push"的说明。

### Happy path B —— 管道内：设计敲定后先落一条
- **Who:** 用户 + grill 刚敲完一个特性的设计。
- **When:** grill 的出口网关。
- **Does:** 在网关里看到常驻的那一项"先记一条 issue"，选了它。
- **Sees:** 设计意图被翻成一条 feature issue（背景 / 期望结果 / 验收怎么算过 / 已排除的替代方案 —— 后者来自 grill 的决策记录；grill 若没收敛出替代方案，该栏写"none"而不是编一个）。建完**回到同一个网关**再走一次（issue 那一项这次不选），可选进 write-spec；spec 的 header 里带一行 `Issue: #N`。若这一轮 grill 其实收出两个互不相干的能力，草稿只覆盖第一个可交付切片 —— 另一件另开一条，且要用户点头才建。

### Happy path C —— 目标仓已有自己的模板
- **Who:** 用户在某个已有 issue 模板规范的仓里干活。
- **When:** 要提一条 issue。
- **Does:** 什么都没做，只是说了要提。
- **Sees:** agent 探到仓内模板（GitHub 的 `.github/ISSUE_TEMPLATE/` 或 GitLab 的 `.gitlab/issue_templates/`），**读它的内容**当成草稿骨架（不用 CLI 的 `--template`，那条路走不通），**用它**而不是技能内置的；仓内模板的段落名可能和内置的不一样，按仓内的来。GitLab 侧还会把填好的正文原样贴给用户过一眼——理由有两个：正文要内联进命令（引号/转义），以及**平台读回时会把 LF 变成 CRLF**，所以"贴出来确认"确认的是**要发的这份**，不是"原样读回的那份"。

### Happy path D —— 冷启动：既不是 bug 也不是新需求
- **Who:** 用户的杂项念头（"把 CI 换成自托管"、"文档该拆一章"）。
- **When:** 想到了，但归类不上。
- **Does:** 说"记一条：…"。
- **Sees:** 走 custom 模板（背景 / 想要什么 / 边界——不做什么），不被硬塞进 bug 或 feature 的框里；标签若仓内有语义对得上的（GitHub 默认可落在 `question`）才加，否则不加。

### Happy path E —— agent 主动开口（唯一一条不由用户起头的路径）
- **Who:** 用户，刚说完一段话，顺手把其中一件事往后推了（"导出那个先放着，先弄 CI"）。
- **When:** 任意一轮对话（不限于 grill），用户把一件事挂起来、且它有可写的形状、且它是这个仓的事。
- **Does:** 没提"issue"两个字。
- **Sees:** agent 按 §3 的三条件判一次（还没做 + 被挂起来 + 有形状且在范围内，三条都中）→ 用一句话提议"要不要记一条 issue？"，附上**已经在手里的**草稿要点（不从零开始问）；用户说"记"才走后面的选模板/搜重/确认流程，说"不用"就当次会话不再提。

### Failure / edge
1. **搜到重复** —— 命中项被列出（标题 + 状态 + 链接 + 摘要）。命中多条时先列**最相关的三条**，用户选定一条后 agent 问"A 更新这条 / B 另开一条 / C 取消"（若用户不选，就拿第一条最相关的当比对对象，并说明选的是哪条）。选"更新"时：若该 issue 不是本人开的，先说明"这是别人开的 issue，改写它等于替对方改描述"（对方的 issue 默认当作"另开/取消"，除非用户明确要求改），再让用户确认；平台写法不同 —— GitHub 走 `gh issue edit --body-file`，GitLab 走 `glab issue update` 的 `--description`（内联），两站都**先把正文落到临时文件再读进来**，传完即删。
2. **分支不对** —— 当前在受保护分支或 detached HEAD 上。agent 说清"落盘模板要写进当前分支、而这里不合适"，跳过落盘，**自己读仓内模板文件（若有）的内容**拿来填草稿（不用 CLI 的 `--template`），或直接拼 body 发出去；**不**偷偷切分支。
3. **模板要落盘** —— 用户点头后，把**三档模板**写进**本仓宿主对应的那一个目录**（GitHub 仓 → `.github/ISSUE_TEMPLATE/`，GitLab 仓 → `.gitlab/issue_templates/`），共三个文件；另一站的目录**不写**（在 GitHub 仓里放一份 GitLab 模板是死文件）。然后**明确说这三个文件还没提交**（交给下一次 commit-and-push 处理，不单独提交）。分支异常时跳过并说明（见 2）。
4. **用户说不发** —— 停，只交付可粘贴的草稿（标题 + 正文）+ 建议用的 `gh`/`glab` 命令。此时**不写临时文件**（草稿本来就在会话里），远端零新建。
5. **创建或搜重失败** —— 分几种：命令根本没发出去（未登录/无此仓）→ 报告原因，草稿保留；命令**可能已到达远端**（断网、超时、5xx）→ **不自动重试**，先搜重确认远端有没有多出一条，再让用户定夺——重试是双开 issue 的最短路径；连**搜重本身**都失败时（也超时/离线）→ 不再猜，把草稿和确切命令交给用户，说明"远端状态未确认，你自己看一眼再决定发不发"。**任何一条失败路径上，已写的临时文件都要删掉**。
6. **用户在已确认的会话之外的仓里提 issue** —— 技能操作的是**当前 worktree 所属仓**的 origin；提交前把"将要写到哪个仓"讲明（`owner/repo`），避免提到 upstream/别人的仓里。
7. **仓没有开 issue 功能**（GitHub 的 issues 开关被关掉，或项目对当前账号不可见/无权限）→ 直接说明"这个仓提不了 issue"，把草稿给你，不硬试。
8. **在 GitLab 上发出去才发现写错了** —— 这是本技能最不能挽回的一种失败：实测该宿主（自建 GitLab、普通成员权限）**删不掉 issue**（`glab issue delete` 与 `glab api -X DELETE` 都返回 403），只能 `close` 并在正文/评论里写"这是误建的，请删"。所以 GitLab 侧的确认话术里必须出现"发出去就只能关闭、删不掉"；GitHub 侧则可删（`gh issue delete <N> --yes`），确认话术照常。

## 3. Scope

**In:**
- 一个新技能（名字：`issue`），承担：选模板 → 拼草稿 → 搜重 → 用户确认 → 创建 → 报 URL/分支名建议。
- 三档内置模板（bug report / feature request / custom），纯 Markdown，**一份两站通用**：换站只是换个目录（GitHub 的 `.github/ISSUE_TEMPLATE/` ↔ GitLab 的 `.gitlab/issue_templates/`），正文与 front matter 不变：
  - bug：症状 / 复现 / 期望 vs 实际 / 环境
  - feature：背景 / 期望结果 / 验收怎么算过 / 已排除的替代方案
  - custom：背景 / 想要什么 / 边界（不做什么）
- 模板的**选择**是：仓内模板优先（路径严格按平台惯例），技能 `assets/` 兜底；**读法是自己读那个文件、把内容拼进正文**，不用 CLI 的 `--template`（实测它在非交互下走不通，证据见 §0）；宿主认不出时（`origin` 不是 GitHub/GitLab 的托管站，或识别不出是哪一个）直接拼 body，不做落盘。
- 在用户**明确同意**时可把三档模板落盘到目标仓 —— 只写**本仓宿主对应的那一个目录**（GitHub → `.github/ISSUE_TEMPLATE/`，GitLab → `.gitlab/issue_templates/`），三档各一份，共三个文件。**落盘是为了给人看和给网页端用**（agent 自己走"读文件"这条路，不依赖它），所以它是可选的。
- 创建前**先搜重**（按模板字段抽关键词；`gh issue list -s all -S` 与 `glab issue list -A --search --in title,description` 的返回集合都限定在 issue 内、不含 PR，两侧搜索都覆盖正文），命中就展示并让用户选"更新 / 另开 / 取消"。
- 标签**只映射到仓内已有标签**（存在才加），绝不新建标签。
- 标题是**可读陈述句**（`type(scope):` 不适用于 issue），遵守反晦涩硬规则的**适用部分**：≤ ~50 字符、禁堆叠修饰、禁 vague verb。**"结果动词开头"对 bug 不适用** —— 症状型标题（"导出空行时崩溃"）本身就是正确写法，别为了凑动词把它改写成"修复导出崩溃"（那是在描述还没做的修复）。feature / custom 仍以结果动词开头。
- 回链（issue 侧全包、但只包到"建议"）：
  - 创建后给一个**分支名建议**，默认形状 `<issue号>-<短 slug>`（如 `123-fix-export-empty-row`）；仓内已有自己的命名惯例时以仓内为准；
  - PR 侧的 `Closes #N`、spec 侧的 `Issue: #N` 一行，分别由 `commit-and-push` 与 `write-spec` 承担（只加极薄的一行耦合）。
- **主动开口的触发条件**（本节是唯一权威，别处只引用；落地表现见 §2 Happy E）——
  **三条同时满足**才开口：
  1. 用户说的是**一件还没做的事**（不是已完成的事）；
  2. 用户用了**把它挂起来的说法**：显式说"记一下 / 提个 issue"，或把它往后推（"这个先放着 / 回头处理 / 回头弄"）；近似句也算 —— 判定看"是不是把这件事挂起来"，不是背短语表；
  3. 这件事**有可写的形状，而且落在当前仓/项目里**：bug 至少有症状或复现之一；需求至少说清了想做什么；且它是这个 repo 的事，不是"回头得去交个税"这类与项目无关的私人待办。

  **条件打架时以"被挂起来"为准**：用户一边在讨论/设计 X、一边说"X 先放着，先做 Y"，这是"正在做"（条件 1 不满足）与"被挂起来"（条件 2 满足）撞在一起 —— 此时**开口**，因为把一件事往后推本身就是记录意图。反过来，用户只是在推敲 X 的细节、没说往后推，**不开口**。

  **同一会话内的冷却**：用户拒过一次之后，本会话不再主动开口（但 grill 网关那一项照旧在，见 §6）。
  只满足其中一两条时**不开口**（纯讨论、纯情绪"这设计真丑"、没往后推的在办事项、已完成的事）。
- 邻技能与文档要跟着改：`grill` 出口网关加一项常驻选项、`write-spec` 模板 header 加一行 `Issue: #N`、`commit-and-push` 在写 PR 描述时**从会话里已知的 issue 号**（或分支名上的 `#N` / `N-`）加 `Closes #N`、`voice.md` 放宽"适用于每个 copy artifact"那句（这四处见 §6 的接口约定）、`using-creed` 的技能表/建议流程/必装清单/网关形状描述加入 `issue`、README 的"Suggested flow"文本块与技能库表同步。
- 管道入口：作为 `grill` 出口网关里**常驻的一项**（选了才进），位置在 `grill → issue → write-spec`。

**Out (this round):**
- ~~自动建分支 / 自动提 PR~~ —— 属 `commit-and-push`；跨技能自动动作会把两个技能的职责搅在一起。
- ~~自动关闭 issue / 自动回写 issue 评论~~ —— 同上；`Closes #N` 已经足够。
- ~~自动创建或补齐标签~~ —— 标签体系是仓主管辖的东西，agent 擅自改不合适。
- ~~GitHub 原生 `.yml` form~~ —— GitLab 不认 yml，双份易漂移；本仓 issue 读者主要是用户 + agent，表单强校验收益有限。
- ~~把 issue 能力塞进 commit-and-push 或 grill~~ —— 时机相反（commit-and-push 是"代码已写好"，issue 是"代码还没写"），混在一起会让技能说不清自己什么时候该上。
- ~~issue 无法创建时的离线兜底（如写到本地文件）~~ —— 与已定的"降级为给你草稿+命令"重叠，且本地文件会变成另一套待办。
- ~~"为每条待办都建 issue"的强制策略~~ —— 会让新建的仓 issue 列表瞬间灌满自动化噪音；改为"每个能力一个 issue"的纪律（见 §6）。
- ~~write-plan 也回链 issue~~ —— 号已经在 spec header 里了，再加一层是重复；YAGNI。

## 4. Decision log（mentoring）

| Decision | Chose | Rejected | Why (user/business impact) |
|----------|-------|----------|----------------------------|
| 能力落点 | A) 独立技能 `skills/issue/` | B) 并进 grill；C) 并进 commit-and-push | 需求从"一句话想法"到"可追踪 issue"再到"设计/计划"，职责单一、任何一步都能单用；代价是 skills 11→12，要改 using-creed 的技能表、建议流程与网关链。 |
| 命名 | A) `issue` | B) `file-issue`；C) `open-issue` | 名字与它干的事一致（处理 issue），调用不歧义；代价是与 `commit-and-push` 的动词短语风格不完全一致。 |
| 入口与时机 | A) 双入口；管道位置 `grill → issue → write-spec` | B) grill 开头就建；C) write-spec 之后才建 | 两个真实场景都顺："刚发现个 bug"→ 当场收工；"我想做个 X"→ 先 grill 再落 issue 再写 spec。B 会让 issue 在还没想清时被建出来、反复重写并甩通知；C 只适用于 feature，bug report 没有 spec，技能会被撕成两半。 |
| 触发方式 | A) 常驻为 grill 网关的一个**选项**（永不自动执行） | B) 只在探到搁置信号时给；C) 强制为默认停靠站 | 常驻"选项"不是常驻副作用：点头才动。B 依赖"搁置信号被说出来"，而这恰恰常被一带而过；C 会让小重构、纯内部改造也过一道 issue，待办池被噪音稀释——与"可追踪"的目标相反。 |
| 误触发防线 | A) 创建**一律先问**；主动开口的判据、条件打架的裁决、会话内冷却，全部以 §3 那一节为准 | B) 只在用户明说"提 issue"时给选项；C) 探测到 bug 迹象就自动建议 | 主动开口要看"用户有没有把这件事挂起来"，而不是背一句短语表：近似句（"这个先放着 / 回头处理"）与显式句一样算。C 是最可能造成误触发的做法（用户只是在讨论、连设计都没定）；B 会漏掉"往后推"这一类真实意图，而它恰恰是待办最自然的说法。 |
| 草稿落盘时机 | A) 草稿留在会话里，只在**要写/读远端的那一刻**落临时文件、完事即删 | B) 草稿一开始就写临时文件 | A 少一次无谓的仓内写入，"用户说不发"时工作区零残留；代价是内联传正文的平台上要先落一次文件（GitLab 的 `update --description`），这一步在真正要发的时候才发生，不会白做。 |
| 分支名建议的依据 | A) 默认 `<issue号>-<短 slug>`，仓内有命名惯例时以仓内为准 | B) 一律沿用本仓现有命名形状 | 本仓现有分支名（`Gusen1453/work`）不带 issue 号，照抄就丢了追踪价值；A 让建议默认有用，同时不越权改一个已经有规矩的仓。 |
| 模板清单 | A) 三档（bug / feature / custom），纯 `.md` | B) 只留 bug / feature；C) `.md` + GitHub `.yml` form | 三档给常见需求都有归处，杂项不必塞进 bug 模板；同一份 `.md` 换站只换个目录名（GitHub 的 `.github/ISSUE_TEMPLATE/` ↔ GitLab 的 `.gitlab/issue_templates/`），格式和正文都不用改。代价：GitHub 上放弃 form 的必填强校验，质量靠模板正文引导。 |
| 模板归属 | A) 技能 `assets/` 是源头；**可选**落盘到目标仓 | B) 不写目标仓；C) 只在目标仓，技能不管 | 落盘是给**人和网页端**用的（网页端要等这三个文件被提交并推上去，见 §2 边界 3）；agent 自己走"读文件拼正文"那条路（`--template` 在非交互下走不通，§0 实测），所以落盘不是必须的。代价是落盘要写仓内文件并需提交，所以必须用户点头。C 会把模板的一致性交给每个仓各自维护。 |
| 落盘写几个目录 | A) 只写本仓宿主对应的那一个目录，三档共三个文件 | B) 两个目录各放一套（六个文件） | 在一个 GitHub 仓里放一份 GitLab 模板是死文件：没人读、还要被 commit-and-push 一起提交。A 让落盘只产出真正用得上的文件；代价是将来这个仓迁到 GitLab 时得再落一次盘。 |
| 标题格式 | A) 可读陈述句 + 反晦涩的适用部分（bug 免结果动词） | B) 强制 `type(scope):`；C) 按模板分两套 | 列表里一眼读懂"什么事"，也不会把两个平台的硬规则搞混（Conventionals 只管 commit）。**"结果动词开头"只对 feature/custom 要求** —— 症状型 bug 标题（"导出空行时崩溃"）天然没有结果动词，硬套只会改写成"修复导出崩溃"，那是在描述一个还没做的修复。 |
| 模板优先级 | A) 仓内模板优先，`assets/` 兜底 | B) 一律用 `assets/`；C) 只用仓内 | 在用户自己维护了模板的仓里，提的 issue 完全合那个仓的规范；在没模板的仓（含 creed 现状）直接用 `assets/` 里那份，永不卡住。 |
| 字段深度 | A) 每档只留"可行动"字段集 | B) 三档统一三段；C) 三档统一富表单（6–8 段） | 每档都短，但都不缺"能开工"的那几条：bug 拿到复现就能上手，feature 拿到验收就知道什么叫做完。代价：轻需求里"已排除的替代方案"容易写成空话，靠"没有就写 none"的诚实规则兜。 |
| 重复与更新 | A) 先搜重，命中就问；创建一律先问 | B) 命中就自动更新；C) 不管重复 | 不会双开 issue，也不会被 agent 偷改已发出的公开文本（issue 编辑不保留版本）。代价：多一次确认，与现有 PR 规则同级，不算新负担。 |
| 标签 | A) 映射到仓内已有标签，不自造 | B) 不打标签；C) 自动补齐缺失标签 | 待办池一眼分得出 bug/需求/其他，也不会凭空长出标签。代价：custom 类落到 `question` 语义略勉强——所以模板里默认不写死标签，仓主可在自己的模板里覆盖。 |
| 回链范围 | A) issue 侧全包，回链交给隔壁技能 | B) 本技能做全套回链；C) 不做回链 | 本技能只管"建 + 搜重 + 分支名建议"；`Closes #N` 由 commit-and-push 加、`Issue: #N` 由 write-spec 写进 header。号的来源**首选本次会话已拿到的号**，退一步才认分支名上的 `#N` / `N-` 前缀（本技能建议的形状是 `123-fix-...`，只认 `#N` 会永远触发不了）；两处都没有就不猜。B 会让两个技能都能改 PR 描述、职责重叠。 |
| 技能骨架 | A) 对齐 commit-and-push（路由 + references/ + assets/） | B) 单 SKILL.md + 两个 reference；C) 只有 SKILL.md | 同构：多宿主命令 + 逐字模板正文 + 分支式流程。模板正文单独成文件才能被**直接拷贝**落盘，不会因为"从长文里抠段落"而带进无关内容。 |

## 5. Acceptance（demo / test language）

> **本机可演示的是 GitHub 侧**（本仓 origin 是 GitHub）**与一台自建 GitLab**（`code.comein.cn` 的 `llm/opencode`）。标签含义：
> - `[需造境]` —— 本机跑得动，但要先把环境凑出来（做法写在条目里）；**技能级验收全是这一类**，因为技能还没写；
> - `[静态]` —— 属技能文件文本，靠读文件判定，不靠跑；
> - `[GitLab·纸上]` —— 这条行为没在第二站试过（本站已试，见 §0）。

宿主能力已在 §0 与 §6 记过，**不在这里重复记账** —— 这一节只列**技能**要做到的事。

- [ ] 场景：用户说"记一下这个 bug"并讲清症状与复现 → 产出符合 bug 模板四段的草稿，且**公开行为为零**直到用户点头 → observable：确认前 `gh issue list` 条数不变。
- [ ] 场景：用户说"记一条：把 CI 换成自托管"（既非 bug 也非 feature）→ 走 custom 模板，正文含"背景 / 想要什么 / 边界" → observable：正文有这三段，且没有出现复现步骤这类 bug 栏位。
- [ ] 场景：用户说"我想做个 X" 且已过 grill → 落成 feature issue，且"已排除的替代方案"一栏反映 grill 的决策记录 → observable：该 issue 正文含这些字段，且**不含**任何 spec 细节（不出现文件路径、不出现 TDD 步骤这类字样）；若 grill 那一轮没收敛出替代方案，该栏的值为 `none`（不是留空、也不是编一个）。
- [ ] `[需造境]` 场景：草稿与**两条以上**已有 issue 都沾边 → agent 先列最相关三条，再问"更新哪条 / 另开 / 取消" → **造境**：先在仓里开两条措辞相近的 issue 当靶子。observable：回复里出现三条以内的候选项与三选问题；用户不选时，agent 明说拿哪一条当比对对象，而不是卡住不问。
- [ ] `[需造境]` 场景：目标仓已有 issue 模板 → 用的是仓内那份，不是技能内置的 → **造境**：先在仓里手写一份段落名与内置**明显不同**的模板（如自己命名"实际表现 / 期望表现"），不要用落盘的那份逐字拷贝 —— 用拷贝就分不出"仓内优先"和"内置兜底"。observable：发出去的正文段落名与手写那份一致。
- [ ] 场景：草稿与一条已有 issue 高度重合 → 用户看到命中项与"更新/另开/取消"三选 → observable：选"更新"时 issue 条数不变、且读回的正文包含新草稿的内容。
- [ ] 场景：仓内只有 `bug`/`enhancement`/`question` → 发出去的 issue 带的就是这些标签之一；若正文语义对不上任何一个，就**不带**标签 → observable：读回该 issue 的 labels 要么为空、要么全部在 `gh label list` 的名单里，且仓内标签列表前后一致。
- [ ] 场景：用户说"先别发" → 只得到可粘贴的草稿 + 一条准确命令 → observable：远端无新 issue，`git status` 里没有新增的临时文件。
- [ ] `[需造境]` 场景：**技能级**的 GitLab 全流程 —— 技能自己去做搜重、自己先查 `glab label list` 再映射、自己回读比对 → **造境**：技能写出来之后，在 `llm/opencode` 上跑一遍完整流程，**只建一条**，跑完 close 掉并在正文标注是探针。observable：搜重那一步确实带了 `-A`；标签那一步确实先查了名单（零标签仓上 issue 的 labels 为空、`glab label list` 仍为 0）；回读 diff 前做了行尾归一。
- [ ] 场景：在受保护分支或 detached HEAD 上被请求落盘模板 → 明确告知并跳过落盘，issue 照常建 → observable：`git branch --show-current` 的输出与开工前一致（受保护分支仍是那个分支、detached 仍是那个 commit），`git status` 无新增模板文件。
- [ ] `[需造境]` 场景：提 issue 前 agent 讲明"要写到哪个仓" → observable：回复里出现 `owner/repo`；**造境**：在一个 fork 或旧 clone 里试（`origin` 不是当前在谈的那个仓），确认 agent 讲的是 `origin` 那个仓而不是用户嘴里的仓。
- [ ] `[需造境]` 场景：仓没有 issue 能力（GitHub 关了 issues 开关）→ 说明并给草稿，不硬试 → **造境**：临时在一个测试仓的 Settings 里关掉 Issues。observable：回复里说明"这个仓提不了 issue"，且没有产生报错重试。
- [ ] 场景：标题是症状型 bug（"导出空行时崩溃"）→ 标题保持症状陈述，不被改写成"修复导出崩溃" → observable：读回的 title 与草稿一致，且不含"修复/新增"这类结果动词。
- [ ] 场景：**正面触发**——用户把某件事挂起来（"这个先放着"/"回头处理"/"记一下"）→ agent 开口，给出草稿要点 → observable：出现草稿确认与创建选项。
- [ ] 场景：**条件打架**——用户在讨论 X 时顺口说"X 先放着，先做 Y" → agent 开口（"被挂起来"压过"正在做"）→ observable：出现 issue 提议。
- [ ] 场景：**不误触发**——用户只是聊、在情绪里说一句（"这设计真丑"）、说的是正在做的事、或只推敲 X 的细节没说往后推 → agent 不主动提 issue → observable：回复里不出现 issue 创建选项，远端无任何创建动作。
- [ ] 场景：issue 建完 → 得到一个分支名建议 → observable：回复里出现形如 `<号>-<短 slug>` 的建议（仓内已有命名惯例时改为照仓内），且**没有**被自动创建成真分支（`git branch` 数量不变）。
- [ ] `[需造境]` 场景：搜重的命中项里有一条是别人开的 → 用户看到"这是别人开的 issue"的提示，默认动作是另开或取消 → **造境**：本仓只有一个身份，先从另一个账号（或第二个本地 clone 用别的身份）开一条 issue 当作"别人的"。observable：选"更新"前必须先有一次针对"改别人描述"的确认。
- [ ] 场景：用户在正常分支上同意落盘模板 → 本仓宿主的那个目录里出现**三份**模板文件，另一站的目录**不**被创建，且回复里说明"这三个文件还没提交" → observable：`git status` 显示三条未跟踪文件路径，且 `.github/` 与 `.gitlab/` 没有同时出现。
- [ ] `[需造境]` 场景：宿主认不出（`origin` 指向一个非 GitHub/GitLab 的托管站）→ 直接拼 body、不落盘、不硬试 → **造境**：临时把一个 scratch 仓的 `origin` 改成假地址（如 `https://example.com/x/y.git`）试一次，试完改回。observable：回复里说明"识别不出宿主"，且没有产生任何命令报错重试。
- [ ] 场景：用户在这次会话里拒过一次 → 本次会话不再**主动**开口 → observable：后续回复里不出现 issue 创建提示；但若用户自己走进 grill 网关，那一项照旧可见。
- [ ] 场景：**不接这个活也顺**——用户在设计收尾时直接选"进 write-spec" → 直通，不需要先关掉 issue 选项 → observable：`grill → write-spec` 这一段只问过**一次**网关问题（issue 与"是否进 write-spec"在同一个题里；只有真的选了"先记一条"才会多走一次网关）。
- [ ] `[需造境]` 场景：issue 建完后开 PR → PR 描述里出现 `Closes #<N>`，spec header 里出现 `Issue: #<N>` → **造境**：这三处要先在技能文件里改好（§6 接口约定），再真跑一次"建 issue → 建分支 → 开 PR"。observable：PR 读回的 body 含 `Closes #<N>`；spec 文件的 header 块（`Owner` 那行之后）里有 `Issue: #<N>`。
- [ ] `[需造境]` 场景：创建时网络中断/超时（命令可能已到达远端）→ agent **不**自动重试，先搜重确认 → **造境**：在 `gh` 前面套一层会超时的 proxy（如 `HTTPS_PROXY=http://127.0.0.1:1`）制造失败。observable：回复里出现"先确认远端有没有多出一条"的步骤，且没有第二次创建命令。
- [ ] 场景：一轮 grill 收敛出**两个互不相干**的能力 → issue 草稿只覆盖第一个可交付切片（与 grill 的 scope 规则一致），不是把两件事塞成一条 → observable：草稿的"想要什么"只讲一件事；另开的那条要在用户点头后才建。
- [ ] 场景：创建失败后收尾 → 临时文件被清掉 → observable：`git status` 里没有残留的临时文件。
- [ ] `[静态]` 场景：issue 技能的 `references/host-cli.md` 指到隔壁坑表的那条相对路径能解析 → observable：从 `skills/issue/references/` 出发，`../../commit-and-push/references/host-cli.md` 指向一个真实存在的文件（改完技能文件后 `ls` 一次即可）。
- [ ] `[静态]` 场景：三档模板正文里没有对读者露出的注释 → observable：`grep -rn '<!--' skills/issue/assets/` **零命中**（那行"本文件由 creed 技能同步，请改源头"说明是**落盘时才追加**的，源文件里本来就没有）。
- [ ] `[静态]` 场景：`grill` 网关的新选项排第 3 位、字母连续、"其他"仍是最后一个字母 → observable：读 `skills/grill/SKILL.md` 的 Transition gate 段，选项按这个顺序，且没有两个"其他"。
- [ ] `[静态]` 场景：四处耦合点各自的技能文件都真的改过 → observable：`grill` 网关多一项、`write-spec` 模板 header 有 `Issue:` 行、`commit-and-push/references/mr-pr.md` 写到"从会话已知的 issue 号加 `Closes #N`"、`commit-and-push/references/voice.md` 那句"applies to every copy artifact"已放宽；`using-creed` 的必装清单/技能表/建议流程/网关形状描述与 README 技能库表也同步了。
- [ ] `[GitLab·纸上]` 场景：**换一站** —— 同一个技能在另一个 GitLab 站上跑通（仓内模板、落盘路径加引号、正文含 `→` 与反引号、搜重带 `-A`） → observable：读回的 description 与草稿一致（除 CRLF 规范化）。本机这台 `code.comein.cn` 上各条已分别跑通，缺的只是"换一站是否同样成立"。
- [ ] `[需造境]` 场景：**在 GitLab 上**确认话术里必须出现"发出去只能关闭、删不掉" → observable：把确认阶段的回复给另一人看，他能在用户点"发"**之前**知道这件事；对照 GitHub 侧同一话术里出现的是"可以删"。
- [ ] `[需造境]` 场景：搜重自身失败（离线）→ agent 不再猜，把草稿与确切命令交给用户，并说明"远端状态未确认" → **造境**：把 `HTTPS_PROXY` 指到一个死端口，让 `issue list` 也一起失败。observable：回复里同时出现草稿、具体命令与"未确认"的说明，且没有自动创建动作。
- [ ] `[静态]` 场景：模板带可用 front matter（`name` / `about` / `labels`），且 `labels` 不写死具体值 → observable：读 `skills/issue/assets/*.md` 三份都能看到 front matter，`labels` 一栏为空或留给落盘时按仓内名单回填。

## 6. Constraints

- **只操作当前 worktree 所属仓的 origin**；提交前讲明 `owner/repo`，避免提到别的仓。
- **不可逆公开写一律先问**（与 commit-and-push 的"新建 PR 必须先问"同级规则）。
- **主动开口的窗口是有意设窄的**：判据（三条件）见 §3，其余场合不主动提。宁可少提，也不要在用户只是讨论或吐槽时插一句。
- **输出语言跟随用户 register**（复用 commit-and-push 的 voice 链：commit 层离用户原话最近，issue 与之一致；中英皆可，不额外翻译）。管道内的正文原料是 grill 的决策记录，但**说话口吻**仍是用户自己的。
- **回链的接口约定**（四处各改自己的文件，本技能不代劳）：
  - `grill`：出口网关加一项常驻选项（位置见下条），进 issue 技能，完成后回同一网关。
  - `write-spec`：模板 header 在 `Owner` 行之后加 `**Issue:** #<N>`，仅在本次会话有 issue 号时才写。
  - `commit-and-push`：写 PR 描述时，若**本次会话已知 issue 号**，就加 `Closes #<N>`；退一步也认分支名里的 `#N` 或 `N-` 前缀（§3 建议的形状是 `123-fix-...`，**不带 `#`**，只认 `#N` 会永远触发不了）。号既不在会话里也不在分支名里 → 加不了，明说不猜。
  - `voice.md`：它现有那句"Non-obscuring checklist —— hard, applies to **every** copy artifact"要放宽一行，说明 issue 标题只取其适用部分（bug 标题不要求结果动词，见 §3）；否则技能间自相矛盾。
- **grill 网关的新选项排在第 3 位**（在"回炉"之后、"其他"之前），出口那一行的字母标记随之顺延；"其他（我来打字）"必须保持是**最后一个字母**（grill 的 Iron Law 要求如此）。`using-creed` 里有两处会因此过时，都要一并改：①"Transition gates"开头那句把网关描述成"same four-option shape (A proceed / B review first / C adjust / D other)"——**grill 的网关本来就只有三项**（A 进 write-spec / B 回炉 / C 其他），加上 issue 后是四项，但形状与别的网关不同，得改成"各项技能的网关形状见其 Hand-off，不都相同"；②"Two gates are custom"那句把 grill 网关写成"only proceed/re-open"，加了 C 项后要补上"或先记一条 issue"。只改成一个笼统的"三选项或四选项"是没用的——那样既没修掉原有的错误描述，也没说清新项在哪。
- 模板正文用占位符，**不留** `<!-- 注释 -->` —— 因为被当作文档读时注释会露出来（落盘时另加的一行"本文件由 creed 技能同步，请改源头"是唯一的例外，且它只在落盘产物里出现，源文件没有）。
- 模板在技能 `assets/` 里带 front matter（`name` / `about` / `labels`），但 `labels` 不写死具体值 —— 不同仓的标签集不同，落盘或选用时按仓内实际名单回填。
- 宿主命令的已知差异必须写进技能 —— **下面每条都标了结论来源：`[实跑]` = 本机真跑过并比对输出；`[核源码]` = 读 gh/glab 源码或 `--help` 推断。技能文件里要带上这两个标记、宿主版本（gh 2.97 + GitHub `Gusen1453/creed`；glab 1.114 + 自建 `code.comein.cn` 的 `llm/opencode`），不许把"核源码"说成"实测"**。**标记本身按仓库的 English-only 惯例写成 `[measured]` / `[source-checked]`**（技能文件是英文的，见 04e474b）—— 语言换掉，语义不许换：`[source-checked]` 永远不能升格成 `[measured]`。
  - **模板不能用 CLI 给**。`[实跑]` `gh issue create --template` 在非交互下必然报错（没有 body 就落进交互分支：`must provide --title and --body when not running interactively`；补 `-F` 报 ``--template` is not supported when using --body`；补 `-e` 报 `--editor ... not supported in non-tty mode`）。`[核源码]` 根因在 `create.go`：`opts.Interactive = !EditorMode && !(titleProvided && bodyProvided)`。`[实跑]` `glab` 的 `--template` 与 `--description` 是**互斥 flag 组**。⇒ 两侧都改成"自己读模板文件 → 填好 → 走 `--body-file`（gh）/ `-d`（glab）"。
  - **创建命令**：gh 用 `-t <title> -F <body.md>`（`--body-file`，不吃 stdin 的多行；`-b` 内联易被 shell 转义搞坏）；glab 用 `-t <title> -d "$(cat body.md)"`（**只有内联**，没有 `--description-file`），加 `-y` 免交互确认。`[实跑]` 两者都会把 issue URL 打到 stdout，**没有 `--json`** —— 要拿号就解析 URL 尾数，或 `gh issue list -s all -L 1 --json number`。
  - **搜重**：gh `gh issue list -s all -S "<kw>"`；glab `glab issue list -A --search "<kw>" --in title,description`。**`-A` 与 `-s all` 都不能省**：`[实跑]` 非交互下两边默认都只列 open，已关闭的重复 issue 会漏掉。`[实跑]` 两侧的搜索都覆盖**正文**（不只标题）。
  - **标签**：`[实跑]` gh 是硬校验 —— 标了不存在的标签就整体失败、issue 不建（`could not add label: ... not found`）；**glab 会自动把标签建出来**（`glab issue create -l probe-xxx` 之后 `glab label list` 从 0 变 1）。⇒ 想在 GitLab 上守住"不新建标签"，必须先 `glab label list` 拿名单再映射，不能直接交给 CLI。
  - **正文保真度**：`[实跑]` 两侧都会被规范化，**"逐字一致"必须是"除已知规范化外一致"**。gh 读回比原文**多一个换行**；glab 读回把 **LF 全变成 CRLF**。
  - **写后回读**：`gh issue view <N> --json body --jq .body` / `glab issue view <N> -F json | jq -r '.description'`，再跟本地那份 `diff`。**diff 会被上面的规范化弄红**，所以比对前要先把两侧的行尾与尾部空行归一，再判"实质一致"。
  - **误建后的收敛**：`[实跑]` `gh issue delete <N> --yes` 可用（能删干净，仓库回到 0 条）；**glab 侧 403**（`glab issue delete` 与 `glab api -X DELETE` 都是 403，该账号不是项目 owner），能用的只有 `glab issue close <N>` + `glab issue update <N> -d ...` 写清"这是误建的，请删"。⇒ **GitLab 上误建留痕且收不干净，这是"创建先问"最硬的理由，确认话术里必须说出来。**
  - **`#N` 回链键**：`[实跑]` 两个宿主都不在分支名里带号（creed 是 `Gusen1453/work`；`llm/opencode` 是 `feat/mcp-loading` / `develop/tool-harness-hooks` 这类）；而 §3 建议的分支名形状是 `123-fix-export-empty-row`（**纯数字，不带 `#`**）。⇒ 若 commit-and-push 只在"看到 `#N`"时才加 `Closes #N`，照建议命名的分支**永远触发不了**。接口约定要改成：**commit-and-push 从本次会话已知的 issue 号取值**（或同时认 `#N` 与 `N-` 前缀两种形状），不能只认 `#N`。
- GitLab 落盘涉及中文标题与空格文件名，路径要加引号。
- 纪律：**一个能力一条 issue**，不 backlog 化；issue 是"以后某个时刻要处理"，不是"这次会话要做"。
- 复用 `commit-and-push/references/host-cli.md` 已沉淀的双宿主坑表，**不重新试错**。具体做法：issue 技能自己的 `references/host-cli.md` 只写 **issue 侧**的命令（create / list / search / template / update / note）与坑，共用部分（`gh auth setup-git`、`glab api` 的 `-f` vs `-F`、读写后要回读校验）**只指向** `../../commit-and-push/references/host-cli.md`，不抄第二份 —— 两份坑表必然漂移。技能是成套安装的，从 `skills/issue/references/` 往上两级到 `skills/` 再进 `commit-and-push/`，相对路径可用。
- **自建 GitLab（`code.comein.cn`）上有本机可用、且已实跑过的宿主**（`llm/opencode`）—— §6 的宿主事实大多来自它，所以"GitLab 侧只有纸面结论"不成立。

## 7. How we'll build it（short）

新增 `skills/issue/`：`SKILL.md` 是路由器（章节表 + Iron Law + 工作流 + Rationalization Table + Red Flags + Checklist），细节落在 `references/{create,templates,host-cli}.md`，三份逐字模板放 `assets/{bug-report,feature-request,custom}.md`。`references/host-cli.md` 只写 issue 侧命令，共用坑表**指向** `commit-and-push` 那一份（理由见 §6）。技能只读仓、只写远端 issue；唯一可选的仓内写入是"用户点头后落盘模板"（只写本仓宿主对应的那一个目录，三份文件），且必须在回复里说明这三个文件还没提交。回链不是本技能做的事，是**四个极薄的耦合点**（接口约定见 §6）：`grill` 出口网关加一项常驻选项、`write-spec` header 加一行 `Issue: #N`、`commit-and-push` 从会话里已知的 issue 号加 `Closes #N`、`voice.md` 放宽"适用于每个 copy artifact"那句 —— 这四处各自的技能文件要同步改，否则回链会停在纸面上、或技能之间自相矛盾。`using-creed` 的必装清单、技能表、建议流程、网关形状描述，以及 README 的"Suggested flow"文本块与技能库表也要一起加。无新模块、无新端口，全是技能文本。

## 8. Open risks

- **常驻网关选项带来决策疲劳** —— 每次设计收尾都多看到一行。缓解：它只是选项、不点即走；"不选它就直通"已写成验收项，可测。若实际用下来觉得吵，退回"只在搁置信号出现时给"（已被否决过一次，但可复评）。
- **内置模板与仓内模板漂移** —— 用户在目标仓改了自己的模板后，内置那份会显得过时。缓解：内置模板只作兜底，且落盘时带"改源头"的说明。
- **落盘后的三个文件要靠下一次 commit-and-push 才提交** —— 用户可能就此忘了，模板一直躺在工作区。缓解：落盘时明说"还没提交"。这与现有"不替用户提交"的纪律一致，是有意为之。
- **自建 GitLab 上误建不可挽回** —— 该宿主（普通成员权限）删不掉 issue，只能 close 后标注"请删"；一次手滑就永久留痕。缓解：创建一律先问已是硬规则，**且 GitLab 的确认话术里要明说"只能关闭、删不掉"**（§2 边界 8 + §5 有验收）。这是全域风险里唯一真正不可逆的那条，比 GitHub 侧的同类风险高一个量级。
- **技能级验收至今为零** —— 到这一轮为止只验过宿主能力（gh/glab 能不能做到），技能本身还没写，所以"技能会不会正确用这些能力"一条都没验过。缓解：§5 已单列 `[需造境]` 技能级条目；写完之后必须真跑一遍，否则不能声称通过。
- **agent 判断"该不该开口"失手** —— 三条件判据（§3）里"被挂起来"仍是个语义判定，近似句可能判歪：漏触发的代价是用户得自己想起来说"记一下"，误触发的代价是多一条草稿确认。缓解：条件打架时明确以"被挂起来"为准，并有意偏向漏触发；若实际发现漏得多，可放宽到"描述完整且明显可复现"时也开口。
- **"搜重"质量依赖关键词** —— 关键词太泛会天天命中无关 issue。缓解：从模板字段里抽关键词而不是从整篇草稿；命中项**展示**给用户判断，不做自动决定。
- **创建可能已到达远端而本地报错** —— 重试会双开 issue。缓解：规定不自动重试，先搜重确认（§2 边界 5），并写成验收项。
- **落盘模板绑定当前分支** —— 在错的基线上落盘。缓解：分支异常即跳过落盘并说明。
