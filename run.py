"""
待办事项管理器 - 统一启动脚本
提供多种启动方式
"""

import sys
import os
import argparse
from pathlib import Path


def print_banner():
    """打印应用横幅"""
    banner = """
    ============================================================
                  待办事项管理器 - Todo Manager
                  版本 1.0.0 - 多平台版
    ============================================================
    """
    print(banner)


def print_usage():
    """打印使用说明"""
    print("使用方式:")
    print("  python run.py [选项]")
    print()
    print("选项:")
    print("  desktop      启动桌面应用 (默认)")
    print("  web          启动网页版 (独立运行)")
    print("  test         测试数据兼容性")
    print("  --help       显示帮助信息")
    print()
    print("示例:")
    print("  python run.py              # 启动桌面应用")
    print("  python run.py web          # 启动网页版")
    print("  python run.py test         # 测试数据兼容性")
    print()


def run_desktop_app():
    """运行桌面应用"""
    print("正在启动桌面应用...")
    print("=" * 60)
    
    try:
        # 添加项目根目录到Python路径
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from desktop.main import main as desktop_main
        desktop_main()
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"启动桌面应用失败: {e}")
        return 1
    
    return 0


def run_web_app():
    """运行网页版（独立）"""
    print("正在启动网页版...")
    print("=" * 60)
    
    try:
        # 添加项目根目录到Python路径
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from web.app import run_web_app as web_main
        web_main(port=5001, debug=False)  # 使用5001端口避免冲突
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"启动网页版失败: {e}")
        return 1
    
    return 0


def test_data_compatibility():
    """测试数据兼容性"""
    print("正在测试数据兼容性...")
    print("=" * 60)
    
    try:
        # 添加项目根目录到Python路径
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from core.storage import TaskStorage
        from core.models import Task
        
        storage = TaskStorage()
        
        # 检查数据文件
        data_file = Path("tasks.json")
        if data_file.exists():
            print(f"[OK] 找到数据文件: {data_file.absolute()}")
            
            # 尝试加载数据
            tasks = storage.load()
            print(f"[OK] 成功加载 {len(tasks)} 个任务")
            
            # 检查任务格式
            if tasks:
                print("任务示例:")
                for i, task in enumerate(tasks[:3]):  # 显示前3个任务
                    print(f"  {i+1}. ID: {task.id}, 内容: {task.content}, 状态: {task.status}")
                if len(tasks) > 3:
                    print(f"  ... 还有 {len(tasks)-3} 个任务")
            else:
                print("[INFO] 数据文件为空")
        else:
            print("[INFO] 数据文件不存在，将在首次运行时创建")
        
        # 检查核心模块
        print("\n检查核心模块...")
        test_task = Task(999, "测试任务", "todo")
        print(f"[OK] 任务模型: {test_task}")
        print(f"[OK] 任务字典: {test_task.to_dict()}")
        
        # 检查API服务器
        print("\n检查API服务器模块...")
        from core.api_server import ApiServer
        print("[OK] API服务器模块可用")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] 数据兼容性测试通过！")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def check_dependencies():
    """检查依赖"""
    print("检查依赖...")
    
    # 必需依赖
    required_dependencies = [
        ("PySide6", "PySide6"),
        ("Flask", "flask"),
    ]
    
    # 可选依赖（用于打包）
    optional_dependencies = [
        ("PyInstaller", "pyinstaller"),
    ]
    
    all_required_ok = True
    
    # 检查必需依赖
    print("必需依赖:")
    for name, module in required_dependencies:
        try:
            __import__(module)
            print(f"  [OK] {name}")
        except ImportError:
            print(f"  [FAIL] {name} (未安装)")
            all_required_ok = False
    
    # 检查可选依赖
    print("\n可选依赖（用于打包）:")
    for name, module in optional_dependencies:
        try:
            __import__(module)
            print(f"  [OK] {name}")
        except ImportError:
            print(f"  [INFO] {name} (未安装，打包时需要)")
    
    if not all_required_ok:
        print("\n请安装缺失的必需依赖:")
        print("  pip install -r requirements.txt")
        return False
    
    print("\n[OK] 所有必需依赖已安装")
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="待办事项管理器启动脚本")
    parser.add_argument(
        "mode",
        nargs="?",
        default="desktop",
        choices=["desktop", "web", "test"],
        help="启动模式 (默认: desktop)"
    )
    
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 根据模式执行
    if args.mode == "desktop":
        print(f"\n启动模式: 桌面应用")
        print("=" * 60)
        return run_desktop_app()
    
    elif args.mode == "web":
        print(f"\n启动模式: 网页版 (独立运行)")
        print("=" * 60)
        print("注意: 此模式独立运行网页版，不与桌面应用共享数据")
        print("      如需与桌面应用同步，请使用桌面应用内置的网页版")
        print("=" * 60)
        return run_web_app()
    
    elif args.mode == "test":
        print(f"\n启动模式: 数据兼容性测试")
        return test_data_compatibility()
    
    else:
        print_usage()
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)