"""
桌面应用入口点
启动PySide6桌面应用
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from desktop.main_window import MainWindow


def main():
    """主函数"""
    # 创建应用实例
    app = QApplication(sys.argv)
    app.setApplicationName("待办事项管理器")
    app.setOrganizationName("TodoManager")
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 打印启动信息
    print("=" * 60)
    print("待办事项管理器 - 桌面应用")
    print("=" * 60)
    print("功能:")
    print("  - 3列卡片式任务管理")
    print("  - 添加、编辑、删除任务")
    print("  - 任务状态移动")
    print("  - 内置Web服务器")
    print("  - 网页版访问: http://localhost:5000")
    print("=" * 60)
    print("提示:")
    print("  - 双击任务卡片编辑内容")
    print("  - 使用工具栏按钮添加任务")
    print("  - 点击'网页版'按钮在浏览器中查看")
    print("=" * 60)
    
    # 设置退出时的清理
    def cleanup():
        if window.api_server:
            window.api_server.stop()
        print("应用已退出")
    
    # 连接应用退出信号
    app.aboutToQuit.connect(cleanup)
    
    # 启动应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()