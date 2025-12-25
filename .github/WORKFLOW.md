# 自动化 PR 工作流程说明

本项目实现了完全自动化的 PR 管理流程，满足以下需求：

## 功能概述

当用户修改 `src/bad_style.py` 并推送到新分支后：

1. ✅ **自动创建 PR** - 无需手动操作
2. ✅ **自动检测代码质量** - 运行 ruff、black、isort、pytest
3. ✅ **自动记录通过的分支** - 写入 `passed_branches/merged_branches.txt`
4. ✅ **自动删除合并后的分支** - 保持仓库整洁
5. ✅ **保护 main 分支** - 防止强制推送和未授权的合并

## 工作流程详解

### 第一步：用户推送修改

```bash
# 用户创建新分支并修改代码
git checkout -b fix/username
# 修改 src/bad_style.py
git add src/bad_style.py
git commit -m "fix: apply PEP 8 standards"
git push origin fix/username
```

### 第二步：自动创建 PR

**触发器**: `.github/workflows/auto-pr.yml`

- **触发条件**: 向非 main 分支推送时修改了 `src/bad_style.py`
- **功能**:
  - 检查是否已存在 PR（避免重复）
  - 自动创建 PR，标题包含分支名
  - PR 描述包含验证步骤说明

### 第三步：自动代码验证

**触发器**: `.github/workflows/pr-validation.yml`

- **触发条件**: PR 打开或更新
- **检查项目**:
  1. `ruff check .` - 代码质量检查
  2. `black --check .` - 代码格式化检查
  3. `isort --check-only .` - 导入排序检查
  4. `pytest -v tests/` - 单元测试

**结果**: 所有检查通过后，PR 可以合并

### 第四步：合并后自动处理

**触发器**: `.github/workflows/post-merge.yml`

- **触发条件**: PR 成功合并到 main
- **执行操作**:
  1. **验证分支名** - 防止注入攻击
  2. **记录分支** - 添加到 `passed_branches/merged_branches.txt`
     - 格式: `YYYY-MM-DD HH:MM:SS UTC - branch-name`
     - 按时间戳排序
     - 保留所有历史记录
  3. **提交更改** - 自动提交记录文件到 main
  4. **删除分支** - 删除远程分支

## 分支保护配置

为了确保 main 分支的安全，需要配置分支保护规则。详细说明请参考：

📖 **[.github/BRANCH_PROTECTION.md](.github/BRANCH_PROTECTION.md)**

### 关键保护措施

1. **禁止直接推送到 main** - 所有更改必须通过 PR
2. **禁止强制推送** - 防止历史记录被覆盖
3. **要求状态检查通过** - 必须通过 CI 验证
4. **要求审批** - 可选，根据团队规模配置

### 快速设置（通过 GitHub UI）

1. 进入仓库 **Settings** → **Branches**
2. 添加规则，分支名称模式: `main`
3. 启用以下选项：
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
     - 添加 `validate` 作为必需检查
   - ✅ Block force pushes
   - ✅ Require conversation resolution before merging

## 安全特性

### 输入验证

- **分支名验证**: 防止路径遍历 (`..`, `//`) 和注入攻击
- **字符限制**: 仅允许字母、数字、`-`、`_`、`/`

### 安全操作

- **临时文件**: 使用临时文件进行排序，防止数据丢失
- **错误处理**: 所有操作都有适当的错误处理
- **最小权限**: 每个工作流只请求必需的权限

## 文件结构

```
.github/
├── workflows/
│   ├── auto-pr.yml         # 自动创建 PR
│   ├── pr-validation.yml   # PR 代码验证
│   └── post-merge.yml      # 合并后处理
├── BRANCH_PROTECTION.md    # 分支保护配置指南
└── WORKFLOW.md            # 本文件

passed_branches/
├── merged_branches.txt     # 记录通过的分支
└── README.md              # 说明文档
```

## 测试工作流

### 测试自动 PR 创建

```bash
git checkout -b test/auto-pr-test
echo "# test" >> src/bad_style.py
git add src/bad_style.py
git commit -m "test: trigger auto PR"
git push origin test/auto-pr-test
```

预期结果: 自动创建 PR

### 测试 PR 验证

- 推送符合 PEP 8 的代码 → 验证通过 ✅
- 推送不符合规范的代码 → 验证失败 ❌

### 测试合并后处理

1. 合并一个通过验证的 PR
2. 检查 `passed_branches/merged_branches.txt` - 应该包含新条目
3. 检查远程分支 - 应该已被删除

## 故障排除

### PR 未自动创建

- 确认修改了 `src/bad_style.py`
- 确认不是推送到 main 分支
- 检查 Actions 标签页的工作流运行日志

### 验证失败

- 运行本地检查: `ruff check .`、`black --check .`、`isort --check-only .`、`pytest tests/`
- 修复问题后重新推送

### 分支未删除

- 检查工作流日志
- 可能的原因: 权限不足、网络问题
- 可以手动删除: `git push origin --delete branch-name`

## 维护建议

1. **定期审查** `passed_branches/merged_branches.txt` 的内容
2. **监控工作流** 失败情况，及时调整
3. **更新依赖** 定期更新 GitHub Actions 版本
4. **审查日志** 检查异常的分支名或模式

## 相关文档

- [README.md](../README.md) - 项目主文档
- [BRANCH_PROTECTION.md](.github/BRANCH_PROTECTION.md) - 分支保护详细配置
- [passed_branches/README.md](passed_branches/README.md) - 分支记录说明

## 技术栈

- **GitHub Actions** - CI/CD 自动化
- **GitHub CLI (gh)** - PR 管理
- **Python 3.11** - 代码运行环境
- **ruff / black / isort** - 代码质量工具
- **pytest** - 测试框架

## 总结

此自动化系统确保：

✅ 所有代码更改都经过审查和测试  
✅ main 分支保持干净和受保护  
✅ 分支生命周期完全自动化管理  
✅ 完整的合并历史记录  
✅ 符合安全最佳实践  

如有问题或建议，请创建 issue 讨论。
