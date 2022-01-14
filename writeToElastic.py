from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(
    cloud_id="cluster-1:dXMa5Fx...",
    http_auth=("elastic", "<password>"),
)
doc = {
    'id': 'H200',
    "descr": "Instabilt, explosivt.",
    "type": "Fysikaliska faror"
}
res = es.index(index="faroangivelser", id=1, body=doc)
print(res['result'])

res = es.get(index="faroangivelser", id=1)
print(res['_source'])

es.indices.refresh(index="faroangivelser")

res = es.search(index="faroangivelser", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])