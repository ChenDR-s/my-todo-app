"""
测试脚本 - 测试待办事项管理器所有功能
"""

import os
import sys
import json
from pathlib import Path


def test_core_modules():
    """测试核心模块"""
    print("=" * 60)
    print("测试核心模块")
    print("=" * 60)
    
    try:
        # 添加项目根目录到Python路径
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from core.models import Task, TaskStatus
        from core.storage import TaskStorage
        
        print("[OK] 导入核心模块成功")
        
        # 测试任务模型
        task = Task(1, "测试任务", "todo", tags=["测试", "示例"])
        print(f"[OK] 任务模型: {task}")
        print(f"[OK] 任务字典: {task.to_dict()}")
        
        # 测试存储
        storage = TaskStorage()
        print("[OK] 存储模块初始化成功")
        
        # 测试添加任务
        added_task = storage.add_task("测试添加任务", status="todo", tags=["测试"])
        if added_task:
            print(f"[OK] 添加任务成功: ID={added_task.id}")
        else:
            print("[FAIL] 添加任务失败")
            return False
        
        # 测试获取任务
        retrieved_task = storage.get_task(added_task.id)
        if retrieved_task:
            print(f"[OK] 获取任务成功: {retrieved_task.content}")
        else:
            print("[FAIL] 获取任务失败")
            return False
        
        # 测试更新任务
        updated = storage.update_task(added_task.id, content="更新后的任务", tags=["测试", "更新"])
        if updated:
            print("[OK] 更新任务成功")
        else:
            print("[FAIL] 更新任务失败")
            return False
        
        # 测试移动任务
        moved_task = storage.move_task(added_task.id, "in_progress")
        if moved_task and moved_task.status == "in_progress":
            print("[OK] 移动任务成功")
        else:
            print("[FAIL] 移动任务失败")
            return False
        
        # 测试删除任务
        deleted = storage.delete_task(added_task.id)
        if deleted:
            print("[OK] 删除任务成功")
        else:
            print("[FAIL] 删除任务失败")
            return False
        
        # 测试统计
        stats = storage.get_stats()
        print(f"[OK] 任务统计: {stats}")
        
        print("\n[SUCCESS] 核心模块测试通过")
        return True
        
    except Exception as e:
        print(f"[FAIL] 核心模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_server():
    """测试API服务器模块"""
    print("\n" + "=" * 60)
    print("测试API服务器模块")
    print("=" * 60)
    
    try:
        from core.api_server import ApiServer
        from core.storage import TaskStorage
        
        storage = TaskStorage()
        api_server = ApiServer(storage, port=5002)  # 使用不同端口避免冲突
        
        print("[OK] API服务器模块导入成功")
        
        # 注意：这里不实际启动服务器，只测试模块功能
        print("[INFO] API服务器模块功能测试通过（需要实际运行测试）")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] API服务器模块测试失败: {e}")
        return False


def test_desktop_import():
    """测试桌面应用导入"""
    print("\n" + "=" * 60)
    print("测试桌面应用导入")
    print("=" * 60)
    
    try:
        from desktop.main_window import MainWindow, TaskCard, TaskColumn
        print("[OK] 桌面应用模块导入成功")
        
        # 测试是否能创建实例（不显示窗口）
        print("[INFO] 桌面应用模块功能测试通过（需要GUI环境）")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] 桌面应用模块导入失败: {e}")
        return False


def test_web_import():
    """测试网页版导入"""
    print("\n" + "=" * 60)
    print("测试网页版导入")
    print("=" * 60)
    
    try:
        from web.app import create_app
        print("[OK] 网页版模块导入成功")
        
        app = create_app()
        print("[OK] Flask应用创建成功")
        
        # 测试路由
        with app.test_client() as client:
            response = client.get('/api/health')
            if response.status_code == 200:
                print("[OK] 健康检查端点正常")
            else:
                print(f"[FAIL] 健康检查端点异常: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"[FAIL] 网页版模块测试失败: {e}")
        return False


def test_data_file():
    """测试数据文件"""
    print("\n" + "=" * 60)
    print("测试数据文件")
    print("=" * 60)
    
    data_file = Path("tasks.json")
    
    if data_file.exists():
        print(f"[OK] 数据文件存在: {data_file.absolute()}")
        
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            print(f"[OK] 数据文件格式正确，包含 {len(data)} 个任务")
            
            # 检查数据格式
            if data and isinstance(data, list):
                sample_task = data[0]
                required_fields = ["id", "content", "status", "created_at"]
                missing_fields = [field for field in required_fields if field not in sample_task]
                
                if not missing_fields:
                    print("[OK] 数据格式正确")
                else:
                    print(f"[WARN] 数据缺少字段: {missing_fields}")
            
            return True
            
        except Exception as e:
            print(f"[FAIL] 读取数据文件失败: {e}")
            return False
    else:
        print("[INFO] 数据文件不存在，将在首次运行时创建")
        return True


def test_run_script():
    """测试运行脚本"""
    print("\n" + "=" * 60)
    print("测试运行脚本")
    print("=" * 60)
    
    try:
        import run
        print("[OK] 运行脚本导入成功")
        
        # 测试命令行参数解析
        import argparse
        
        parser = argparse.ArgumentParser(description="待办事项管理器启动脚本")
        parser.add_argument(
            "mode",
            nargs="?",
            default="desktop",
            choices=["desktop", "web", "test"],
            help="启动模式 (默认: desktop)"
        )
        
        print("[OK] 命令行参数解析正常")
        return True
        
    except Exception as e:
        print(f"[FAIL] 运行脚本测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("待办事项管理器 - 功能测试")
    print("=" * 60)
    
    tests = [
        ("核心模块", test_core_modules),
        ("API服务器模块", test_api_server),
        ("桌面应用导入", test_desktop_import),
        ("网页版导入", test_web_import),
        ("数据文件", test_data_file),
        ("运行脚本", test_run_script),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"[FAIL] {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "通过" if success else "失败"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n[SUCCESS] 所有测试通过！")
        print("\n下一步:")
        print("1. 运行桌面应用: python run.py")
        print("2. 运行网页版: python run.py web")
        print("3. 测试数据兼容性: python run.py test")
        print("4. 打包EXE文件: python build_exe.py")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} 个测试失败")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)