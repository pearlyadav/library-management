from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv('.env')

client = AsyncIOMotorClient(f'mongodb+srv://pearl:{os.environ.get("MONGO_PASS")}@librarymanagement.wvufcww.mongodb.net/?retryWrites=true&w=majority')

library_db = client.library