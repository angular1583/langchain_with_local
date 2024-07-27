from pymongo import MongoClient

def get_mongo_client():
    return MongoClient("mongodb+srv://Hitesh:Ghjkl!1234@cluster0.k22qi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

def get_mongo_db():
    client = get_mongo_client()
    return client["e_commerce"]

def get_collections_and_fields(db):
    collections = db.list_collection_names()
    collection_fields = {}
    
    for collection in collections:
        sample_doc = db[collection].find_one()
        if sample_doc:
            fields = list(sample_doc.keys())
            collection_fields[collection] = fields
    
    return collection_fields

def generate_prompt(collection, fields):
    prompt = f"Collection: {collection}\nFields: {', '.join(fields)}\n\n"
    prompt += "Please provide a brief description of the data stored in this collection based on the available fields."
    return prompt

# Usage example
db = get_mongo_db()
collection_fields = get_collections_and_fields(db)


def generatemongodbPrompt():
    for collection, fields in collection_fields.items():
        prompt = generate_prompt(collection, fields)
        print(prompt)
        print("---")
    return collection_fields