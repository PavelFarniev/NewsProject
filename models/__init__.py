"""Классы предметной области: автор, новость, комментарий."""

from .authors import Author
from .comments import Comment
from .news import News

__all__ = ["Author", "News", "Comment"]
