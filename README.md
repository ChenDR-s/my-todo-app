# 待办事项管理器 - Todo Manager

![GitHub](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/status-stable-green)

一个简单的多平台待办事项管理工具，提供桌面应用和网页版。

## 📋 项目状态
- **版本**: v1.0.0
- **状态**: 稳定可用
- **最后更新**: 2026-03-13
- **GitHub**: [sephiroth8500-byte/todo-manager](https://github.com/sephiroth8500-byte/todo-manager)

## ✨ 功能特性

### 桌面应用 (PySide6)
- ✅ 3列卡片式界面（待办、进行中、已完成）
- ✅ 添加、编辑、删除任务
- ✅ 双击卡片编辑内容
- ✅ 任务状态移动
- ✅ 任务标签支持
- ✅ 内置Web服务器
- ✅ 浅色主题，响应式布局

### 网页版 (Flask)
- ✅ 3列卡片式显示
- ✅ 实时数据同步（每10秒自动刷新）
- ✅ 任务统计信息
- ✅ 连接状态提示
- ✅ 移动端适配
- ✅ 只读查看（修改需通过桌面应用）

### 核心功能
- ✅ 数据自动保存（JSON格式）
- ✅ 兼容现有`tasks.json`格式
- ✅ 主从API架构（桌面为主，网页为从）
- ✅ 统一图标设计
- ✅ 多平台支持

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动应用

#### 方式一：桌面应用（推荐）
```bash
python run.py
# 或
python run.py desktop
```

桌面应用启动后：
- 显示3列卡片界面
- 自动启动Web服务器（端口5000）
- 状态栏显示网页版地址

#### 方式二：网页版（独立运行）
```bash
python run.py web
```
访问：http://localhost:5001

#### 方式三：测试数据兼容性
```bash
python run.py test
```

## 📁 项目结构

```
todo_manager/
├── core/                    # 共享核心模块
│   ├── models.py           # 数据模型
│   ├── storage.py          # 文件存储
│   └── api_server.py       # API服务器
├── desktop/                # 桌面应用
│   ├── main_window.py      # 主窗口
│   └── main.py            # 入口点
├── web/                    # 网页版
│   ├── app.py             # Flask应用
│   ├── templates/         # HTML模板
│   │   ├── index.html     # 主页面
│   │   └── error.html     # 错误页面
│   └── static/            # 静态资源
├── resources/              # 资源文件
│   └── icons/             # 图标（待添加）
├── tasks.json             # 数据文件（自动创建）
├── run.py                 # 统一启动脚本
├── requirements.txt       # 依赖列表
└── README.md             # 本文档
```

## 🎯 使用指南

### 桌面应用操作
1. **添加任务**：点击工具栏"添加任务"按钮或各列底部的"+添加任务"按钮
2. **编辑任务**：双击任务卡片
3. **删除任务**：暂无直接删除按钮（可通过编辑清空内容）
4. **移动任务**：暂无拖放功能（后续版本添加）
5. **打开网页版**：点击工具栏"网页版"按钮或菜单"视图→打开网页版"

### 网页版功能
1. **自动刷新**：每10秒自动从桌面应用获取最新数据
2. **连接状态**：右下角显示连接状态（绿色=已连接，红色=断开）
3. **统计信息**：顶部显示任务统计
4. **移动端优化**：
   - 📱 **响应式设计**：完美适配手机、平板和桌面设备
   - 👆 **触摸优化**：卡片点击区域优化，支持长按菜单
   - 🔄 **下拉刷新**：在页面顶部下拉即可刷新数据
   - 📋 **复制分享**：长按卡片可复制内容或分享任务
   - 🎯 **触摸目标**：符合移动端最佳实践的最小触摸目标尺寸
   - 📊 **自适应布局**：根据屏幕尺寸自动调整列数和布局
5. **只读查看**：修改任务需通过桌面应用

### 数据文件
- 位置：`tasks.json`（与应用同级目录）
- 格式：JSON，兼容旧版本
- 备份：建议定期备份此文件

## 🔧 技术架构

### 系统架构
```
┌─────────────────┐     HTTP API     ┌─────────────────┐
│  桌面应用        │◄────────────────►│  网页版         │
│  (PySide6)      │   (localhost)    │  (Flask)        │
│                 │                  │                 │
│  • 主程序        │                  │  • Web界面      │
│  • 数据文件读写  │                  │  • API代理      │
│  • 内置Web服务器 │                  │                 │
└─────────────────┘                  └─────────────────┘
         │                                    │
         ▼                                    ▼
   ┌────────────┐                      ┌────────────┐
   │ tasks.json │                      │ 浏览器      │
   │ (本地文件)  │                      │ 访问        │
   └────────────┘                      └────────────┘
```

### 数据模型
```json
{
  "id": 1,
  "content": "学习Python",
  "status": "todo",  // "todo", "in_progress", "done"
  "created_at": "2024-03-11T10:30:00",
  "tags": ["学习", "编程"]
}
```

## 📦 打包为EXE

### 使用PyInstaller打包
```bash
# 打包桌面应用
pyinstaller --onefile --windowed --name="TodoManager" desktop/main.py

# 打包后文件位置
# dist/TodoManager.exe
```

### 打包配置建议
```bash
pyinstaller --onefile --windowed --name="TodoManager" \
  --add-data="core;core" \
  --add-data="web;web" \
  --icon="resources/icons/app.ico" \
  desktop/main.py
```

## 🔄 数据迁移

### 从旧版本迁移
1. 旧版本数据格式：
```json
[{"id": 1, "content": "任务1"}, {"id": 2, "content": "任务2"}]
```

2. 新版本自动兼容：
- 旧任务自动添加`status: "todo"`
- 旧任务自动添加`created_at`时间戳
- 旧任务自动添加空标签数组

### 手动迁移（如果需要）
```python
from core.storage import TaskStorage
storage = TaskStorage("old_tasks.json")
tasks = storage.load()
# 任务已自动转换格式
```

## 🐛 故障排除

### 常见问题

1. **网页版无法连接**
   - 确保桌面应用正在运行
   - 检查防火墙是否阻止端口5000
   - 访问 http://localhost:5000 测试

2. **数据文件损坏**
   - 备份`tasks.json`文件
   - 删除损坏的文件，程序会自动创建新文件
   - 从备份恢复数据

3. **依赖安装失败**
   - 使用国内镜像：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`
   - 确保Python版本≥3.8

4. **端口冲突**
   - 桌面应用使用端口5000
   - 独立网页版使用端口5001
   - 可修改`core/api_server.py`中的端口配置

### 日志查看
- 桌面应用：控制台输出
- 网页版：浏览器开发者工具（F12）→ 控制台
- 数据文件：`tasks.json`（文本编辑器查看）

## 📱 部署到服务器

### 网页版服务器部署
1. 复制`web/`目录到服务器
2. 安装依赖：`pip install Flask`
3. 修改`web/app.py`中的存储路径
4. 使用生产服务器部署（如Gunicorn + Nginx）

### 配置示例（Gunicorn）
```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 "web.app:create_app()"
```

## 📄 许可证

本项目采用MIT许可证。

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📞 支持与反馈

- 问题报告：GitHub Issues
- 功能建议：GitHub Discussions
- 紧急问题：邮件联系

## 🎉 更新日志

### v1.0.0 (2024-03-11)
- 初始版本发布
- 桌面应用基本功能
- 网页版查看功能
- 数据兼容性支持
- 统一启动脚本

---

**提示**：这是一个小工具项目，用户数<10人，设计目标是稳定、快速、低成本。如有复杂需求，请考虑更专业的任务管理工具。