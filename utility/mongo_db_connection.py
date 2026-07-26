import pymongo

from utility.env_setup import environment


class MongoDbClient:

    def __init__(self):
        self.__host_url=environment.MONGO_HOST_URL
        #self.__host_url='mongodb://localhost:27017/'
        print(self.__host_url)
        self.__client=self.__initiate_connection()
        print(self.__client)
    def __initiate_connection(self):
       return pymongo.MongoClient("mongodb://localhost:27017/",)

    def create_database(self, db_name, data):
        db=self.__client[db_name]

        self.write_to_db(data,db_name=db_name,
                         collection_name='user_details')
        print(db, db_name)
        return db

    def __get_collection(self, db_name, collection_name):
        db = self.__client[db_name]
        collection = db[collection_name]
        return collection

    def write_to_db(self, data, collection_name, db_name):
        collection=self.__get_collection(db_name=db_name, collection_name=collection_name)
        res=collection.insert_one(data)
        return res

    def update_data(self, data, update_criteria,collection_name, db_name):
        collection = self.__get_collection(db_name=db_name, collection_name=collection_name)
        res = collection.update_one(update_criteria, data)
        return res

    def get_data(self, collection_name, db_name, query=None):
        collection=self.__get_collection(db_name=db_name, collection_name=collection_name)
        if query:
            return collection.find()
        else:
            return collection.find(query)









if __name__=='__main__':
    # Connect to the MongoDB server
    MongoDbClient().create_database('test_create_2',{'name': 'John Doe', 'age': 30, 'city': 'Example City'})
    #client = pymongo.MongoClient("mongodb://localhost:27017/")
    # print(client)
    # # Replace 'your_database_name' with the desired database name
    #
    # db_name = 'your_database_name'
    # db = client[db_name]
    #
    # print(f"Connected to the '{db_name}' database.")
    #
    # # Optional: Create a collection (similar to a table in relational databases)
    # collection_name = 'your_collection_name'
    # collection = db[collection_name]
    #
    # # print(f"Created a collection named '{collection_name}'.")
    # #
    # # Example: Insert a document into the collection
    # sample_data = {'name': 'John Doe', 'age': 30, 'city': 'Example City'}
    # result = collection.insert_one(sample_data)
    # #
    # # print(f"Inserted document with ID: {result.inserted_id}")
    # # Replace 'your_database_name' and 'your_collection_name' with your actual database and collection names
    #
    #
    # # Retrieve all data
    # all_data = collection.find()
    # print("All data:")
    # for document in all_data:
    #     print(document)
    #
    # # Retrieve data where the name ends with "Doe"
    # doe_data = collection.find({'name': {'$regex': 'Doe$'}})
    # print("\nData where name ends with 'Doe':")
    # for document in doe_data:
    #     print(document)