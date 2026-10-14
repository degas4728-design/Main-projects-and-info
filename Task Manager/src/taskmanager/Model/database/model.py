from sqlalchemy import Table, Integer, String, MetaData, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)