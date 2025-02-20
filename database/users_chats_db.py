import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users_collection = self.db["users"]  # ✅ Fixed Collection Name
        self.chats_collection = self.db["groups"]  # ✅ Fixed Collection Name

    async def add_user(self, user_id, name):
        user_data = {"id": user_id, "name": name, "ban_status": {"is_banned": False, "reason": ""}}
        await self.users_collection.insert_one(user_data)

    async def is_user_exist(self, user_id):
        user = await self.users_collection.find_one({"id": user_id})
        return bool(user)

    async def add_chat(self, chat_id, title):
        chat_data = {"id": chat_id, "title": title, "chat_status": {"is_disabled": False, "reason": ""}}
        await self.chats_collection.insert_one(chat_data)

    async def is_chat_exist(self, chat_id):
        chat = await self.chats_collection.find_one({"id": chat_id})
        return bool(chat)

# ✅ Database Instance
db = Database(DATABASE_URI, DATABASE_NAME)
users_collection = db.users_collection  # ✅ Fix: Correctly Assign Users Collection
chats_collection = db.chats_collection  # ✅ Fix: Correctly Assign Chats Collection
