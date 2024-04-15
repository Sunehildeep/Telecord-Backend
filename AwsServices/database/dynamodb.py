from database.Models.UserTable import UserTable
from database.Models.CommunityTable import CommunityTable
from database.Models.ChatsTable import ChatsTable
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


class DynamoDB:
    def __init__(self):
        self.dynamo_resource = boto3.resource('dynamodb', aws_access_key_id=aws_access_key,
                                              aws_secret_access_key=aws_secret_access_key)

        self.user_table = UserTable(self.dynamo_resource)
        self.user_created_table = self.user_table.create_table('Users')
        self.print_table_creation_status('Users', self.user_created_table)

        self.community_table = CommunityTable(self.dynamo_resource)
        self.community_created_table = self.community_table.create_table(
            'Communities')
        self.print_table_creation_status(
            'Communities', self.community_created_table)

        self.chats_table = ChatsTable(self.dynamo_resource)
        self.chat_index = self.chats_table.create_table('Chats')
        self.print_table_creation_status('Chats', self.chat_index)

    def print_table_creation_status(self, table_name, created_table):
        if created_table is not None:
            print(f"Table {table_name} was created successfully!")
        else:
            print(f"Table {table_name} already exists.")

    def putCommunity(self, community):
        return self.community_table.put_community(community)

    def getCommunity(self, user_name):
        return self.community_table.get_community(user_name)

    def getCommunityById(self, community_id):
        return self.community_table.get_community_by_id(community_id)

    def update_profile(self, user_data):
        return self.user_table.update_profile(user_data)

    def search_users(self, query, pageNumber):
        return self.user_table.search_users(query, pageNumber)

    def get_user(self, email):
        return self.user_table.get_user(email)

    def delete_user(self, user_data):
        return self.user_table.delete_user(user_data)

    def signUp(self, user_data):
        return self.user_table.sign_up(user_data)

    def login(self, user_data):
        return self.user_table.login(user_data)

    def join_community(self, data):
        return self.community_table.join_community(data)

    def leave_community(self, data):
        return self.community_table.leave_community(data)

    def searchCommunity(self, query):
        return self.community_table.search_community(query)

    def saveChat(self, msg):
        return self.chats_table.put_chat(msg)

    def getChats(self, communityId):
        return self.chats_table.get_chats(communityId)

    def deleteCommunity(self, data):
        return self.community_table.delete_community(data)

    def update_username(self, data):
        return self.user_table.update_username(data)

    def update_profile_picture(self, data):
        return self.user_table.update_profile_picture(data)

    def update_community_image(self, data):
        return self.community_table.update_community_image(data)
