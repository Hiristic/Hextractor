from pprint import pprint

from elastic_enterprise_search import AppSearch
import configparser

config = configparser.ConfigParser()
config.read('elastic.ini')


class ElasticCloudAppSearch:
    def __init__(self):
        # Connecting to an instance on Elastic Cloud w/ an App Search private key
        self.app_search = AppSearch(
            config['ELASTIC_APP_SEARCH']['app_search_url'],
            http_auth=config['ELASTIC_APP_SEARCH']['http_auth_key']
        )

    def schema_get(self, index):
        resp = self.app_search.get_schema(engine_name=index)
        pprint(resp)

    def index_doc(self, index, id, doc):
        doc['id'] = id
        try:
            return self.app_search.index_documents(engine_name=index, documents=doc)
        except Exception as ex:
            print('Failed indexing doc: {0}'.format(repr(ex)))

if __name__ == "__main__":
    indexWriter = ElasticCloudAppSearch()
    pprint(indexWriter.get_version())
    #indexWriter.schema_get("imvelo-search")