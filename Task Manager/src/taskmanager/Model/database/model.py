from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
metadata_obj = MetaData()

users_table = Table(
    "users",
    metadata_obj,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("login", String),
    Column("password", Integer, nullable=False)
)


tasks_table = Table(
    "tasks",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", Integer),
    Column("start_time", DateTime ),
    Column("end_time", DateTime ),
)