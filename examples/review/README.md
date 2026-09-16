# 3 分钟演示：统计成功、零数据、输入错误

这三个文件使用虚构数据。请从仓库根目录执行下面的命令。
`$LASTEXITCODE` 必须紧接 Python 命令读取，避免被下一条外部命令覆盖。

## 1. 有缺失与重复，但可以生成报告

```powershell
python -m datacheck examples/review/scores.csv
$LASTEXITCODE
```

预期退出 0，JSON 包含：

| 字段 | 预期值 |
| --- | --- |
| row_count | 3 |
| column_count | 2 |
| missing_cell_count | 1 |
| duplicate_row_count | 1 |
| duplicate_record_examples | [4] |
| columns 中 score 的 missing_ratio | 0.3333 |

`0` 是有效文本，Bob 的空分数才是缺失。重复行仍计入总行数和缺失比例分母。
退出 0 表示报告生成成功，不表示数据没有质量问题。

## 2. 只有表头

```powershell
python -m datacheck examples/review/header_only.csv
$LASTEXITCODE
```

预期退出 0：0 行、2 列、0 缺失、0 重复，两个字段的缺失比例都为 0.0。
这是没有数据记录的合法文件；并不证明它满足业务方对数据量的要求。

## 3. 一行多了一个字段

```powershell
python -m datacheck examples/review/wrong_width.csv
$LASTEXITCODE
```

预期退出 2，不输出 JSON，错误写入 stderr：

```text
datacheck: Record 4: expected 2 fields, got 3.
```

不要忽略多出的字段，否则可能把错误结构当成有效数据。
本项目记录编号包含表头，跳过表头后的空白行，和含多行字段文件的物理行号不一定相同。

## 用户动手部分

先预测结果，再在 `reports/` 中新建或编辑你自己的样例；不要覆盖仓库中的固定演示文件。
例如把 `scores.csv` 复制到 `reports/my-scores.csv`，将 Bob 的分数改成 `NULL`，再次运行。
把预测、实际缺失数和解释填写到当天作业，不要把本页预期当成自己的运行证据。

## 回归检查

```powershell
python -m unittest discover -s tests -v
$LASTEXITCODE
```

当前 17 项测试应通过、退出 0。演示包用来帮助人运行和理解，自动测试用来发现行为回退，两者不替代个人解释。
