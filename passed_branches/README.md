# passed_branches

该目录用于记录 **CI 通过且 PR 已合并** 的分支。

## 自动化流程

当用户修改 `src/bad_style.py` 并推送到新分支时：

1. **自动创建 PR** - `.github/workflows/auto-pr.yml` 自动创建 Pull Request
2. **CI 验证** - `.github/workflows/pr-validation.yml` 运行代码检查和测试
   - ruff (代码质量检查)
   - black (格式化检查)
   - isort (导入排序检查)
   - pytest (单元测试)
3. **合并后处理** - `.github/workflows/post-merge.yml` 在 PR 合并后：
   - 将分支名称和时间戳记录到 `merged_branches.txt`
   - 自动删除已合并的分支

## 文件说明

- **记录文件**: `merged_branches.txt`
- **格式**: `YYYY-MM-DD HH:MM:SS UTC - branch-name`
- **写入来源**: [.github/workflows/post-merge.yml](../.github/workflows/post-merge.yml)

## 分支保护

main 分支受到保护，不能被直接推送或强制合并。所有更改必须通过 PR 流程。

详见: [.github/BRANCH_PROTECTION.md](../.github/BRANCH_PROTECTION.md)
