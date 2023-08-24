from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import csv
import numpy as np
import os

def salaryPD(content):

    with open('salary.csv', 'w') as output:
        for head in content:
            output.write(head.get_text('span').replace('span','\n').replace('USD','\n'))

    df=pd.read_fwf('salary.csv')

    even_df = df.iloc[1::2].reset_index(drop=True)
    # even_df.columns = ['The ']

    odd_df = df.iloc[::2].reset_index(drop=True)
    # odd_df.columns = ['Salary']

   
    # df = pd.concat([even_df+ odd_df], axis=1, ignore_index=True)
    # df = pd.DataFrame(df)
 
    df=even_df+' '+odd_df
    df.to_csv('salary.csv',index=None)

    return 'salary.csv'


file='./Data/General.html'
with open(file, 'r', encoding='utf-8') as file:
    content = file.read()
soup = BeautifulSoup(content, 'html.parser')

salary=soup.find_all('span',class_='job-search-card__salary-info')
Final_Salary=salaryPD(salary)


# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# def linkedin_salary_scraper(search_query, location):
#     base_url = "https://www.linkedin.com/jobs/search/"
#     params = {
#         "keywords": search_query,
#         "location": location,
#     }

#     salary_listings = []

#     response = requests.get(base_url, params=params)
#     soup = BeautifulSoup(response.content, "html.parser")

#     listings = soup.find_all("li", class_="result-card")
#     for listing in listings:
#         job_title = listing.find("h3", class_="result-card__title").text.strip()
#         company = listing.find("h4", class_="result-card__subtitle").text.strip()
#         location = listing.find("span", class_="job-result-card__location").text.strip()

#         salary_info = listing.find("span", class_="job-search-card__salary-info")
#         if salary_info:
#             salary = salary_info.text.strip()
#         else:
#             salary = "Not provided"

#         salary_listings.append({
#             "Job Title": job_title,
#             "Company": company,
#             "Location": location,
#             "Salary": salary,
#         })

#     return salary_listings

# if __name__ == "__main__":
#     search_query = "Python Developer"  # Change this to your desired job title
#     location = "New York"  # Change this to your desired location
#     salaries = linkedin_salary_scraper(search_query, location)

#     df = pd.DataFrame(salaries)

#     file_name = f"{search_query}_{location}_salaries.xlsx"
#     df.to_excel(file_name, index=False)

#     print(f"Scraped salary information saved to {file_name}")