from sqlalchemy import Table, Column, Integer, String, MetaData

metadata_obj = MetaData()

users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("login", String),
    Column("password", Integer)
)


tasks_table = Table(
    "tasks",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", Integer)
)