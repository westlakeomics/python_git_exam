# Python PEP 8 + GitHub 流程考核（操作题）

本仓库用于“编程操作题”考试：考察候选人对 **Python 基本代码规范（PEP 8 思想）** 与 **GitHub 基础协作流程（分支 / 提交 / PR）** 的掌握。


## 📚 重要文档

在开始之前，**请先阅读以下文档**以避免常见错误：

- 🆘 **[FAQ.md](FAQ.md)** - Git 推送权限问题常见问答（必读！）
- 📘 **[CONTRIBUTING.md](CONTRIBUTING.md)** - 完整贡献指南和 Fork 工作流
- 🎨 **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)** - 图解 Git 权限问题和工作流
- ⚙️ **[.github/WORKFLOW.md](.github/WORKFLOW.md)** - 自动化工作流程文档

**⚠️ 如果你遇到 403 权限错误，请查看 [FAQ.md](FAQ.md) 的解决方案！**

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

## 六、常见问题与故障排除

### ⚠️ 推送时遇到权限错误 403

**错误信息示例：**
```
remote: Permission to westlakeomics/Python_Git_exam.git denied to <username>.
fatal: unable to access 'https://github.com/westlakeomics/Python_Git_exam.git/': The requested URL returned error: 403
```

**原因分析：**

这是 GitHub 的正常安全机制。**Public（公开）仓库 ≠ 任何人都可以推送**

- ✅ **Public 仓库**：任何人都可以**查看**和**克隆**代码
- ❌ **写入权限**：只有仓库的**协作者（Collaborators）** 或**所有者（Owner）** 才能直接推送代码

**解决方案有两种：**

#### 方案 1：Fork 工作流（推荐给外部贡献者）

如果你不是仓库的协作者，需要使用 Fork 工作流：

1. **Fork 这个仓库**
   - 点击 GitHub 页面右上角的 "Fork" 按钮
   - 这会在你的账户下创建一个副本

2. **克隆你 Fork 的仓库**
   ```bash
   # 克隆你自己的 Fork（注意 URL 中的用户名是你的）
   git clone https://github.com/你的用户名/Python_Git_exam.git
   cd Python_Git_exam
   ```

3. **按正常流程工作**
   ```bash
   # 创建分支
   git checkout -b fix/你的用户名
   
   # 修改 src/bad_style.py
   # ...
   
   # 提交并推送到你自己的 Fork
   git add .
   git commit -m "fix: pep8 refactor"
   git push -u origin fix/你的用户名
   ```

4. **创建 Pull Request**
   - 推送后，GitHub 会提示你创建 PR
   - 或者访问原仓库页面，点击 "New pull request"
   - 选择 `base: westlakeomics/Python_Git_exam:main` ← `compare: 你的用户名/Python_Git_exam:fix/你的用户名`

5. **后续更新**
   - 如果需要同步原仓库的最新更改：
   ```bash
   # 添加原仓库为上游
   git remote add upstream https://github.com/westlakeomics/Python_Git_exam.git
   
   # 同步上游更新
   git fetch upstream
   git checkout main
   git merge upstream/main
   git push origin main
   ```

#### 方案 2：请求协作者权限（推荐给团队成员）

如果你是考核候选人或团队成员：

1. **联系仓库管理员**
   - 请求将你添加为 Collaborator
   - 管理员需要在：`Settings` → `Collaborators and teams` → `Add people`

2. **接受邀请**
   - 你会收到一封邮件邀请
   - 点击邮件中的链接接受邀请
   - 或访问：`https://github.com/westlakeomics/Python_Git_exam/invitations`

3. **克隆并正常工作**
   ```bash
   # 现在可以直接克隆原仓库
   git clone https://github.com/westlakeomics/Python_Git_exam.git
   cd Python_Git_exam
   
   # 按照上面 "四、本地运行建议" 的步骤操作
   git checkout -b fix/你的用户名
   # ...修改代码
   git push -u origin fix/你的用户名
   ```

### 其他常见问题

**Q: 我已经克隆了原仓库，但推送时还是报错 403，怎么办？**

A: 如果你不是协作者，需要：
1. Fork 原仓库到你的账户
2. 修改你本地仓库的远程地址：
   ```bash
   # 查看当前远程地址
   git remote -v
   
   # 修改为你的 Fork
   git remote set-url origin https://github.com/你的用户名/Python_Git_exam.git
   
   # 验证修改
   git remote -v
   
   # 现在可以推送了
   git push -u origin fix/你的用户名
   ```

**Q: Fork 后如何确保我的 PR 能被自动化工作流处理？**

A: 自动化工作流会在**目标仓库**（`westlakeomics/Python_Git_exam`）中运行，所以：
- ✅ 你的 Fork 中推送分支
- ✅ 创建 PR 到原仓库
- ✅ PR 创建后，原仓库的 GitHub Actions 会自动运行验证
- ✅ 合并后，分支会被记录到原仓库的 `passed_branches/merged_branches.txt`

**Q: 使用 HTTPS 还是 SSH？**

A: 两种方式都可以：
- **HTTPS**（推荐新手）: `https://github.com/用户名/仓库名.git`
  - 首次推送时需要输入 GitHub 用户名和密码（或 Personal Access Token）
- **SSH**: `git@github.com:用户名/仓库名.git`
  - 需要先配置 SSH 密钥：[GitHub SSH 设置指南](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)

更多详细说明，请参考 [CONTRIBUTING.md](CONTRIBUTING.md)
