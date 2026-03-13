"""
网页版应用
提供简单的Web界面查看任务
"""

import os
import sys
from flask import Flask, render_template, jsonify, request

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.storage import TaskStorage
from core.models import TaskStatus


def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 初始化存储
    storage = TaskStorage()
    
    @app.route('/')
    def index():
        """首页 - 显示任务看板"""
        tasks = storage.load()
        
        # 按状态分组
        tasks_by_status = {
            "todo": [],
            "in_progress": [],
            "done": []
        }
        
        for task in tasks:
            if task.status in tasks_by_status:
                tasks_by_status[task.status].append(task.to_dict())
        
        # 获取统计信息
        stats = storage.get_stats()
        
        return render_template(
            'index.html',
            tasks_by_status=tasks_by_status,
            stats=stats,
            TaskStatus=TaskStatus
        )
    
    @app.route('/api/tasks')
    def get_tasks():
        """获取所有任务（API端点）"""
        try:
            tasks = storage.load()
            tasks_data = [task.to_dict() for task in tasks]
            return jsonify({
                "success": True,
                "data": tasks_data,
                "count": len(tasks_data)
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/stats')
    def get_stats():
        """获取任务统计（API端点）"""
        try:
            stats = storage.get_stats()
            return jsonify({
                "success": True,
                "data": stats
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/health')
    def health_check():
        """健康检查端点"""
        return jsonify({
            "status": "healthy",
            "service": "todo-manager-web"
        })
    
    @app.errorhandler(404)
    def not_found(error):
        """404错误处理"""
        return render_template('error.html', 
                             error_code=404,
                             error_message="页面未找到"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500错误处理"""
        return render_template('error.html',
                             error_code=500,
                             error_message="服务器内部错误"), 500
    
    return app


def run_web_app(port=5000, debug=False):
    """
    运行网页版应用
    
    Args:
        port: 端口号
        debug: 是否启用调试模式
    """
    app = create_app()
    
    print("=" * 60)
    print("待办事项管理器 - 网页版")
    print("=" * 60)
    print(f"访问地址: http://localhost:{port}")
    print("功能:")
    print("  - 3列卡片式任务显示")
    print("  - 自动刷新（每10秒）")
    print("  - 任务统计信息")
    print("=" * 60)
    print("注意: 网页版为只读，修改任务请在桌面应用中操作")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == "__main__":
    # 独立运行网页版
    run_web_app(port=5001, debug=True)  # 使用5001端口避免与桌面应用冲突