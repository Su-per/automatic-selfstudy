from threading import Thread
from config import header, APPLY_URL
import aiohttp
import asyncio
from datetime import datetime
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

    async def request_apply(self, arr):
        pass

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
