from botocore.exceptions import ClientError


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
                    {"AttributeName": "Email", "KeyType": "HASH"},
                    {"AttributeName": "Password", "KeyType": "RANGE"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "Email", "AttributeType": "S"},
                    {"AttributeName": "Password", "AttributeType": "S"}
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
            return {'message': 'User signed up successfully!'}
        except Exception as e:
            return {'error': str(e)}

    def login(self, user_data):
        try:
            response = self.table.get_item(
                Key={'Email': user_data['Email'], 'Password': user_data['Password']})
            if 'Item' in response:
                return {'message': 'User logged in successfully!'}
            else:
                return {'error': 'Invalid credentials!'}
        except Exception as e:
            return {'error': str(e)}
        
    def update_profile(self, user_data):
        try:
            response = self.table.update_item(
                Key={'Email': user_data['Email'], 'Password': user_data['Password']},
                UpdateExpression="set FirstName=:f, LastName=:l, ProfilePic=:p",
                ExpressionAttributeValues={
                    ':f': user_data['FirstName'],
                    ':l': user_data['LastName'],
                    ':p': user_data['ProfilePic']
                },
                ReturnValues='UPDATED_NEW')
            
            if "Attributes" in response:
                return {'message': 'Profile updated successfully!'}
            else:
                return {'error': 'Profile not updated!'}
        except Exception as e:
            return {'error': str(e)}
        
    def search_users(self, query, pageNumber):
        try:
            response = self.table.scan(
                FilterExpression="contains(FirstName, :query) or contains(LastName, :query)",
                ExpressionAttributeValues={":query": query}
            )
            users = response.get("Items", [])
            return users
        except Exception as e:
            return {'error': str(e)}
        
    def delete_user(self, user_data):
        try:
            response = self.table.delete_item(
                Key={'Email': user_data['Email'], 'Password': user_data['Password']})
            return {'message': 'User deleted successfully!'}
        except Exception as e:
            return {'error': str(e)}
