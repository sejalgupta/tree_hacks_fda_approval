import json
import pandas as pd
from io import StringIO
# from llm_requests import ask_gpt
import re

def predicates(user_data):  
    """
    Given the device description and intended use, get the similar devices

    Args:
        user_data (dict): two keys with Device Description and Indication for Use

    Returns:
        list: top 3 k numbers of devices that are similar
    """    

    ## TEMPORARY ##  
    return ['K201525', 'K221805']

def get_vector_db_table_information(k_number, section_title):
    """
    Get the table text from the vector db for the predicate

    Args:
        k_number (str): the predicate device's k number
        section_title (str): the section title that has the desired table

    Returns:
        str: The table content in text format
    """  

    ## TEMPORARY ##  
    original = [
      ["IItteemm", "Subject Device", "Predicate Device"],
      [None, "ECG 2.0 App", "ECG App"],
      ["Manufacturer", "Apple Inc.", "Apple Inc."],
      ["Submission\nReference", "K201525", "DEN180044"],
      [None, "ECG 2.0 App", "ECG App"],
      [
        "Intended Use",
        "An electrocardiograph software device\nfor over-the-counter use creates,\nanalyzes, and displays\nelectrocardiograph data, and can\nprovide information for identifying\ncardiac arrhythmias. This device is not\nintended to provide a diagnosis.",
        "An electrocardiograph software device for\nover-the-counter use creates, analyzes, and\ndisplays electrocardiograph data, and can\nprovide information for identifying cardiac\narrhythmias. This device is not intended to\nprovide a diagnosis."
      ],
      [
        "Indications for\nUse",
        "The ECG app is a software-only mobile\nmedical application intended for use\nwith the Apple Watch to create, record,\nstore, transfer, and display a single\nchannel electrocardiogram (ECG)\nsimilar to a Lead I ECG. The ECG app\ndetermines the presence of atrial\nfibrillation (AFib), sinus rhythm, and\nhigh heart rate (no detected AF with\nheart rate 100-150 bpm) on a\nclassifiable waveform. The ECG app is\nnot recommended for users with other\nknown arrhythmias.\nThe ECG app is intended for over-the-\ncounter (OTC) use. The ECG data\ndisplayed by the ECG app is intended\nfor informational use only. The user is\nnot intended to interpret or take clinical\naction based on the device output\nwithout consultation of a qualified\nhealthcare professional. The ECG\nwaveform is meant to supplement\nrhythm classification for the purposes\nof discriminating AFib from sinus\nrhythm and is not intended to replace\ntraditional methods of diagnosis or\ntreatment.\nThe ECG app is not intended for use by\npeople under 22 years old.",
        "The ECG app is a software-only mobile\nmedical application intended for use with\nthe Apple Watch to create, record, store,\ntransfer and display a single channel\nelectrocardiogram (ECG) similar to a Lead\nI ECG. The ECG app determines the\npresence of atrial fibrillation (AF) or sinus\nrhythm on a classifiable waveform. The\nECG app is not recommended for users\nwith other known arrhythmias.\nThe ECG app is intended for over-the-\ncounter (OTC) use. The ECG data\ndisplayed by the ECG app is intended for\ninformational use only. The user is not\nintended to interpret or take clinical action\nbased on the device output without\nconsultation of a qualified healthcare\nprofessional. The ECG waveform is meant\nto supplement rhythm classification for the\npurposes of discriminating AF from normal\nsinus rhythm and not intended to replace\ntraditional methods of diagnosis or\ntreatment.\nThe ECG app is not intended for use by\npeople under 22 years old."
      ],
      [
        "Principle of\nOperation",
        "The ECG 2.0 app acquires platform\nsensor data from Apple Watch. After\nacquisition, the ECG 2.0 app\nalgorithms process and classify the\nsignal and display the classification to\nthe user.",
        "The ECG app acquires platform sensor\ndata from Apple Watch. After acquisition,\nthe ECG app algorithms process and\nclassify the signal and display the\nclassification to the user."
      ],
      [None, "ECG 2.0 App", "ECG App"],
      [
        "ECG Session\nClassification\nResults",
        "- Low Heart Rate (< 50 bpm)\n- Sinus Rhythm (50-99 bpm)\n- High Heart Rate (No AFib) (100-150\nbpm)\n- Atrial Fibrillation (50-99 bpm)\n- Artial Fibrillation High Heart Rate\n(100-150 bpm)\n- Inconclusive\n- Poor Recording\n- High Heart Rate ( > 150 bpm)",
        "- Low Heart Rate (< 50 bpm)\n- Sinus Rhythm (50-100 bpm)\n- Atrial Fibrillation (50-120 bpm)\n- Inconclusive\n- Inconclusive - Poor Recording\n- High Heart Rate ( > 120 bpm)"
      ],
      [
        "Clinical\nApplication",
        "The ECG 2.0 app is intended to\nsupplement rhythm classification for\nthe purposes of discriminating Afib\nfrom normal rhythms. The device is not\nintended to replace traditional methods\nor diagnosis.",
        "The ECG app is intended to supplement\nrhythm classification for the purposes of\ndiscriminating Afib from normal rhythms.\nThe device is not intended to replace\ntraditional methods or diagnosis."
      ],
      [
        "Compatibility\nwith Intended\nPlatforms",
        "iOS version 14.0\nWatchOS version 7.0\nApple Watch Series 4, Apple Watch\nSeries 5\niPhone 6s - iPhone 11 models",
        "iOS 12.1.1 - 14.0.1\nWatchOS 5.1.2 - 7.0.1\nApple Watch Series 4, Apple Watch Series\n5, Apple Watch Series 6\niPhone 5s - iPhone 11 models"
      ]
    ]
    return json.dumps(original)
    
