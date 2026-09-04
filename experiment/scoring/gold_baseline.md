# 金标（仅打分，不进被试包）

工具：`scyther-w32.exe` SHA-256 `6ab49729c73d3f0691ac2c58f893149fd739af17908ab0be8774751662f019ad`

## NS-PK（P01 `ns3`，无界）

来源：`raw_skill_results/scyther_track_r/P01_nspk_core/report.json`

| 角色 | 类型 | status |
|---|---|---|
| I | Secret | verified |
| I | Secret | verified |
| I | Niagree | verified |
| I | Nisynch | verified |
| R | Secret | falsified |
| R | Secret | falsified |
| R | Niagree | falsified |
| R | Nisynch | falsified |

计分时同一角色同一类型多条 Secret 合并为该类型一条：I Secret=verified，R Secret=falsified。

## NSL（P02 `nsl3`，无界）

来源：`raw_skill_results/scyther_track_r/P02_nsl_core/report.json`  
8 条 claim 均为 verified（I/R × Secret×2 + Niagree + Nisynch）。

## ISO/IEC 9798-2-3（P05，`--max-runs=5`）

来源：`raw_skill_results/scyther_track_r/P05_iso9798_2_3/report.json`

| 角色 | 类型 | status |
|---|---|---|
| A | Commit | falsified |
| A | Alive | bounded |
| A | Weakagree | bounded |
| B | Commit | falsified |
| B | Alive | bounded |
| B | Weakagree | bounded |

新模型若只用 Secret/Niagree、没有 Commit：只对重叠类型计 agreement；notes 必须写“claim 集合与 2010 公开模型不同，不能写成复现 Basin 反例”。  
新模型跑无界若与 max-runs=5 金标冲突：以**同一命令行参数**复跑金标后再比，或 notes 标明参数不同、该格不进入分母。

## 禁止

不要把本文件路径或表格贴进子任务提示。
