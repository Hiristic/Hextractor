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
        res = self.es.get(index=index, id=1)
        pprint(res['_source'])

#es.indices.refresh(index="test-index")

    def search(self, index, value):
        res = self.es.search(index=index, body={"match_all": {}})
        print("Got %d Hits:" % res['hits']['total']['value'])
        for hit in res['hits']['hits']:
            print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

    def get_docs_field_with_value(self, index_name,  field_name, field_text):
        for doc in helpers.scan(self.es, index=index_name,
                                              query={"query": {
                                                  "match_phrase": {
                                                      field_name: {
                                                          "query": field_text}}}}):
            yield doc['_source']

    def search_doc_field_with_value(self, index_name, field_name, field_text):
        return self.es.search(index=index_name, body={"query": {
                                                      "match_phrase": {
                                                          field_name: {
                                                              "query": field_text}}}})

    def search_doc_field_with_multiple_values(self, index_name, field_name, field_text, field2_name, field2_value):
        return self.es.search(index=index_name, body={"query": {"bool": { "must":[
                                                        {"match_phrase": {
                                                              field_name: {
                                                                  "query": field_text}}},
                                                        {"match_phrase": {
                                                              field2_name: {
                                                                   "query": field2_value}}}
                                                        ]}}})


if __name__ == "__main__":
    es = ElasticCloudSearch()
    pprint(es.get_es().info())

    # One search for all lists
    reply = es.search_doc_field_with_value("*list-index", "cas_no", "15571-58-1")
    print("All lists: "+str(reply.get("hits").get("total").get("value")))
