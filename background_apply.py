from threading import Thread
from datetime import datetime
from random import randint
from config import header, SELFSTUDY_APPLY_URL, MASSAGE_APPLY_URL
import aiohttp
import asyncio
import json


class BackgroundApply(Thread):
    db = []
    selfstudy_time = (0, 0)
    massage_time = (0, 0)

    def __init__(self, db, selfstudy_time, massage_time):
        self.db = db
        self.selfstudy_time = selfstudy_time
        self.massage_time = massage_time
        super().__init__()

    async def request_apply(self, dict, apply_type):
        await asyncio.sleep(0.1 * randint(1, 10))

        if apply_type == "selfstudy":
            url = SELFSTUDY_APPLY_URL
        elif apply_type == "massage":
            url = MASSAGE_APPLY_URL

        for _ in range(10):
            async with aiohttp.ClientSession() as session:
                header["authorization"] = dict["access_token"]
                async with session.put(url=url, headers=header) as response:
                    res = json.loads(await response.text())
                    if "success" in res:
                        print(f"{dict['email']} 성공")
                        return
        print(f"{dict['email']} 실패")
        print(res)

    def apply(self, apply_type):
        if len([i for i in self.db if i["apply_type"] == apply_type]) == 0:
            return
        tasks = [
            self.request_apply(i, apply_type)
            for i in [i for i in self.db if i["apply_type"] == apply_type]
        ]
        asyncio.run(asyncio.wait(tasks))

    def run(self):
        do_selfstudy, do_massage = False, False
        while True:
            dt = datetime.now()
            if (dt.hour, dt.minute) == self.selfstudy_time and do_selfstudy == False:
                self.apply(apply_type="selfstudy")
                do_selfstudy = True
            elif (dt.hour, dt.minute) == self.massage_time and do_massage == False:
                self.apply(apply_type="massage")
                do_massage = True
