# Create the CLI application, that would populate MongoDB database with random data. The input should ask for :
# *database name
# *collection name
# *field name with types (string, number, date string objects etc.) with range of values (lets say field name = price ,
# then value is number (float, int) which is random number from a(min) to b(max) )
# *number o documents to create.

from pymongo import MongoClient
from typing import Dict
import random
import pandas as pd


class DatabaseManager:
    def __init__(
        self, host: str, port: int, db_name: str, collection_name: str
    ) -> None:
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, document: Dict) -> str:
        result = self.collection.insert_one(document)
        return str(result.inserted_id)


def populate_database():
    host = input("Please enter the MongoDB host (default: localhost): ") or "localhost"
    port = int(input("Please enter the MongoDB port (default: 27017): ") or 27017)
    db_name = input("Please enter the database name: ")
    collection_name = input("Please enter the collection name: ")
    field_quant = int(input("Please enter the number of fields to create: "))
    doc_quant = int(input("Please enter the number of documents to create: "))

    document_manager = DatabaseManager(host, port, db_name, collection_name)

    field_names = []
    field_types = []
    for _ in range(field_quant):
        field_name = input("Please enter the field name: ")
        field_type = input("Please enter the field type (string, number, date): ")
        field_names.append(field_name)
        field_types.append(field_type)

    for _ in range(doc_quant):
        document = {}
        for i in range(field_quant):
            field_name = field_names[i]
            field_type = field_types[i]
            if field_type == "string":
                value = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
            elif field_type == "number":
                min_value = float(input("Please enter the minimum value: "))
                max_value = float(input("Please enter the maximum value: "))
                value = random.uniform(min_value, max_value)
            elif field_type == "date":
                value = random_date()
            else:
                value = None

            document[field_name] = value

        document_manager.create_document(document)

    print("Database population completed.")


def random_date(start_date="2020-01-01", end_date="2023-12-31"):
    start_timestamp = pd.to_datetime(start_date).timestamp()
    end_timestamp = pd.to_datetime(end_date).timestamp()
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    random_datetime = pd.to_datetime(random_timestamp, unit="s")
    formatted_date = random_datetime.strftime("%Y-%m-%d")
    return formatted_date


if __name__ == "__main__":
    populate_database()
