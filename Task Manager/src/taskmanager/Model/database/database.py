from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import  Session, sessionmaker
from sqlalchemy import URL, create_engine, text, insert
from .config import setting
from .model import metadata_obj, users_table, tasks_table
import asyncio 

engine = create_async_engine(url=setting.DATABASE_URL, echo=True, pool_size=5, max_overflow=1)
Session = sessionmaker(bind=engine)
session = Session()

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)

async def create_user(user):
    async with engine.begin() as conn:

        stmt = insert(users_table).values(
            [
                {"login": user.login},
                {"password": user.password_hash},
            ]
        )
        await conn.execute(stmt)
        await conn.commit()


# async def create_task(user):
#     async with engine.begin() as conn:

#         stmt = insert(tasks_table).values(
#             [
#                 {"title": task.title},
#                 {"description": task.description},
#                 {"start_time": task.start_time},
#                 {"end_time": task.end_time}
#             ]
#         )
#         await conn.execute(stmt)
#         await conn.commit()

async def delete_task(user):
    async with engine.begin() as conn:
        pass
async def patch_task(user):
    async with engine.begin() as conn:
        pass
