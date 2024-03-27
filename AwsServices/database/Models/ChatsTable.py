from botocore.exceptions import ClientError
from chalice import Response


class ChatsTable:
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists. Otherwise, it is set by 'create_table'.
        self.table = None

    def create_table(self, table_name):
        """
        Creates an Amazon DynamoDB table that can be used to store movie data.
        The table uses the release year of the movie as the partition key and the
        title as the sort key.

        :param table_name: The name of the table to create.
        :return: The newly created table if successful, None if the table already exists.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "ChatId", "KeyType": "HASH"},  # Partition key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "ChatId", "AttributeType": "N"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                },
            )
            self.table.wait_until_exists()
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                # Table already exists, return None
                self.table = self.dyn_resource.Table(table_name)
                return None
            else:
                # Unexpected error, re-raise
                raise
        else:
            return self.table

    def put_chat(self, chat):
        """
        Adds a new chat to the table.

        :param chat: A dictionary with the chat data.
        :return: The response from the put_item call.
        """
        response = self.table.put_item(Item=chat)
        return response

    def get_chats(self, communityId):
        """
        Gets all chats for a given community.

        :param communityId: The ID of the community to get chats for.
        :return: The response from the query call.
        """
        # Get all chats, then filter by communityId and sort by Time
        response = self.table.scan()
        chats = response['Items']
        chats = [chat for chat in chats if chat['CommunityId'] == communityId]
        chats.sort(key=lambda chat: chat['Time'])
        return Response(body=chats, status_code=200)
