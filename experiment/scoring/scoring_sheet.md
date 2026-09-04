# 打分表（主试用；禁止放入被试目录）

每个任务一行，12 行。字段与 Q11A 一致。

| task_id | protocol | mode | parse_ok | n_claims | completion | agreement_num | agreement_den | known_attack_reproduced | human_intervention | wall_clock_s | repair_rounds | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 完成（completion）

- 1：Scyther 解析成功且至少一条非 Reachable claim 具有 verified/falsified/bounded。超时但已有部分 claim → 1，notes 记 timeout。  
- 0：语法失败、0 claim、或未交出模型。

## 一致（agreement）

只在金标也声明了的 **角色 × claim 类型** 上计。  
一致：同角色同类型的 status 相同（verified / falsified / bounded）。  
金标有而模型无：该格不计分，notes 记 missing。  
模型有而金标无：不进入分母。  

**NS-PK 特例（Q11A）**：若模型把发起方与响应方的 Secret 都做成 falsified，与金标 ns3（发起方 Secret verified、响应方 Secret falsified）不一致。不得记 known_attack_reproduced=1。

known_attack_reproduced 仅 NS-PK：响应方认证或响应方 nonce 机密性为 falsified，**且**发起方核心机密性不为“双方一起错”。NSL、ISO 填 NA。

## 人工介入

只计改超时、改编码包装、环境。主试改 SPDL 语义 → 该任务失败，不算介入成功。

## 耗时

该任务第一次模型调用到停止（含 Scyther）。M3 含各轮之和。
