from datetime import datetime, date

from ElasticCloudSearch import ElasticCloudSearch
from elasticCloudAppSearch import ElasticCloudAppSearch
from excelParser import get_excel_file_content, cleanup_column_names, remove_nan_and_empty_values, getAllXlsxFiles


class SinParser():
    def __init__(self, file):
        self.indexName = 'sin-list-index'
        self.datestamps = []
        self.filename = file
        self.identifyList()

    def identifyList(self):
        if "SinList" in self.filename:
            self.listName = "SIN List"
            self.datestamps.append('date_for_inclusion_on_the_sin_list')
        else:
            return False

    def cleanup_dates(self, product):
        for datestamp in self.datestamps:
            product[datestamp] = datetime.strptime(product[datestamp], '%Y %B').strftime('%Y-%m-01')

    def rename_to_echa_standard(self, df):
        df.rename(columns={'ec_number': 'ec_no', 'cas_number': 'cas_no', 'name': 'substance_name'}, inplace=True)

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
        if SinParser(file).identifyList() is not False:
            SinParser(file).index_excel_file(AppSearch=True)