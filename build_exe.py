"""
打包脚本 - 将待办事项管理器打包为EXE文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_pyinstaller():
    """检查PyInstaller是否安装"""
    try:
        import PyInstaller
        print("[OK] PyInstaller已安装")
        return True
    except ImportError:
        print("[FAIL] PyInstaller未安装")
        print("请安装: pip install pyinstaller")
        return False


def create_spec_file():
    """创建PyInstaller spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent

# 添加数据文件
datas = [
    (str(project_root / "core"), "core"),
    (str(project_root / "web"), "web"),
    (str(project_root / "resources"), "resources"),
]

# 如果有图标文件，添加图标
icon_path = project_root / "resources" / "icons" / "app.ico"
if icon_path.exists():
    icon = str(icon_path)
else:
    icon = None

# 分析选项
a = Analysis(
    ['desktop/main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PySide6',
        'flask',
        'jinja2',
        'werkzeug',
        'core',
        'core.models',
        'core.storage',
        'core.api_server',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)

# 打包选项
pyz = PYZ(a.pure)

# 可执行文件配置
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TodoManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)

# 收集文件
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TodoManager',
)
'''
    
    spec_file = Path("TodoManager.spec")
    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print(f"[OK] 已创建spec文件: {spec_file}")
    return spec_file


def build_exe():
    """构建EXE文件"""
    print("=" * 60)
    print("开始构建待办事项管理器EXE文件")
    print("=" * 60)
    
    # 检查依赖
    if not check_pyinstaller():
        return False
    
    # 创建spec文件
    spec_file = create_spec_file()
    
    # 运行PyInstaller
    print("\n运行PyInstaller...")
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            str(spec_file)
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        
        if result.returncode == 0:
            print("[SUCCESS] 构建成功！")
            print(f"EXE文件位置: dist/TodoManager/TodoManager.exe")
            
            # 检查文件大小
            exe_path = Path("dist/TodoManager/TodoManager.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"文件大小: {size_mb:.2f} MB")
            
            return True
        else:
            print("[FAIL] 构建失败")
            print("标准输出:")
            print(result.stdout)
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"[FAIL] 构建过程中发生错误: {e}")
        return False


def create_portable_version():
    """创建便携版本（包含所有依赖）"""
    print("\n" + "=" * 60)
    print("创建便携版本")
    print("=" * 60)
    
    # 源目录
    source_dir = Path("dist/TodoManager")
    if not source_dir.exists():
        print("[FAIL] 请先构建EXE文件")
        return False
    
    # 目标目录
    portable_dir = Path("TodoManager_Portable")
    
    # 复制文件
    print(f"复制文件到: {portable_dir}")
    try:
        # 删除旧目录
        if portable_dir.exists():
            shutil.rmtree(portable_dir)
        
        # 复制整个目录
        shutil.copytree(source_dir, portable_dir)
        
        # 创建启动脚本
        launch_script = portable_dir / "启动.bat"
        with open(launch_script, "w", encoding="gbk") as f:
            f.write("@echo off\n")
            f.write("echo 正在启动待办事项管理器...\n")
            f.write("start TodoManager.exe\n")
            f.write("echo 如果无法启动，请确保已安装Microsoft Visual C++ Redistributable\n")
            f.write("pause\n")
        
        print("[OK] 便携版本创建完成")
        print(f"目录: {portable_dir}")
        print("包含文件:")
        for item in portable_dir.iterdir():
            if item.is_file():
                print(f"  - {item.name}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] 创建便携版本失败: {e}")
        return False


def create_installer():
    """创建安装程序（可选）"""
    print("\n" + "=" * 60)
    print("创建安装程序（可选）")
    print("=" * 60)
    print("可以使用以下工具创建安装程序:")
    print("1. Inno Setup (推荐): https://jrsoftware.org/isinfo.php")
    print("2. NSIS: https://nsis.sourceforge.io/")
    print("3. WiX Toolset: https://wixtoolset.org/")
    print()
    print("Inno Setup脚本示例 (TodoManager.iss):")
    print('''[Setup]
AppName=待办事项管理器
AppVersion=1.0.0
DefaultDirName={pf}\\TodoManager
DefaultGroupName=待办事项管理器
UninstallDisplayIcon={app}\\TodoManager.exe
OutputDir=installer
OutputBaseFilename=TodoManager_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\\TodoManager\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\\待办事项管理器"; Filename: "{app}\\TodoManager.exe"
Name: "{group}\\卸载待办事项管理器"; Filename: "{uninstallexe}"
Name: "{commondesktop}\\待办事项管理器"; Filename: "{app}\\TodoManager.exe"

[Run]
Filename: "{app}\\TodoManager.exe"; Description: "启动待办事项管理器"; Flags: nowait postinstall skipifsilent
''')
    print()
    print("将上述内容保存为TodoManager.iss，使用Inno Setup编译")
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("待办事项管理器 - 打包工具")
    print("=" * 60)
    print("选项:")
    print("  1. 构建EXE文件")
    print("  2. 创建便携版本")
    print("  3. 创建安装程序（生成脚本）")
    print("  4. 全部执行")
    print("  0. 退出")
    print()
    
    try:
        choice = input("请选择 (0-4): ").strip()
        
        if choice == "0":
            print("退出")
            return
        
        elif choice == "1":
            build_exe()
        
        elif choice == "2":
            if build_exe():
                create_portable_version()
        
        elif choice == "3":
            create_installer()
        
        elif choice == "4":
            if build_exe():
                create_portable_version()
                create_installer()
        
        else:
            print("无效选择")
            
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()