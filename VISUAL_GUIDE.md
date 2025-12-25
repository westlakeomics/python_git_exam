# Git 推送权限问题图解 / Git Push Permission Visual Guide

## 问题场景

```
开发者 (zhiyuajun)
    |
    | git push -u origin fix/test
    ↓
❌ 403 Forbidden Error
    |
westlakeomics/Python_Git_exam (Public 仓库)
```

**错误消息：**
```
remote: Permission to westlakeomics/Python_Git_exam.git denied to zhiyuajun.
fatal: unable to access 'https://github.com/westlakeomics/Python_Git_exam.git/': The requested URL returned error: 403
```

---

## 核心概念图解

### Public 仓库权限模型

```
┌─────────────────────────────────────────────────────────┐
│           westlakeomics/Python_Git_exam                  │
│                  (Public 仓库)                           │
└─────────────────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
    [所有人]                    [协作者 Only]
        │                           │
        ↓                           ↓
   ┌─────────┐                 ┌─────────┐
   │ 可以做: │                 │ 可以做: │
   ├─────────┤                 ├─────────┤
   │ ✅ 查看  │                 │ ✅ 查看  │
   │ ✅ 克隆  │                 │ ✅ 克隆  │
   │ ✅ Fork │                 │ ✅ Fork │
   │ ✅ Issue│                 │ ✅ Issue│
   │ ❌ Push │                 │ ✅ Push │
   │ ❌ Merge│                 │ ✅ Merge│
   └─────────┘                 └─────────┘
```

**关键点：**
- Public（公开）只是**可见性**设置
- Write（写入）权限需要**明确授予**
- 这是 GitHub 的安全设计

---

## 解决方案 1: Fork 工作流（推荐）

### 流程图

```
1. Fork 仓库
   ┌──────────────────────────────┐
   │ westlakeomics/Python_Git_exam│  (原仓库)
   └──────────────────────────────┘
                  │
                  │ Fork (在 GitHub 网页点击)
                  ↓
   ┌──────────────────────────────┐
   │   你的用户名/Python_Git_exam  │  (你的副本)
   └──────────────────────────────┘

2. 克隆你的 Fork
   $ git clone https://github.com/你的用户名/Python_Git_exam.git
   
3. 添加上游
   $ git remote add upstream https://github.com/westlakeomics/Python_Git_exam.git
   
   本地配置：
   ┌─────────────────┐
   │  本地仓库        │
   └─────────────────┘
         │        │
         │        └─────→ upstream (原仓库) ← 只读，用于同步
         │
         └──────────────→ origin (你的 Fork) ← 可写，用于推送

4. 创建分支并工作
   main
    │
    └─→ fix/你的用户名  ← 在这里工作

5. 推送到你的 Fork
   本地分支
      │
      │ git push -u origin fix/你的用户名
      ↓
   你的 Fork (你的用户名/Python_Git_exam)
      │
      │ ✅ 成功！不会报 403 错误
      │

6. 创建 Pull Request
   你的 Fork                           原仓库
   (你的用户名/Python_Git_exam)    →   (westlakeomics/Python_Git_exam)
    fix/你的用户名                      main
         │
         └───────── Pull Request ─────→
         
7. 等待审查和合并
   Pull Request
         │
         ├─→ CI 自动运行 ✅
         │
         ├─→ 代码审查
         │
         └─→ 合并到 main
```

### 时序图

```
你               你的Fork          原仓库         GitHub Actions
│                │                │                │
│──Fork────────→ │                │                │
│                │                │                │
│──clone────────→│                │                │
│                │                │                │
│──commit───→    │                │                │
│                │                │                │
│──push─────→    │                │                │
│                │                │                │
│──Create PR────────────────────→ │                │
│                │                │                │
│                │                │───trigger─────→│
│                │                │                │
│                │                │←─CI result────┤
│                │                │                │
│                │                │                │
│←─PR merged────────────────────┤                │
│                │                │                │
```

---

## 解决方案 2: 协作者直接推送

### 流程图

