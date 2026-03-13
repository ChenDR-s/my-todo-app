#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的待办事项管理器
功能：
1. 添加任务
2. 查看任务
3. 删除任务
4. 退出程序
"""

import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    """从文件加载任务列表"""
    if not os.path.exists(TASKS_FILE):
        # 如果文件不存在，创建空列表并保存
        tasks = []
        save_tasks(tasks)
        return tasks
    
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        return tasks
    except (json.JSONDecodeError, FileNotFoundError):
        # 如果文件损坏或读取失败，返回空列表
        return []

def save_tasks(tasks):
    """保存任务列表到文件"""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(tasks):
    """添加新任务"""
    print("\n" + "="*40)
    print("添加新任务")
    print("="*40)
    
    task_content = input("请输入任务内容: ").strip()
    
    if not task_content:
        print("错误：任务内容不能为空！")
        return tasks
    
    # 创建新任务
    new_task = {
        "id": len(tasks) + 1,
        "content": task_content
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✓ 任务已添加 (ID: {new_task['id']})")
    return tasks

def view_tasks(tasks):
    """查看所有任务"""
    print("\n" + "="*40)
    print("任务列表")
    print("="*40)
    
    if not tasks:
        print("暂无任务")
        print("="*40)
        return
    
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['content']}")
    
    print("="*40)
    print(f"总计: {len(tasks)} 个任务")

def delete_task(tasks):
    """删除任务"""
    print("\n" + "="*40)
    print("删除任务")
    print("="*40)
    
    if not tasks:
        print("暂无任务可删除")
        return tasks
    
    view_tasks(tasks)
    
    try:
        task_num = int(input("\n请输入要删除的任务编号: "))
        
        if 1 <= task_num <= len(tasks):
            deleted_task = tasks.pop(task_num - 1)
            
            # 更新剩余任务的ID
            for i, task in enumerate(tasks, 1):
                task['id'] = i
            
            save_tasks(tasks)
            print(f"✓ 任务已删除: {deleted_task['content']}")
        else:
            print(f"错误：编号 {task_num} 无效，请输入 1-{len(tasks)} 之间的数字")
    except ValueError:
        print("错误：请输入有效的数字")
    
    return tasks

def display_menu():
    """显示主菜单"""
    print("\n" + "="*40)
    print("待办事项管理器")
    print("="*40)
    print("1. 添加任务")
    print("2. 查看任务")
    print("3. 删除任务")
    print("4. 退出程序")
    print("="*40)

def main():
    """主函数"""
    print("欢迎使用待办事项管理器！")
    
    # 加载现有任务
    tasks = load_tasks()
    
    while True:
        display_menu()
        
        try:
            choice = input("\n请选择操作 (1-4): ").strip()
            
            if choice == '1':
                tasks = add_task(tasks)
            elif choice == '2':
                view_tasks(tasks)
            elif choice == '3':
                tasks = delete_task(tasks)
            elif choice == '4':
                print("\n感谢使用，再见！")
                break
            else:
                print("错误：请输入 1-4 之间的数字")
        except KeyboardInterrupt:
            print("\n\n程序被中断，正在退出...")
            break
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()