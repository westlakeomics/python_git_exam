# Python PEP 8 + GitHub 流程考核（操作题）

本仓库用于“编程操作题”考试：考察候选人对 **Python 基本代码规范（PEP 8 思想）** 与 **GitHub 基础协作流程（分支 / 提交 / PR）** 的掌握。


## 🚀 自动化工作流

**本项目已配置完全自动化的 PR 流程！**

当你推送修改 `src/bad_style.py` 的新分支后，系统会自动：
1. ✅ 创建 Pull Request
2. ✅ 运行代码质量检查（ruff、black、isort、pytest）
3. ✅ 合并后记录分支名到 `passed_branches/merged_branches.txt`
4. ✅ 自动删除已合并的分支

详细说明请查看: [**自动化工作流程文档**](.github/WORKFLOW.md)

## 一、考试目标
你需要在 **不改变既有功能/输出** 的前提下，修复仓库中的代码规范问题，使其通过 CI 的自动检查。

CI 会检查：
- Python 代码质量（ruff）
- 格式化（black --check）
- 导入排序（isort --check-only）
- 单元测试（pytest）
- 基础提交信息规范（可选：本仓库版本不在 CI 中强制检查提交信息，但会在人工复核中查看）

## 二、任务要求（必须全部完成）
1. **创建新分支**：从 `main` 创建分支，命名建议(请将user替换为实际的用户名)：`fix/user` 或 `task/user-fix`。
2. **修复代码规范问题**：
   - 修复 `src/bad_style.py` 里的 PEP 8/可读性问题（命名、导入、空格、长行、文档字符串、异常、重复代码等）
   - 允许你拆分函数、增加辅助函数、增加类型注解、增加合理注释/Docstring
   - **不得修改程序对外行为**：单元测试应全部通过
3. **提交并推送**：
   - 进行至少 1 次 commit（建议 1~3 次，小步提交）
   - 提交信息建议格式：`fix: make code pep8 compliant`（也可使用你们团队规范）
4. **发起 Pull Request**：
   - PR 标题清晰说明做了什么
   - PR 描述中写明：你修复了哪些类型的问题（例如：imports/formatting/naming/docstring）

## 三、通过标准
- GitHub Actions 绿灯（全部 job 通过）
- PR 内容清晰、可读
- 不引入功能回归（pytest 通过）

## 四、本地运行建议
1、创建环境（建议使用 Python 3.11）

```bash
conda create --name myenv python=3.11 -y
conda activate myenv

2、从 main 拉出分支：

git checkout -b fix/user # ****请将user替换为实际的用户名****
修改 src/bad_style.py，修复规范问题但不改行为


pip install -r requirements.txt

3、运行测试
python -m pytest -q tests/

# 运行静态检查（与 CI 一致）
ruff check .
black --check .
isort --check-only .

4、推送并创建 PR：
git add .
git commit -m "fix: pep8 refactor"
git push -u origin fix/user #（****请将user替换为实际的用户名****）
PR 页面等待 GitHub Actions 执行，看到 grading-ci / grade (lint + format + tests) 为绿色即通过。

## 五、评分方式
- 60%：CI 是否通过（ruff/black/isort/pytest）
- 20%：代码可读性（命名、函数长度、注释与 docstring 是否合理）
- 20%：GitHub 流程规范（分支、提交粒度、PR 描述）
