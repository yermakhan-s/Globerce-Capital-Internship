import asyncio
import random
import aioredis

import time
from string import ascii_letters

async def main():
    redis = aioredis.from_url("redis://localhost")
    await redis.flushdb()








    

if __name__ == "__main__":
    asyncio.run(main())
