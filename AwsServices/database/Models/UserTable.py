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
                    {"AttributeName": "UserId", "KeyType": "HASH"},  # Partition key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "UserId", "AttributeType": "N"},
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
                return None
            else:
                # Unexpected error, re-raise
                raise
        else:
            return self.table
        
    def sign_up(self, user_data):
        try:
            print("Checkinh: ",user_data)
            self.table.put_user(Item=user_data)
            return {'message': 'User signed up successfully!'}
        except Exception as e:
            return {'error': str(e)}
    
    def login(self, user_data):
        try:
            response = self.table.get_item(Key={'UserId': user_data['UserId']})
            if 'Item' in response:
                return {'message': 'User logged in successfully!'}
            else:
                return {'error': 'Invalid credentials!'}
        except Exception as e:
            return {'error': str(e)}