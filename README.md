# DataCheck · CSV 数据体检

拿到一份 CSV 后，先检查缺失值、重复记录和格式错误，再开始分析。

这是 `daydayup` 的主项目，面向 Python 后端／数据方向的学习与作品积累。当前实现是 **Python 标准库命令行工具**；HTTP API 和报告数据库属于后续计划。

## 30 秒运行

需要 Python 3.11 或以上，无第三方依赖。请在仓库根目录运行：

```bash
python -m datacheck examples/orders.csv
python -m unittest discover -s tests -v
```

Windows 本地目录：`D:\githubupload\daydayup`。

示例 CSV 是虚构数据，共 5 条记录、4 列。报告应包含：

```json
{
  "schema_version": 1,
  "row_count": 5,
  "column_count": 4,
  "missing_cell_count": 3,
  "duplicate_row_count": 1,
  "duplicate_record_examples": [5]
}
```

这是输出节选；完整 JSON 还包含 `columns`，列出每列的缺失数和缺失比例。

保存完整报告到一个**尚不存在**的文件：

```bash
python -m datacheck examples/orders.csv --output report.json
```

输出文件已存在时会报错；请换一个文件名。输入文件不会被覆盖。生成的 `report.json` 已加入忽略规则。

## 统计口径与边界

| 项目 | 当前行为 |
| --- | --- |
| 输入格式 | UTF-8（兼容 BOM）、逗号分隔、第一条记录为表头 |
| 表头 | 去除首尾空白；空名称、重名均报错 |
| 缺失值 | 去除首尾空白后是空字符串；`0`、`NULL`、`NaN` 都保留为普通文本 |
| 重复记录 | 整行所有字段去除首尾空白后相同；每组首次出现不计入重复数 |
| 缺失比例 | 该列缺失数 / 数据行数，保留 4 位小数；零数据行时为 0.0 |
| 空白行 | 表头后的空白物理行跳过；`,,,` 是实际记录，正常统计 |
| 引号与换行 | 交给 Python CSV 解析器处理，支持引号内逗号和换行 |
| 记录编号 | 表头为 1，忽略空白行；多行字段仍算一条记录，因此不是编辑器行号 |
| 错误 | 列数不一致、CSV 引号解析失败、编码错误、文件错误：stderr 提示并退出 2 |
| 发现数据问题 | 缺失值或重复记录仍正常生成报告并退出 0；质量门禁尚未实现 |
| 成功 | stdout 输出 JSON，或写入指定新文件；退出 0 |

仅有表头是合法输入，空文件不是。不要把 CSV 解析通过等同于业务数据正确：本版不推断类型、不校验金额范围、不自动清洗，也不支持 Excel、GBK 或任意分隔符。报告不包含原始单元格值，但会包含列名。

精确查重使用 `set` 保存不同记录，内存随不同记录的数量与内容长度增加。当前适合本地小文件，尚未进行性能基准测试，也没有生产级文件大小／资源限制。

## 项目导航

| 路径 | 内容 |
| --- | --- |
| [datacheck/analyzer.py](datacheck/analyzer.py) | CSV 解析、统计及输入规则 |
| [datacheck/__main__.py](datacheck/__main__.py) | 命令行、文件读写和错误出口 |
| [tests](tests) | 统计边界与真实命令行进程测试 |
| [8 周路线图](docs/ROADMAP.md) | 阶段目标和第一周安排 |
| [当前任务与独立提示词](docs/DAY_02.md) | 第 2 天：首版验收、演示与代码阅读 |
| [三种场景演示包](examples/review/README.md) | 正常数据、仅表头、错误列数的命令和预期 |
| [首日任务](docs/DAY_01.md) | CLI 最小版本与首日独立提示词 |
| [项目进度摘要](docs/PROGRESS.md) | 已验证事实、阻碍、下一步 |
| [每日流程与交作业模板](docs/WORKFLOW.md) | 验收、复盘和提交规则 |
| [开发记录](docs/daily) | 每日真实进展、证据与限制 |
| [账号展示草案](docs/PROFILE_DRAFT.md) | 可复用的真实个人简介 |

## 工程验证

GitHub Actions 配置在 Windows / Ubuntu、Python 3.11 / 3.12 上运行同一套测试。工作流配置不代表远端检查已通过；实际状态请查看 [Actions](https://github.com/Edgar-30/daydayup/actions)。本地验证记录见进度摘要。

工作流用法参考 [actions/checkout](https://github.com/actions/checkout) 和 [actions/setup-python](https://github.com/actions/setup-python) 官方说明。

## 开发方式

代码由 Codex 辅助实现和调试，仓库所有者逐步阅读、亲自验证和练习。开发完成与个人掌握分别记录；尚未验收的能力不写成已经独立掌握。每次提交对应实际功能、修复、测试或可复用文档改进。
