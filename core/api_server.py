"""
API服务器模块
提供Web API供网页版访问
"""

import threading
from flask import Flask, jsonify, request
from typing import Dict, Any
from .storage import TaskStorage


class ApiServer:
    """API服务器类"""
    
    def __init__(self, storage: TaskStorage, port: int = 5000):
        """
        初始化API服务器
        
        Args:
            storage: 任务存储实例
            port: 服务器端口
        """
        self.storage = storage
        self.port = port
        self.app = Flask(__name__)
        self.thread = None
        self._setup_routes()
    
    def _setup_routes(self):
        """设置API路由"""
        
        @self.app.route('/')
        def index():
            """首页重定向到API文档"""
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>待办事项管理器 API</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h1 { color: #333; }
                    .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                    code { background: #eee; padding: 2px 5px; border-radius: 3px; }
                </style>
            </head>
            <body>
                <h1>待办事项管理器 API 服务器</h1>
                <p>此服务器为网页版提供数据接口。</p>
                <p>请访问 <a href="/api/tasks">/api/tasks</a> 获取任务数据。</p>
                
                <h2>可用端点：</h2>
                <div class="endpoint">
                    <strong>GET /api/tasks</strong> - 获取所有任务
                </div>
                <div class="endpoint">
                    <strong>GET /api/stats</strong> - 获取任务统计
                </div>
                <div class="endpoint">
                    <strong>GET /api/health</strong> - 健康检查
                </div>
                
                <p style="margin-top: 30px; color: #666;">
                    注意：网页版为只读，添加/编辑/删除任务请在桌面应用中操作。
                </p>
            </body>
            </html>
            """
        
        @self.app.route('/api/tasks', methods=['GET'])
        def get_tasks():
            """获取所有任务"""
            try:
                tasks = self.storage.load()
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
        
        @self.app.route('/api/tasks/<int:task_id>', methods=['GET'])
        def get_task(task_id: int):
            """获取单个任务"""
            try:
                task = self.storage.get_task(task_id)
                if task:
                    return jsonify({
                        "success": True,
                        "data": task.to_dict()
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": f"任务 {task_id} 不存在"
                    }), 404
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """获取任务统计"""
            try:
                stats = self.storage.get_stats()
                return jsonify({
                    "success": True,
                    "data": stats
                })
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """健康检查端点"""
            return jsonify({
                "status": "healthy",
                "service": "todo-manager-api",
                "port": self.port
            })
        
        @self.app.errorhandler(404)
        def not_found(error):
            """404错误处理"""
            return jsonify({
                "success": False,
                "error": "端点不存在"
            }), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """500错误处理"""
            return jsonify({
                "success": False,
                "error": "服务器内部错误"
            }), 500
    
    def start(self, debug: bool = False):
        """
        启动API服务器（在后台线程中）
        
        Args:
            debug: 是否启用调试模式
        """
        if self.thread and self.thread.is_alive():
            print(f"API服务器已在端口 {self.port} 运行")
            return
        
        def run_server():
            """运行Flask服务器的内部函数"""
            try:
                self.app.run(
                    host='0.0.0.0',
                    port=self.port,
                    debug=debug,
                    use_reloader=False,
                    threaded=True
                )
            except Exception as e:
                print(f"API服务器启动失败: {e}")
        
        # 在后台线程中启动服务器
        self.thread = threading.Thread(
            target=run_server,
            daemon=True  # 设置为守护线程，主程序退出时自动结束
        )
        self.thread.start()
        
        print(f"API服务器已启动，访问地址: http://localhost:{self.port}")
        print(f"API文档: http://localhost:{self.port}/")
    
    def stop(self):
        """停止API服务器"""
        # Flask没有内置的stop方法，通常让线程自然结束
        # 这里主要是标记线程应该结束
        if self.thread and self.thread.is_alive():
            print("正在停止API服务器...")
            # 在实际应用中，可能需要更复杂的停止机制
            # 但对于简单应用，守护线程会在主程序退出时自动结束
    
    def is_running(self) -> bool:
        """检查服务器是否正在运行"""
        return self.thread is not None and self.thread.is_alive()
    
    def get_server_info(self) -> Dict[str, Any]:
        """获取服务器信息"""
        return {
            "running": self.is_running(),
            "port": self.port,
            "url": f"http://localhost:{self.port}",
            "api_endpoint": f"http://localhost:{self.port}/api/tasks"
        }


def create_api_server(storage: TaskStorage, port: int = 5000) -> ApiServer:
    """
    创建API服务器的工厂函数
    
    Args:
        storage: 任务存储实例
        port: 服务器端口
        
    Returns:
        ApiServer实例
    """
    return ApiServer(storage, port)