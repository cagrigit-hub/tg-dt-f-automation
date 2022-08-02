import os
import time
import pymongo

from telethon import TelegramClient
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    Channel,
    ChannelParticipantCreator
)
from telethon.tl.functions.channels import GetParticipantRequest
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

class TeleFlexWorker:
    def __init__(self,session,api_id,api_hash) -> None:
        self.session = session
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(self.session, self.api_id, self.api_hash)
        self.conn = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.conn['tele_flex']
        self.coll = self.db['Telegram_Admins']
        self.err = self.db['Catches']
        self.coll.create_index([("Telegram Address", pymongo.ASCENDING)])



    async def connect(self):
        try:
            await self.client.connect()
        except:
            Exception("Error connecting to Telegram")

    async def disconnect(self):
        try:
            await self.client.disconnect()
        except:
            Exception("Error disconnecting from Telegram")

    async def get_specific_group_admins(self, group):
        try:
            items = []
            channel = await self.client.get_entity(group)
            creator = False
            async for user in self.client.iter_participants(channel, filter=ChannelParticipantsAdmins):
                if not user.bot:
                    if not creator:
                        participant = await self.client(GetParticipantRequest(channel.id, user.id))
                        if (type(participant.participant) == ChannelParticipantCreator):
                            item = {
                                "Group Name": channel.title,
                                "Name": user.first_name,
                                "Lastname": user.last_name,
                                "Telegram Address": "https://web.telegram.org/k/#"
                                + str(user.id),
                                "Username" : user.username,
                                "type": "Creator",
                            }
                            creator = True
                            items.append(item)
                        else:
                            item = {
                                "Group Name": channel.title,
                                "Name": user.first_name,
                                "Lastname": user.last_name,
                                "Telegram Address": "https://web.telegram.org/k/#"
                                + str(user.id),
                                "Username" : user.username,
                                "type": "Admin",
                            }
                            items.append(item)
                    else:
                        item = {
                                "Group Name": channel.title,
                                "Name": user.first_name,
                                "Lastname": user.last_name,
                                "Telegram Address": "https://web.telegram.org/k/#"
                                + str(user.id),
                                "Username" : user.username,
                                "type": "Admin",
                            }
                        items.append(item)
            return [True, items]
        except Exception as e:
            return [False, e.__str__()]


    async def write_group_admins(self, groups):
            await self.connect()
            conversations = defaultdict(list)
            for group in groups:
                info = await self.get_specific_group_admins(group)
                time.sleep(1)
                if info[0]:
                    print("success")
                    for item in info[1]:
                        conversations[item['Group Name']].append(item)
                        
                else:
                    try:
                        print("Admin privilege required.")
                        self.err.insert_one({"Group Name": group, "Error": info[1]})
                    except Exception as e:
                        print(e)
            for conversation in conversations:
                self.coll.insert_one({"Group Name": conversation, "Admins": conversations[conversation]})
            await self.disconnect()

            