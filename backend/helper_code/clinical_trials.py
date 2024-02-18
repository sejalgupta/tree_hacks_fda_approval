
import requests
import json

def fetch_clinical_trials(rank):
    # Send a GET request to the URL
    url = f'https://classic.clinicaltrials.gov/api/query/full_studies?expr=AREA[IsUnapprovedDevice]Yes OR AREA[IsFDARegulatedDevice]Yes&min_rnk={rank}&max_rnk={rank+1}&fmt=json'
    response = requests.get(url)
    # Check if the request was successful
    
    if response.status_code == 200:
        try:
            # Parse the response content as JSON 
            data = response.json() 
            protocol = data['FullStudiesResponse']['FullStudies'][0]['Study']["ProtocolSection"]
            description = protocol["DescriptionModule"]["BriefSummary"]
            eligibility = protocol['EligibilityModule']['EligibilityCriteria']
            design = protocol['DesignModule'] 
            intervention = protocol["ArmsInterventionsModule"] # experimental and control 
            outcomes= protocol['OutcomesModule']
            identification = protocol["IdentificationModule"]["BriefTitle"] 
            clinical_trial = {"Eligibility":eligibility,"Study Design":design,"Intervention": intervention,"Outcomes": outcomes}
                # change the data format 
            prompt = {"text": f"[INST] Write a clinical trial device design given this description: {description} [\INST] {design}"}
            
            return prompt 
        except ValueError:
            # In case the response is not in JSON format
            return
            #return "The response could not be parsed as JSON."
    else:
        return
        # If the request was unsuccessful
        #return f"Request failed with status code: {response.status_code}"

# Example usage
# for all create a template of "prompt" 
    
#ncts = ["NCT03635190","NCT04176926","NCT05266235","NCT05693168"]
rank=0 
file_path = 'clinicaldata.jsonL'
while rank<=2000:
    result = fetch_clinical_trials(rank)
    with open(file_path, 'a') as file:
        # Convert the Python dictionary to a JSON string and write it to the file
        json_string = json.dumps(result)
        file.write(json_string + '\n')
    rank+=1 
    

# Writing data to a JSONL file


    # continuous learning (can put slight weight on more soon)
#print(fetch_clinical_trials())
    