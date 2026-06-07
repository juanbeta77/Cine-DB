import pymongo


MONGO_URI = "mongodb://localhost:27017/"

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["Cine-DB"]  
    print("Conexión exitosa a MongoDB Local")
except Exception as e:
    print(f"Error al conectar a MongoDB Local: {e}")