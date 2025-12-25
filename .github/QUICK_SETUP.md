# ⚡ 快速设置检查清单

仓库管理员在首次使用前必须完成以下配置，用时约 **5 分钟**。

## 📋 设置检查清单

### ✅ 步骤 1：启用 GitHub Actions PR 创建权限（必需）

**为什么需要**：允许工作流自动创建 Pull Request

**操作步骤**：
1. [ ] 进入仓库主页
2. [ ] 点击 **Settings**（设置）标签
3. [ ] 左侧菜单选择 **Actions** → **General**
4. [ ] 滚动到页面底部的 **Workflow permissions** 部分
5. [ ] 找到并勾选 ✅ **"Allow GitHub Actions to create and approve pull requests"**
6. [ ] 点击 **Save** 按钮

**验证**：设置后该选项应保持勾选状态

📖 详细说明：[SETUP_GUIDE.md](SETUP_GUIDE.md)

---

### ✅ 步骤 2：配置分支保护规则（推荐）

**为什么需要**：保护 main 分支，防止未经审查的代码直接提交

**操作步骤**：
1. [ ] 进入仓库 **Settings** → **Branches**
2. [ ] 点击 **Add branch protection rule**
3. [ ] 输入分支名称模式：`main`
4. [ ] 勾选以下选项：
   - [ ] ✅ **Require a pull request before merging**
   - [ ] ✅ **Require status checks to pass before merging**
     - [ ] 添加 `validate` 到必需检查列表
   - [ ] ✅ **Block force pushes**
   - [ ] ✅ **Require conversation resolution before merging**
5. [ ] 点击 **Create** 或 **Save changes**

**验证**：尝试直接推送到 main 分支应被拒绝

📖 详细说明：[BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)

---

### ✅ 步骤 3：测试自动化工作流（推荐）

**验证所有配置正常工作**

**操作步骤**：
```bash
# 1. 克隆仓库（如果还未克隆）
git clone https://github.com/westlakeomics/Python_Git_exam.git
cd Python_Git_exam

# 2. 创建测试分支
git checkout -b test/setup-verification

# 3. 修改测试文件
echo "# setup test $(date +%s)" >> src/bad_style.py

# 4. 提交并推送
git add src/bad_style.py
git commit -m "test: verify auto PR creation"
git push origin test/setup-verification
```

**验证清单**：
- [ ] Actions 标签页显示 "Auto Create PR" 工作流运行
- [ ] 工作流状态为 ✅ Success（绿色对勾）
- [ ] Pull Requests 标签页出现自动创建的 PR
- [ ] PR 标题为：`Fix: PEP 8 compliance for bad_style.py - test/setup-verification`
- [ ] PR Validation 工作流自动运行

**清理测试**：
```bash
# 关闭或删除测试 PR
gh pr close test/setup-verification --delete-branch
# 或者通过 GitHub UI 手动关闭
```

---

## ❌ 常见问题

### Q1: "Allow GitHub Actions to create and approve pull requests" 选项是灰色的

**原因**：组织级别的设置未启用

**解决**：
- 如果这是组织仓库，需要组织管理员在组织设置中启用此选项
- 访问：`https://github.com/organizations/[ORG-NAME]/settings/actions`
- 启用后返回仓库设置，选项将变为可用

### Q2: 工作流失败，显示权限错误

**错误信息**：
```
GitHub Actions is not permitted to create or approve pull requests
```

**解决**：
1. 确认已完成步骤 1 的设置
2. 等待 2-5 分钟让设置生效
3. 重新触发工作流（推送新的提交或重新运行工作流）

### Q3: PR 被创建但没有自动运行验证

**原因**：PR Validation 工作流的触发条件不匹配

**检查**：
- 确认修改的是 `src/` 或 `tests/` 目录下的 `.py` 文件
- 检查工作流日志查看详细信息

---

## 📚 完整文档

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 详细的权限设置指南
- [WORKFLOW.md](WORKFLOW.md) - 完整的工作流说明
- [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) - 分支保护配置详情

---

## ✨ 设置完成后

恭喜！🎉 您的仓库现在已配置好自动化 PR 工作流。

**用户工作流程**：
1. 用户创建新分支并修改 `src/bad_style.py`
2. 推送到远程仓库
3. 🤖 GitHub Actions 自动创建 PR
4. 🤖 自动运行代码质量检查
5. 👥 管理员审查并合并 PR
6. 🤖 自动记录分支名并清理

**需要帮助？**
- 查看 [SETUP_GUIDE.md](SETUP_GUIDE.md) 的故障排除部分
- 检查 [Actions 运行日志](../../actions)
- 创建 Issue 报告问题
