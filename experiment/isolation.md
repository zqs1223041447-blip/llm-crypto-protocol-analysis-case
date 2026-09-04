# 隔离规则

## 主试（本对话 / 编排进程）可以

- 准备本目录输入包
- 启动子任务并只注入该任务允许的文件
- 调用 Scyther
- 打开 `scoring/` 与 `raw_skill_results/` 金标 XML 做打分
- 把 M3 的工具原始输出（stderr、xml 摘要、非金标）回喂同一子任务

## 主试不可以

- 在本污染对话里撰写待评 SPDL
- 把金标路径、claim 表、article_final、本 grilling 纪要写入子任务提示

## 子任务（被试）可以读

仅其工作目录内的输入包，例如：

- `packs/task_briefs/<协议>.md`
- `packs/M0_shared/<协议>.md`
- （M1/M2/M3）`packs/M1/<协议>.md`
- （M2/M3）`schema/structured_analysis.md`
- （M3 第 2 轮起）本任务上一轮工具输出

## 子任务禁止读

- `models_track_*`
- `results/`、`raw_skill_results/`、`ground_truth/`
- `article_final.md`、`draft.md`、`analysis_brief.md`
- `experiment_v2/scoring/`
- `experiment_v2/REVIEW.md`（含金标摘要）
- 本对话纪要

一旦发现子任务读了禁止路径，该条作废重跑。

## 正文必须披露

单操作者、提示与目录隔离，不是双盲实验室。
