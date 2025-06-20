import os
import json
from pymongo import MongoClient


MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "ThuocBietDuoc2"
JSON_FOLDER = "/Users/vohaison/Documents/crawlData/caoThuoc/caoThuoc/save"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

for filename in os.listdir(JSON_FOLDER):
    if filename.endswith(".json"):
        collection_name = os.path.splitext(filename)[0]
        file_path = os.path.join(JSON_FOLDER, filename)

        print(f"📥 Importing {filename} → Collection: {collection_name}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                db[collection_name].delete_many({})

                if isinstance(data, list):
                    db[collection_name].insert_many(data)
                else:
                    db[collection_name].insert_one(data)

                print(f"✅ Đã import vào collection: {collection_name}")
        except Exception as e:
            print(f"❌ Lỗi với file {filename}: {e}")
