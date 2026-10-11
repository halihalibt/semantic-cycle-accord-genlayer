# SCA-3 V1 — 手动失败恢复

DOCUMENTED BUT NOT EXECUTED。先查证，再决定是否重试。存在交易哈希时先看原交易；可能成功时先读取合约，防止重复操作。不要自动上诉、finalize、请求 faucet 或发送补偿交易。

| 看到的情况 | 处理方式 |
| --- | --- |
| 本人拒绝签名 | 取消操作；记录是否已产生哈希。不能假定已上链。确认没有提交和状态变化后才重新准备 |
| 网络错误 | 不签名；回到 studio.genlayer.com，核验61999。已发出的交易先查原网络与哈希，停止本执行序列 |
| 测试 GEN 不足 | 停止；记录余额和实际预算。后续由本人按另行授权的免费测试币方式处理，不购买 GEN、不输入凭据 |
| RPC 429 | 停止重复请求，按 Retry-After 或服务提示等待；单路、低频查状态，不叠加重试。没有提示也不得密集刷新 |
| 已提交但暂无 receipt | 保存哈希、时间、账号、参数；查该哈希及权威状态，不能再次点写入 |
| ACCEPTED 尚未 FINALIZED | 等待原交易最终状态；不把 ACCEPTED 标记完成，不进入依赖写入 |
| FINALIZED 但执行错误 | 不是成功。保存原始错误/trace，读取状态确认是否变更，停止并报告；不改变源码/Prompt |
| Validator 分歧 | 保存各轮、轮换、参与者与原始结果；停止本测试序列交审查。不强制 FIT，不刷相同评估 |
| UNDETERMINED | 保存所有证据并停止；不能保证稍后成功，不自动上诉或新发交易 |
| 超时或页面断连 | 仅代表观察超时。先查哈希和合约；没有哈希也须排查是否提交成功，不能直接重发 |
| 重复操作 | 查原交易与状态。create 可能产生额外 Intent；assess 对同 snapshot 有防重放；eligible PENDING 内的重复 confirm 返回 false，terminal confirm 拒绝。不要把 false 当新增确认 |
| Intent ID 与预计不同 | 保存实际返回，用 get_intent 和 owner records 核实。重新映射 A/C/B 参数；没有证据不猜 ID |
| Cycle ID 与预计不同 | 用 assessment 返回及 get_assessment 核对实际 cycle_id，再 get_cycle；不拿另一 Cycle 的 ID |
| 缺少 snapshot_id | 不确认。get_cycle(actual_cycle_id) 必须 found=true 并给出真实 digest；缺失则停止 |
| STALE_VERSION | 读取三 Intent 的当前版本、内容、状态、到期时间；旧参数不能重用。修改后需重新审查和明确授权，不能偷偷 update |
| Intent 到期 | 不评估/确认。已超期 PENDING 的清理或创建新 Intent 是另一笔写入，需单独批准；本轮不执行 |

查询优先使用 Studio 的真实交易详情及 Stable Explorer。本轮通过空参数请求核实接口分派能力；这不证明任何真实交易的 receipt/status 语义。后续用真实哈希确认可用的 `eth_getTransactionByHash` / `eth_getTransactionReceipt` 或实际 Stable 支持的查询接口。`gen_getTransactionReceipt` / `gen_getTransactionStatus` 若返回 method not found，不能硬套新版文档、数字状态码或反复请求，也不代表网络停机。禁止 `sim_getFeeConfig`。

每次恢复记录：原哈希（如有）、实际 signer、方法/参数、错误、最后已知共识状态、执行结果、读到的状态及下一步是否需要另行批准。无法确定时 STOP，把证据返回审查。没有确定成功，不做后续依赖写入。
