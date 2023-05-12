'''
Python client-side logical representation of an Azure Cosmos DB SQL API.
'''

import json
from typing import Iterable, Union
from azure.cosmos import exceptions, CosmosClient, PartitionKey, DatabaseProxy, ContainerProxy
import config

# The name of our database.
DATABASE_ID = "DB"
# The name of our container.
CONTAINER_ID = "Collection"
# The partition key of your containers
PARTITION_KEY = "id"
# TEMP
MAX_ITEM_COUNT = 20

class CosmosSQL():
    '''Class to interact with Cosmos DB'''
    def __init__(self) -> None:
        '''Creates a cosmos client instance'''
        self.client = CosmosClient(config.ENDPOINT, config.KEY)

    def create_item(self, body: dict):
        '''Insert or update the specified item.'''

        container = self.get_container_client(DATABASE_ID, CONTAINER_ID)

        try:
            item = container.upsert_item(body)
        except exceptions.CosmosHttpResponseError:
            print('Error inserting TODO item.')
            return None
        return item

    def read_item_by_partition_key(self, partition_key: str, appointment_id: str) -> Iterable[dict]:
        '''Get the item identified by the provided doc_id.'''

        container = self.get_container_client(DATABASE_ID, CONTAINER_ID)

        try:
            query = f"SELECT * FROM c  WHERE c.partition_key ='{partition_key}' and c.appointment_id='{appointment_id}'"
            item = container.query_items(
                query=query, enable_cross_partition_query=False
            )
        except exceptions.CosmosHttpResponseError:
            print('Error reading TODO item.')
            return None
        return item 

    def read_items_by_partiton_key(self, partition_key: str)-> Iterable[dict]:
        '''Get the item identified by the provided doc_id.'''

        container = self.get_container_client(DATABASE_ID, CONTAINER_ID)

        try:
            query = f"SELECT * FROM c  WHERE c.partition_key ='{partition_key}'"
            items = container.query_items(
                query=query, enable_cross_partition_query=False
            )
        except exceptions.CosmosHttpResponseError:
            print('Error reading TODO item.')
            return None
        return list(items)

    def read_item(self, item_id: int):
        '''Get the item identified by the provided doc_id.'''

        container = self.get_container_client(DATABASE_ID, CONTAINER_ID)

        try:
            item = container.read_item(item=item_id, partition_key=item_id)
        except exceptions.CosmosHttpResponseError:
            print('Error reading TODO item.')
            return None
        return item


    def read_items(self) -> Iterable[dict]:
        container = self.get_container_client(DATABASE_ID, CONTAINER_ID)

        try:
            items = container.read_all_items(max_item_count=MAX_ITEM_COUNT)
        except exceptions.CosmosHttpResponseError:
            print('Error reading TODO item.')
            return None
        return list(items)


    def update_item(self, item_id: str, new_body: dict):
        '''Replaces the specified item if it exists in the container.'''

        container = self.get_container_client(DATABASE_ID, CONTAINER_ID)

        try:
            read_item = container.read_item(item=item_id, partition_key=item_id)
            for property, value in new_body.items():
                read_item[property]  = value
            container.replace_item(item=read_item, body=read_item)
        except exceptions.CosmosHttpResponseError:
            print('The replace failed or the item with given id does not exist.')
            return None
        return read_item


    def delete_item(self, item_id: str) -> None:
        '''Delete the item identified by the provided doc_id.'''

        container = self.get_container_client(DATABASE_ID, CONTAINER_ID)

        try:
            container.delete_item(item=item_id, partition_key=item_id)
        except exceptions.CosmosResourceNotFoundError:
            print(f'Item {id} does not exist.')
        except exceptions.CosmosHttpResponseError:
            print(f'Item {id} was not deleted successfully.')

    def get_container_client(self, database_name: str, container_name: str) -> Union[None, ContainerProxy]:
        '''Get a container client given a database and container name.'''
        # TODO: Add check if container exists
        container = self.create_container(database_name, container_name, PARTITION_KEY)
        return container
    
    def create_container(self, database_name: str, container_name: str, partition_key: str)-> Union[None, ContainerProxy]:
        '''Create a container if it does not already exist on the service.'''
        database = self.get_database_client(database_name)
        try:
            container = database.create_container_if_not_exists(id=container_name,  partition_key=PartitionKey(path=f"/{partition_key}"))
        except exceptions.CosmosHttpResponseError:
            print("The container creation failed.")
        print(f"{container_name} container created.")
        return container


    def get_database_client(self, database_name: str) -> Union[None, DatabaseProxy]:
        '''Get a database client based on a database name.'''
        # database = self.client.get_database_client(database_name)
        # if not database:
        # TODO: find simple way to check if a database exists
        self.create_database(database_name)
        database = self.client.get_database_client(database_name)
        return database


    def create_database(self, database_name: str)-> Union[None, DatabaseProxy]:
        '''Create a database if it does not already exist on the service.'''
        try:
            database = self.client.create_database_if_not_exists(database_name)
        except exceptions.CosmosHttpResponseError:
            print(f"{database_name} database creation failed.")
        print(f"{database_name} database created.")
        return database
