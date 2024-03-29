import os
import together
import json
import openai
from pydantic import BaseModel, Field

together_api_key = "26dac6e7a637994fd6e540067bf994c6e859aa517a3ff3794d7078d299cc7e84"
together.api_key = together_api_key 
wandb_api_key = "8b87053f36270a3afddd98e782ced32670927d85"
# define model
m = "togethercomputer/Llama-2-7B-32K-Instruct"
m2 =  "mistralai/Mistral-7B-Instruct-v0.2"

def load_data():
# Upload file
    data_path = "clinicaldata_intervention.jsonl" 
    resp1 = together.Files.check(file=data_path)
    file_resp = together.Files.upload(file=data_path)
    #print(file_resp) 
    file_id = file_resp["id"]
    return file_id
def start_finetune(file_id,model):
    resp = together.Finetune.create(
        training_file = file_id,
        model = model,
            n_epochs = 3,
            n_checkpoints = 1,
            batch_size = 4,
            learning_rate = 1e-5,
            suffix = 'test_510k_intervention',
            wandb_api_key = wandb_api_key
    )

    fine_tune_id = resp['id']
    id = "ft-143dbbbb-6380-415f-b033-156cbd0a349f" 
def deploy(name):
    together.Models.start(name)
    print(together.Models.ready(name))

def inference(description,name,prompt):
    output = together.Complete.create(
        prompt = prompt,
        model = name,
    )
    return output['output']['choices'][0]['text']

