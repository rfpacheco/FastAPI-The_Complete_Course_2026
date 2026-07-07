from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Index, Text


class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(255), nullable=False, unique=True)
    username: str = Column(String(255), nullable=False, unique=True)
    first_name: str = Column(String(255), nullable=False)
    last_name: str = Column(String(255), nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    is_active: bool = Column(Boolean, default=True)
    role: str = Column(String(50), default="user", nullable=False)
    phone_number: str = Column(String, nullable=True)

    __table_args__ = (
        Index("idx_users_email", "email"),
        Index("idx_users_username", "username"),
    )


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, default=1, nullable=False)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        Index("idx_todos_owner_id", "owner_id"),
    )