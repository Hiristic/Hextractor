import math
import os
import re
import pandas as pd

#from EchaParser import EchaParser
#from SinParser import SinParser


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

def getAllXlsxFiles():
    xlsxFiles = []
    for filename in os.listdir('./chem_lists'):
        if filename.endswith('echa-substance-evaluation---corap-list-export.xlsx') and not filename.startswith('~'):
            xlsxFiles.append(filename)
    return xlsxFiles


#if __name__ == "__main__":
#    AppSearch = True
#    for file in getAllXlsxFiles():
#        if EchaParser(file).identifyList() is not False:
#            EchaParser(file).index_excel_file(AppSearch=AppSearch)
#        elif SinParser(file).identifyList() is not False:
#            SinParser(file).index_excel_file(AppSearch=AppSearch)
#        else:
#            print("Unknown file: "+file)
