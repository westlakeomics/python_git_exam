# GitHub Actions 自动 PR 权限设置指南

## 问题描述

当推送新分支时，自动 PR 工作流失败，错误信息：
```
pull request create failed: GraphQL: GitHub Actions is not permitted to create or approve pull requests (createPullRequest)
Error: Process completed with exit code 1.
```

这是因为 GitHub 默认出于安全考虑，禁止 GitHub Actions 创建或批准 Pull Request。

## 解决方案

### 方案一：启用 GitHub Actions 创建 PR 的权限（推荐）

这是最简单且最自动化的解决方案。需要仓库管理员权限。

#### 步骤：

1. **进入仓库设置**
   - 导航到仓库主页
   - 点击 **Settings**（设置）

2. **配置 Actions 权限**
   - 在左侧菜单中选择 **Actions** → **General**
   - 滚动到页面底部找到 **Workflow permissions** 部分

3. **启用 PR 创建权限**
   - 找到选项：**"Allow GitHub Actions to create and approve pull requests"**
   - ✅ **勾选此选项**
   - 点击 **Save**（保存）

#### 截图位置说明：
```
Settings → Actions → General → Workflow permissions
   ↓
[✓] Allow GitHub Actions to create and approve pull requests
```

#### 注意事项：
- 如果此选项为灰色（不可选），可能是因为：
  - 组织级别的设置未启用
  - 需要先到 **Organization Settings** → **Actions** → **General** 启用相同选项
- 对于个人账户的公开仓库，此选项可以直接在仓库中设置
- 设置更改可能需要几分钟生效

### 方案二：使用 Personal Access Token（备选方案）

如果无法启用方案一，可以使用个人访问令牌。

#### 步骤：

1. **创建 Personal Access Token (PAT)**
   - 访问 GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
   - 点击 **Generate new token**
   - 设置名称：`Auto PR Workflow`
   - 选择 Repository access：仅此仓库
   - 权限设置：
     - **Contents**: Read and write
     - **Pull requests**: Read and write
   - 生成并复制 token（注意：只显示一次）

2. **添加 Secret 到仓库**
   - 进入仓库 Settings → Secrets and variables → Actions
   - 点击 **New repository secret**
   - Name: `PAT_TOKEN`
   - Value: 粘贴刚才创建的 token
   - 点击 **Add secret**

3. **修改工作流文件**
   编辑 `.github/workflows/auto-pr.yml`，将：
   ```yaml
   env:
     GH_TOKEN: ${{ github.token }}
   ```
   改为：
   ```yaml
   env:
     GH_TOKEN: ${{ secrets.PAT_TOKEN }}
   ```

#### 注意事项：
- PAT 有过期时间，需要定期更新
- 使用 PAT 创建的 PR 将显示为个人创建，而非 bot
- 建议使用方案一（更简单且更安全）

## 验证设置

设置完成后，测试工作流：

1. **创建测试分支并修改文件**
   ```bash
   git checkout -b test/auto-pr-$(date +%s)
   echo "# test" >> src/bad_style.py
   git add src/bad_style.py
   git commit -m "test: verify auto PR creation"
   git push origin test/auto-pr-$(date +%s)
   ```

2. **检查 Actions 标签页**
   - 应该能看到 "Auto Create PR" 工作流运行
   - 状态应该为 ✅ Success（成功）

3. **检查 Pull Requests 标签页**
   - 应该能看到自动创建的 PR
   - 标题格式：`Fix: PEP 8 compliance for bad_style.py - [分支名]`

4. **清理测试**
   ```bash
   # 删除测试分支（如果 PR 被合并会自动删除）
   git push origin --delete test/auto-pr-*
   ```

## 工作流程说明

启用权限后，完整的自动化流程如下：

```
1. 用户创建分支并修改 src/bad_style.py
         ↓
2. 推送到远程分支
         ↓
3. [自动] Auto Create PR 工作流触发
         ↓
4. [自动] 创建 Pull Request
         ↓
5. [自动] PR Validation 工作流运行
         ↓  (ruff/black/isort/pytest)
         ↓
6. [手动] 用户或管理员合并 PR
         ↓
7. [自动] Post Merge Actions 工作流触发
         ↓
8. [自动] 记录分支名到 passed_branches/merged_branches.txt
         ↓
9. [自动] 删除已合并的分支
```

## 安全考虑

### 为什么 GitHub 默认禁止这个权限？

这是一个安全特性，防止：
- 恶意工作流自动批准有安全风险的代码
- 工作流权限提升攻击
- 未经审查的代码自动合并

### 启用此权限是否安全？

是的，在以下情况下是安全的：
1. ✅ 仓库有适当的分支保护规则（见 [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)）
2. ✅ 工作流文件受到保护（main 分支保护）
3. ✅ PR 仍需通过 CI 检查才能合并
4. ✅ PR 创建后仍需人工审查和批准

我们的设置包含：
- 工作流只创建 PR，不自动批准或合并
- 所有 PR 必须通过 CI 验证
- main 分支有保护规则，防止未授权合并

## 故障排除

### 问题：设置选项为灰色

**原因**：组织级别未启用

**解决**：
1. 如果在组织仓库中，需要组织管理员：
   - 访问 `https://github.com/organizations/[ORG-NAME]/settings/actions`
   - 启用 "Allow GitHub Actions to create and approve pull requests"
2. 然后返回仓库设置，选项应该可用

### 问题：工作流仍然失败

**检查清单**：
1. ✅ 确认已保存设置并等待几分钟
2. ✅ 工作流文件中包含正确的权限：
   ```yaml
   permissions:
     contents: write
     pull-requests: write
   ```
3. ✅ 推送的分支不是 `main`
4. ✅ 修改的文件是 `src/bad_style.py`
5. ✅ 查看 Actions 日志获取详细错误信息

### 问题：PR 被创建但 CI 检查未运行

**原因**：PR Validation 工作流触发条件不匹配

**检查**：
- 确认修改了 `src/` 或 `tests/` 目录下的 `.py` 文件
- 查看 `.github/workflows/pr-validation.yml` 的触发条件

## 相关文档

- [自动化工作流程详细说明](WORKFLOW.md)
- [分支保护配置](BRANCH_PROTECTION.md)
- [GitHub 官方文档：管理 Actions 权限](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)

## 联系支持

如果按照以上步骤仍无法解决问题：
1. 查看 [GitHub Actions 日志](../../actions) 获取详细错误信息
2. 创建 Issue 并附上：
   - 错误截图
   - 工作流日志
   - 已尝试的解决步骤

## 总结

- ✅ **推荐方案**：启用 "Allow GitHub Actions to create and approve pull requests"
- ⚠️ **备选方案**：使用 Personal Access Token（需要定期维护）
- 🔒 **安全性**：配合分支保护规则，此设置是安全的
- 🎯 **目标**：实现完全自动化的 PR 创建和验证流程