"""
# Create client
client = openai.OpenAI(
    base_url = "https://api.together.xyz/v1",
    api_key = together_api_key,
)

# Define the schema for the output.
class Eligibility(BaseModel):
    exclusion_criteria: str = Field(description="exclusion")
    inclusion_criteria: str = Field(description="inclusion")
    
# Generate
chat_completion = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    response_format={
        "type": "json_object", 
        "schema": Eligibility.model_json_schema()
    },
    messages=[
        {"role": "system", "content": "You are a helpful assistant that answers in JSON."},
        {"role": "user", "content": "Create an exclusion and inclusion criteria "}
    ],
)

created_user = json.loads(chat_completion.choices[0].message.content)
print(json.dumps(created_user, indent=2))

"""
def create_prompt(description) :
    prompts = {}
    prompts["eligibility"] = f"""[INST] Write the inclusion and exclusion criterias given this description: {description}[\INST]\n
                    Examples: 

                    input: The study is a prospective, single-arm, non-randomized, non-blinded, non-controlled, non-significant risk, single center study enrolling up to 200 healthy adult subjects consented to undergo an apheresis donation procedure. Subjects will be connected to the Zynex Cardiac Monitor, Model 1500 (CM-1500) to characterize changes in the relative index during an apheresis donation procedure\n
                    output: Inclusion Criteria:\n\nAbility to provide written informed consent\nAbility and willingness to comply with the study procedures and duration requirements\n18 years of age or older\nConsented to undergo an apheresis procedure with an automated blood component device\n\nExclusion Criteria:\n\nFemales who are pregnant or breastfeeding\nUndergone an amputation of the left upper extremity\nDiagnosed with dextrocardia\nSubjects who have a pacemaker\n
                    \n
                    input: Study objectives include assessing the use of Irrisept irrigation solution in lumbar spinal fusion procedures and effect on clinical and patient reported outcome measures. This includes assessing postoperative SSI as well as fusion rates in addition to patient reported outcome measures.\n
                    output: Age 18-85, undergoing primary lumbar spinal fusion (less than or equal to 3 levels)\n\nExclusion Criteria:\n\nPrior lumbar fusion (decompression only okay), spinal infection, spinal neoplasm\n
                    
                    \n
                    input: The purpose of this study is to demonstrate how Moovcare, a mobile medical application, can be used to monitor Patient-Reported Outcomes (PROs) related to cancer treatment, cancer complications, and cancer relapse in patients with lung cancer. PROs are symptoms directly reported by patients through the completion of a survey. Up to 50 patients undergoing treatment and/or surveillance for new or existing diagnoses of lung cancer at the University of North Carolina's Lineberger Comprehensive Cancer Center will be prospectively enrolled to the use of the mobile medical application Moovcare® for 6 months. Moovcare® is not FDA approved, and its role in improving clinical care is being studied through this research. Moovcare® automatically delivers electronic patient reported outcome (ePRO) surveys on common symptoms experienced by lung cancer patients.\n
                    output: "Inclusion Criteria:\n\n18 years or older\n\nDiagnosis of lung cancer (any histology, any stage) undergoing outpatient treatment and/or surveillance/monitoring at UNC.\n\nThis may include stage I and II patients who have completed lung resection and/or are undergoing radiation, stage II and III patients receiving neoadjuvant, adjuvant, or definitive chemotherapy, stage IV patients undergoing active therapy or monitoring, patients undergoing surveillance for treated or untreated stage I-III lung cancer, and both limited and extensive small cell lung cancer. The study team will request the confirmation of the lung cancer diagnosis from the managing clinician. Patients can be enrolled at any point in their lung cancer treatment trajectory (i.e., not just at initiation of first-line treatment) after a diagnosis of lung cancer has been assigned by the treating clinician. This may include patients assigned a diagnosis of lung cancer without a tissue diagnosis.\n\nSpeaks and understands English\nReliable access to the internet and email\nAccess to a mobile phone (or device that can receive text messages for registration)\n\nExclusion Criteria:\n\nDementia, altered mental status, or any psychiatric condition that would prohibit the understanding or rendering of informed consent or completing study procedures\nCurrent participation in other PRO monitoring trials\nInability to read and speak English\nCurrent incarceration\n
                    \n
        """
    example_str = json.dumps({'ArmGroupList': {'ArmGroup': [{'ArmGroupLabel': 'Validation Arm', 'ArmGroupType': 'Experimental', 'ArmGroupDescription': 'Participants will wear the Sparkle device (test device) while instrumented with an esophageal manometry catheter (reference standard) to record respiratory effort.', 'ArmGroupInterventionList': {'ArmGroupInterventionName': ['Device: Sparkle']}}]}, 'InterventionList': {'Intervention': [{'InterventionType': 'Device', 'InterventionName': 'Sparkle', 'InterventionDescription': 'The Sparkle device is a single-use device intended to aid the diagnosis of sleep-disordered breathing; however, this study is intended only to validate the respiratory effort signal and does not assess diagnostic performance.', 'InterventionArmGroupLabelList': {'InterventionArmGroupLabel': ['Validation Arm']}}]}})
    prompts["intervention"] = f"""[INST] Write the interventions section for the clinical trial design of medical devices given this particular device description: {description}[\INST]\n
                    Example: 

                    input: This study has been developed in order to demonstrate the validity of the Sparkle respiratory effort signal
                    output: {example_str}  
                   
                   
        """
    prompts["design"] = f"""[INST] Write the inclusion and exclusion criterias given this description: {description}[\INST]\n
                    Examples: 

                    input: The study is a prospective, single-arm, non-randomized, non-blinded, non-controlled, non-significant risk, single center study enrolling up to 200 healthy adult subjects consented to undergo an apheresis donation procedure. Subjects will be connected to the Zynex Cardiac Monitor, Model 1500 (CM-1500) to characterize changes in the relative index during an apheresis donation procedure\n
                    output: Inclusion Criteria:\n\nAbility to provide written informed consent\nAbility and willingness to comply with the study procedures and duration requirements\n18 years of age or older\nConsented to undergo an apheresis procedure with an automated blood component device\n\nExclusion Criteria:\n\nFemales who are pregnant or breastfeeding\nUndergone an amputation of the left upper extremity\nDiagnosed with dextrocardia\nSubjects who have a pacemaker\n
                    \n
                    input: Study objectives include assessing the use of Irrisept irrigation solution in lumbar spinal fusion procedures and effect on clinical and patient reported outcome measures. This includes assessing postoperative SSI as well as fusion rates in addition to patient reported outcome measures.\n
                    output: Age 18-85, undergoing primary lumbar spinal fusion (less than or equal to 3 levels)\n\nExclusion Criteria:\n\nPrior lumbar fusion (decompression only okay), spinal infection, spinal neoplasm\n
                    
                    \n
                    input: The purpose of this study is to demonstrate how Moovcare®, a mobile medical application, can be used to monitor Patient-Reported Outcomes (PROs) related to cancer treatment, cancer complications, and cancer relapse in patients with lung cancer. PROs are symptoms directly reported by patients through the completion of a survey. Up to 50 patients undergoing treatment and/or surveillance for new or existing diagnoses of lung cancer at the University of North Carolina's Lineberger Comprehensive Cancer Center will be prospectively enrolled to the use of the mobile medical application Moovcare® for 6 months. Moovcare® is not FDA approved, and its role in improving clinical care is being studied through this research. Moovcare® automatically delivers electronic patient reported outcome (ePRO) surveys on common symptoms experienced by lung cancer patients.\n
                    output: "Inclusion Criteria:\n\n18 years or older\n\nDiagnosis of lung cancer (any histology, any stage) undergoing outpatient treatment and/or surveillance/monitoring at UNC.\n\nThis may include stage I and II patients who have completed lung resection and/or are undergoing radiation, stage II and III patients receiving neoadjuvant, adjuvant, or definitive chemotherapy, stage IV patients undergoing active therapy or monitoring, patients undergoing surveillance for treated or untreated stage I-III lung cancer, and both limited and extensive small cell lung cancer. The study team will request the confirmation of the lung cancer diagnosis from the managing clinician. Patients can be enrolled at any point in their lung cancer treatment trajectory (i.e., not just at initiation of first-line treatment) after a diagnosis of lung cancer has been assigned by the treating clinician. This may include patients assigned a diagnosis of lung cancer without a tissue diagnosis.\n\nSpeaks and understands English\nReliable access to the internet and email\nAccess to a mobile phone (or device that can receive text messages for registration)\n\nExclusion Criteria:\n\nDementia, altered mental status, or any psychiatric condition that would prohibit the understanding or rendering of informed consent or completing study procedures\nCurrent participation in other PRO monitoring trials\nInability to read and speak English\nCurrent incarceration\n
                    \n
        """
    prompts["outcomes"] = f"""[INST] Write the inclusion and exclusion criterias given this description: {description}[\INST]\n
                    Examples: 

                    input: The study is a prospective, single-arm, non-randomized, non-blinded, non-controlled, non-significant risk, single center study enrolling up to 200 healthy adult subjects consented to undergo an apheresis donation procedure. Subjects will be connected to the Zynex Cardiac Monitor, Model 1500 (CM-1500) to characterize changes in the relative index during an apheresis donation procedure\n
                    output: Inclusion Criteria:\n\nAbility to provide written informed consent\nAbility and willingness to comply with the study procedures and duration requirements\n18 years of age or older\nConsented to undergo an apheresis procedure with an automated blood component device\n\nExclusion Criteria:\n\nFemales who are pregnant or breastfeeding\nUndergone an amputation of the left upper extremity\nDiagnosed with dextrocardia\nSubjects who have a pacemaker\n
                    \n
                    input: Study objectives include assessing the use of Irrisept irrigation solution in lumbar spinal fusion procedures and effect on clinical and patient reported outcome measures. This includes assessing postoperative SSI as well as fusion rates in addition to patient reported outcome measures.\n
                    output: Age 18-85, undergoing primary lumbar spinal fusion (less than or equal to 3 levels)\n\nExclusion Criteria:\n\nPrior lumbar fusion (decompression only okay), spinal infection, spinal neoplasm\n
                    
                    \n
                    input: The purpose of this study is to demonstrate how Moovcare®, a mobile medical application, can be used to monitor Patient-Reported Outcomes (PROs) related to cancer treatment, cancer complications, and cancer relapse in patients with lung cancer. PROs are symptoms directly reported by patients through the completion of a survey. Up to 50 patients undergoing treatment and/or surveillance for new or existing diagnoses of lung cancer at the University of North Carolina's Lineberger Comprehensive Cancer Center will be prospectively enrolled to the use of the mobile medical application Moovcare® for 6 months. Moovcare® is not FDA approved, and its role in improving clinical care is being studied through this research. Moovcare® automatically delivers electronic patient reported outcome (ePRO) surveys on common symptoms experienced by lung cancer patients.\n
                    output: "Inclusion Criteria:\n\n18 years or older\n\nDiagnosis of lung cancer (any histology, any stage) undergoing outpatient treatment and/or surveillance/monitoring at UNC.\n\nThis may include stage I and II patients who have completed lung resection and/or are undergoing radiation, stage II and III patients receiving neoadjuvant, adjuvant, or definitive chemotherapy, stage IV patients undergoing active therapy or monitoring, patients undergoing surveillance for treated or untreated stage I-III lung cancer, and both limited and extensive small cell lung cancer. The study team will request the confirmation of the lung cancer diagnosis from the managing clinician. Patients can be enrolled at any point in their lung cancer treatment trajectory (i.e., not just at initiation of first-line treatment) after a diagnosis of lung cancer has been assigned by the treating clinician. This may include patients assigned a diagnosis of lung cancer without a tissue diagnosis.\n\nSpeaks and understands English\nReliable access to the internet and email\nAccess to a mobile phone (or device that can receive text messages for registration)\n\nExclusion Criteria:\n\nDementia, altered mental status, or any psychiatric condition that would prohibit the understanding or rendering of informed consent or completing study procedures\nCurrent participation in other PRO monitoring trials\nInability to read and speak English\nCurrent incarceration\n
                    \n
        """
    return prompts

