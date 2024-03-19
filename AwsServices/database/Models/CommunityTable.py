from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

class CommunityTable:
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
                    {"AttributeName": "CommunityId", "KeyType": "HASH"},  # Partition key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "CommunityId", "AttributeType": "N"},
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
        
    def put_community(self, community):
        """
        Adds a new community to the table.
        
        :param community: A dictionary with the community data.
        :return: The response from the put_item call.
        """
        print(community)
        response = self.table.put_item(Item=community)
        return response
    
    def get_community(self, username):
        """
        Retrieves community details when the username is present in the GroupMembers list.

        :param username: The username of the user.
        :return: A list of community details where the user is a member.
        """
        response = self.table.scan(
            FilterExpression=Attr("GroupMembers").contains(username)
        )
        communities = response.get("Items", [])
        return communities
    
    def join_community(self, data):
        """
        Adds a user to a community.

        :param data: A dictionary with the user and community details.
        :return: The response from the update_item call.
        """
        response = self.table.update_item(
            Key={"CommunityId": data["community_id"]},
            UpdateExpression="SET GroupMembers = list_append(GroupMembers, :user)",
            ExpressionAttributeValues={":user": [data["user_name"]]},
            ReturnValues="UPDATED_NEW",
        )
        return response

