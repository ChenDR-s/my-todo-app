# Git上传操作指南

## 问题诊断
您遇到的错误：
```
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/sephiroth8500-byte/todo-manager.git'
```

**原因**：您的本地分支名称是`master`，但GitHub默认使用`main`分支。

## 解决方案

### 方案一：重命名本地分支（推荐）
在`my_todo_app`目录中执行以下命令：

```bash
# 1. 重命名本地分支从master到main
git branch -M main

# 2. 添加新文件到Git（.gitignore和LICENSE）
git add .gitignore LICENSE

# 3. 提交更改
git commit -m "添加.gitignore和MIT许可证"

# 4. 推送到GitHub
git push -u origin main
```

### 方案二：使用现有master分支
如果您想保留`master`分支名称：

```bash
# 1. 添加新文件
git add .gitignore LICENSE

# 2. 提交更改
git commit -m "添加.gitignore和MIT许可证"

# 3. 推送到GitHub的master分支
git push -u origin master
```

## 完整操作步骤

### 步骤1：打开命令提示符
1. 在`my_todo_app`文件夹中，按住Shift键并右键点击
2. 选择"在此处打开命令窗口"或"在此处打开PowerShell窗口"

### 步骤2：执行Git命令
根据您选择的方案，执行以下命令：

#### 如果选择方案一（使用main分支）：
```bash
git branch -M main
git add .gitignore LICENSE
git commit -m "添加.gitignore和MIT许可证"
git push -u origin main
```

#### 如果选择方案二（使用master分支）：
```bash
git add .gitignore LICENSE
git commit -m "添加.gitignore和MIT许可证"
git push -u origin master
```

### 步骤3：验证上传成功
1. 访问 https://github.com/sephiroth8500-byte/todo-manager
2. 确认能看到所有文件
3. 确认有`.gitignore`和`LICENSE`文件

## 常见问题解决

### 1. 如果提示"Please tell me who you are"
```bash
git config --global user.name "您的名字"
git config --global user.email "您的邮箱"
```

### 2. 如果提示"Authentication failed"
```bash
# 重新设置远程仓库
git remote remove origin
git remote add origin https://github.com/sephiroth8500-byte/todo-manager.git
```

### 3. 如果提示"Updates were rejected"
```bash
# 强制推送（谨慎使用）
git push -f origin main
```

## 后续Git操作

### 添加更多文件
```bash
# 添加所有新文件
git add .

# 或添加特定文件
git add README.md requirements.txt

# 提交更改
git commit -m "更新文档和依赖"

# 推送到GitHub
git push
```

### 查看状态
```bash
git status          # 查看当前状态
git log --oneline   # 查看提交历史
```

### 拉取更新（如果多人协作）
```bash
git pull origin main
```

## GitHub页面设置

### 1. 添加项目描述
1. 访问您的GitHub仓库
2. 点击"Settings"（设置）
3. 在"Description"中添加项目描述

### 2. 添加项目标签
1. 在仓库页面，点击"Manage topics"
2. 添加标签：`python`、`gui`、`flask`、`todo-app`

### 3. 设置README显示
1. 确保`README.md`在根目录
2. GitHub会自动显示README内容

## 项目状态检查

上传成功后，您的项目应该包含以下文件：
- ✅ `README.md` - 项目文档
- ✅ `requirements.txt` - 依赖列表
- ✅ `.gitignore` - Git忽略文件
- ✅ `LICENSE` - MIT许可证
- ✅ `run.py` - 启动脚本
- ✅ `core/` - 核心模块
- ✅ `desktop/` - 桌面应用
- ✅ `web/` - 网页版
- ✅ `resources/` - 资源文件

## 下一步建议

1. **完善项目信息**：在GitHub上添加详细描述和标签
2. **创建Release**：发布v1.0.0版本
3. **分享项目**：将GitHub链接分享给其他人
4. **收集反馈**：鼓励用户提交Issue和反馈

## 联系方式

如果遇到问题：
1. 检查本指南中的解决方案
2. 搜索错误信息在线解决方案
3. 联系项目维护者

**恭喜！** 您的项目现在已经成功上传到GitHub，可以分享给其他人使用了。