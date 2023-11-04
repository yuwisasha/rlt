from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient("localhost", 27017)
db = client.sampleDB
collection = db.sample_collection
