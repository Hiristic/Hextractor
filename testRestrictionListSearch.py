

from ElasticCloudSearch import ElasticCloudSearch

if __name__ == "__main__":
    es = ElasticCloudSearch()
    #pprint(es.get_es().info())

    reply = es.search_doc_field_with_value("sin-list-index", "cas_no", "15571-58-1")
    print("SIN List: "+str(reply.get("hits").get("total").get("value")))

    reply = es.search_doc_field_with_value("echa-candidate-list-index", "cas_no", "15571-58-1")
    print("REACH Kandidatlistan: "+str(reply.get("hits").get("total").get("value")))

    reply = es.search_doc_field_with_value("echa-authorisation-list-index", "cas_no", "3846-71-7")
    print("REACH Bilaga XIV: " + str(reply.get("hits").get("total").get("value")))

    reply = es.search_doc_field_with_value("echa-restriction-list-index", "cas_no", "96-32-2")
    print("REACH Bilaga XVII: " + str(reply.get("hits").get("total").get("value")))

    reply = es.search_doc_field_with_value("echa-corap-list-index", "cas_no", "108-87-2")
    print("REACH CoRAP: " + str(reply.get("hits").get("total").get("value")))

    reply = es.search_doc_field_with_multiple_values("prio-list-index", "cas_no", "15571-58-1", "priority_level", "Phase-out substance")
    print("PRIO Utfasningsämnen: " + str(reply.get("hits").get("total").get("value")))

    reply = es.search_doc_field_with_multiple_values("prio-list-index", "cas_no", "108-78-1", "priority_level", "Priority risk-reduction substance")
    print("PRIO Riskminskning: " + str(reply.get("hits").get("total").get("value")))

    # One search for all lists
    reply = es.search_doc_field_with_value("*list-index", "cas_no", "15571-58-1")
    print("All lists: "+str(reply.get("hits").get("total").get("value")))
