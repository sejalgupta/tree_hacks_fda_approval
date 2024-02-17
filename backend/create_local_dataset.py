from helper_code.extract_510k import get_k_numbers, get_pdf_link
from helper_code.extract import download_pdf_to_file
import pandas as pd
import os
import time 
import random
import csv

def load_pd_frame(csv_filename):

    # Check if the CSV file exists
    if os.path.exists(csv_filename):
        # Load the DataFrame from the CSV file
        df = pd.read_csv(csv_filename)
        print(f"Loaded DataFrame from {csv_filename}")
    else:
        # Initialize an empty DataFrame with the desired columns if CSV doesn't exist
        df_columns = ["k_number", "url", "download_pdf_to_file", "product_code", "nct_code", "pdf_filename"]
        df = pd.DataFrame(columns=df_columns)
        save_df(df, csv_filename)
        print("Initialized new DataFrame")

    return df

def get_dataset(k_numbers, df, start_index, end_index, csv_filename, indices_visited_filename):
    for i in range(start_index, end_index):
        k_number = k_numbers[i]
        print("k num", k_number)
        print("index", i)
        
        info = get_pdf_link(k_number)
        random_integer = random.randint(5, 15)
        time.sleep(random_integer)

        if info is None:
            print("no info found")
        elif "summary_url" in info:
            pdf_filename = "./pdfs/" + k_number[0] + ".pdf"
            pdf_file = download_pdf_to_file(info["summary_url"], pdf_filename)
            random_integer = random.randint(5, 15)
            time.sleep(random_integer)

            if pdf_file:
                # Add the information to the DataFrame
                info_to_insert = info.copy()  # Make a copy to avoid modifying the original
                info_to_insert["pdf_filename"] = pdf_filename  # Add the PDF filename to the info
                df = pd.concat([df, pd.DataFrame([info_to_insert])], ignore_index=True)
                save_df(df, csv_filename)
                print("GOT IT")
            else:
                print("download failed - pdf file not found")
        else:
            print("no summary url")
        
        # Open the CSV file in append mode ('a') so we can add to it without overwriting existing content
        with open(indices_visited_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write the new row to the CSV file
            writer.writerow([str(i)])
    return df

def save_df(df, csv_filename):
    df.to_csv(csv_filename, index=False)
    print(f"DataFrame saved to {csv_filename}")


if __name__ == "__main__":

    #MAKE SURE TO CREATE A /pdfs FOLDER IN THE DIRECTORY
    start = 0 #FILL IN
    end = 0 #FILL IN
    start = 6000
    end = 10000

    csv_filename = "./data/pdf_dataset.csv"

    df = load_pd_frame(csv_filename)

    k_filename = "./data/k_numbers.csv"
    k_numbers = get_k_numbers(k_filename)

    indices_visited_filename = "index_done.csv"

    df = get_dataset(k_numbers, df, start, end, csv_filename, indices_visited_filename)

    # Save the DataFrame to a CSV file
    save_df(df, csv_filename)