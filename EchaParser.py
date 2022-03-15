import math
from datetime import date, datetime

from ElasticCloudSearch import ElasticCloudSearch
from elasticCloudAppSearch import ElasticCloudAppSearch
from excelParser import getAllXlsxFiles, cleanup_column_names, remove_nan_and_empty_values, get_excel_file_content


class EchaParser():
    def __init__(self, file):
        self.indexName = 'echa-lists-index'
        self.datestamps = []
        self.filename = file
        self.identifyList()

    def identifyList(self):
        if "restriction-list" in self.filename:
            self.indexName = 'echa-restriction-list-index'
            self.listName = "ECHA restriction list"
            print("Identified {} from {}".format(self.listName, self.filename))

        elif "authorisation-list" in self.filename:
            self.indexName = 'echa-authorisation-list-index'
            self.listName = "ECHA authorisation list"
            self.datestamps.append('sunset_date')
            self.datestamps.append('latest_application_date')
            print("Identified {} from {}".format(self.listName, self.filename))

        elif "candidate-list" in self.filename:
            self.indexName = 'echa-candidate-list-index'
            self.listName = "ECHA SVHC candidate list"
            self.datestamps.append('date_of_inclusion')
            print("Identified {} from {}".format(self.listName, self.filename))

        elif "corap-list" in self.filename:
            self.indexName = 'echa-corap-list-index'
            self.listName = "ECHA CORAP list"
            self.datestamps.append('latest_update')
            self.datestamps.append('corap_publication_date')
            print("Identified {} from {}".format(self.listName, self.filename))

        else:
            print("Not ECHA list "+self.filename)
            return False

    def cleanup_dates(self, product):
        for datestamp in self.datestamps:
            product[datestamp] = datetime.strptime(product[datestamp], '%d/%m/%Y').strftime('%Y-%m-%d')

    def remove_nan_year(self, product):  # Workaround for stupid nan float
        try:
            if math.isnan(product['year']):
                # print("Found nan year and fixed")
                product['year'] = None
        except:
            pass

    def index_excel_file(self, AppSearch=True):
        df = get_excel_file_content(self.filename)
        if AppSearch:
            indexWriter = ElasticCloudAppSearch()
        else:
            indexWriter = ElasticCloudSearch()

        cleanup_column_names(df)
        df = remove_nan_and_empty_values(df)

        products = df.to_dict(orient='records')
        for product in products:
            #if product.get("cas_no") != product.get("ec_no"):  # Not a product
            product['index_updated'] = date.today()
            product['list_name'] = self.listName
            self.cleanup_dates(product)  # Ugly workaround for removing nan in float columns
            self.remove_nan_year(product)
            indexWriter.index_doc(self.indexName, product.get("substance_name")+'_'+self.listName, product)


if __name__ == "__main__":
    for file in getAllXlsxFiles():
        if EchaParser(file).identifyList() is not False:
            EchaParser(file).index_excel_file(AppSearch=False)