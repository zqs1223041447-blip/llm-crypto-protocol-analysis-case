# 预注册 lemma（跑之前锁定，禁止事后只报告变绿的）

## IKEv2（②）

- 仓库：`experiment_v2/public_models/tamarin-ikev2`
- 模型：`ikev2.spthy`（Minimal IKEv2 / RFC 7815 口径，**不是** RFC 7296 全文）
- 不跑：pq-*、full-model（内存/时间超出本实验预算时不作为主案例）

预注册：

1. `exists_session`（exists-trace，可执行性）
2. `aliveness`
3. `weak_agreement`
4. `agreement`
5. `key_secrecy`

超时上限：每条 lemma 600 秒。超时记 timeout，不删 lemma。

## TLS 1.3（③）

- 目标：TLS13Tamarin `src/rev21` 点名 lemma
- 口径：draft-21，**不是** RFC 9846
- 克隆因 Windows 路径 `rev10+` 失败时改在 WSL/`D:\grokSpace\downloads` 检出

检出位置：`D:\grokSpace\downloads\TLS13Tamarin\src\rev21`（WSL，避开 Windows 的 `rev10+` 非法路径）。
实际模型文件：`proofs/injective_auth.spthy`（已展开的 draft-21 理论）。

预注册（跑前锁定）：

1. `handshake_secret`（机密性类）
2. `secret_session_keys`（机密性类）
3. `injective_mutual_entity_authentication`（认证类）

每条 timeout 600s。该理论体量大，超时记 timeout，不事后改选变绿 lemma。不声称 RFC 9846。

若全模型无法在 600s×3 内得到任何属性行：TLS 进失败/局限，不充当主案例。
