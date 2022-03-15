from datetime import datetime, date

from ElasticCloudSearch import ElasticCloudSearch
from elasticCloudAppSearch import ElasticCloudAppSearch
from excelParser import get_excel_file_content, cleanup_column_names, remove_nan_and_empty_values, getAllXlsxFiles


class PrioParser():
    def __init__(self, file):
        self.indexName = 'prio-list-index'
        self.datestamps = []
        self.filename = file
        self.identifyList()

    def identifyList(self):
        if "prio_database" in self.filename:
            self.listName = "PRIO List"
        else:
            return False

    def rename_to_echa_standard(self, df):
        df.rename(columns={'eg_nr': 'ec_no', 'cas_nr': 'cas_no'}, inplace=True)

    def index_excel_file(self, AppSearch=True):
        df = get_excel_file_content(self.filename)
        if AppSearch:
            indexWriter = ElasticCloudAppSearch()
        else:
            indexWriter = ElasticCloudSearch()

        cleanup_column_names(df)
        self.rename_to_echa_standard(df)
        df = remove_nan_and_empty_values(df)

        products = df.to_dict(orient='records')
        for product in products:
            product['index_updated'] = date.today()
            product['list_name'] = self.listName
            indexWriter.index_doc(self.indexName, product.get("substance_name")+'_'+self.listName, product)

if __name__ == "__main__":
    for file in getAllXlsxFiles():
        if PrioParser(file).identifyList() is not False:
            PrioParser(file).index_excel_file(AppSearch=True)
            PrioParser(file).index_excel_file(AppSearch=False)