import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        
        # ✅ Users और Groups की Collections को सही से Define करें
        self.users = self.db["users"]
        self.groups = self.db["groups"]

    def new_user(self, id, name):
        return {
            "id": id,
            "name": name,
            "ban_status": {
                "is_banned": False,
                "ban_reason": "",
            },
        }

    def new_group(self, id, title):
        return {
            "id": id,
            "title": title,
            "chat_status": {
                "is_disabled": False,
                "reason": "",
            },
        }
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.users.insert_one(user)  # ✅ अब self.users सही से काम करेगा
    
    async def is_user_exist(self, id):
        user = await self.users.find_one({"id": int(id)})  # ✅ अब self.users से Query होगी
        return bool(user)
    
    async def total_users_count(self):
        return await self.users.count_documents({})
    
    async def remove_ban(self, id):
        await self.users.update_one(
            {"id": id}, 
            {"$set": {"ban_status": {"is_banned": False, "ban_reason": ""}}}
        )
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        await self.users.update_one(
            {"id": user_id}, 
            {"$set": {"ban_status": {"is_banned": True, "ban_reason": ban_reason}}}
        )

    async def get_ban_status(self, id):
        user = await self.users.find_one({"id": int(id)})
        if not user:
            return {"is_banned": False, "ban_reason": ""}
        return user.get("ban_status", {"is_banned": False, "ban_reason": ""})

    async def get_all_users(self):
        return self.users.find({})  # ✅ अब self.users से Query होगी

    async def delete_user(self, user_id):
        await self.users.delete_many({"id": int(user_id)})  

    async def get_banned(self):
        users = self.users.find({"ban_status.is_banned": True})  # ✅ अब self.users सही से इस्तेमाल हो रहा है
        chats = self.groups.find({"chat_status.is_disabled": True})
        b_chats = [chat["id"] async for chat in chats]
        b_users = [user["id"] async for user in users]
        return b_users, b_chats

    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.groups.insert_one(chat)  # ✅ अब self.groups सही से इस्तेमाल हो रहा है
    
    async def get_chat(self, chat):
        chat = await self.groups.find_one({"id": int(chat)})  
        return chat.get("chat_status") if chat else False

    async def re_enable_chat(self, id):
        await self.groups.update_one(
            {"id": int(id)}, 
            {"$set": {"chat_status": {"is_disabled": False, "reason": ""}}}
        )
        
    async def total_chat_count(self):
        return await self.groups.count_documents({})
    
    async def get_all_chats(self):
        return self.groups.find({})  

    async def get_db_size(self):
        return (await self.db.command("dbstats"))["dataSize"]

db = Database(DATABASE_URI, DATABASE_NAME)  # ✅ अब सही Database Object बनेगा
