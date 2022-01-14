import math
import os
import re
from datetime import date, datetime

import pandas as pd
from pandas import DataFrame

from ElasticCloudSearch import ElasticCloudSearch
from elasticCloudAppSearch import ElasticCloudAppSearch
from pdfParser import writeToFile


def cleanup_column_names(dataframe):  # Remove uppercase, spaces and special chars
    for col in dataframe.columns:
        dataframe.rename(columns={col: re.sub('[^a-z0-9_]+', '', col.lower().replace(' ', '_'))}, inplace=True)
    dataframe.rename(columns={'ec__list_no': 'ec_no'}, inplace=True)  # corap list workaround
    # print("Columns: "+df.columns)



def get_excel_file_content(filename):
    # filename = "echa-restriction-list-export.xlsx"
    # filename = "echa-authorisation-list-export.xlsx"
    # filename = "echa-candidate-list-of-svhc-for-authorisation-export.xlsx"
    # filename = "echa-substance-evaluation---corap-list-export.xlsx"
    return pd.read_excel("./chem_lists/" + filename)

def remove_nan_and_empty_values_tests(df):
    df1 = df.where(pd.notnull(df), None)  # Remove NaN va
    df11 = df.where(pd.notna(df), None)
    year_original = df['year']
    year = df.where(math.isnan(df['year']), None)
    df1['year'] = year
    year_num = pd.to_numeric(year)
    year_int = pd.to_numeric(year, downcast='integer')
    year_str = year.astype(str)
    year_str2 = year_str.where(pd.notnull(year_str), None)
    year_str3 = year_str.replace('nan', None)
    #df11 = df1.astype(int)
    #df.where(pd.notna(df), None)
    df2 = df1.dropna(how='all', axis=1)
    df3 = df2.replace('-', '')
    df4 = df2.replace('nan', 'None')
    df.info()
   # df11.info()
    df2.info()
    dfnull = pd.isnull(df3)
    for row in df3.iterrows():
        year = row[1]['year']
        print(row[1]['year'])
        if math.isnan(row[1]['year']):
            print("Found"+row[1]['year'])
        else:
            print("not")
    return df3

def remove_nan_and_empty_values(df):
    df1 = df.where(pd.notnull(df), None)  # Remove NaN va
    df2 = df1.dropna(how='all', axis=1)  # Remove empty columns
    df3 = df2.replace('-', '')  # Remove -
    return df3

def remove_nan_year(product):  # Workaround for stupid nan float
    try:
        if math.isnan(product['year']):
            # print("Found nan year and fixed")
            product['year'] = None
    except:
        pass

def getAllXlsxFiles():
    xlsxFiles = []
    for filename in os.listdir('./chem_lists'):
        if filename.endswith('.xlsx') and not filename.startswith('~'):
            xlsxFiles.append(filename)
    return xlsxFiles


class EchaParser():
    def __init__(self, file):
        self.indexName = 'echa-lists-index'
        self.datestamps = []
        self.filename = file
        self.identifyList()

    def identifyList(self):
        if "restriction-list" in self.filename:
            self.listName = "restriction-list"
            print("Identified {} from {}".format(self.listName, self.filename))

        elif "authorisation-list" in self.filename:
            self.listName = "authorisation-list"
            self.datestamps.append('sunset_date')
            self.datestamps.append('latest_application_date')
            print("Identified {} from {}".format(self.listName, self.filename))

        elif "candidate-list" in self.filename:
            self.listName = "svhc-candidate-list"
            self.datestamps.append('date_of_inclusion')
            print("Identified {} from {}".format(self.listName, self.filename))

        elif "corap-list" in self.filename:
            self.listName = "corap-list"
            self.datestamps.append('latest_update')
            self.datestamps.append('corap_publication_date')
            print("Identified {} from {}".format(self.listName, self.filename))

        else:
            print("Not ECHA list "+self.filename)
            return False

    def cleanup_dates(self, product):
        for datestamp in self.datestamps:
            product[datestamp] = datetime.strptime(product[datestamp], '%d/%m/%Y').strftime('%Y-%m-%d')


    def index_excel_file(self):
        df = get_excel_file_content(self.filename)
        indexWriter = ElasticCloudAppSearch()
        #indexWriter = ElasticCloudSearch()

        cleanup_column_names(df)
        df = remove_nan_and_empty_values(df)

        products = df.to_dict(orient='records')
        for product in products:
            #if product.get("cas_no") != product.get("ec_no"):  # Not a product
            product['index_updated'] = date.today()
            product['list_name'] = self.listName
            self.cleanup_dates(product)  # Ugly workaround for removing nan in float columns
            remove_nan_year(product)
            indexWriter.index_doc(self.indexName, product.get("substance_name")+'_'+self.listName, product)


if __name__ == "__main__":
    files = getAllXlsxFiles()
    for file in getAllXlsxFiles():
        if EchaParser(file).identifyList() is not False:
            echa = EchaParser(file)
            echa.index_excel_file()

    
