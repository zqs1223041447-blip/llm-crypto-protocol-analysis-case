# 任务：Needham–Schroeder–Lowe 公钥协议（NSL）

## 范围（四种方式共用）

分析 **Lowe 对 Needham–Schroeder 公钥协议的修复版**（文献中称 NSL / Needham–Schroeder-Lowe）。假定双方已经持有对方长期公钥，三消息核心，不含认证服务器。必须按修复后的协议建模，不要建成未修复的 1978 核心。

## 输出

1. 一份可被 Scyther 解析的 SPDL（角色至少发起方与响应方）。
2. 为每个角色声明 `Secret`、`Niagree`、`Nisynch`（或同等认证/机密性 claim）。
3. 攻击者：Dolev-Yao 公开网络。

## 禁止

- 读取任何现成 `.spdl` 参考实现
- 把符号模型结果写成实现安全证明