def generate_clinical_trial(device):
    prompts = create_prompt(device) 
    eligibility_name = "pkafleprabhakar@gmail.com/Mistral-7B-Instruct-v0.2-test_510k_2-2024-02-18-04-44-40"
    intervention_name = ""
    eligibility = inference(device,eligibility_name,prompts['eligibility'])
    intervention = inference(device,"",prompts['intervention'])
    outcomes = inference(device,"",prompts['outcomes'])
    design = inference(device,"",prompts['design']) 
    return [eligibility,intervention,outcomes,design] 

def generate_eligibility(device):
    prompts = create_prompt(device) 
    eligibility_name = "pkafleprabhakar@gmail.com/Mistral-7B-Instruct-v0.2-test_510k_2-2024-02-18-04-44-40"
    intervention_name = ""
    eligibility = inference(device,eligibility_name,prompts['eligibility'])
    return eligibility



if __name__ == "__main__":
    file_id = load_data()
    # see if you want to finetune
    #start_finetune(file_id,m2)  
    #name = "pkafleprabhakar@gmail.com/Mistral-7B-Instruct-v0.2-test_510k_2-2024-02-18-04-44-40"
    # name of deployed 
    #deploy(name) 
    #print(together.Models.ready(name))
    device =  """
    The Fitbit ECG App is a software-only medical device used to create, record, display, store
    and analyze a single channel ECG. The Fitbit ECG App consists of a Device application
    (“Device app”) on a consumer Fitbit wrist-worn product and a mobile application tile
    (“mobile app”) on Fitbit’s consumer mobile application. The Device app uses data from
    electrical sensors on a consumer Fitbit wrist-worn product to create and record an ECG. The
    algorithm on the Device app analyzes a 30 second recording of the ECG and provides results
    to the user. Users are able to view their past results as well as a pdf report of the waveform
    similar to a Lead I ECG on the mobile app.
    """
    #prompts = create_prompt(device)
    #print(inference(device,name,prompts["eligibility"]))
    generate_eligibility(device)