```
1. 请求权限
   开发者
     │
     │ 请求协作者权限
     ↓
   管理员
     │
     │ Settings → Collaborators → Add people
     ↓
   发送邀请

2. 接受邀请
   开发者
     │
     │ 收到邮件/通知
     │
     │ 点击接受
     ↓
   成为协作者 ✅

3. 克隆原仓库
   $ git clone https://github.com/westlakeomics/Python_Git_exam.git
   
   本地配置：
   ┌─────────────────┐
   │  本地仓库        │
   └─────────────────┘
         │
         └──────────────→ origin (原仓库) ← 可写！

4. 创建分支并推送
   main
    │
    └─→ fix/你的用户名
         │
         │ git push -u origin fix/你的用户名
         ↓
   westlakeomics/Python_Git_exam
         │
         │ ✅ 成功！
         │
         └─→ 自动创建 PR (配置了 auto-pr.yml)
```

---

## 决策树：我应该用哪种方式？

```
                     开始
                      │
                      ↓
          ┌─────────────────────┐
          │ 你是否有协作者权限？   │
          └─────────────────────┘
                 │        │
            是   │        │ 否
                 ↓        ↓
           ┌─────────┐  ┌──────────────┐
           │ 方案 2   │  │ 能否联系管理员？│
           │ 直接推送 │  └──────────────┘
           └─────────┘      │        │
                       能   │        │ 不能
                            ↓        ↓
                      ┌─────────┐ ┌─────────┐
                      │ 请求权限 │ │ 方案 1   │
                      │ 后用方案2│ │Fork 工作流│
                      └─────────┘ └─────────┘
                                       │
                                       ↓
                                  推荐给所有
                                  外部贡献者
```

---

## 常见错误对比

### ❌ 错误做法

```
1. 直接克隆原仓库，尝试推送（无协作者权限）
   
   $ git clone https://github.com/westlakeomics/Python_Git_exam.git
   $ git checkout -b fix/test
   $ git push -u origin fix/test
   
   ❌ Error: Permission denied (403)
```

### ✅ 正确做法 (Fork)

```
1. Fork → 克隆你的 Fork → 推送 → 创建 PR
   
   [GitHub 网页] Fork 仓库
   
   $ git clone https://github.com/你的用户名/Python_Git_exam.git
   $ git checkout -b fix/test
   $ git push -u origin fix/test
   
   ✅ 成功推送到你的 Fork
   
   [GitHub 网页] 创建跨仓库 PR
```

### ✅ 正确做法 (协作者)

```
1. 获得权限 → 克隆原仓库 → 推送
   
   [等待管理员添加为协作者]
   [接受邀请]
   
   $ git clone https://github.com/westlakeomics/Python_Git_exam.git
   $ git checkout -b fix/test
   $ git push -u origin fix/test
   
   ✅ 成功推送
   ✅ 自动创建 PR
```

---

## Fork vs 协作者对比表

| 特性              | Fork 工作流       | 协作者直接推送    |
|------------------|------------------|-----------------|
| **需要权限**      | ❌ 不需要         | ✅ 需要         |
| **推送目标**      | 你的 Fork        | 原仓库          |
| **工作副本位置**  | 你的账户下        | 原仓库分支      |
| **PR 创建**       | 手动跨仓库       | 自动创建        |
| **适用人群**      | 所有人           | 团队成员        |
| **学习价值**      | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     |
| **开源标准**      | ✅ 标准流程       | 团队内部流程    |
| **远程配置**      | origin + upstream| 仅 origin       |
| **同步复杂度**    | 需要同步上游     | 自动最新        |
| **推荐度（外部）** | 🌟 强烈推荐      | N/A            |
| **推荐度（团队）** | 可选             | 🌟 推荐         |

---

## 认证方式对比

### HTTPS vs SSH

```
HTTPS (使用 Personal Access Token)
┌─────────────────────────────────────┐
│ git clone https://github.com/...    │
│                                     │
│ 优点:                                │
│ ✅ 配置简单                          │
│ ✅ 适合新手                          │
│ ✅ 防火墙友好                        │
│                                     │
│ 缺点:                                │
│ ❌ 需要输入 Token                    │
│ ❌ Token 可能过期                    │
└─────────────────────────────────────┘

SSH (使用 SSH 密钥)
┌─────────────────────────────────────┐
│ git clone git@github.com:...        │
│                                     │
│ 优点:                                │
│ ✅ 无需输入密码                      │
│ ✅ 更安全                            │
│ ✅ 长期使用方便                      │
│                                     │
│ 缺点:                                │
│ ❌ 初始配置复杂                      │
│ ❌ 某些网络可能阻止                  │
└─────────────────────────────────────┘
```

