from bs4 import BeautifulSoup
import pandas as pd
import os

def create_empty_csv(file_name):
    df = pd.DataFrame(columns=['Placeholder'])
    df.to_csv(file_name, index=False)

def extract_data_to_csv(soup, class_name, file_name):
    data = [element.get_text() for element in soup.find_all('span', class_=class_name)]
    df = pd.DataFrame(data, columns=['Data'])
    df.to_csv(file_name, index=False)
##############################

def main():

    input_file = 'Data/Google_Careers.html'    
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')

##############################
    
    extract_data_to_csv(soup, 'ObfsIf-eEDwDf ObfsIf-eEDwDf-PvhD9-purZT-OiUrBf ObfsIf-eEDwDf-hJDwNd-Clt0zb', 'titles.csv')

    extract_data_to_csv(soup, 'RP7SMd', 'companies.csv')

    extract_data_to_csv(soup, 'pwO9Dc vo5qdf', 'locations.csv')

    extract_data_to_csv(soup, 'wVSTAb', 'difficulties.csv')

##############################
    titles_df = pd.read_csv('titles.csv')
    companies_df = pd.read_csv('companies.csv')
    locations_df = pd.read_csv('locations.csv')
    difficulties_df = pd.read_csv('difficulties.csv')

    result_df = titles_df  
    result_df = pd.concat([titles_df, companies_df, locations_df, difficulties_df], axis=1)
    result_df.columns = ['Titre', 'Societe', 'Location', 'Difficulté']
##############################

    os.remove('titles.csv')
    os.remove('companies.csv')
    os.remove('locations.csv')
    os.remove('difficulties.csv')
##############################

    # result_df.to_csv('google_jobs.csv', index=False)
    result_df.to_excel('google_jobs.xlsx', index=False)
##############################
if __name__ == "__main__":
    main()