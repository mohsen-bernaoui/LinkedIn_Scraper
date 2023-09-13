from bs4 import BeautifulSoup
import pandas as pd
import os

def create_empty_csv(file_name):
    df = pd.DataFrame(columns=['Placeholder'])
    df.to_csv(file_name, index=False)

# Define a function to extract data and save it to a CSV file
def extract_data_to_csv(soup, class_name, file_name):
    data = [element.get_text() for element in soup.find_all('span', class_=class_name)]
    df = pd.DataFrame(data, columns=['Data'])
    df.to_csv(file_name, index=False)

def main():
    # Define the input file containing HTML data
    input_file = 'Data/Google_Careers.html'

    # Read the HTML file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(content, 'html.parser')

    # Extract and save job titles to CSV
    extract_data_to_csv(soup, 'QJPWVe', 'titles.csv')

    # Extract and save company names to CSV
    extract_data_to_csv(soup, 'RP7SMd', 'companies.csv')

    # Extract and save locations to CSV
    extract_data_to_csv(soup, 'pwO9Dc vo5qdf', 'locations.csv')

    # Extract and save difficulty levels to CSV
    extract_data_to_csv(soup, 'wVSTAb', 'difficulties.csv')

    # Read the extracted CSV files
    titles_df = pd.read_csv('titles.csv')
    companies_df = pd.read_csv('companies.csv')
    locations_df = pd.read_csv('locations.csv')
    difficulties_df = pd.read_csv('difficulties.csv')

    # Concatenate the DataFrames (verify that they have the same number of rows)
    result_df = titles_df  # Initialize with titles_df

    # Concatenate other DataFrames
    result_df = pd.concat([titles_df, companies_df, locations_df, difficulties_df], axis=1)

    # Remove temporary CSV files
    os.remove('titles.csv')
    os.remove('companies.csv')
    os.remove('locations.csv')
    os.remove('difficulties.csv')

    # Save the concatenated DataFrame to CSV and Excel
    # result_df.to_csv('google_jobs.csv', index=False)
    result_df.to_excel('google_jobs.xlsx', index=False)

if __name__ == "__main__":
    main()
