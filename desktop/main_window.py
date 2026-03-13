"""
桌面应用主窗口
PySide6主界面实现
"""

import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QMessageBox, QInputDialog, QToolBar, QStatusBar,
    QApplication, QSplitter, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, QSize, QUrl, Signal, QMimeData
from PySide6.QtGui import QAction, QDesktopServices, QIcon, QFont, QDrag

from core.storage import TaskStorage
from core.api_server import ApiServer
from core.models import TaskStatus


class TaskCard(QFrame):
    """任务卡片组件"""
    
    clicked = Signal(int)  # 点击信号，传递任务ID
    double_clicked = Signal(int)  # 双击信号，传递任务ID
    delete_requested = Signal(int)  # 删除请求信号，传递任务ID
    
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.task_id = task.id
        self.setup_ui()
    
    def setup_ui(self):
        """设置卡片界面"""
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setLineWidth(1)
        self.setMidLineWidth(0)
        self.setMinimumHeight(100)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # 顶部栏（优先级和删除按钮）
        top_layout = QHBoxLayout()
        
        # 优先级指示器
        priority_color = self._get_priority_color(self.task.priority)
        priority_indicator = QLabel("●")
        priority_indicator.setStyleSheet(f"color: {priority_color}; font-size: 16px;")
        priority_indicator.setToolTip(f"优先级: {self.task.priority}")
        top_layout.addWidget(priority_indicator)
        
        top_layout.addStretch()
        
        # 删除按钮
        delete_button = QPushButton("×")
        delete_button.setFixedSize(24, 24)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
            QPushButton:pressed {
                background-color: #ff2222;
            }
        """)
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.clicked.connect(self.on_delete_clicked)
        top_layout.addWidget(delete_button)
        
        main_layout.addLayout(top_layout)
        
        # 任务内容
        content_label = QLabel(self.task.content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(content_label)
        
        # 如果有描述，显示描述
        if self.task.description:
            desc_label = QLabel(self.task.description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #666; font-size: 12px; margin-top: 5px;")
            main_layout.addWidget(desc_label)
        
        # 底部信息栏
        bottom_layout = QHBoxLayout()
        
        # 任务ID
        id_label = QLabel(f"ID: {self.task.id}")
        id_label.setStyleSheet("color: #666; font-size: 11px;")
        bottom_layout.addWidget(id_label)
        
        # 状态标签
        status_text = TaskStatus.get_display_name(self.task.status)
        status_label = QLabel(status_text)
        status_color = self._get_status_color(self.task.status)
        status_label.setStyleSheet(f"""
            background-color: {status_color};
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
        """)
        bottom_layout.addWidget(status_label)
        
        bottom_layout.addStretch()
        
        # 标签显示
        if self.task.tags:
            tags_text = "🏷️ " + ", ".join(self.task.tags[:3])  # 最多显示3个标签
            if len(self.task.tags) > 3:
                tags_text += "..."
            tags_label = QLabel(tags_text)
            tags_label.setStyleSheet("color: #888; font-size: 11px;")
            bottom_layout.addWidget(tags_label)
        
        main_layout.addLayout(bottom_layout)
        
        # 如果有到期时间，显示到期时间
        if self.task.due_date:
            from datetime import datetime
            try:
                due_date = datetime.fromisoformat(self.task.due_date)
                due_text = due_date.strftime("到期: %Y-%m-%d")
                due_label = QLabel(due_text)
                
                # 检查是否过期
                if self.task.is_overdue():
                    due_label.setStyleSheet("color: #ff4444; font-size: 11px; font-weight: bold;")
                    due_label.setToolTip("任务已过期！")
                else:
                    due_label.setStyleSheet("color: #666; font-size: 11px;")
                
                main_layout.addWidget(due_label)
            except ValueError:
                pass
        
        # 设置鼠标事件
        self.setCursor(Qt.PointingHandCursor)
    
    def on_delete_clicked(self):
        """删除按钮点击事件"""
        self.delete_requested.emit(self.task_id)
    
    def _get_status_color(self, status):
        """根据状态获取颜色"""
        colors = {
            "todo": "#ff9800",      # 橙色
            "in_progress": "#2196f3",  # 蓝色
            "done": "#4caf50"       # 绿色
        }
        return colors.get(status, "#9e9e9e")
    
    def _get_priority_color(self, priority):
        """根据优先级获取颜色"""
        colors = {
            "high": "#f44336",    # 红色
            "medium": "#ff9800",   # 橙色
            "low": "#4caf50"      # 绿色
        }
        return colors.get(priority, "#9e9e9e")
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.task_id)
            # 开始拖放
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 开始拖放"""
        if not (event.buttons() & Qt.LeftButton):
            return
        
        # 检查是否移动了足够的距离才开始拖放
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        
        # 创建拖放对象
        drag = QDrag(self)
        mime_data = QMimeData()
        
        # 设置拖放数据
        mime_data.setText(str(self.task_id))
        drag.setMimeData(mime_data)
        
        # 设置拖放时的预览图像
        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos() - self.pos())
        
        # 开始拖放
        drag.exec(Qt.MoveAction)
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit(self.task_id)
        super().mouseDoubleClickEvent(event)


