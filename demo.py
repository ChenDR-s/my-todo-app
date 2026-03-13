#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
待办事项管理器演示
展示程序的主要功能
"""

import json
import os

def demonstrate_features():
    """演示程序功能"""
    print("待办事项管理器功能演示")
    print("="*60)
    
    # 1. 展示文件结构
    print("1. 项目文件结构:")
    print("   - main.py: 主程序文件")
    print("   - tasks.json: 任务数据文件（程序运行时自动创建）")
    print("   - README.md: 使用说明文档")
    
    # 2. 展示主菜单
    print("\n2. 主菜单界面:")
    print("   " + "="*40)
    print("   待办事项管理器")
    print("   " + "="*40)
    print("   1. 添加任务")
    print("   2. 查看任务")
    print("   3. 删除任务")
    print("   4. 退出程序")
    print("   " + "="*40)
    
    # 3. 展示数据文件格式
    print("\n3. 数据存储格式 (tasks.json):")
    sample_tasks = [
        {"id": 1, "content": "学习Python编程"},
        {"id": 2, "content": "完成项目作业"}
    ]
    print(json.dumps(sample_tasks, ensure_ascii=False, indent=2))
    
    # 4. 展示功能流程
    print("\n4. 使用流程:")
    print("   a. 运行程序: python main.py")
    print("   b. 选择1添加任务，输入任务内容")
    print("   c. 选择2查看所有任务")
    print("   d. 选择3删除指定编号的任务")
    print("   e. 选择4退出程序")
    
    # 5. 检查当前状态
    print("\n5. 当前项目状态:")
    if os.path.exists("main.py"):
        print("   ✓ main.py 文件存在")
    else:
        print("   ✗ main.py 文件不存在")
    
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)
            print(f"   ✓ tasks.json 文件存在，包含 {len(tasks)} 个任务")
        except:
            print("   ✓ tasks.json 文件存在（可能为空或格式错误）")
    else:
        print("   ℹ tasks.json 文件不存在（程序首次运行时会自动创建）")
    
    if os.path.exists("README.md"):
        print("   ✓ README.md 文件存在")
    else:
        print("   ✗ README.md 文件不存在")
    
    print("\n" + "="*60)
    print("演示完成！")
    print("要使用程序，请运行: python main.py")

if __name__ == "__main__":
    demonstrate_features()