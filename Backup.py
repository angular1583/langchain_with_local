from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3",
    # url="http://localhost:11434",
    verbose=True
)

response = llm.invoke("are you able tot build mongodb and sql queries")
print(response)

# import { ChatOllama } from "@langchain/community/chat_models/ollama";

# ollamaLlm = new ChatOllama({
#   baseUrl: "http://localhost:11434",
#   model: "llama2"
# });

# const response = await ollamaLlm.invoke(
#   "Simulate a rap battle between Stephen Colbert and John Oliver"
# );
# console.log(response.content);