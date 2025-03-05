import pymongo

MONGO_URI = "mongodb+srv://dbyta:et98XfKSurnLobko@rag-ml-cluster.fai9y.mongodb.net/"
client = pymongo.MongoClient(MONGO_URI)
db = client["rag-ml-cluster"]
collection = db["rag_ml"]

models_dict = {
    "Llama V3 70B Instruct": "accounts/fireworks/models/llama-v3-70b-instruct",
    "Mixtral 8x7B Instruct": "accounts/fireworks/models/mixtral-8x7b-instruct",
    "FireFunction V1": "accounts/fireworks/models/firefunction-v1"
}
tokens_dict = {
    "Llama V3 70B Instruct": "4,096",
    "Mixtral 8x7B Instruct": "8,000",
    "FireFunction V1": "4,096"
}
