import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users_collection = self.db["users"]  # ✅ Users Collection
        self.chats_collection = self.db["groups"]  # ✅ Groups Collection

    def new_user(self, user_id, name):
        return {
            "id": user_id,
            "name": name,
            "ban_status": {"is_banned": False, "ban_reason": ""}
        }

    def new_group(self, chat_id, title):
        return {
            "id": chat_id,
            "title": title,
            "chat_status": {"is_disabled": False, "reason": ""}
        }

    async def add_user(self, user_id, name):
        user = self.new_user(user_id, name)
        await self.users_collection.insert_one(user)  # ✅ Fix: Use `users_collection`

    async def is_user_exist(self, user_id):
        user = await self.users_collection.find_one({"id": int(user_id)})  # ✅ Fix
        return bool(user)

    async def add_chat(self, chat_id, title):
        chat = self.new_group(chat_id, title)
        await self.chats_collection.insert_one(chat)  # ✅ Fix: Use `chats_collection`

    async def get_chat(self, chat_id):
        chat = await self.chats_collection.find_one({"id": int(chat_id)})  # ✅ Fix
        return chat.get("chat_status") if chat else None

# ✅ Correct Database Object Initialization
db = Database(DATABASE_URI, DATABASE_NAME)
users_collection = db.users_collection  # ✅ Fix: Now it exists
chats_collection = db.chats_collection  # ✅ Fix: Now it exists
