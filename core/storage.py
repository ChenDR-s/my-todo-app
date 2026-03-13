"""
数据存储模块
处理任务的持久化存储
"""

import json
import os
from pathlib import Path
from typing import List, Optional
from .models import Task


class TaskStorage:
    """任务数据存储管理"""
    
    def __init__(self, file_path: str = "tasks.json"):
        """
        初始化存储
        
        Args:
            file_path: 数据文件路径
        """
        self.file_path = Path(file_path)
        self._tasks: List[Task] = []
        self._next_id = 1
    
    def load(self) -> List[Task]:
        """
        从文件加载所有任务
        
        Returns:
            任务列表
        """
        if not self.file_path.exists():
            # 文件不存在，创建空列表
            self._tasks = []
            self._next_id = 1
            self._save_to_file()
            return self._tasks
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 转换数据为Task对象
            self._tasks = []
            for item in data:
                try:
                    task = Task.from_dict(item)
                    self._tasks.append(task)
                except (KeyError, ValueError) as e:
                    print(f"警告：跳过无效任务数据: {e}, 数据: {item}")
            
            # 计算下一个可用ID
            if self._tasks:
                self._next_id = max(task.id for task in self._tasks) + 1
            else:
                self._next_id = 1
            
            return self._tasks
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"加载数据失败，创建新文件: {e}")
            self._tasks = []
            self._next_id = 1
            self._save_to_file()
            return self._tasks
    
    def save(self, tasks: List[Task]) -> bool:
        """
        保存任务列表到文件
        
        Args:
            tasks: 要保存的任务列表
            
        Returns:
            是否保存成功
        """
        self._tasks = tasks
        return self._save_to_file()
    
    def _save_to_file(self) -> bool:
        """内部方法：保存到文件"""
        try:
            # 确保目录存在
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 转换为字典列表
            data = [task.to_dict() for task in self._tasks]
            
            # 写入文件
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def get_next_id(self) -> int:
        """
        获取下一个可用的任务ID
        
        Returns:
            下一个ID
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        根据ID获取任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务对象，如果不存在则返回None
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
    
    def add_task(self, content: str, status: str = "todo", 
                 priority: str = "medium", due_date: Optional[str] = None,
                 description: str = "", tags: Optional[List[str]] = None, **kwargs) -> Optional[Task]:
        """
        添加新任务
        
        Args:
            content: 任务内容
            status: 任务状态
            priority: 任务优先级 ("high", "medium", "low")
            due_date: 到期时间字符串 (ISO格式)
            description: 任务详细描述
            tags: 标签列表
            **kwargs: 其他任务属性
            
        Returns:
            新创建的任务，如果失败则返回None
        """
        try:
            task_id = self.get_next_id()
            task = Task(
                id=task_id,
                content=content,
                status=status,
                priority=priority,
                due_date=due_date,
                description=description,
                tags=tags or []
            )
            self._tasks.append(task)
            
            if self._save_to_file():
                return task
            else:
                # 保存失败，回滚ID
                self._next_id -= 1
                if task in self._tasks:
                    self._tasks.remove(task)
                return None
                
        except Exception as e:
            print(f"添加任务失败: {e}")
            return None
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """
        更新任务属性
        
        Args:
            task_id: 任务ID
            **kwargs: 要更新的属性
            
        Returns:
            更新后的任务，如果不存在则返回None
        """
        task = self.get_task(task_id)
        if not task:
            return None
        
        try:
            # 更新属性
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            
            # 自动更新updated_at字段
            from datetime import datetime
            task.updated_at = datetime.now().isoformat()
            
            if self._save_to_file():
                return task
            else:
                return None
                
        except Exception as e:
            print(f"更新任务失败: {e}")
            return None
    
    def delete_task(self, task_id: int) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否删除成功
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        try:
            self._tasks.remove(task)
            return self._save_to_file()
            
        except Exception as e:
            print(f"删除任务失败: {e}")
            return False
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        按状态筛选任务
        
        Args:
            status: 任务状态
            
        Returns:
            符合状态的任务列表
        """
        return [task for task in self._tasks if task.status == status]
    
    def move_task(self, task_id: int, new_status: str) -> Optional[Task]:
        """
        移动任务到新状态
        
        Args:
            task_id: 任务ID
            new_status: 新状态
            
        Returns:
            移动后的任务，如果失败则返回None
        """
        return self.update_task(task_id, status=new_status)
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """
        搜索任务（内容、标签、描述）
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的任务列表
        """
        if not keyword:
            return self._tasks
        
        keyword_lower = keyword.lower()
        results = []
        
        for task in self._tasks:
            # 搜索任务内容
            if keyword_lower in task.content.lower():
                results.append(task)
                continue
            
            # 搜索描述
            if task.description and keyword_lower in task.description.lower():
                results.append(task)
                continue
            
            # 搜索标签
            for tag in task.tags:
                if keyword_lower in tag.lower():
                    results.append(task)
                    break
        
        return results
    
    def filter_tasks_by_priority(self, priority: str) -> List[Task]:
        """
        按优先级筛选任务
        
        Args:
            priority: 优先级 ("high", "medium", "low")
            
        Returns:
            符合优先级的任务列表
        """
        return [task for task in self._tasks if task.priority == priority]
    
    def filter_tasks_by_tag(self, tag: str) -> List[Task]:
        """
        按标签筛选任务
        
        Args:
            tag: 标签名称
            
        Returns:
            包含该标签的任务列表
        """
        return [task for task in self._tasks if tag in task.tags]
    
    def get_tasks_with_due_date(self) -> List[Task]:
        """
        获取有到期时间的任务
        
        Returns:
            有到期时间的任务列表
        """
        return [task for task in self._tasks if task.due_date]
    
    def get_overdue_tasks(self) -> List[Task]:
        """
        获取已过期的任务
        
        Returns:
            已过期的任务列表
        """
        from datetime import datetime
        overdue_tasks = []
        
        for task in self._tasks:
            if task.due_date:
                try:
                    due_date = datetime.fromisoformat(task.due_date)
                    if due_date < datetime.now():
                        overdue_tasks.append(task)
                except ValueError:
                    # 日期格式无效，跳过
                    continue
        
        return overdue_tasks
    
    def get_all_tags(self) -> List[str]:
        """
        获取所有唯一的标签
        
        Returns:
            标签列表
        """
        tags = set()
        for task in self._tasks:
            tags.update(task.tags)
        return sorted(list(tags))
    
    def get_stats(self) -> dict:
        """
        获取任务统计信息
        
        Returns:
            统计信息字典
        """
        stats = {
            "total": len(self._tasks),
            "todo": 0,
            "in_progress": 0,
            "done": 0,
            "high_priority": 0,
            "medium_priority": 0,
            "low_priority": 0,
            "with_due_date": 0,
            "overdue": 0,
            "total_tags": 0,
            "unique_tags": 0
        }
        
        # 状态统计
        for task in self._tasks:
            if task.status == "todo":
                stats["todo"] += 1
            elif task.status == "in_progress":
                stats["in_progress"] += 1
            elif task.status == "done":
                stats["done"] += 1
            
            # 优先级统计
            if task.priority == "high":
                stats["high_priority"] += 1
            elif task.priority == "medium":
                stats["medium_priority"] += 1
            elif task.priority == "low":
                stats["low_priority"] += 1
            
            # 到期时间统计
            if task.due_date:
                stats["with_due_date"] += 1
        
        # 过期任务统计
        stats["overdue"] = len(self.get_overdue_tasks())
        
        # 标签统计
        all_tags = []
        for task in self._tasks:
            all_tags.extend(task.tags)
        stats["total_tags"] = len(all_tags)
        stats["unique_tags"] = len(set(all_tags))
        
        return stats
