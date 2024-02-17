import json
import csv

def get_fda_k_numbers():
    file_name = './data/device-510k-0001-of-0001.json'

    # Open and read the JSON file
    with open(file_name, 'r') as file:
        data = json.load(file)

    all_device_data = data['results']

    k_numbers = [["K Number"]]

    for device in all_device_data:
        k_numbers.append([device["k_number"]])

    return k_numbers

def write_csv(k_numbers, filename):
    # Writing to csv file
    with open(filename, 'w', newline='') as csvfile:
        # Creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # Writing the data
        csvwriter.writerows(k_numbers)

    print(f"Data has been written to {filename}")

if __name__ == "__main__":
    k_numbers = get_fda_k_numbers()

    write_csv(k_numbers, 'k_numbers.csv')