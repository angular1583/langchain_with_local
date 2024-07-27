from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from langchain_community.llms import Ollama
from mongodb import generatemongodbPrompt

# Initialize FastAPI app
app = FastAPI()

# Define request model
class QueryRequest(BaseModel):
    databaseType: str
    question: str

# Environment variables for database connections
# mongo_client = MongoClient("mongodb+srv://Hitesh:Ghjkl!123@cluster0.k22qi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# MongoDB connection
def get_mongo_client():
    return MongoClient("mongodb+srv://Hitesh:Ghjkl!1234@cluster0.k22qi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="yourdatabase"
    )

# LangChain setup
llm = llm = Ollama(
    model="llama3",
    # url="http://localhost:11434",
    verbose=True
)

# Function to generate SQL query
def generate_sql_query(question):
    query = "SELECT COUNT(*) FROM products;"
    return query

# Function to generate MongoDB query
def generate_mongo_query(question):
    query = {"$count": "product_count"}
    return query

# API endpoint to handle queries
@app.post("/query")
async def handle_query(request: QueryRequest):
    if request.databaseType.lower() == "sql":
        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = generate_sql_query(request.question)
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        return {"result": result[0]}
    
    elif request.databaseType.lower() == "mongodb":
        dbDetails = generatemongodbPrompt()
        prompt = 'Write a MongoDB query for the following question: ${request.question}. The MongoDB structure is as follows: ${dbDetails}. Return only the complete query. If you are unable to generate the query, return false.'
        query = llm.invoke(prompt)
        print(query)
        print('####')
        client = get_mongo_client()
        db = client["e_commerce"]
        collection = db["products"]
        query = generate_mongo_query(request.question)
        result = list(collection.aggregate([query]))
        client.close()
        return {"result": result[0]["product_count"] if result else 0}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid database type")

# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)