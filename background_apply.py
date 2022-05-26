from threading import Thread
from datetime import datetime
from random import randint
from config import header, SELFSTUDY_APPLY_URL, MASSAGE_APPLY_URL
import aiohttp
import asyncio
import json


class BackgroundApply(Thread):
    db = []
    apply_time = (0, 0)

    def __init__(self, db, apply_time, apply_type):
        self.db = db
        self.apply_time = apply_time
        self.apply_type = apply_type
        super().__init__()

    async def request_apply(self, dict):
        pass
    
    def apply(self):
        if len([i for i in self.db if i["apply_type"] == self.apply_type]) == 0:
            return
        tasks = [
            self.request_apply(i)
            for i in [i for i in self.db if i["apply_type"] == self.apply_type]
        ]
        asyncio.run(asyncio.wait(tasks))

    def run(self):
        while True:
            dt = datetime.now()
            if (dt.hour, dt.minute) == self.apply_time:
                self.apply()
                break
