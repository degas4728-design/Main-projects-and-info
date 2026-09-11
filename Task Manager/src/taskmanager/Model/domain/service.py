# import os
# import sys

# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from taskmanager.Model.database.database import create_tables, insert_data
from pydantic import BaseModel, PositiveInt, ValidationError


class User():
    def __init__(self, login, password):
        self.login = ''
        self.password = 0

class Task():
    def __init__(self, description, title):
        self.description = description
        self.title = title


def get_tasks(self):
    pass

def set_task(self, description, title):
    pass

def change_description(self, description):
    pass

def change_title(self, title):
    pass



async def main():
    await create_tables()
    await insert_data()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())