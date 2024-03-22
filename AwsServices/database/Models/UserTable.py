from botocore.exceptions import ClientError
from chalice import Response


class UserTable:
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
                    {"AttributeName": "Email", "KeyType": "HASH"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "Email", "AttributeType": "S"}
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

    def sign_up(self, user_data):
        try:
            self.table.put_item(Item=user_data)
            return Response(body={'message': 'User signed up successfully!'}, status_code=201)
        except Exception as e:
            return {'error': str(e)}

    def login(self, user_data):
        try:
            response = self.table.get_item(
                Key={'Email': user_data['Email']})
            if 'Item' in response:
                # Compare the password
                if response['Item']['Password'] == user_data['Password']:
                    return Response(body={'user': response['Item'], 'message': 'User logged in successfully!'}, status_code=200)
                else:
                    return Response(body={'error': 'Invalid credentials!'}, status_code=401)
            else:
                return Response(body={'error': 'Invalid credentials!'}, status_code=401)
        except Exception as e:
            return {'error': str(e)}

    def update_profile(self, user_data):
        try:
            response = self.table.update_item(
                Key={'Email': user_data['Email'],
                     'Password': user_data['Password']},
                UpdateExpression="set FirstName=:f, LastName=:l, ProfilePic=:p",
                ExpressionAttributeValues={
                    ':f': user_data['FirstName'],
                    ':l': user_data['LastName'],
                    ':p': user_data['ProfilePic']
                },
                ReturnValues='UPDATED_NEW')

            if "Attributes" in response:
                return Response(body={'message': 'Profile updated successfully!'}, status_code=200)
            else:
                return Response(body={'error': 'Invalid credentials!'}, status_code=401)
        except Exception as e:
            return Response(body={'error': str(e)}, status_code=500)

    def get_user(self, email):
        try:
            response = self.table.get_item(
                Key={'Email': email})
            if 'Item' in response:
                return Response(body={'user': response['Item'], 'message': 'User found!'}, status_code=200)
            else:
                return Response(body={'error': 'User not found!'}, status_code=404)
        except Exception as e:
            print('Error:', e)
            return Response(body={'error': str(e)}, status_code=500)

    def search_users(self, query, pageNumber):
        try:
            response = self.table.scan(
                FilterExpression="contains(FirstName, :query) or contains(LastName, :query)",
                ExpressionAttributeValues={":query": query}
            )
            users = response.get("Items", [])
            return users
        except Exception as e:
            return Response(body={'error': str(e)}, status_code=500)

    def delete_user(self, user_data):
        try:
            response = self.table.delete_item(
                Key={'Email': user_data['Email'], 'Password': user_data['Password']})
            return Response(body={'message': 'User deleted successfully!'}, status_code=200)
        except Exception as e:
            return Response(body={'error': str(e)}, status_code=500)
