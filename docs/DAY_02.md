# 第 2 天：补齐首版验收与演示

日期：2026-09-16。

## 根据真实进度调整

用户确认今天有 1 小时，昨天尚未亲自验证。因此本次推进首版运行与理解验收，原定的自定义缺失值功能顺延，不新增业务功能。
本次独立交付是可供陌生人重复使用的正常／边界／异常演示包。

| 任务 | 具体工作与岗位价值 | 预计时间 | 交付与验收 |
| --- | --- | --- | --- |
| 主要目标：亲自跑通首版 | 执行三种 CSV 场景并观察 JSON／错误／退出码，练输入契约与故障定位 | Codex 准备 10–20 分钟；用户 20 分钟 | examples/review 三个样例及说明；本人记录每条命令的实际结果，与表中预期核对 |
| 配套 1：解释一条统计路径 | 阅读 analyzer 与 CLI，说明空值、查重和错误出口，练可维护 Python 代码阅读 | 用户 25 分钟 | 两道问题的本人回答，以及自己样例的一次预测与验证 |
| 配套 2：留下证据与阻碍 | 运行现有测试、核查可访问的 CI、填写作业，练真实工程汇报 | Codex 10–15 分钟；用户 15 分钟 | 测试命令与结果、个人作业、更新摘要；未取得的远端结果明确标记 |

Codex 时间是预估；用户实际耗时由用户填写。最小 20 分钟版本：跑 scores.csv 和 wrong_width.csv，记录退出码并解释为什么不同，其余顺延。

## 你的 60 分钟

### 0–20 分钟：运行与比较

```powershell
Set-Location 'D:\githubupload\daydayup'
python -m datacheck examples/review/scores.csv
$LASTEXITCODE
python -m datacheck examples/review/header_only.csv
$LASTEXITCODE
python -m datacheck examples/review/wrong_width.csv
$LASTEXITCODE
```

预期依次是：3 行／1 缺失／1 重复、退出 0；0 行／2 列、退出 0；第 4 条记录列数错误、退出 2。
详细字段见 [演示包](../examples/review/README.md)。先查看 CSV 并写预测，再查看预期或执行命令。

### 20–45 分钟：阅读与动手

按 `__main__.py → analyze_csv → _analyze → 返回报告` 的调用顺序看代码。
重点只看三处：字段 `strip()`、`seen` 查重、`row_count` 为 0 时的比例计算。
在自己的 `reports/my-scores.csv` 中改一个字段，先预测结果再验证。

两个问题，请用自己的话回答：

1. scores.csv 中重复行为什么仍包含在总行数与缺失比例分母里？如果再加一条 `Alice,0`，总行数、重复数和 score 缺失比例各是多少？
2. scores.csv 有缺失和重复却退出 0，wrong_width.csv 为什么退出 2？调用它的脚本应该如何区分“生成报告失败”和“报告显示质量问题”？

先回答，再由教练反馈；不能用 Codex 的运行结果替代本人验证。

### 45–60 分钟：回归与交作业

```powershell
python -m unittest discover -s tests -v
$LASTEXITCODE
```

按 [WORKFLOW](WORKFLOW.md) 填完整交作业模板，附两道问题答案。至少提供三种演示的实际结果、测试结果、你亲自改过的字段和实际耗时。
今日用户作业未收到前，理解状态维持“待补充”；没有自动判定为已通过。

## 独立完整的 Codex 执行提示词

```text
在 D:\githubupload\daydayup 仓库继续 DataCheck，远端 https://github.com/Edgar-30/daydayup.git。
用户是 Python 最熟悉的大三学生，目标 Python 后端／数据方向，每天约 1 小时阅读验证。2026-09-16 用户确认有 1 小时，但首日尚未亲自验证。

今天目标是首版验收演示包与学习交接，自定义缺失值功能顺延。
先检查 git status --short --branch、remote、最近提交与远端状态，阅读 AGENTS.md、README.md、docs/PROGRESS.md、docs/DAY_02.md、docs/WORKFLOW.md、最近 daily 记录及 datacheck/tests 实现。尊重用户未提交修改和中断遗留文件。

范围：补可复用的正常／仅表头／列数错误演示文件与中文说明，维护任务和进度记录。如果已有内容完成则检查后复用，不重复改写或制造提交。不加入 API、数据库和新的缺失值规则；确实发现缺陷时先定位，再做与验收相关的最小修复。

预期：scores.csv 为 3 行、2 列、1 缺失、1 重复、重复编号 [4]、score 缺失比例 0.3333，退出 0；header_only.csv 为 0 行、2 列、0 缺失与重复，比例 0.0，退出 0；wrong_width.csv 不产生 JSON，stderr 提示 Record 4: expected 2 fields, got 3.，退出 2。保留原来的输入和输出文件保护。

检查：实际运行三个示例并核对输出及退出码，运行 python -m unittest discover -s tests -v，运行 git diff --check。按风险验证，文档与样例无需新写一层重复测试。远端 CI 若可读取就检查对应提交的运行，无法读取则说明原因与未验证范围，不关闭 TLS 校验，不伪造结果。

给用户安排 20 分钟运行、25 分钟代码阅读和手动改样例、15 分钟回归与复盘；20 分钟最小版本只跑正常与错误场景并解释退出码。提供两道与实际代码相关的问题，等待用户答案后反馈。个人掌握与 Codex 自检分开记录。

用户已授权本仓库正常实现、调试、提交和推送。确认变更归属、检查通过后仅暂存当日相关文件，使用有意义的提交，正常推送 main 并核对远端哈希；禁止强推和改写历史。无实质变更不提交。权限或网络阻碍如实报告，不泄露凭据。

最终报告修改、验证命令与结果、遗留问题、代码理解要点与取舍；分别说明文件已修改、本地提交的真实 hash、是否已推送及验证链接。更新 docs/PROGRESS.md 和当天记录，尚未执行的步骤使用待验证状态，不替用户写完成作业或掌握结论。
```
