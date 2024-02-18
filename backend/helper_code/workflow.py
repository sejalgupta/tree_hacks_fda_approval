
#from tabula import read_pdf
import json


statement_before = "have to mention why something isn't applicable"
fda_steps = {"IDE_Application": "An investigational device exemption (IDE) allows the investigational device to be used in a clinical study in order to collect safety and effectiveness data. Clinical studies are most often conducted to support a PMA. Only a small percentage of 510(k)s require clinical data to support the application.",
            "Submission Type":"Identification of key information that may be useful to FDA in the initial processing and review of the 510(k) submission, including content from current Form FDA 3514, Section A. 23",
            "Cover Letter": "Attach a cover letter and any documents that refer to other submissions. ",
            "Applicant Information": "Information on the applicant and correspondent, if applicable, consistent with content from current Form FDA 3514, Sections B and C. ",
            "Pre-Submission Correspondence": "Information on prior submissions for the same device included in the current submission, such as submission numbers for a prior not substantially equivalent (NSE) determination, prior deleted or withdrawn 510(k), Q-Submission, Investigational Device Exemption (IDE) application, premarket approval (PMA) application, humanitarian device exemption (HDE) application, or De Novo classification request. ",
            "Consensus Standards": "Identification of voluntary consensus standard(s) used, if applicable. This includes both FDA-recognized and nonrecognized consensus standards. ",
            "Device Description":"Identification of listing number if listed with FDA. Descriptive information for the device, including a description of the technological characteristics of the device including materials, design, energy source, and other device features, as defined in section 513(i)(1)(B) of the FD&C Act and 21 CFR 807.100(b)(2)(ii)(A). Descriptive information also includes a description of the principle of operation for achieving the intended effect and the proposed conditions of use, such as surgical technique for implants; anatomical location of use; user interface; how the device interacts with other devices; and/or how the device interacts with the patient.Information on whether the device is intended to be marketed with accessories. Identification of any applicable device-specific guidance document(s) or special controls for the device type as provided in a special controls document (or alternative measures identified that provide at least an equivalent assurance of safety and effectiveness) or in a device-specific classification regulation, and/or performance standards. See “The 510(k) Program: Evaluating Substantial Equivalence in Premarket Notifications [510(k)].”26",
            "Proposed Indications for Use": "Identification of the proposed indications for use of the device. The term indications for use, as defined in 21 CFR 814.20(b)(3)(i), describes the disease or condition the device will diagnose, treat, prevent, cure, or mitigate, including a description of the patient population for which the device is intended.28 The whole goal of this section is to be a summary of the rest of your submission and includesinformation from the cover letter as well as a summary of the substantial equivalence comparisonand of the testing that was performed.",
            "Classification": "Identification of the classification regulation number that seems most appropriate for the subject device, as applicable.",
            "Predicates and Substantial Equivalence": "Identification of a predicate device (e.g., 510(k) number, De Novo number, reclassified PMA number, classification regulation reference, if exempt and limitations to exemption are exceeded, or statement that the predicate is a preamendments device). The submission should include a comparison of the predicate and subject device and a discussion why any differences between the subject and predicate do not impact safety and effectiveness [see section 513(i)(1)(A) of the FD&C Act and 21 CFR 807.87(f)]. A reference device should also be included in the discussion, if applicable. See “The 510(k) Program: Evaluating Substantial Equivalence in Premarket Notifications [510(k)].”31",
            "Design/Special Controls, Risks to Health, and Mitigation Measures": "Applicable to Special 510(k) submissions only. Identification of the device changes and the risk analysis method(s) used to assess the impact of the change(s) on the device and the results of the analysis. Risk control measures to mitigate identified risks (e.g., labeling, verification). See “The Special 510(k) Program.”32",
            "Labeling": "Submission of proposed labeling in sufficient detail to satisfy the requirements of 21 CFR 807.87(e). Generally, if the device is an invitro diagnostic device, the labeling must also satisfy the requirements of 21 CFR 809.10. Additionally, the term “labeling” generally includes the device label, instructions for use, and any patient labeling. See “Guidance on Medical Device Patient Labeling.”34",
            "Reprocessing": "Information for assessing the reprocessing validation and labeling, if applicable. See “Reprocessing Medical Devices in Health Care Settings: Validation Methods and Labeling.”35",
            "Sterility": "Information on sterility and validation methods, if applicable. See “Submission and Review of Sterility Information in Premarket Notification (510(k)) Submissions for Devices Labeled as Sterile.”36" ,
            "Shelf Life": "Summary of methods used to establish that device performance is maintained for the entirety of the proposed shelf-life37 (e.g., mechanical properties, coating integrity, pH, osmolality) ",
            "Biocompatibility": "Information on the biocompatibility assessment of patient contacting materials, if applicable. See “Use of International Standard ISO 10993-1, ‘Biological evaluation of medical devices - Part 1: Evaluation and testing within a risk management process.’”38",
            "Software/Firmware": "Submission of applicable software documentation, if applicable. See “Guidance for the Content of Premarket Submissions for Software Contained in Medical Devices.”39",
            "Cybersecurity/Interoperability": "Submission of applicable information regarding the assessment of cybersecurity, if applicable. See “Content for Premarket Submissions for Management of Cybersecurity in Medical Devices” and “Design Considerations and Premarket Submission Recommendations for Interoperable Medical Devices.”41",
            "Electromagnetic Compatibility (EMC)": "Submission of the EMC, Electrical, Mechanical, Wireless and Thermal Safety testing for your device or summarize why testing is not needed. See “Electromagnetic Compatibility (EMC) of Medical Devices”42 and “Radio Frequency Wireless Technology in Medical Devices.”43",
            "Performance Testing-(bench)": "For non-in vitro diagnostic devices: Provide information on the non-clinical test reports submitted, referenced, or relied on in the 510(k) for a determination of substantial equivalence. For in vitro diagnostic devices: Provide analytical performance, comparison studies, reference range/expected values, and clinical study information. ",
            "Performance Testing-(animal)": "Provide information on animal testing",
            "Performance Testing-(clinical)": "Provide information on clinical testing",
            "References": "Inclusion of any literature references, if applicable.",
            "Administrative Documentation ": "Inclusion of additional administrative forms applicable to the submission, including but not limited to a general summary of submission/executive summary (recommended), a Truthful and Accuracy Statement, 45 and a 510(k) Summary46 or statement. 47",
            "Amendment/Additional Information (AI) response": "Inclusion of responses to Additional Information requests.48"
            }
