import json
from PIL import Image
import fitz
# from nltk.metrics import jaccard_distance
# from nltk.util import ngrams
import requests

HEADERS = [
    ["Predicate Devices"],
    ["Device Description"],
    ["Indications for use"],
    [
        "Comparison with Predicate Device",
        "Comparison with Technological Characteristics",
        "Substantial Equivalence"
    ],
    ["Technological Characteristics"],
    ["Performance Data"],
    ["Conclusion"]
]
HEADERS_OF_INTEREST = [header[0] for header in HEADERS[:4]]
# Anything before `510(k) summary` header is FDA's cover letter
start_at = "510(k) summary"
# Right now we are not concerned with any content beyond this.
# If we have a final list of all possible headers, this will be more effective
break_at = [
] 

# add a delay in between requests 
def download_pdf_to_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        return None

def jaccard_similarity(word1, word2):
    # set1 = set(ngrams(word1.lower(), n=2))
    # set2 = set(ngrams(word2.lower(), n=2))
    # return 1 - jaccard_distance(set1, set2)
    pass

def show_page(page):
    pix = page.get_pixmap()
    
    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    img.show()

def extract_text_from_page(page, pdf_data, start):
    current_section = pdf_data[-1]
    text = page.get_text("dict", sort=True)["blocks"]
    new_headers = []
    
    done = False
    for block in text:
        if block['type'] != 0:
            continue
        for line in block['lines']:
            for span in line['spans']:
                if "font" in span and "bold" in span['font'].lower():# and \
                        # len(line['spans']) == 1: # Get all potential headers
                    if current_section['title'] == "Predicate Devices":
                        print("span: ", span['text'])
                    if not start:
                        if jaccard_similarity(start_at, span['text']) > 0.8:
                            print("Starting at", span["text"])
                            start = True
                        break
                    print(f"Potential header: {span['text']}")
                    for w in break_at:
                        if jaccard_similarity(w, span['text']) > 0.6:
                            print("Breaking at", span["text"])
                            done = True
                            break
                    if done:
                        break
                    match_header = False
                    for header in HEADERS:
                        for option in header:
                            if jaccard_similarity(option, span['text']) > 0.5:
                                print("header: ", option, "span: ", span['text'])
                                current_section = {"title": header[0], "text": "", "type": "text"}
                                pdf_data.append(current_section)
                                new_headers.append({"text": header[0], "bbox": span["bbox"]})
                                match_header = True
                                break
                        if match_header:
                            break
                current_section['text'] += span['text'] + " "
            current_section['text'] += "\n"
            if done:
                break
        current_section['text'] += "\n"
        if done:
            break
    
    return done, new_headers

def integrate_tables(page, tables, table_data, page_headers, prev_header, continue_from_last=False):
    current_table = table_data[-1]
    h, w = page.rect.height, page.rect.width
    if not tables.tables:
        return False
    for tab in tables.tables:
        r = fitz.Rect(*tab.bbox)
        page.draw_rect(r, color=(1, 1, 1), fill=(1,1,1))
        tab_data = tab.extract()
        if continue_from_last and len(tab_data[0]) == len(current_table["text"][0]) and tab.bbox[1] < 200: # Same number of column
            add_first_row = 0 if tab.header.external else 1 # If has header, we dont want to add that cause already has
            current_table["text"].extend(tab_data[add_first_row:])
            continue_from_last = tab.bbox[3] > h - 200 # Probably the last element in the page so continue
            continue
        title = prev_header # Base case
        for header in page_headers:
            if tab.bbox[1] > header['bbox'][1]: # We want to get the last header before the table
                title = header['text']
            else:
                break
        table_data.append({"title": title, "text": tab_data, "type": "table"})
        continue_from_last = tab.bbox[3] > h - 200 # Probably the last element in the page so continue
    return continue_from_last


def extract_content_from_pdf(pdf_file):
    print(pdf_file)
    text_data = [{"title": "", "text": "", "type": "text"}]
    table_data = [{"title": "", "text": [], "type": "table"}]
    headers = [{"text": "", "bbox": (0, 0, 0, 0)}]

    # Open the PDF file
    pdf_document = fitz.open(pdf_file)

    start = True
    continue_table = False
    # Iterate through each page in the PDF; ignore first page- it is most probably cover letter
    for page_num in range(1, pdf_document.page_count):
        print("----- Page: {} -----".format(page_num))
        page = pdf_document[page_num]
        if page.search_for("FORM FDA 3881"):
            print("Skipping cover letter page")
            continue
        page_tables = page.find_tables(strategy='lines_strict')
        for tab in page_tables.tables:
            r = fitz.Rect(*tab.bbox)
            page.add_redact_annot(r)
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
        
        done, new_headers = extract_text_from_page(page, text_data, start)
        new_headers = [{"text": header["text"], "bbox": header["bbox"]} for header in new_headers]
        continue_table = integrate_tables(page, page_tables, table_data, new_headers, headers[-1]["text"], continue_table)
        headers += new_headers

        if done:
            break
    
    pdf_data = []
    for section in table_data + text_data:
        # if section["title"] != "":
        if section["title"] in HEADERS_OF_INTEREST:
            section["text"] = str(section["text"])
            pdf_data.append(section)
        
    # Close the PDF file
    pdf_document.close()
    print("headers: ", headers)
    # print("Data", sections_of_interest)
    return pdf_data


if __name__ == "__main__":
    url = 'https://www.accessdata.fda.gov/cdrh_docs/pdf23/K232986.pdf'  # Replace with the URL of your PDF
    # pdf_file = download_pdf(url)
    pdf_file = "./data/K231531.pdf"


    if pdf_file:
        extracted_text = extract_content_from_pdf(pdf_file)
        print(extracted_text)
        #extracted_tables = extract_tables_from_pdf(pdf_file)
        with open("extracted_text.json", "w") as file:
            json.dump(extracted_text, file)
    else:
        print("Failed to download the PDF.")

