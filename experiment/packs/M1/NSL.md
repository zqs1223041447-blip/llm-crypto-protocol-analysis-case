# M1 资料：NSL（1978 核心叙述 + Lowe 1996 修复）

## A. 1978 公钥会话核心（修复前，供对照）

Needham & Schroeder, CACM 1978。公钥预分配后的三步：

1. A → B : {Na, A}Kb  
2. B → A : {Na, Nb}Ka  
3. A → B : {Nb}Kb  

（{·}K 表示用公钥 K 加密。Ka/Kb 为 A/B 的公钥。）

## B. Lowe 1996 对修复的定义

来源：Lowe, G. Breaking and Fixing the Needham-Schroeder Public-Key Protocol using FDR. TACAS 1996 / LNCS 1055.  
公开摘要：用 CSP/FDR 分析该协议，发现攻击者可冒充另一主体；修改协议后在小系统上显示安全，并给出规模化论证。

修复：在第 2 条消息的密文中加入响应者身份 B。Paulson 对 Lowe 修复的通行写法（Cambridge NS_Public 教程对 Lowe 协议的转述）：

1. A → B : {Na, A}Kb  
2. B → A : {Na, Nb, B}Ka  
3. A → B : {Nb}Kb  

本任务建模 **B 节（NSL）**，不要建成 A 节。

## C. 不提供

FDR 代码、Scyther SPDL、金标 claim 表。
