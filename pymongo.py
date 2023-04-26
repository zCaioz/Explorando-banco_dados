import pymongo as pyM
from pprint import pprint

client = pyM.MongoClient("sua host")
db = client.test 
collection = db.test_collection 
posts = db.posts

documento = [{
    "nome": "Caio Toys",
    "cpf": "123456789",
    "endereco": "maringá-pr",
    "conta": ["0001", "corrente"],
    "saldo": 900
},{
    "nome": "Neuman",
    "cpf": "631247892",
    "endereco": "maringá-pr",
    "conta": ["0001", "corrente"],
    "saldo": 500

}]

result = posts.insert_many(documento)
result.inserted_ids

pprint.pprint(db.posts.find_one({"nome": "Caio Toys"}))

for post in posts.find():
    pprint.pprint(post)

pprint.pprint(posts.find_one({"conta": "corrente"}))

for post in posts.find({}).sort("cpf"):
    print(post)
    