def convert_text_to_table(text):
    """
    Take the text from the vector's metadata and parse into a list of lists

    Args:
        text (str): a json string of a list of lists

    Returns:
        list: list of lists of the predicate information
    """    
    table = json.loads(text)
    return table

def get_ground_truth_table(data):
    """
    Get the version of the comparison to predicate table without any content modifications

    Args:
        data (list): list of lists that contain information about the predicate device

    Returns:
        Pandas Dataframe: dataframe with columns for the Comparison Fields, Predicate Device, Subject Device, Comparison
    """    
    headers = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    # Keep the first two columns
    df = df.iloc[:, :2]

    # Rename the columns
    rename_dict = {df.columns[0]: 'Comparison Fields', df.columns[1]: 'Predicate Device'}
    df.rename(columns=rename_dict, inplace=True)

    # Add in columns for the current device and the comparison
    df["Subject Device"] = None
    df["Comparison"] = None

    return df

def populate_fields_chatgpt(df, device_description, indications_use):
    output = StringIO()
    df.to_csv(output, index=False)  # Set index=False to exclude row indices in the output
    csv_string = output.getvalue()

    print(csv_string)

    # prompt = f"""I have a table that compares a subject device to a predicate device on a number of conditions. 
    
    # Here is the current version of the table: {csv_string}

    # Currently, the table is missing information about the subject device and the comparison between the predicate and subject devices. 

    # This is the known information about the subject device:
    # 1. Device Description: {device_description}
    # 2. Indications for Use: {indications_use}

    # Can you please output only an updated version of the table with filling any missing fields with the given information? The format of your output should be in this format {csv_string}
    # """

    # response = ask_gpt(prompt)
    # answer_csv_string = response["choices"][0]["message"]["content"]

    # print(answer_csv_string)
    
    # csv_buffer = StringIO(answer_csv_string)
    # new_df = pd.read_csv(csv_buffer)

    return df

