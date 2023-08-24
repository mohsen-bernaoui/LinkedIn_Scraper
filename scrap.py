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
    empty_df = pd.DataFrame({'Salaire': empty_data})
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


    if os.path.getsize('salary.csv') == 0:
        return True
        
    else :
        df=pd.read_fwf('salary.csv')

        odd_df = df.iloc[::2].reset_index(drop=True)
        even_df = df.iloc[1::2].reset_index(drop=True)

    
        df=even_df+' '+odd_df
        df.to_csv('salary.csv',index=None)

        return 'salary.csv'

#############################

def main():

#############################
    file='Data/General.html'
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
    try:
        df1.drop(df1.columns[1], axis=1, inplace=True)
    except IndexError:
        True

    df2 = pd.read_csv('company.csv')
    try:
        df2.drop(df2.columns[1], axis=1, inplace=True)
    except IndexError:
        True
        
    df3 = pd.read_csv('location.csv')
    try:
        df3.drop(df3.columns[1], axis=1, inplace=True)
    except IndexError:
        True

    df4 = pd.read_csv('day.csv')
    try:
        df4.drop(df4.columns[1], axis=1, inplace=True)
    except IndexError:
        True

    if os.stat('salary.csv')==0:
        # mch sur mel == aamel aaliha tala mb3d ,ken tji erreur mb3 fel sal (feragh wala maabi raw mnha)
        df5 = pd.read_csv('salary.csv')
        try:
            df5.drop(df5.columns[1], axis=1, inplace=True)
        except IndexError:
            True
    else :
        os.remove('salary.csv')
    df5 = pd.read_csv('salary.csv')

#############################
    df1.columns = ['Titre']
    df2.columns = ['societe']
    df3.columns = ['location']
    df4.columns = ['jour']
    try:
        df5.columns = ['salaire']
    except FileNotFoundError as e:
        bf5=create_null_column_csv()

#############################
    result_df = pd.concat([df1, df2, df3, df4, df5], axis=1)

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
    result_df.to_excel('merged_file.xlsx',index=False)

#############################
if __name__ == "__main__":
    main()
    # mb3d zid el query eli fel fichier test en commentaire ,twali taamel demande direct w tbadel esm el fichier direct (esm el job+wel blasa)
    # ken tzid query bch fonction general jdida tbadel el traitement