from database.Models.UserTable import UserTable
from database.Models.CommunityTable import CommunityTable
from database.Models.ChatsTable import ChatsTable

class DynamoDB:
    def __init__(self, resource):
        self.dynamo_resource = resource

        self.user_table = UserTable(self.dynamo_resource)
        self.user_created_table = self.user_table.create_table('Users')
        self.print_table_creation_status('Users', self.user_created_table)

        self.community_table = CommunityTable(self.dynamo_resource)
        self.community_created_table = self.community_table.create_table('Communities')
        self.print_table_creation_status('Communities', self.community_created_table)

        self.chats_table = ChatsTable(self.dynamo_resource)
        self.chat_index = self.chats_table.create_table('Chats')
        self.print_table_creation_status('Chats', self.chat_index)


    def print_table_creation_status(self, table_name, created_table):
        if created_table is not None:
            print(f"Table {table_name} was created successfully!")
        else:
            print(f"Table {table_name} already exists.")
