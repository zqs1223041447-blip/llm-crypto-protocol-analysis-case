# 主案例：Minimal IKEv2

- 规范：RFC 7296（全文不在结论内）；模型目标 RFC 7815 Minimal IKEv2。
- 模型：`tamarin-ikev2/ikev2.spthy`（SHA-256 `53d1826f88accf17957308300809fdb3cf76e9c437855332ebaae2eb94336411`）
- 工具：tamarin-prover 1.12.0，`--derivcheck-timeout=0`，不用 `--quit-on-warning`
- 预注册结果：exists_session / aliveness / weak_agreement / agreement / key_secrecy 全部 verified
- 封装失败（不计为协议结论）：quit-on-warning + derivation-check timeout → missing_summary
- 边界：非 RFC 7296 全文；符号抽象；发起方取向模型
