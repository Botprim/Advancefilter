import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users_collection = self.db["users"]  # ✅ Users Collection
        self.chats_collection = self.db["groups"]  # ✅ Groups Collection

# ✅ सही Database ऑब्जेक्ट बनाएं और Collection एक्सेस करें
db = Database(DATABASE_URI, DATABASE_NAME)
users_collection = db.users_collection  # ✅ Fix: `col` की जगह `users_collection`
chats_collection = db.chats_collection  # ✅ Fix: `col` की जगह `chats_collection`
