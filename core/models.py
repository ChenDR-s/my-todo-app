"""
核心数据模型
定义任务数据结构和相关操作
"""

import json
from datetime import datetime
from typing import Optional, List, Dict, Any


class Task:
    """任务数据类"""
    
    def __init__(self, 
                 id: int, 
                 content: str, 
                 status: str = "todo",
                 created_at: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 priority: str = "medium",
                 due_date: Optional[str] = None,
                 description: str = "",
                 updated_at: Optional[str] = None):
        """
        初始化任务
        
        Args:
            id: 任务ID
            content: 任务内容
            status: 任务状态 ("todo", "in_progress", "done")
            created_at: 创建时间字符串 (ISO格式)
            tags: 标签列表
            priority: 任务优先级 ("high", "medium", "low")
            due_date: 到期时间字符串 (ISO格式)
            description: 任务详细描述
            updated_at: 最后更新时间字符串 (ISO格式)
        """
        self.id = id
        self.content = content
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.tags = tags or []
        self.priority = priority
        self.due_date = due_date
        self.description = description
        self.updated_at = updated_at or datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于JSON序列化）"""
        return {
            "id": self.id,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at,
            "tags": self.tags,
            "priority": self.priority,
            "due_date": self.due_date,
            "description": self.description,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """从字典创建任务实例（兼容旧格式）"""
        # 兼容旧格式：如果没有status字段，设为"todo"
        status = data.get("status", "todo")
        
        # 确保状态是有效值
        if status not in ["todo", "in_progress", "done"]:
            status = "todo"
        
        # 兼容旧格式：如果没有priority字段，设为"medium"
        priority = data.get("priority", "medium")
        if priority not in ["high", "medium", "low"]:
            priority = "medium"
        
        return cls(
            id=data["id"],
            content=data["content"],
            status=status,
            created_at=data.get("created_at"),
            tags=data.get("tags", []),
            priority=priority,
            due_date=data.get("due_date"),
            description=data.get("description", ""),
            updated_at=data.get("updated_at")
        )
    
    def __repr__(self) -> str:
        return f"Task(id={self.id}, content='{self.content}', status='{self.status}', priority='{self.priority}')"
    
    def update_priority(self, new_priority: str) -> bool:
        """更新任务优先级"""
        if new_priority in ["high", "medium", "low"]:
            self.priority = new_priority
            return True
        return False
    
    def set_due_date(self, due_date: str) -> None:
        """设置到期时间"""
        self.due_date = due_date
    
    def is_overdue(self) -> bool:
        """检查任务是否过期"""
        if not self.due_date:
            return False
        
        from datetime import datetime
        try:
            due_date = datetime.fromisoformat(self.due_date)
            return due_date < datetime.now()
        except ValueError:
            return False
    
    def get_formatted_created_at(self) -> str:
        """获取格式化的创建时间"""
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(self.created_at)
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return self.created_at
    
    def get_formatted_updated_at(self) -> str:
        """获取格式化的更新时间"""
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(self.updated_at)
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return self.updated_at
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id and self.content == other.content
    
    def move_to_status(self, new_status: str) -> bool:
        """移动任务到新状态"""
        if new_status in ["todo", "in_progress", "done"]:
            self.status = new_status
            return True
        return False
    
    def add_tag(self, tag: str) -> None:
        """添加标签"""
        if tag and tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> bool:
        """移除标签"""
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False


class TaskStatus:
    """任务状态常量"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    
    @classmethod
    def all_statuses(cls) -> List[str]:
        """获取所有状态"""
        return [cls.TODO, cls.IN_PROGRESS, cls.DONE]
    
    @classmethod
    def get_display_name(cls, status: str) -> str:
        """获取状态的显示名称"""
        names = {
            cls.TODO: "待办事项",
            cls.IN_PROGRESS: "进行中",
            cls.DONE: "已完成"
        }
        return names.get(status, status)


class TaskPriority:
    """任务优先级常量"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
    @classmethod
    def all_priorities(cls) -> List[str]:
        """获取所有优先级"""
        return [cls.HIGH, cls.MEDIUM, cls.LOW]
    
    @classmethod
    def get_display_name(cls, priority: str) -> str:
        """获取优先级的显示名称"""
        names = {
            cls.HIGH: "高",
            cls.MEDIUM: "中",
            cls.LOW: "低"
        }
        return names.get(priority, priority)
    
    @classmethod
    def get_color(cls, priority: str) -> str:
        """获取优先级的颜色"""
        colors = {
            cls.HIGH: "#f44336",    # 红色
            cls.MEDIUM: "#ff9800",   # 橙色
            cls.LOW: "#4caf50"       # 绿色
        }
        return colors.get(priority, "#9e9e9e")
