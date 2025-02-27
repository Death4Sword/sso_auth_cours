import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class DynamoDBHelper():

        
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    ACCESS_SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')

    dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    region_name='eu-west-3'
    )

    table_name = "Users"

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'  #Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Creating table {table_name} ...")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} created successfully!")
    except Exception as e:
        table = dynamodb.Table(table_name)
        table.load()
        print(f"Table {table_name} already exists!")
        print(f"Exception: {e}")
        print("Continuing with existing table...")



    user_data = {
    "email": "johndoe@gmail.com",
    "password": "password123"
    }

    table.put_item(Item=user_data)

    print("User inserted successfully!")

    def get_user(self, email):
        response = self.table.get_item(Key={"email": email})
        item = response.get("Item")
        return item
    
    def insert_user(self, user_data):
        self.table.put_item(Item=user_data)
        print("User inserted successfully!")
        return True
    
    
    def delete_user(self, email):
        self.table.delete_item(Key={"email": email})
        print("User deleted successfully!")
        return True


