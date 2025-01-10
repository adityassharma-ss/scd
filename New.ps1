Here's a prompt for generating a prescription based on a doctor-patient conversation:


---

Prompt for Language Model

Task:
You are a medical assistant AI. Your task is to generate a prescription based on the conversation between a doctor and a patient. Ensure that the prescription is accurate, professional, and contextually appropriate. Use the given conversation to extract the required details such as symptoms, diagnosis, medications, and any additional instructions.

Input Format:
A text-based conversation between a doctor and a patient. Example:

Doctor: Hello, what brings you here today?  
Patient: I have been experiencing headaches and dizziness for the past three days.  
Doctor: Have you had any fevers or nausea?  
Patient: Yes, mild fever but no nausea.  
Doctor: Understood. I will prescribe some medication to help with your symptoms.

Output Format:
Generate a prescription in the following format:

**Prescription**  
Doctor's Name: [Extracted from conversation or use "Dr. [Last Name]"]  
Patient's Name: [Extracted from conversation]  
Date: [Current Date]  
Patient's DOB: [Mention "Not Provided" if unavailable]  

**Diagnosis:**  
[Summarize the key findings from the conversation]  

**Prescription Details:**  
- Medication 1: [Name, Dosage, Frequency, Duration]  
- Medication 2: [Name, Dosage, Frequency, Duration]  
...  

**Additional Instructions:**  
[Specific advice or instructions provided by the doctor]  

**Follow-Up:**  
[Optional follow-up advice if mentioned]  

**Signature:**  
[Dr. [Last Name]]


---

Sample Input

Doctor: Hello, what seems to be the problem?  
Patient: I've been having a sore throat and coughing a lot, especially at night.  
Doctor: How long has this been happening?  
Patient: Around 4 days now.  
Doctor: Do you have a fever or chills?  
Patient: Slight fever, yes.  
Doctor: Any allergies to medications?  
Patient: No.  
Doctor: Alright, I will prescribe some antibiotics and a cough syrup for you.

Sample Output

**Prescription**  
Doctor's Name: Dr. Smith  
Patient's Name: John Doe  
Date: 10-Jan-2025  
Patient's DOB: Not Provided  

**Diagnosis:**  
Upper respiratory infection with mild fever and sore throat.  

**Prescription Details:**  
- Amoxicillin 500mg: Take 1 tablet every 8 hours for 7 days.  
- Cough Syrup: Take 10ml twice a day after meals for 5 days.  

**Additional Instructions:**  
- Drink plenty of fluids.  
- Rest well and avoid cold drinks.  

**Follow-Up:**  
Visit after 7 days if symptoms persist.  

**Signature:**  
Dr. Smith

This format ensures the model generates precise, professional prescriptions tailored to the conversation. Let me know if you'd like adjustments!

