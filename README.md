# 基于大模型的密码协议智能分析：工程实践案例

本仓库只收录**可交稿成果与可复核证据**，不收录写作流水线、多智能体 Prompt、旧版实验台账和第三方完整克隆。

交稿正文：

- [`paper/基于大模型的密码协议智能分析方法及工程应用研究.md`](paper/基于大模型的密码协议智能分析方法及工程应用研究.md)

被试模型为 **Grok 4.6**（提示与目录隔离）。专业工具为本地 **Scyther** 与 **Tamarin 1.12.0**。

## 先读哪里

| 目的 | 路径 |
|---|---|
| 读文章 | `paper/基于大模型的密码协议智能分析方法及工程应用研究.md` |
| 看四种方式得分 | `experiment/scoring/v2_mode_metrics.csv`、`experiment/scoring/v2_task_scores.csv` |
| 看 IKEv2 主案例 | `experiment/case_study.md`、`experiment/scoring/ikev2_lemma_table.csv` |
| 看 TLS 失败（无属性表） | `experiment/scoring/tls_lemma_table.csv`、`experiment/tamarin/tls13/` |
| 复跑 Scyther 生成模型 | `experiment/models/` + `scripts/run_scyther_bytes.py` |
| 核对金标（公开 ns3/nsl3/ISO 2010） | `baseline/scyther/` |
| 文献与版本表 | `refs/` |

## 目录说明

```
paper/          交稿正文（主笔版结构）
refs/           已核验参考文献与版本/来源账本
experiment/     隔离实验合同、输入包、生成模型、工具原始结果
baseline/       计分用公开模型及其 Scyther XML（不是 AI 生成物）
scripts/        仅保留 Windows 下调用 Scyther 的脚本
```

### `paper/`

终稿。图链接指向 `experiment/figures/`。旧稿 `article_final.md`（实验台账体）**未收录**。

### `experiment/`

| 路径 | 内容 |
|---|---|
| `CONTRACT.md` | 已锁定实验合同 |
| `isolation.md` | 被试隔离规则 |
| `lemma_registry.md` | IKEv2 / TLS 预注册 lemma（禁止事后改选） |
| `run_matrix.csv` | 12 条任务（3 协议 × 4 方式） |
| `packs/` | 各方式允许的输入包（M0 短描述、M1 资料、任务书） |
| `schema/` | 结构化分析字段、M3 回喂规则 |
| `models/` | 最终 SPDL（M3 为修复后版本） |
| `scyther/ns/` | NS-PK 四方式报告 |
| `scyther/nsl_round1/` | NSL 首轮（含 M0/M3 语法失败） |
| `scyther/nsl_m3_final/` | NSL 完整框架第 2 轮 |
| `scyther/iso_round1/` | ISO 首轮 |
| `scyther/iso_m3_final/` | ISO 完整框架第 2 轮 |
| `tamarin/ikev2/` | `ikev2.spthy` 与 5 条 lemma 日志（verified） |
| `tamarin/tls13/` | TLS13Tamarin 展开理论在 Tamarin 1.12.0 上的崩溃日志 |
| `scoring/` | 计分口径与汇总表 |
| `figures/` | 正文图 1、图 4 |

四种方式在表中的内部名：`direct`（直接大模型）、`retrieval`（检索增强）、`structured`（检索+结构化）、`full_loop`（完整框架）。

### `baseline/scyther/`

公开模型复跑，只用于「结果一致」分母：

- `P01_nspk_core`：Needham–Schroeder 公钥三消息核心
- `P02_nsl_core`：Needham–Schroeder–Lowe
- `P05_iso9798_2_3`：ISO/IEC 9798-2 机制 3 的 2010 年编码（≠ 2019 标准）

### `refs/`

- `references.md`：GB/T 7714 顺序编码
- `source_ledger.csv`：来源登记
- `protocol_version_map.csv`：现行文本 vs 公开模型版本

## 主要结果（与正文一致）

- 最终任务完成率：直接大模型 1/3，检索增强 2/3，检索+结构化 3/3，完整框架 3/3（完整框架**首轮**仅 1/3）。
- NS-PK 四种方式均与公开 ns3 一致（发起方成立，响应方 Secret/Niagree/Nisynch 被证伪）。
- Minimal IKEv2（RFC 7815 口径，**不是** RFC 7296 全文）：`exists_session`、`aliveness`、`weak_agreement`、`agreement`、`key_secrecy` 全部 verified。
- TLS 1.3 draft-21 预注册 3 条 lemma：Tamarin 1.12.0 在 `shapeTerm` / `F_State_C1` 崩溃，**无** verified/falsified 摘要；不得写成 RFC 9846 结论。

## 复现要点

1. Scyther：Windows 可执行文件 + `scripts/run_scyther_bytes.py`（按二进制/latin-1 读输出）。NS 用 `--unbounded`，ISO 用 `--max-runs=5`。
2. Tamarin：WSL 中 `tamarin-prover` 1.12.0。IKEv2 **不要**加 `--quit-on-warning`（会把 derivation-check 超时误杀成失败）；使用 `--derivcheck-timeout=0`。
3. 公开 IKEv2 模型来源：[mnm-team/tamarin-ikev2](https://github.com/mnm-team/tamarin-ikev2) 的 `ikev2.spthy`（本仓库已放入运行所用副本）。
4. TLS 模型来源：[tls13tamarin/TLS13Tamarin](https://github.com/tls13tamarin/TLS13Tamarin) `src/rev21`（本仓库**不**整库收录；Windows 无法检出路径 `rev10+`）。

## 明确不收录（过程文件）

以下内容留在原工作区，**不进入本仓库**：

- 多智能体总控与各 AGENT Prompt（`00_MASTER_PROMPT.md`、`agents/` 等）
- 旧正文 `article_final.md` / `draft.md` 及 Track-R/G/F/E 台账
- `models_track_*`、`raw_skill_results` 中除金标三条以外的轨道产物
- 玩具 `SignedDH` / TLS 替代模型
- 旧图（四轨柱状图、热力图等）
- `优秀历史案例/` 对照稿
- 第三方完整 git 克隆（TLS13Tamarin、tamarin-ikev2 全库）
- 输入包审阅稿 `REVIEW.md`、禁止清单草稿等写作过程文件

## 许可与引用

正文与实验数据用于工程实践案例交付。引用请同时给出本仓库与 `refs/references.md` 中的原始规范/工具文献。
