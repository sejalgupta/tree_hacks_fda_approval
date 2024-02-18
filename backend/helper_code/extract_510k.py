import csv
import os
import json
import re
import requests
from bs4 import BeautifulSoup
from .save_k_numbers import get_fda_k_numbers, write_csv

def get_k_numbers(filename):
    k_numbers = []

    if not os.path.exists('./'+filename):
        k_numbers = get_fda_k_numbers()
        write_csv(k_numbers, filename)
    else:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for i, row in enumerate(csv_reader):
                if i != 0: k_numbers.append(row)
    
    return k_numbers

def generate_url(k_number):
    url = 'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=' + str(k_number[0])
    return url

def get_pdf_link(k_number):
    url = generate_url(k_number)

    # print(url)
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        summary = soup.find_all(lambda tag: tag.name == 'a' and tag.get_text() == 'Summary')

        href_link = summary[0]['href'] if summary and summary[0].has_attr('href') else None
        
        # Find the 'Classification Product Code' <th> tag
        product_code_th = soup.find('th', string='Classification Product Code')
        product_code_a = product_code_th.find_next_sibling('td').find('a') if product_code_th else None
        product_code = product_code_a.get_text() if product_code_a else None

        # Find the 'Clinical Trials' <th> tag
        clinical_trials_th = soup.find('th', string='Clinical Trials')
        clinical_trials_a = clinical_trials_th.find_next_sibling('td').find('a') if clinical_trials_th else None
        nct_code = clinical_trials_a.get_text() if clinical_trials_a else None


        if href_link is None: 
            return None
        
        info = {
            "k_number": k_number[0],
            "url": url,
            "summary_url": href_link,
            "product_code": product_code,
            "nct_code": nct_code
        }
        return info
    else:
        print("ERROR GETTING TO WEBSITE")

    print("no info found")
    return None
        
def get_all_links(k_numbers, max_num = 10):

    print("got k numbers!")

    links = []
    count = 0
    for num in k_numbers:
        pdf_link = get_pdf_link(num)

        if pdf_link is not None: 
            links.append(pdf_link)
            count += 1
            print("Count", count)
       
        if count >= max_num:
            return links
    
    return links

def save_pdf_links(input_filename, output_filename):
    '''
    UPDATE THIS FUNCTION!!!
    '''

    k_numbers = get_k_numbers(input_filename)
    links = get_all_links(k_numbers)

    with open(output_filename, 'w') as file:
        json.dump(links, file, indent=4)

    print(f"Data saved to {output_filename}")

if __name__ == "__main__":
    pdf_links = get_all_links("k_numbers.csv")
    save_pdf_links("k_numbers.csv", "510k_pdf_links")
