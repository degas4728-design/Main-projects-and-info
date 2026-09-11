from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import  Session, sessionmaker
from sqlalchemy import URL, create_engine, text, insert
from .config import setting
from .model import metadata_obj, users_table
import asyncio 

engine = create_async_engine(url=setting.DATABASE_URL, echo=True, pool_size=5, max_overflow=1)
Session = sessionmaker(bind=engine)
session = Session()



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)
        await conn.run_sync(metadata_obj.create_all)

async def insert_data():
    async with engine.begin() as conn:
        # stmt = """ insert into test(id, login) VALUES ( 1,ARRAY['n']), ( 2,ARRAY['a']); """

        # stmt = insert(users_table).values(
        #     [
        #         {"login": "user1"},
        #         {"login": "user2"},
        #     ]
        # )
        # await conn.execute(stmt)
        # await conn.commit()

# async def get_engine():
#     async with engine.connect() as conn:
#         res = await conn.execute(text("SELECT VERSION()"))
#         print(f"{res.first()=}")

# asyncio.run(get_engine())