# Branch Protection Configuration

This document describes how to configure branch protection rules for the `main` branch to prevent force pushes and unauthorized merges.

## Required Settings

To ensure the main branch is properly protected, configure the following settings in GitHub:

### Via GitHub UI

1. Navigate to: **Settings** → **Branches** → **Branch protection rules**
2. Click **Add branch protection rule**
3. Set **Branch name pattern**: `main`
4. Enable the following settings:

#### Essential Protection Rules:
- ✅ **Require a pull request before merging**
  - ✅ Require approvals: 1 (or more based on team size)
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  
- ✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - Add required status checks:
    - `validate` (from PR Validation workflow)
  
- ✅ **Require conversation resolution before merging**

- ✅ **Do not allow bypassing the above settings**

- ✅ **Restrict who can push to matching branches** (optional but recommended)
  - Only allow administrators or specific teams

#### Critical Settings to Prevent Force Merges:
- ✅ **Block force pushes** - This prevents force pushes to main
- ✅ **Require linear history** (optional) - Prevents merge commits, requires rebase or squash

### Via GitHub CLI (gh)

```bash
# Basic protection
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["validate"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

## Verification

After setting up branch protection, verify it works:

1. Try to push directly to main:
   ```bash
   git checkout main
   git commit --allow-empty -m "test"
   git push origin main
   ```
   **Expected**: Push should be rejected

2. Try to force push to main:
   ```bash
   git push --force origin main
   ```
   **Expected**: Force push should be blocked

3. Try to merge a PR without status checks passing:
   **Expected**: Merge button should be disabled until checks pass

## Workflow Integration

With branch protection enabled:

1. User modifies `src/bad_style.py` on a feature branch
2. User pushes the branch → Auto-PR workflow creates a PR
3. PR Validation workflow runs (ruff, black, isort, pytest)
4. If all checks pass, the PR can be merged
5. On merge, Post Merge Actions workflow:
   - Records the branch name to `passed_branches/merged_branches.txt`
   - Deletes the merged branch

## Security Notes

- Branch protection prevents:
  - Direct pushes to main
  - Force pushes to main
  - Merging without required status checks
  - Bypassing review requirements

- The post-merge workflow includes:
  - Branch name validation to prevent injection attacks
  - Safe file operations with temporary files
  - Proper error handling

## Troubleshooting

### "Branch protection rule prevents push"
This is expected behavior. All changes must go through PRs.

### "Required status check 'validate' is expected"
The PR Validation workflow must complete successfully before merging.

### Workflow not triggering
- Check that the branch name doesn't match the ignore pattern
- Verify that `src/bad_style.py` was actually modified
- Check workflow run logs in Actions tab

## References

- [GitHub Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions Permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
