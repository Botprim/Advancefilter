import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]

        # ✅ Users और Groups की Collections Define करें
        self.users_collection = self.db["users"]
        self.chats_collection = self.db["groups"]

    def new_user(self, user_id, name):
        return {
            "id": user_id,
            "name": name,
            "ban_status": {
                "is_banned": False,
                "ban_reason": ""
            }
        }

    def new_group(self, chat_id, title):
        return {
            "id": chat_id,
            "title": title,
            "chat_status": {
                "is_disabled": False,
                "reason": ""
            }
        }

    async def add_user(self, user_id, name):
        user = self.new_user(user_id, name)
        await self.users_collection.insert_one(user)

    async def is_user_exist(self, user_id):
        user = await self.users_collection.find_one({"id": int(user_id)})
        return bool(user)

    async def total_users_count(self):
        return await self.users_collection.count_documents({})

    async def remove_ban(self, user_id):
        await self.users_collection.update_one(
            {"id": int(user_id)},
            {"$set": {"ban_status": {"is_banned": False, "ban_reason": ""}}}
        )

    async def ban_user(self, user_id, reason="No Reason"):
        await self.users_collection.update_one(
            {"id": int(user_id)},
            {"$set": {"ban_status": {"is_banned": True, "ban_reason": reason}}}
        )

    async def get_ban_status(self, user_id):
        user = await self.users_collection.find_one({"id": int(user_id)})
        if not user:
            return {"is_banned": False, "ban_reason": ""}
        return user.get("ban_status", {"is_banned": False, "ban_reason": ""})

    async def get_all_users(self):
        return self.users_collection.find({})

    async def delete_user(self, user_id):
        await self.users_collection.delete_many({"id": int(user_id)})

    async def get_banned(self):
        users = self.users_collection.find({"ban_status.is_banned": True})
        chats = self.chats_collection.find({"chat_status.is_disabled": True})
        banned_users = [user["id"] async for user in users]
        banned_chats = [chat["id"] async for chat in chats]
        return banned_users, banned_chats

    async def add_chat(self, chat_id, title):
        chat = self.new_group(chat_id, title)
        await self.chats_collection.insert_one(chat)

    async def get_chat(self, chat_id):
        chat = await self.chats_collection.find_one({"id": int(chat_id)})
        return False if not chat else chat.get("chat_status")

    async def re_enable_chat(self, chat_id):
        await self.chats_collection.update_one(
            {"id": int(chat_id)},
            {"$set": {"chat_status": {"is_disabled": False, "reason": ""}}}
        )

    async def disable_chat(self, chat_id, reason="No Reason"):
        await self.chats_collection.update_one(
            {"id": int(chat_id)},
            {"$set": {"chat_status": {"is_disabled": True, "reason": reason}}}
        )

    async def total_chat_count(self):
        return await self.chats_collection.count_documents({})

    async def get_all_chats(self):
        return self.chats_collection.find({})

    async def get_db_size(self):
        stats = await self.db.command("dbstats")
        return stats["dataSize"]

# ✅ Database Object बनाएं, जिससे हम इसे `bot.py` में Import कर सकें
db = Database(DATABASE_URI, DATABASE_NAME)
