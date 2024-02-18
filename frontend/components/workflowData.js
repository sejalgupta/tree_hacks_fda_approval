const WorkflowData = {
    "steps": {
        "IDE_Application": {
            "description": "An investigational device exemption (IDE) allows the investigational device to be used in a clinical study in order to collect safety and effectiveness data. Clinical studies are most often conducted to support a PMA. Only a small percentage of 510(k)s require clinical data to support the application.",
            "guidance": {
                "name": "IDE Guidance",
                "link": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-812"
            },
            "condition": 0
        },
        "Submission Type": {
            "description": "Identification of key information that may be useful to FDA in the initial processing and review of the 510(k) submission, including content from current Form FDA 3514, Section A. 23",
            "guidance": {
                "name": "Submission Guidance",
                "link": "https://www.fda.gov/media/72421/download"
            },
            "condition": null
        },
        "Cover Letter": {
            "description": "Attach a cover letter and any documents that refer to other submissions. ",
            "guidance": null,
            "condition": null
        },
        "Applicant Information": {
            "description": "Information on the applicant and correspondent, if applicable, consistent with content from current Form FDA 3514, Sections B and C. ",
            "guidance": null,
            "condition": null
        },
        "Pre-Submission Correspondence": {
            "description": "Information on prior submissions for the same device included in the current submission, such as submission numbers for a prior not substantially equivalent (NSE) determination, prior deleted or withdrawn 510(k), Q-Submission, Investigational Device Exemption (IDE) application, premarket approval (PMA) application, humanitarian device exemption (HDE) application, or De Novo classification request. ",
            "guidance": null,
            "condition": null
        },
        "Consensus Standards": {
            "description": "Identification of voluntary consensus standard(s) used, if applicable. This includes both FDA-recognized and nonrecognized consensus standards. ",
            "guidance": {
                "name": "Consensus Guidance",
                "link": "https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/standards-and-conformity-assessment-program."
            },
            "condition": null
        },
        "Device Description": {
            "description": "Identification of listing number if listed with FDA. Descriptive information for the device, including a description of the technological characteristics of the device including materials, design, energy source, and other device features, as defined in section 513(i)(1)(B) of the FD&C Act and 21 CFR 807.100(b)(2)(ii)(A). Descriptive information also includes a description of the principle of operation for achieving the intended effect and the proposed conditions of use, such as surgical technique for implants; anatomical location of use; user interface; how the device interacts with other devices; and/or how the device interacts with the patient.Information on whether the device is intended to be marketed with accessories. Identification of any applicable device-specific guidance document(s) or special controls for the device type as provided in a special controls document (or alternative measures identified that provide at least an equivalent assurance of safety and effectiveness) or in a device-specific classification regulation, and/or performance standards. See \u201cThe 510(k) Program: Evaluating Substantial Equivalence in Premarket Notifications [510(k)].\u201d26",
            "guidance": null,
            "condition": null
        },
        "Proposed Indications for Use": {
            "description": "Identification of the proposed indications for use of the device. The term indications for use, as defined in 21 CFR 814.20(b)(3)(i), describes the disease or condition the device will diagnose, treat, prevent, cure, or mitigate, including a description of the patient population for which the device is intended.28 The whole goal of this section is to be a summary of the rest of your submission and includesinformation from the cover letter as well as a summary of the substantial equivalence comparisonand of the testing that was performed.",
            "guidance": {
                "name": "Indication for Use Guidance",
                "link": "https://www.fda.gov/media/124401/download"
            },
            "condition": null
        },
        "Classification": {
            "description": "Identification of the classification regulation number that seems most appropriate for the subject device, as applicable.",
            "guidance": {
                "name": "Classification Guidance",
                "link": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-807/subpart-E/section-807.87"
            },
            "condition": null
        },
        "Predicates and Substantial Equivalence": {
            "description": "Identification of a predicate device (e.g., 510(k) number, De Novo number, reclassified PMA number, classification regulation reference, if exempt and limitations to exemption are exceeded, or statement that the predicate is a preamendments device). The submission should include a comparison of the predicate and subject device and a discussion why any differences between the subject and predicate do not impact safety and effectiveness [see section 513(i)(1)(A) of the FD&C Act and 21 CFR 807.87(f)]. A reference device should also be included in the discussion, if applicable. See \u201cThe 510(k) Program: Evaluating Substantial Equivalence in Premarket Notifications [510(k)].\u201d31",
            "guidance": null,
            "condition": null
        },
        "Design/Special Controls, Risks to Health, and Mitigation Measures": {
            "description": "Applicable to Special 510(k) submissions only. Identification of the device changes and the risk analysis method(s) used to assess the impact of the change(s) on the device and the results of the analysis. Risk control measures to mitigate identified risks (e.g., labeling, verification). See \u201cThe Special 510(k) Program.\u201d32",
            "guidance": null,
            "condition": null
        },
        "Labeling": {
            "description": "Submission of proposed labeling in sufficient detail to satisfy the requirements of 21 CFR 807.87(e). Generally, if the device is an invitro diagnostic device, the labeling must also satisfy the requirements of 21 CFR 809.10. Additionally, the term \u201clabeling\u201d generally includes the device label, instructions for use, and any patient labeling. See \u201cGuidance on Medical Device Patient Labeling.\u201d34",
            "guidance": null,
            "condition": null
        },
        "Reprocessing": {
            "description": "Information for assessing the reprocessing validation and labeling, if applicable. See \u201cReprocessing Medical Devices in Health Care Settings: Validation Methods and Labeling.\u201d35",
            "guidance": null,
            "condition": null
        },
        "Sterility": {
            "description": "Information on sterility and validation methods, if applicable. See \u201cSubmission and Review of Sterility Information in Premarket Notification (510(k)) Submissions for Devices Labeled as Sterile.\u201d36",
            "guidance": null,
            "condition": null
        },
        "Shelf Life": {
            "description": "Summary of methods used to establish that device performance is maintained for the entirety of the proposed shelf-life37 (e.g., mechanical properties, coating integrity, pH, osmolality) ",
            "guidance": null,
            "condition": 1
        },
        "Biocompatibility": {
            "description": "Information on the biocompatibility assessment of patient contacting materials, if applicable. See \u201cUse of International Standard ISO 10993-1, \u2018Biological evaluation of medical devices - Part 1: Evaluation and testing within a risk management process.\u2019\u201d38",
            "guidance": null,
            "condition": 2
        },
        "Software/Firmware": {
            "description": "Submission of applicable software documentation, if applicable. See \u201cGuidance for the Content of Premarket Submissions for Software Contained in Medical Devices.\u201d39",
            "guidance": {
                "name": "Software Guidance",
                "link": "https://www.fda.gov/media/153781/download"
            },
            "condition": 3
        },
        "Cybersecurity/Interoperability": {
            "description": "Submission of applicable information regarding the assessment of cybersecurity, if applicable. See \u201cContent for Premarket Submissions for Management of Cybersecurity in Medical Devices\u201d and \u201cDesign Considerations and Premarket Submission Recommendations for Interoperable Medical Devices.\u201d41",
            "guidance": null,
            "condition": null
        },
        "Electromagnetic Compatibility (EMC)": {
            "description": "Submission of the EMC, Electrical, Mechanical, Wireless and Thermal Safety testing for your device or summarize why testing is not needed. See \u201cElectromagnetic Compatibility (EMC) of Medical Devices\u201d42 and \u201cRadio Frequency Wireless Technology in Medical Devices.\u201d43",
            "guidance": {
                "name": "EMC testing guidance",
                "link": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/detail.cfm?standard__identification_no=41539"
            },
            "condition": 4
        },
        "Performance Testing-(bench)": {
            "description": "For non-in vitro diagnostic devices: Provide information on the non-clinical test reports submitted, referenced, or relied on in the 510(k) for a determination of substantial equivalence. For in vitro diagnostic devices: Provide analytical performance, comparison studies, reference range/expected values, and clinical study information. ",
            "guidance": null,
            "condition": 6
        },
        "Performance Testing-(animal)": {
            "description": "Provide information on animal testing",
            "guidance": null,
            "condition": 5
        },
        "Performance Testing-(clinical)": {
            "description": "Provide information on clinical testing",
            "guidance": {
                "name": "Clinical Guidance",
                "link": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/cfrsearch.cfm?fr=820.30"
            },
            "condition": null
        },
        "References": {
            "description": "Inclusion of any literature references, if applicable.",
            "guidance": null,
            "condition": null
        },
        "Administrative Documentation ": {
            "description": "Inclusion of additional administrative forms applicable to the submission, including but not limited to a general summary of submission/executive summary (recommended), a Truthful and Accuracy Statement, 45 and a 510(k) Summary46 or statement. 47",
            "guidance": null,
            "condition": null
        },
        "Amendment/Additional Information (AI) response": {
            "description": "Inclusion of responses to Additional Information requests.48",
            "guidance": null,
            "condition": null
        }
    },
    "conditions": [
        "Is your device considered a significant risk?",
        "Do you have applicable product testing to demonstrate performance over the stated shelf life. This oftenincludes accelerated age testing?",
        "Do you have anything that is in direct or indirect patient contact?",
        "Does your device have software or electrical components?",
        "Does your device have electrically powered components, regardless of whether those components are in patient contact or not",
        "Do you need to do animal testing?",
        "See \u201cRecommended Content and Format of NonClinical Bench Performance Testing Information in Premarket Submissions.\u201d"
    ]
}

export default WorkflowData;