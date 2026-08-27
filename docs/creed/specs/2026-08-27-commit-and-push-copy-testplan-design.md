# commit-and-push 文案反晦涩 + Test plan 拆分 Spec

**Status:** Draft
**Date:** 2026-08-27
**Owner:** Gusen1453

## 1. One-liner（board slide）

让 commit/PR 文案像用户自己打的一行字（短、直接、说结果），消息格式严格符合 Conventional Commits、中英皆可按用户 register，再把 Test plan 拆成"已跑过的脚本证据"和"留给人的验收"两块——reader 一眼分清什么是事实、什么是该我动手的。

## 2. User scenarios（source of truth）

### Happy path（反晦涩·声音）
- **Who:** 用户本人，上一个特性开发中和 coding agent 多轮交互过（描述需求、改过文案、纠过方向）。
- **When:** 特性收尾，用户说"commit / push / 开 PR"。
- **Does:** 技能先"听"整个特性生命周期里用户说这个改动时的原话（不是只看当前最后一轮；跨会话并有记忆档案时沿用），抽出用户的 register（短句、直接、说结果、具体名词动词受偏爱）；再叠一份反晦涩硬规则（结果动词开头 / subject ≤~50 chars / 禁堆叠修饰词 / 禁 vague verb）。
- **Sees:** commit 标题格式合规（`type(scope): subject`，type 走 Conventional Commits 枚举，scope 从仓库惯例取）、一行看得懂，正文照用户中英文偏好书写；PR Summary 读起来像自己打的字，reviewer 零解码负担。

### Happy path（Test plan 拆分）
- **Who:** PR reviewer / 用户本人验收。
- **When:** 打开 PR description 的 `## Test plan`。
- **Does:** 发现两个清楚分开的块：`Automated (ran before commit)` 里是已经跑过的脚本验证（命令+结果，证据性质）；`Acceptance (user/product)` 里才是开放的人工验收步骤。
- **Sees:** 不再把"跑测试"这种已成事实的事当待办打勾——需要自己动手的是什么一目了然。

### Failure / edge（素材薄）
- **Who:** 用户，只说了"commit 这个"，会话里没有该特性的原话。
- **When:** 取样式信号不足。
- **Sees / system does:** 退回纯硬规则清单（结果动词、短、无 vague verb），文案稳定但不刻意模仿个人腔调；不编造用户"风格"。

### Failure / edge（诚实原则）
- **Who:** 技能本身。
- **When:** Automated 块里某项脚本并没有在提交前实际跑过。
- **Sees / system does:** 该项**不勾选**、不写进已跑列表；以实际跑过的那些为准，或在 Acceptance 里标明"待验证"。

## 3. Scope

**In:**
- commit 标题/正文与 PR title/Summary 采纳"会话取样（全特性生命周期）+ 硬规则"的声音机制
- commit 消息强制 Conventional Commits 格式：`type(scope): subject`，type 走标准枚举（feat/fix/docs/chore/refactor/test/…），scope 从仓库 commit 惯例取（本仓库为 `skills` 等）；subject 仍受反晦涩硬规则约束
- commit 语言中英皆可，跟随用户的偏好/register（会话原话是哪种就以哪种落 commit，不额外翻译）
- 跨会话记忆档案：稳定 register 沉淀后后续会话沿用（hook 挂在本项目会话记忆）
- `## Test plan` Iron Law 强制章不变，内部分 `Automated (ran before commit)` 与 `Acceptance (user/product)` 两块
- 反晦涩硬规则清单作为最小回退

**Out (this round):**
- ~~从 `git log --author` 取历史 commit 作为风格源~~ — 否决：AI 协作者仓库的历史 commit 多为 AI 写的晦涩长句（本仓库那条 `fix(skills): make skill copy English-only Translate…` 就是），等于原地再训练一遍晦涩
- ~~强制 commit 只用一种语言（如 English-only）~~ — 否决：中英皆可通过，跟随用户 register；格式合规比语言唯一更重要
- 不重写 Iron Law 章节结构（仍是单个 `## Test plan` 强制章）
- 不改 test-design / tdd / review 的职责边界

## 4. Decision log（mentoring）

| Decision | Chose | Rejected | Why (user/business impact) |
|----------|-------|----------|----------------------------|
| 声音来源 | A) 会话取样（全特性生命周期）+ 记忆档案 + 硬规则回退 | C) git log --author 取历史 | PR 像自己写的一样可读、可持续；历史取样会复制已有晦涩。拒绝 C 是因为本仓库反例就在 git log 里。 |
| commit 格式 | 强制 Conventional Commits（`type(scope): subject`，type 走标准枚举） | 自由句式 / 仅模板无约束 | reviewer 和工具（changelog/revert/CI 解析）都能稳定工作；换中英不破格式。 |
| commit 语言 | 中英皆可，跟随用户 register | English-only 强制 | 用户怎么说话就怎么写，不额外翻译；"像自己打的一行字"要求语言也像自己。 |
| 取样窗口 | 整个特性开发的多轮用户原话 | 只看最近一轮 | 一个特性靠多处语境才能说清；只取末轮会丢失 first intent。 |
| Test plan 结构 | A) 单强制章内拆两块 | B) 两个顶层章 | reviewer 一眼分清证据 vs 待办，又不破坏 Iron Law 的"必须含 ## Test plan"。 |

## 5. Acceptance（demo / test language）

- [ ] 场景：会话里用户完整描述过一个特性（含纠偏），最后的 commit + PR 标题/Summary 能看出用户腔调（短句/结果先行/具体名词），且没有叠形容词、没有 vague verb → observable: 标题 ≤ ~50 chars，Summary 用结果动词。
- [ ] 场景：commit subject 符合 `type(scope): subject`（type 在标准枚举内），语言中英皆可随用户偏好 → observable: `git log --oneline` 每行都可被 changelog/CI 工具解析。
- [ ] 场景：会话里用户只说了"commit 这个" → 文案走硬规则回退，风格稳定，不模仿任何噪音腔调。
- [ ] 场景：APR 含测试 → `## Test plan` 出现两块，Automated 块只列**实际跑过**的脚本（带命令），Acceptance 块是留给人的人工步骤。
- [ ] 场景：Automated 某脚本没跑 → 该项不在已跑列表中如实出现，不得勾选。

## 6. Constraints

- commit 消息必须符合 Conventional Commits 格式硬规则（type 枚举 / scope 惯例 / subject 反晦涩），语言中英皆可、随用户 register
- commit 消息语言与「skill 文件内容」语言解耦：skill 文件 copy 仍跟随仓库 English-only 惯例（4802aa2），commit 消息不受此约束
- 硬规则约束力高于取样：取样结果违反任何反晦涩硬规则（含 commit 格式）即被修正

## 7. How we'll build it（short）

在 commit-and-push 技能内，于撰写 commit/PR 文案前插入"声音取样"步骤（扫描本会话或记忆档案，抽取 register 概要），并将反晦涩硬规则收敛为一条小清单；commit 消息强制 Conventional Commits 格式（`type(scope): subject`，type 枚举 + subject 反晦涩），语言中英皆可随 register；Test plan 模板改为两块结构。均为 SKILL.md 文本改动，无新模块/端口/IO。

## 8. Open risks

- 记忆档案可能沉淀了过气风格 → 按项目会话记忆陈旧策略处理；以当前会话原话为更高优先级
- "像用户腔调"难以自动验证 → 用 Acceptance 的反例判定：reviewer 说"还是不知道要我查什么"即失败