# first element is name, second element is link 
Guidance_docs = {
                "IDE_Application": ["IDE Guidance","https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-812"],
                "Submission Type": ["Submission Guidance", "https://www.fda.gov/media/72421/download"],
                "Consensus Standards": ["Consensus Guidance", "https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/standards-and-conformity-assessment-program."],
                "Proposed Indications for Use": ["Indication for Use Guidance","https://www.fda.gov/media/124401/download"],
                 "Software/Firmware": ["Software Guidance", "https://www.fda.gov/media/153781/download"],
                 "Classification": ["Classification Guidance", "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-807/subpart-E/section-807.87"],
                 "Electromagnetic Compatibility (EMC)": ["EMC testing guidance", "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/detail.cfm?standard__identification_no=41539"],
                 "Performance Testing-(clinical)": ["Clinical Guidance", "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/cfrsearch.cfm?fr=820.30"],
}

Condition = {"IDE_Application":"Is your device considered a significant risk?",
            "Shelf Life": "Do you have applicable product testing to demonstrate performance over the stated shelf life. This oftenincludes accelerated age testing?",
             "Biocompatibility": "Do you have anything that is in direct or indirect patient contact?",
             "Software/Firmware": "Does your device have software or electrical components?",
             "Electromagnetic Compatibility (EMC)":"Does your device have electrically powered components, regardless of whether those components are in patient contact or not",
             "Performance Testing-(animal)": "Do you need to do animal testing?",
             "Performance Testing-(bench)": "See “Recommended Content and Format of NonClinical Bench Performance Testing Information in Premarket Submissions.”"
             }
#print(fda_steps)
#tables = read_pdf("docs/workflow.pdf",pages=all)
#tables[0] 
responses = []

def generate_all_workflows():
    # create all pathways 
    for x in fda_steps:
        if (x in Condition):
            print(x)
            print("yes") 
            #render_condition(Condition[x]) # this means create a line from top section to yes section and yes in the line or green to denote yes in the line and no goes directly to next section 
        #render(x) # X should be the name of the field + 
responses = {"IDE_Application": "yes",
             "Shelf Life":"yes",
             "BiocompatBiocompatibilityability":"yes",
             "Software/Firmware": "yes",
             "Electromagnetic Compatibility (EMC), Electrical, Mechanical, Wireless and Thermal Safety": "yes",
             "Performance Testing-(animal)": "no",
             "Performance Testing-(bench)": "no"
}

# assume responses is in ["question":response]
def generate_your_workflow(responses):
    for step in fda_steps:
        if (step in Condition):
            answer = responses[step] 
            if answer == "yes": 
                print("yes highlight") # you can highlight 
            else:
                print("no highlight")
        else:
            # highlight line beneath it 
            print("branch right under")
            

    
    #if x in responses: 
        #print("yes")# go through conditions and make all those lines much bigger based on yes vs no  
# generate_all_workflows()
            
if __name__ == "__main__":
    descriptions = {
        "steps": {}, # {description: str, guidance: {name: str, link: str}, condition: int}
        "conditions": [] # str
    }
    for title in Condition:
        descriptions["conditions"].append(Condition[title])
    for title in fda_steps:
        descriptions["steps"][title] = {
            "description": fda_steps[title],
            "guidance": {"name": Guidance_docs[title][0], "link": Guidance_docs[title][1]} if title in Guidance_docs else None,
            "condition": descriptions["conditions"].index(Condition[title]) if title in Condition else None
        }
    with open("workflow.json", "w") as f:
        json.dump(descriptions, f, indent=4)