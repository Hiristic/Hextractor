import os
from datetime import date

import pandas as pd
from pandas import DataFrame
from tika import parser
from tika import language
import re
from elastic_enterprise_search import EnterpriseSearch
import json

from ElasticCloudSearch import ElasticCloudSearch
from elasticCloudAppSearch import ElasticCloudAppSearch
from pdfParser import PDFParser


def get_excel_file_content(filename):
    return pd.read_excel("./chem_lists/" + filename, header=None)


class AFSpdfParser:
    def __init__(self, filename): 
        self.doc = {}
        self.split_doc = {}  # Used for subsections
        self.parsed_pdf = parser.from_file(filename)
        self.data = self.parsed_pdf['content']
        self.products = []

        tika_server_status = self.parsed_pdf['status']
        print(tika_server_status)  # TODO Do status test

    def clean_data(self, data):
        casnr_lines_cleaned = []
        for line in data:
            line = re.sub('[\n|\t]', '', line)
            line = re.sub('CAS-nr[ ]{1,}Ämne', '', line)
            line = re.sub('  ', ' ', line)
            line = re.split('(?= Se .*?)', line)[0]
            line += '\n'
            casnr_lines_cleaned.append(line)
        return casnr_lines_cleaned

    def parseTextToXls(self):

        cas_nrindex = re.split('(?=\nCAS-nummerindex \n)', self.data, flags = re.IGNORECASE)
        # lines_per_page = re.split('(?=\nCAS-nr  Ämne\n)', cas_nrindex[1])
        casnr_lines = re.split('(?=\n[0-9]{2,7}[-][0-9]{2}[-][0-9]{1}.*)', cas_nrindex[1], flags=re.IGNORECASE)[1:]

        casnr_lines_recreated = []

        # Do basic extraction and cleaning
        casnr_lines_cleaned = []
        casnr_lines_cleaned = self.clean_data(casnr_lines)
        df = DataFrame({'./chem_list/CAS-nummerindex': casnr_lines_cleaned})
        df.to_excel('AFS-CAS-nummerindex.xlsx', sheet_name='CAS-nummerindex', index=False)


    def parseTextFromXls(self):
        # Manual cleaning needs to be done. F*ng pdfs
        df = get_excel_file_content('AFS-CAS-nummerindex-cleaned.xlsx')
        #df_t = df.T
        list = df['CAS-nummerindex'].tolist()
        casnr_lines_cleaned = self.clean_data(df['CAS-nummerindex'])

            #line = line.sub('\n', '').strip('CAS-nr Ämne', '')+'\n'
        for line in casnr_lines_cleaned:
            #substance = re.split('\n(?P<cas>[0-9]{2,7}[-][0-9]{2}[-][0-9]{1})[ ]{1,}(?P<name>.*?)[ ]{1,}(?P<cat>[ A\n| B\n|\n]{1})', line, flags = re.IGNORECASE)
            #regex = r'(?P<cas>[0-9]{2,7}[-][0-9]{2}[-][0-9]{1})[ ]{1,}(?P<name>.*?(?=( \n|\n| A\n| B\n))){1}(?=(?P<cat>( A\n| B\n|\n){1}))'
            #regex = r'(?P<cas>[0-9]{2,7}[-][0-9]{2}[-][0-9]{1})[ ]{1,}(?P<name>.*?( \n|\n| A\n| B\n)){1}'
            regex = r'(?P<cas>[0-9]{2,7}[-][0-9]{2}[-][0-9]{1})[ ]{1,}(?P<name>.*?(?P<cat> \n|\n| A\n| B\n){1}){1}'
            substance = re.split(regex, line, flags=re.IGNORECASE)
            #matches = re.finditer(regex, line, re.MULTILINE)

            p = re.compile(regex)
            m = p.search(line)
            cas = m.group('cas')


            if substance.__len__() > 1:
                # strip " Se "
                substance[2] = re.split('( Se )',substance[2], flags=re.IGNORECASE)[0]
                #print(line + substance[1] + " " + substance[2])
                if substance.__len__() > 5:
                    rest = re.split('\n(?P<name>.*(?=(\n\nA \n|\n\nB \n|\n\n)))(?=(?P<cat>(\n\nA \n|\n\nB \n|\n){0,1}))', substance[6], flags=re.IGNORECASE)
                    if rest.__len__() > 1:
                        substance[2] += rest[1]
                        substance[4] = rest[2]
                        print(line + substance[1] + " " + substance[2] + " " + substance[4])
                        casnr_lines_cleaned.append(substance[1] + " " + substance[2] + " " + substance[4])
                else:
                    casnr_lines_cleaned.append(substance[1] + " " + substance[2])

        print(casnr_lines_cleaned)




    def index_afs_file(self, AppSearch=True):
        if AppSearch:
            indexWriter = ElasticCloudAppSearch()
        else:
            indexWriter = ElasticCloudSearch()

        for product in self.products:
            product['index_updated'] = date.today()
            product['list_name'] = self.listName
            indexWriter.index_doc(self.indexName, product.get("substance_name")+'_'+self.listName, product)



def getAFSPdfFile():
    pdfFiles = []
    for filename in os.listdir('./chem_lists'):
        if filename.endswith('.pdf'):
            pdfFiles.append(filename)

    return pdfFiles.sort(key=str.lower)

def getParserDetails():
    from tika import config
    print(config.getParsers())
    print(config.getMimeTypes())
    print(config.getDetectors())



if __name__ == "__main__":
    filename = "hygieniska-gransvarden-afs-2018-1.pdf"
    fileparser = AFSpdfParser("./chem_lists/"+filename)

    fileparser.parseTextFromXls()

