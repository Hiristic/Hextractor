from datetime import datetime
from pprint import pprint

from elasticsearch import Elasticsearch, helpers
import configparser

config = configparser.ConfigParser()
config.read('elastic.ini')


class ElasticCloudSearch:
    def __init__(self):
        self.es = Elasticsearch(
            cloud_id=config['ELASTIC']['cloud_id'],
            api_key=(config['ELASTIC']['api_key_id'], config['ELASTIC']['api_key']),
        )

    def get_es(self):
        return self.es

    def index_doc(self, index, id, doc):
        try:
            return self.es.index(index=index, id=id, body=doc)
        except Exception as ex:
            print('Failed indexing doc: {0}'.format(repr(ex)))

    def get_doc(self, index, id):
        res = self.es.get(index="test-index", id=1)
        pprint(res['_source'])

#es.indices.refresh(index="test-index")

    def search(self, index, value):
        res = self.es.search(index=index, query={"match_all": {}})
        print("Got %d Hits:" % res['hits']['total']['value'])
        for hit in res['hits']['hits']:
            print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


if __name__ == "__main__":
    es = ElasticCloudSearch().get_es()
    pprint(es.info())