class TaskColumn(QWidget):
    """任务列组件（待办事项、进行中、已完成）"""
    
    def __init__(self, title, status, parent=None):
        super().__init__(parent)
        self.title = title
        self.status = status
        self.task_cards = {}  # task_id -> TaskCard
        self.setup_ui()
    
    def setup_ui(self):
        """设置列界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # 列标题
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333;
            padding: 8px;
            background-color: #f0f0f0;
            border-radius: 5px;
        """)
        layout.addWidget(title_label)
        
        # 任务计数
        self.count_label = QLabel("0 个任务")
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.count_label)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 滚动区域内容
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(8)
        self.content_layout.addStretch()  # 添加弹性空间
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
        
        # 添加任务按钮
        add_button = QPushButton("+ 添加任务")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_button.clicked.connect(self.on_add_task)
        layout.addWidget(add_button)
        
        # 启用拖放
        self.setAcceptDrops(True)
        self.content_widget.setAcceptDrops(True)
        scroll_area.setAcceptDrops(True)
    
    def add_task_card(self, task):
        """添加任务卡片"""
        if task.id in self.task_cards:
            return
        
        task_card = TaskCard(task)
        self.task_cards[task.id] = task_card
        
        # 插入到弹性空间之前
        self.content_layout.insertWidget(self.content_layout.count() - 1, task_card)
        
        # 连接信号
        main_window = self.get_main_window()
        if main_window:
            task_card.clicked.connect(main_window.on_task_clicked)
            task_card.double_clicked.connect(main_window.on_task_double_clicked)
            task_card.delete_requested.connect(main_window.delete_task)
        
        self.update_count()
    
    def remove_task_card(self, task_id):
        """移除任务卡片"""
        if task_id in self.task_cards:
            task_card = self.task_cards.pop(task_id)
            task_card.setParent(None)
            task_card.deleteLater()
            self.update_count()
    
    def clear_cards(self):
        """清空所有卡片"""
        for task_id in list(self.task_cards.keys()):
            self.remove_task_card(task_id)
    
    def update_count(self):
        """更新任务计数"""
        count = len(self.task_cards)
        self.count_label.setText(f"{count} 个任务")
    
    def get_main_window(self):
        """获取主窗口实例"""
        parent = self.parent()
        while parent is not None:
            if isinstance(parent, MainWindow):
                return parent
            parent = parent.parent()
        return None
    
    def on_add_task(self):
        """添加任务按钮点击事件"""
        main_window = self.get_main_window()
        if main_window:
            main_window.add_task_to_status(self.status)
    
    def dragEnterEvent(self, event):
        """拖放进入事件"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """拖放释放事件"""
        if event.mimeData().hasText():
            try:
                task_id = int(event.mimeData().text())
                main_window = self.get_main_window()
                if main_window:
                    # 移动任务到当前列的状态
                    main_window.move_task(task_id, self.status)
                event.acceptProposedAction()
            except ValueError:
                event.ignore()
    
    def dragMoveEvent(self, event):
        """拖放移动事件"""
        if event.mimeData().hasText():
            event.acceptProposedAction()


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.storage = TaskStorage()
        self.api_server = None
        
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_statusbar()
        
        # 加载数据
        self.load_tasks()
        
        # 启动API服务器
        self.start_api_server()
    
    def setup_ui(self):
        """设置主界面"""
        self.setWindowTitle("待办事项管理器")
        self.setGeometry(100, 100, 1200, 700)
        
        # 设置窗口图标（如果有）
        # self.setWindowIcon(QIcon("resources/icons/app.ico"))
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建3个任务列
        self.columns = {}
        
        # 待办事项列
        todo_column = TaskColumn("待办事项", "todo", self)
        self.columns["todo"] = todo_column
        main_layout.addWidget(todo_column)
        
        # 进行中列
        in_progress_column = TaskColumn("进行中", "in_progress", self)
        self.columns["in_progress"] = in_progress_column
        main_layout.addWidget(in_progress_column)
        
        # 已完成列
        done_column = TaskColumn("已完成", "done", self)
        self.columns["done"] = done_column
        main_layout.addWidget(done_column)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            TaskColumn {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)
    
    def setup_menu(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        new_action = QAction("新建任务", self)
        new_action.triggered.connect(self.add_task)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑(&E)")
        
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.refresh_tasks)
        edit_menu.addAction(refresh_action)
        
        edit_menu.addSeparator()
        
        # 标签管理
        tag_action = QAction("标签管理", self)
        tag_action.triggered.connect(self.manage_tags)
        edit_menu.addAction(tag_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图(&V)")
        
        web_action = QAction("打开网页版", self)
        web_action.triggered.connect(self.open_web_version)
        view_menu.addAction(web_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_toolbar(self):
        """设置工具栏"""
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # 添加任务按钮
        add_action = QAction("添加任务", self)
        add_action.triggered.connect(self.add_task)
        toolbar.addAction(add_action)
        
        toolbar.addSeparator()
        
        # 刷新按钮
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.refresh_tasks)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # 网页版按钮
        web_action = QAction("网页版", self)
        web_action.triggered.connect(self.open_web_version)
        toolbar.addAction(web_action)
    
    def setup_statusbar(self):
        """设置状态栏"""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        statusbar.addWidget(self.status_label)
        
        # 服务器状态标签
        self.server_status_label = QLabel("")
        statusbar.addPermanentWidget(self.server_status_label)
    
    def load_tasks(self):
        """加载任务数据"""
        tasks = self.storage.load()
        
        # 清空所有列
        for column in self.columns.values():
            column.clear_cards()
        
        # 添加任务到对应列
        for task in tasks:
            if task.status in self.columns:
                self.columns[task.status].add_task_card(task)
        
        # 更新状态栏
        stats = self.storage.get_stats()
        self.status_label.setText(f"总计: {stats['total']} 个任务 | 待办: {stats['todo']} | 进行中: {stats['in_progress']} | 已完成: {stats['done']}")
    
    def refresh_tasks(self):
        """刷新任务显示"""
        self.load_tasks()
        self.status_label.setText("已刷新")
    
    def add_task(self):
        """添加新任务"""
        text, ok = QInputDialog.getText(
            self, "添加任务", "请输入任务内容:"
        )
        
        if ok and text:
            task = self.storage.add_task(text, status="todo")
            if task:
                self.columns["todo"].add_task_card(task)
                self.refresh_tasks()
                self.status_label.setText(f"已添加任务: {text}")
            else:
                QMessageBox.warning(self, "错误", "添加任务失败")
    
    def add_task_to_status(self, status):
        """添加任务到指定状态列"""
        text, ok = QInputDialog.getText(
            self, f"添加到{TaskStatus.get_display_name(status)}", "请输入任务内容:"
        )
        
        if ok and text:
            task = self.storage.add_task(text, status=status)
            if task:
                self.columns[status].add_task_card(task)
                self.refresh_tasks()
                self.status_label.setText(f"已添加任务到{TaskStatus.get_display_name(status)}: {text}")
            else:
                QMessageBox.warning(self, "错误", "添加任务失败")
    
    def on_task_clicked(self, task_id):
        """任务点击事件"""
        task = self.storage.get_task(task_id)
        if task:
            self.status_label.setText(f"选中任务: {task.content}")
    
    def on_task_double_clicked(self, task_id):
        """任务双击事件（编辑）"""
        task = self.storage.get_task(task_id)
        if not task:
            return
        
        # 获取新内容
        new_text, ok = QInputDialog.getText(
            self, "编辑任务", "修改任务内容:", text=task.content
        )
        
        if ok and new_text and new_text != task.content:
            # 更新任务
            updated = self.storage.update_task(task_id, content=new_text)
            if updated:
                # 重新加载任务
                self.refresh_tasks()
                self.status_label.setText(f"已更新任务: {new_text}")
    
    def delete_task(self, task_id):
        """删除任务"""
        task = self.storage.get_task(task_id)
        if not task:
            return
        
        # 确认对话框
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除任务 '{task.content}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.storage.delete_task(task_id):
                # 从对应列移除
                if task.status in self.columns:
                    self.columns[task.status].remove_task_card(task_id)
                self.refresh_tasks()
                self.status_label.setText(f"已删除任务: {task.content}")
            else:
                QMessageBox.warning(self, "错误", "删除任务失败")
    
    def move_task(self, task_id, new_status):
        """移动任务到新状态"""
        task = self.storage.get_task(task_id)
        if not task:
            return
        
        if task.status == new_status:
            return
        
        # 移动任务
        moved_task = self.storage.move_task(task_id, new_status)
        if moved_task:
            # 从原列移除
            if task.status in self.columns:
                self.columns[task.status].remove_task_card(task_id)
            
            # 添加到新列
            if new_status in self.columns:
                self.columns[new_status].add_task_card(moved_task)
            
            self.refresh_tasks()
            self.status_label.setText(f"已移动任务到{TaskStatus.get_display_name(new_status)}")
    
    def start_api_server(self):
        """启动API服务器"""
        from core.api_server import ApiServer
        self.api_server = ApiServer(self.storage, port=5000)
        self.api_server.start(debug=False)
        
        # 更新状态栏
        if self.api_server.is_running():
            self.server_status_label.setText(f"网页版: http://localhost:5000")
        else:
            self.server_status_label.setText("API服务器启动失败")
    
    def open_web_version(self):
        """打开网页版"""
        if self.api_server and self.api_server.is_running():
            QDesktopServices.openUrl(QUrl("http://localhost:5000"))
        else:
            QMessageBox.warning(self, "错误", "API服务器未运行，无法打开网页版")
    
    def manage_tags(self):
        """管理标签"""
        try:
            # 尝试导入标签管理对话框
            from tag_manager import TagManagerDialog
            
            # 获取所有标签
            all_tags = self.storage.get_all_tags()
            
            # 创建标签管理对话框
            dialog = TagManagerDialog(all_tags, self)
            dialog.tags_updated.connect(self.on_tags_updated)
            dialog.exec()
        except ImportError:
            # 如果标签管理模块不存在，显示简单对话框
            all_tags = self.storage.get_all_tags()
            if all_tags:
                tags_text = "\n".join(f"• {tag}" for tag in all_tags)
                message = f"当前所有标签 ({len(all_tags)} 个):\n\n{tags_text}"
            else:
                message = "当前没有标签"
            
            QMessageBox.information(self, "标签管理", message)
    
    def on_tags_updated(self, tags):
        """标签更新事件"""
        # 这里可以保存标签配置到文件
        # 目前只是更新显示
        self.status_label.setText(f"标签已更新，共 {len(tags)} 个标签")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = (
            "待办事项管理器\n\n"
            "版本: 1.0.0\n\n"
            "一个简单的多平台待办事项管理工具\n\n"
            "功能:\n"
            "• 3列卡片式任务管理\n"
            "• 桌面应用 + 网页版\n"
            "• 数据自动保存\n"
            "• 支持任务标签"
        )
        QMessageBox.about(self, "关于待办事项管理器", about_text)
