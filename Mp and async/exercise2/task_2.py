import asyncio
import aiohttp
from prettytable import PrettyTable
import os
import random


async def check_way():
    status_storage = 0
    while True:
            storage_way = input('Введите куда сохранить результат запросов:')
            if  os.path.exists(storage_way):
                if os.path.isdir(storage_way):
                    if os.access(storage_way, os.W_OK) :
                        status_storage = 'd'
                        break
                    else:
                        print('Нет доступа к объекту, лежащему по заданному пути')
                if os.path.isfile(storage_way):
                    if os.access(storage_way, os.W_OK) :
                        status_storage = 'f'
                        break
                    else:
                        print('Нет доступа к объекту, лежащему по заданному пути')
                else:
                    print('Объект, лежащий по заданному пути, не является ни папкой, ни файлом')
            else:
                print("Задан неверный путь")
    return storage_way, status_storage



async def load_file(session, link, storage_way,status_storage ):
    if status_storage == 'f':    
        async with session.get(link) as resp:
            with open(storage_way, 'wb') as file:
                file.write(await resp.read())

    elif status_storage == 'd':
        random_name = ''
        random_prefix = 0
        while True:
            random_prefix = random.randint(1,1000)
            random_name = f'img{random_prefix}'
            if os.path.exists(storage_way + f'{random_name}') != True:
                break


        async with session.get(link) as resp:
            file_type = resp.headers.get('Content-Type', '')
            part_of_way = ''
            if 'jpeg' in file_type or 'jpg' in file_type:
                part_of_way = '.jpg'
            elif 'png' in file_type:
                part_of_way = '.png'
            elif 'gif' in file_type:
                part_of_way = '.gif'
            elif 'webp' in file_type:
                part_of_way = '.webp'
            elif 'bmp' in file_type:
                part_of_way = '.bmp'
            elif 'svg' in file_type:
                part_of_way = '.svg'
            else:
                part_of_way = '.bin' 
            random_name = random_name + part_of_way
            with open(os.path.join(storage_way,random_name), 'wb') as file:
                file.write(await resp.read())

async def main():
    status_requests, list_status, list_storage, tasks  = [], [], [], []
    status_storage = 0
    link = ''
    main_table = PrettyTable()
    

    storage_way, status_storage = await check_way()
    async with aiohttp.ClientSession() as session:
        while True:
            link = input("Введите ссылку:")
            if link == '': break
                
            async with session.get(link) as resp:
                if resp.status != 200:
                    list_status.append([link, 'Ошибка'])
                else:
                    list_status.append([link, 'Успех'])  
                    task = asyncio.create_task(load_file(session, link, storage_way,status_storage))   
                    tasks.append(task)
        if tasks:
            await asyncio.gather(*tasks)            

    main_table.field_names = ['Ссылка', 'Статус']
    for i in list_status: main_table.add_row([i[0],i[1]])

    print(main_table)




if __name__ == "__main__":
    asyncio.run(main())


