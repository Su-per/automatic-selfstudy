from threading import Thread
from datetime import datetime
from random import randint
from config import header, APPLY_URL
import aiohttp
import asyncio
import json


class BackgroundApply(Thread):
    db = []
    hour = 0
    minute = 0

    def __init__(self, db, hour, minute):
        self.db = db
        self.hour = hour
        self.minute = minute
        super().__init__()

    async def request_apply(self, dict):
        await asyncio.sleep(0.1 * randint(1, 10))
        for _ in range(10):
            async with aiohttp.ClientSession() as session:
                header["authorization"] = dict["access_token"]
                async with session.put(APPLY_URL, headers=header) as response:
                    res = json.loads(await response.text())
                    if "success" in res:
                        print(f"{dict['email']} 성공")
                        return
        print(f"{dict['email']} 실패")

    def apply(self):
        if len(self.db) == 0:
            return
        tasks = [self.request_apply(i) for i in self.db]
        asyncio.run(asyncio.wait(tasks))

    def run(self):
        while True:
            dt = datetime.now()
            if dt.hour == self.hour and dt.minute == self.minute:
                self.apply()
                break
