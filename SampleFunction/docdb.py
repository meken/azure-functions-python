import pydocumentdb.document_client as document_client
import pydocumentdb.documents as documents

class Repository:
    DB_NAME = "contacs"
    COLL_NAME = "contactInfo"
    COLLECTION = "dbs/%s/colls/%s" % (DB_NAME, COLL_NAME)

    def __init__(self, host, token):
        self.client = document_client.DocumentClient(host, {"masterKey": token})

    def _ensure_db_exists(self):
        if len(list(self.client.ReadDatabases())) == 0:
            self.client.CreateDatabase({"id": self.DB_NAME})
            props = {
                "id": self.COLL_NAME,
                "indexingPolicy": {
                    "indexingMode": "consistent"
                },
                "partitionKey": {
                    "paths": ["/email"],
                    "kind": documents.PartitionKind.Hash
                }
            }
            self.client.CreateCollection("dbs/%s" % self.DB_NAME, props)

    def insert(self, contactDetails):
        self._ensure_db_exists()
        return self.client.CreateDocument(self.COLLECTION, contactDetails)
