from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
from chalice import Response


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
                    {"AttributeName": "CommunityId",
                        "KeyType": "HASH"},  # Partition key
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
        response = self.table.put_item(Item=community)
        return Response(body=response, status_code=201)

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

        return Response(body=communities, status_code=200)

    def get_community_by_id(self, community_id):
        """
        Retrieves community details when the community_id is present in the table.

        :param community_id: The ID of the community.
        :return: The community details.
        """
        response = self.table.get_item(Key={"CommunityId": community_id})
        community = response.get("Item", {})

        return Response(body=community, status_code=200)

    def search_community(self, query):
        """
        Retrieves community details when the query is present in the table.

        :param query: The query to search for.
        :return: The community details.
        """
        response = self.table.scan(
            FilterExpression=Attr("CommunityName").contains(query)
        )
        communities = response.get("Items", [])

        return Response(body=communities, status_code=200)

    def join_community(self, data):
        """
        Adds a user to a community.

        :param data: A dictionary with the user and community details.
        :return: The response from the update_item call.
        """
        response = self.table.update_item(
            Key={"CommunityId": data["CommunityId"]},
            UpdateExpression="SET GroupMembers = list_append(GroupMembers, :user)",
            ExpressionAttributeValues={":user": [data["Username"]]},
            ReturnValues="UPDATED_NEW",
        )

        return Response(body=response, status_code=200)

    def leave_community(self, data):
        """
        Removes a user from a community.

        :param data: A dictionary with the user and community details.
        :return: The response from the update_item call.
        """
        # First, retrieve the index of the username in the GroupMembers list
        community = self.table.get_item(
            Key={"CommunityId": data["CommunityId"]})
        group_members = community.get("Item", {}).get("GroupMembers", [])

        try:
            index = group_members.index(data["Username"])
        except ValueError:
            print("User not found in the community")
            return Response(body={"message": "User not found in the community"}, status_code=404)

        # Now, remove the user from the GroupMembers list using the retrieved index
        response = self.table.update_item(
            Key={"CommunityId": data["CommunityId"]},
            UpdateExpression="REMOVE GroupMembers[%s]" % index,
            ReturnValues="UPDATED_NEW",
        )

        return Response(body=response, status_code=200)
    
    def delete_community(self, data):
        """
        Deletes a community.

        :param data: A dictionary with the community details.
        :return: The response from the delete_item call.
        """
        try:
            response = self.table.delete_item(Key={"CommunityId": data["CommunityId"]})

            if "Attributes" in response:
                    return Response(body={'message': 'Profile updated successfully!'}, status_code=200)
            else:
                    return Response(body={'error': 'Invalid credentials!'}, status_code=401)
        
        except Exception as e:
            return Response(body={'error': str(e)}, status_code=500)
    
