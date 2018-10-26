import os
import aiohttp
import asyncio
import aiofiles
import motor.motor_asyncio

DEFAULT_PATH = '/tmp/images'
DEFAULT_FILENAME = '{name}.jpeg'

MONGO_CONNECTION_URL = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'test'
MONGO_COL_NAME = 'mycollection'


'''
Напишите метод, принимающий на вход два параметра: 
    список URL’ов изображений и строку пути для записи. 
    В данном методе должно производиться ПАРАЛЛЕЛЬНОЕ скачивание этих изображений 
        с последующей записью этих URL’ов в БД MongoDB, 
        а также сохранением скаченных файлов по пути, указанном во втором параметре.
'''


async def process_image_urls(urls_for_fetch, path=DEFAULT_PATH):
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_URL)
    mongo_collection = mongo_client[MONGO_DB_NAME][MONGO_COL_NAME]
    tasks = []

    for i in range(0, len(urls_for_fetch)):
        filepath = os.path.join(path, DEFAULT_FILENAME.format(name=str(i)))
        tasks.append(asyncio.ensure_future(store_image_from_url(urls_for_fetch[i], filepath)))
        await mongo_collection.insert_one({"myId": i, "url": urls_for_fetch[i], "path": filepath})

    await asyncio.gather(*tasks)


async def store_image_from_url(url, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            res = await response.read()

    async with aiofiles.open(path, "wb") as out:
        await out.write(res)
        await out.flush()


if __name__ == '__main__':
    urls = [
        'https://images.pexels.com/photos/219998/pexels-photo-219998.jpeg',
        'https://images.pexels.com/photos/853168/pexels-photo-853168.jpeg',
        'https://images.pexels.com/photos/46710/pexels-photo-46710.jpeg',
        'https://static.toiimg.com/thumb/58475411/Kolkata-in-pictures.jpg?width=748&height=499',
        'https://i.ytimg.com/vi/qh7LLydY8eo/maxresdefault.jpg',
        'https://static.euronews.com/articles/stories/03/21/73/66/880x495_cmsv2_298e3b01-877d-57e3-9ce0-0542084c5af4-3217366.jpg',
        'https://secure.i.telegraph.co.uk/multimedia/archive/03597/POTD_chick_3597497k.jpg',
        'http://images4.fanpop.com/image/photos/19400000/rainbow-sky-beautiful-pictures-19401741-1093-614.jpg',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPADl-Pbn2nK8Tl_zFJvxvEznroQL3UlsJyl-4pCrx5hCbWZy8eA',
        'https://s4.reutersmedia.net/resources/r/?m=02&d=20171018&t=2&i=1206067272&w=&fh=545&fw=810&ll=&pl=&sq=&r=2017-10-18T190508Z_7738_MRPRC14191C48B0_RTRMADP_0_RUSSIA-ANIMALS',
    ]

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(process_image_urls(urls))
    loop.run_until_complete(future)
    loop.close()
