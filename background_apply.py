from threading import Thread
from datetime import datetime
from config import header, APPLY_URL
import aiohttp
import asyncio
import json


class BackgroundApply(Thread):
    db: list
    apply_time: tuple
    apply_type: str

    def __init__(self, db, apply_time, apply_type):
        self.db = db
        self.apply_time = apply_time
        self.apply_type = apply_type
        super().__init__()

    async def request_apply(self, dict):
        url = APPLY_URL[self.apply_type]
        header["authorization"] = dict["access_token"]

        for _ in range(10):
            async with aiohttp.ClientSession() as session:
                async with session.put(url=url, headers=header) as response:
                    res = json.loads(await response.text())
                    if "success" in res:
                        print(f"{dict['email']} 성공")
                        return
        print(f"{dict['email']} 실패", res["timeStamp"])

    def apply(self):
        apply_db = [i for i in self.db if i["apply_type"] == self.apply_type]
        if len(apply_db) == 0:
            return
        tasks = [self.request_apply(i) for i in apply_db]
        asyncio.run(asyncio.wait(tasks))

    def run(self):
        while True:
            dt = datetime.now()
            if (dt.hour, dt.minute) == self.apply_time:
                self.apply()
                break
