from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import csv
import numpy as np
import os

#############################

def create_null_column_csv():
    
    empty_data = [None]
    empty_df = pd.DataFrame(empty_data)
    empty_df.to_csv('empty.csv', index=False)

#############################

def titrePD(content):

    with open('titre.csv', 'w') as output:
        for head in content:
            output.write(head.get_text('h3').replace('h3','\n'))

    df=pd.read_fwf('titre.csv')
    df.to_csv('titre.csv',index=None)

    return 'titre.csv'

def companyPD(content):

    with open('company.csv', 'w') as output:
        for head in content:
            output.write(head.get_text('a'))

    df=pd.read_fwf('company.csv')
    df.to_csv('company.csv',index=None)

    # cols = df.columns.tolist()
    # cols = [cols[1]] + cols[0:1] + cols[2:]
    # df = df[cols]

    return 'company.csv'

def locationPD(content):

    with open('location.csv', 'w') as output:
        for head in content:
            output.write(head.get_text('span').replace('span','\n'))

    df=pd.read_fwf('location.csv')
    df.to_csv('location.csv',index=None)

    return 'location.csv'

def DayPD(content):

    with open('day.csv', 'w') as output:
        for value in content:
            output.write(value + '\n')

    df=pd.read_fwf('day.csv')
    df.to_csv('day.csv',index=None)

    return 'day.csv'

def salaryPD(content):

    with open('salary.csv', 'w') as output:
        for head in content:
            output.write(head.get_text('span').replace('span','\n').replace('USD','\n'))


    try :
        df=pd.read_fwf('salary.csv')
    except pd.errors.EmptyDataError:
        return create_null_column_csv()
    else:
        odd_df = df.iloc[::2].reset_index(drop=True)
        even_df = df.iloc[1::2].reset_index(drop=True)

        df=even_df+' '+odd_df
        df.to_csv('salary.csv',index=None)

        return 'salary.csv'

#############################

def main():

#############################
    file='Data/emploi.html'
    with open(file, 'r', encoding='utf-8') as file:
        content = file.read()
        
    soup = BeautifulSoup(content, 'html.parser')

    titre =soup.find_all('h3',class_='base-search-card__title') 
    Final_title=titrePD(titre)

    company=soup.find_all('a',class_='hidden-nested-link')
    Final_Company=companyPD(company)

    location=soup.find_all('span',class_='job-search-card__location')
    Final_Location=locationPD(location)

    day = soup.find_all('time')
    jour = [date.get('datetime') for date in day]
    Final_Date=DayPD(jour)

    salary=soup.find_all('span',class_='job-search-card__salary-info')
    Final_Salary=salaryPD(salary)
        
#############################
    df1 = pd.read_csv('titre.csv')
    if len(df1.columns) > 1:
        df1.drop(df1.columns[1], axis=1, inplace=True)

    df2 = pd.read_csv('company.csv')
    if len(df2.columns) > 1:
        df2.drop(df2.columns[1], axis=1, inplace=True)

    df3 = pd.read_csv('location.csv')
    if len(df3.columns) > 1:
        df3.drop(df3.columns[1], axis=1, inplace=True)

    df4 = pd.read_csv('day.csv')
    if len(df4.columns) > 1:
        df4.drop(df4.columns[1], axis=1, inplace=True)

    try:
        df5 = pd.read_csv('salary.csv')
    except pd.errors.EmptyDataError:
        result_df = pd.concat([df1, df2, df3, df4], axis=1)
        result_df.columns = ['Titre', 'Societe', 'Location', 'Jour']
    else:
        if len(df5.columns) > 0: 
            result_df = pd.concat([df1, df2, df3, df4, df5], axis=1)
            result_df.columns = ['Titre', 'Societe', 'Location', 'Jour', 'Salaire']
    

    



#############################
    os.remove('company.csv')
    os.remove('day.csv')
    os.remove('location.csv')
    os.remove('titre.csv')
    os.remove('salary.csv')

    
    try:
        os.remove('empty.csv')
    except FileNotFoundError as e:
        True
    # momken tji erreur y9lk fichier mch mawjoud
#############################


    result_df.to_csv('merged_file.csv', index=False)
    os.remove('merged_file.csv')
    result_df.to_excel('merged_file.xlsx',index=False)

#############################
if __name__ == "__main__":
    main()
    # mb3d zid el query eli fel fichier test en commentaire ,twali taamel demande direct w tbadel esm el fichier direct (esm el job+wel blasa)
    # ken tzid query bch fonction general jdida tbadel el traitement