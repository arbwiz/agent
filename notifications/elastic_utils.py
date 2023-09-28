import json
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


def insert_documents(documents):
    id = 0
    for document in documents:
        es.index(index="events", id=str(id), document=json.dumps(document))
        id += 1


if __name__ == "__main__":
    with open("documents.json", "r") as f:
        documents = json.load(f)

    insert_documents(documents)
