# SCA-3 V1 — 手动 Studio 执行包

DOCUMENTED BUT NOT EXECUTED。本包仅供后续单独批准后的手动执行。本轮没有部署、交易或签名。当前没有真实合约地址、交易哈希或 snapshot_id。

## 1. 部署前

1. 打开 https://studio.genlayer.com/ 。只用 Stable Studionet，Chain ID **61999 / 0xf22f**，RPC https://studio.genlayer.com/api 。不要进入 studio-dev 或其他网络。
2. 下载完整原始 Python 文件：https://github.com/halihalibt/semantic-cycle-accord-genlayer/blob/7906f4e3c7c619ffdef0ae12147a78f5d018cebb/contracts/semantic_cycle_accord.py 。GitHub 文件页选择原始文件下载；保留两行 GenVM/Depends 文件头，不编辑源码。
3. Windows PowerShell 核对文件：`Get-FileHash .\semantic_cycle_accord.py -Algorithm SHA256`。必须等于 `88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442`。
4. 构造参数：**无**。`__init__(self)` 没有其他参数。参数列表是空数组 `[]`，不是空字符串、0、钱包地址或管理员。具体 JSON 外壳需按当前 Studio 表单确认。
5. 仅由你操作自己控制的钱包。核对页面右上角的实际账号地址。准备三枚不同地址 A/B/C；把公开地址记下来即可。不要发给 Work 私钥、助记词、钱包导出、凭据或二维码。不要把本次云浏览器自动显示的账号当成你的执行账号。
6. 查看你实际账号的测试 GEN 余额。各操作的准确估费/预算/实际消耗目前 UNKNOWN；`eth_gasPrice=0` 只能证明外层兼容层报价，不能证明协议费用为零。签名前查看 Studio/钱包实际费用及余额；若要求现金付款、换网或无法解释费用，STOP。
7. 如果界面没有网络选择器，域名和只读 eth_chainId 必须对应上面的 Stable 网络；不要用“GenLayer Studio”标题代替链 ID 核验。错网时取消准备操作，回到正确网址，再核验。不签名。

## 2. 后续获准后的部署步骤（本轮未执行）

1. 官方文档说明：在 Your Contracts 处使用 New Contract / Add From File，把完整文件载入，点击文件打开编辑器。本轮实际看到了 Your Contracts、上传图标和模板列表；图标提示及当前按钮文字 **NEEDS MANUAL CONFIRMATION**。
2. 用当前界面的 Run and Debug / 播放入口打开部署面板。这些名称来自官方文档，当前部署面板、费用确认和钱包交互没有打开，均 **NEEDS MANUAL CONFIRMATION**。
3. 检查 Constructor Inputs：应没有输入项，空参数。若出现必填参数或源码/ABI不符，停止并返回截图，不能猜填。
4. 检查完整源码、Stable 链、实际签名账号、费用/预算和余额。只有收到后续明确授权，你本人才能按实际 Deploy 控件发起部署并亲自审阅/批准签名。Work 不点击部署或签名。内置账号与外部钱包的确认界面可能不同；不能假定每种内置钱包都会弹出扩展钱包签名框。若没有清晰的本人确认流程，先停止核实。
5. 从真实交易时间线或详情中复制交易哈希和合约地址。保存共识状态、执行结果、Validator/round 信息及日志。界面位置 **NEEDS MANUAL CONFIRMATION**；只有哈希不算成功。不要在等待过程中反复点击 Deploy。
6. 等待 **FINALIZED + 成功执行**，通过 Stable Explorer https://explorer-studio.genlayer.com/ 搜索实际哈希，复制其实际详情链接。不要猜 Explorer URL 路径。失败/未定/分歧时保留日志并停止。

回传模板（填真实值，未获得就写 UNKNOWN）：

```text
network / chainId: Stable Studionet / 61999
actual_signer: <实际公开地址>
source_sha256: 88de2802bbe4e795dcae2bb0c4028477133d41bdc9b7940d6aef273367ded442
constructor_args: []
deployment_tx_hash: <实际值，当前不存在>
contract_address: <实际值，当前不存在>
consensus_status: <原始状态>
execution_result: <原始执行结果>
validator_round_evidence: <原始详情或 UNKNOWN>
explorer_url: <实际复制链接>
fee_estimate / budget / consumed: <分别填写或 UNKNOWN>
error_or_trace: <原始输出或无>
```

## 3. 部署成功后的首次只读检查（尚未发生）

1. 选择实际已部署合约，打开官方文档所述 Read Methods；实际标签 **NEEDS MANUAL CONFIRMATION**。
2. 调用 `get_protocol_stats(offset=0, limit=50)`，明确填写 0 和 50。此步骤是只读，不执行任何 write。
3. 新合约预期：protocol=`SCA-3-V1`，network_id=61999，intent_total/cycle_total/active_total/aborted_total/expired_cycles_cleaned/assessment_total 均为0，effective_intent_counts_page 中 OPEN/RESERVED/CONSUMED/CANCELLED/EXPIRED 均为0；offset/next_offset=0，has_more=false，semantic_matching_available=true。
4. true 只说明方法已实现，不证明真实 AI 共识已通过。保存实际读出结果；不一致时停止。
5. 后续三钱包参数和读出闸门在 [ONCHAIN_E2E_TEST_VECTORS.md](ONCHAIN_E2E_TEST_VECTORS.md)。每笔写入都等待最终成功并读取验证，顺序为 A创建→B创建→C创建→参与者评估→A确认→B确认→C确认。不要在本阶段执行。

## 4. 依据与局限

2026-10-11 公开页面可访问，浏览器只观察页面，没有载入合约、创建/导入签名钱包、请求 faucet、访问秘密或执行交易。页面存在账号余额显示；本轮没有验证用户钱包或签名弹窗。按钮、费用和部署细节须后续本人确认。

官方资料（本轮查阅；文档也包含更新的 v0.6 内容，不能据此替换 Stable 工具链）：

- https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio
- https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio/loading-contract
- https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio/deploying-contract
- https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio/execute-transaction

STOP：本轮不部署、不签名、不发送交易、不合并 PR、不进入 4B/4C。