---

## 完整工作流可视化 (Fork)

```
┌─────────────────────────────────────────────────────────────────┐
│                          GitHub 生态                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         westlakeomics/Python_Git_exam (原仓库)            │  │
│  │                      main                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↑                                     │
│                           │                                     │
│                           │ 5. Pull Request                     │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         你的用户名/Python_Git_exam (你的 Fork)             │  │
│  │                 fix/你的用户名                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↑                                     │
│                           │ 4. Push                             │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                        本地环境                                  │
├───────────────────────────┼─────────────────────────────────────┤
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              本地仓库                                     │  │
│  │                                                           │  │
│  │  remotes/                                                │  │
│  │    ├─ origin/fix/你的用户名  (你的 Fork)                  │  │
│  │    └─ upstream/main          (原仓库，只读)              │  │
│  │                                                           │  │
│  │  本地分支:                                                │  │
│  │    ├─ main                                               │  │
│  │    └─ fix/你的用户名 ← 当前工作分支                       │  │
│  │                                                           │  │
│  │  工作流程:                                                │  │
│  │    1. Fork (GitHub 网页)                                 │  │
│  │    2. git clone (你的 Fork)                              │  │
│  │    3. git commit                                         │  │
│  │    4. git push origin fix/你的用户名                      │  │
│  │    5. 创建 PR (GitHub 网页)                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 故障排除流程图

```
                遇到 403 错误
                      │
                      ↓
         ┌────────────────────────┐
         │ 检查：你推送到哪里了？    │
         └────────────────────────┘
                │            │
                ↓            ↓
         原仓库 URL      你的 Fork URL
                │            │
                ↓            ↓
         ┌──────────┐   ┌──────────┐
         │是协作者？ │   │ 应该成功  │
         └──────────┘   │ 检查认证  │
                │       └──────────┘
           是   │   否
                ↓   ↓
         ┌──────────┐   ┌──────────┐
         │ 检查认证  │   │ 使用 Fork │
         │ (PAT/SSH)│   │ 工作流   │
         └──────────┘   └──────────┘
```

---

## 快速参考卡片

### Fork 工作流速查

```bash
# 1. Fork (GitHub 网页)

# 2. 克隆你的 Fork
git clone https://github.com/你的用户名/Python_Git_exam.git
cd Python_Git_exam

# 3. 添加上游
git remote add upstream https://github.com/westlakeomics/Python_Git_exam.git

# 4. 创建分支
git checkout -b fix/你的用户名

# 5. 工作、提交
git add .
git commit -m "fix: your changes"

# 6. 推送到你的 Fork
git push -u origin fix/你的用户名

# 7. 创建 PR (GitHub 网页)

# 8. 同步上游（定期）
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 协作者工作流速查

```bash
# 1. 接受邀请 (Email/GitHub)

# 2. 克隆原仓库
git clone https://github.com/westlakeomics/Python_Git_exam.git
cd Python_Git_exam

# 3. 创建分支
git checkout -b fix/你的用户名

# 4. 工作、提交
git add .
git commit -m "fix: your changes"

# 5. 推送
git push -u origin fix/你的用户名

# 6. PR 自动创建 ✅
```

---

## 总结

### 记住这些关键点：

1. **Public ≠ Push Access** 📌
   - Public 只控制可见性
   - 写入需要明确权限

2. **Fork 是标准流程** 🌟
   - 适合所有外部贡献
   - GitHub 开源项目标准

3. **两个远程：origin + upstream** 🔄
   - origin: 你的 Fork（可写）
   - upstream: 原仓库（只读）

4. **PR 连接两个仓库** 🔗
   - 从你的 Fork
   - 到原仓库

5. **定期同步很重要** 🔄
   - `git fetch upstream`
   - `git merge upstream/main`

---

## 相关文档

- 📘 [CONTRIBUTING.md](CONTRIBUTING.md) - 详细贡献指南
- 📘 [FAQ.md](FAQ.md) - 常见问题解答
- 📘 [README.md](README.md) - 项目说明

---

**版本**: 1.0  
**最后更新**: 2025-12-25  
**适用项目**: westlakeomics/Python_Git_exam