if __name__ == "__main__":
    
    device_description = "The Fitbit ECG App is a software-only medical device used to create, record, display, store and analyze a single channel ECG. The Fitbit ECG App consists of a Device application (“Device app”) on a consumer Fitbit wrist-worn product and a mobile application tile (“mobile app”) on Fitbit’s consumer mobile application. The Device app uses data from electrical sensors on a consumer Fitbit wrist-worn product to create and record an ECG. The algorithm on the Device app analyzes a 30 second recording of the ECG and provides results to the user. Users are able to view their past results as well as a pdf report of the waveform similar to a Lead I ECG on the mobile app."
    indications_for_use = "The Fitbit ECG App is a software-only mobile medical application intended for use with Fitbit wrist-wearable devices to create, record, store, transfer, and display a single channel electrocardiogram (ECG) qualitatively similar to a Lead I ECG. The Fitbit ECG App determines the presence of atrial fibrillation (AFib) or sinus rhythm on a classifiable waveform. The AF detection function is not recommended for users with other known arrhythmias. The Fitbit ECG App is intended for over-the-counter (OTC) use. The ECG data displayed by the Fitbit ECG App is intended for informational use only. The user is not intended to interpret or take clinical action based on the device output without consultation of a qualified healthcare professional. The ECG waveform is meant to supplement rhythm classification for the purposes of discriminating AFib from normal sinus rhythm and not intended to replace traditional methods of diagnosis or treatment. The Fitbit ECG App is not intended for use by people under 22 years old."
    
    # from 510k copy paste
    original = [
      ["IItteemm", "Subject Device", "Predicate Device"],
      [None, "ECG 2.0 App", "ECG App"],
      ["Manufacturer", "Apple Inc.", "Apple Inc."],
      ["Submission\nReference", "K201525", "DEN180044"],
      [None, "ECG 2.0 App", "ECG App"],
      [
        "Intended Use",
        "An electrocardiograph software device\nfor over-the-counter use creates,\nanalyzes, and displays\nelectrocardiograph data, and can\nprovide information for identifying\ncardiac arrhythmias. This device is not\nintended to provide a diagnosis.",
        "An electrocardiograph software device for\nover-the-counter use creates, analyzes, and\ndisplays electrocardiograph data, and can\nprovide information for identifying cardiac\narrhythmias. This device is not intended to\nprovide a diagnosis."
      ],
      [
        "Indications for\nUse",
        "The ECG app is a software-only mobile\nmedical application intended for use\nwith the Apple Watch to create, record,\nstore, transfer, and display a single\nchannel electrocardiogram (ECG)\nsimilar to a Lead I ECG. The ECG app\ndetermines the presence of atrial\nfibrillation (AFib), sinus rhythm, and\nhigh heart rate (no detected AF with\nheart rate 100-150 bpm) on a\nclassifiable waveform. The ECG app is\nnot recommended for users with other\nknown arrhythmias.\nThe ECG app is intended for over-the-\ncounter (OTC) use. The ECG data\ndisplayed by the ECG app is intended\nfor informational use only. The user is\nnot intended to interpret or take clinical\naction based on the device output\nwithout consultation of a qualified\nhealthcare professional. The ECG\nwaveform is meant to supplement\nrhythm classification for the purposes\nof discriminating AFib from sinus\nrhythm and is not intended to replace\ntraditional methods of diagnosis or\ntreatment.\nThe ECG app is not intended for use by\npeople under 22 years old.",
        "The ECG app is a software-only mobile\nmedical application intended for use with\nthe Apple Watch to create, record, store,\ntransfer and display a single channel\nelectrocardiogram (ECG) similar to a Lead\nI ECG. The ECG app determines the\npresence of atrial fibrillation (AF) or sinus\nrhythm on a classifiable waveform. The\nECG app is not recommended for users\nwith other known arrhythmias.\nThe ECG app is intended for over-the-\ncounter (OTC) use. The ECG data\ndisplayed by the ECG app is intended for\ninformational use only. The user is not\nintended to interpret or take clinical action\nbased on the device output without\nconsultation of a qualified healthcare\nprofessional. The ECG waveform is meant\nto supplement rhythm classification for the\npurposes of discriminating AF from normal\nsinus rhythm and not intended to replace\ntraditional methods of diagnosis or\ntreatment.\nThe ECG app is not intended for use by\npeople under 22 years old."
      ],
      [
        "Principle of\nOperation",
        "The ECG 2.0 app acquires platform\nsensor data from Apple Watch. After\nacquisition, the ECG 2.0 app\nalgorithms process and classify the\nsignal and display the classification to\nthe user.",
        "The ECG app acquires platform sensor\ndata from Apple Watch. After acquisition,\nthe ECG app algorithms process and\nclassify the signal and display the\nclassification to the user."
      ],
      [None, "ECG 2.0 App", "ECG App"],
      [
        "ECG Session\nClassification\nResults",
        "- Low Heart Rate (< 50 bpm)\n- Sinus Rhythm (50-99 bpm)\n- High Heart Rate (No AFib) (100-150\nbpm)\n- Atrial Fibrillation (50-99 bpm)\n- Artial Fibrillation High Heart Rate\n(100-150 bpm)\n- Inconclusive\n- Poor Recording\n- High Heart Rate ( > 150 bpm)",
        "- Low Heart Rate (< 50 bpm)\n- Sinus Rhythm (50-100 bpm)\n- Atrial Fibrillation (50-120 bpm)\n- Inconclusive\n- Inconclusive - Poor Recording\n- High Heart Rate ( > 120 bpm)"
      ],
      [
        "Clinical\nApplication",
        "The ECG 2.0 app is intended to\nsupplement rhythm classification for\nthe purposes of discriminating Afib\nfrom normal rhythms. The device is not\nintended to replace traditional methods\nor diagnosis.",
        "The ECG app is intended to supplement\nrhythm classification for the purposes of\ndiscriminating Afib from normal rhythms.\nThe device is not intended to replace\ntraditional methods or diagnosis."
      ],
      [
        "Compatibility\nwith Intended\nPlatforms",
        "iOS version 14.0\nWatchOS version 7.0\nApple Watch Series 4, Apple Watch\nSeries 5\niPhone 6s - iPhone 11 models",
        "iOS 12.1.1 - 14.0.1\nWatchOS 5.1.2 - 7.0.1\nApple Watch Series 4, Apple Watch Series\n5, Apple Watch Series 6\niPhone 5s - iPhone 11 models"
      ]
    ]

    text = json.dumps(original)
    table = convert_text_to_table(text)
    df = get_ground_truth_table(table)

    new_df = populate_fields_chatgpt(df, device_description, indications_for_use)

    try:
        new_df = populate_fields_chatgpt(df, device_description, indications_for_use)
    except:
        new_df = df

    print(new_df)