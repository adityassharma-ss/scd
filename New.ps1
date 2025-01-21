
import pandas as pd
import PyPDF2

def extract_skills_from_pdf(pdf_path):
    """Extract text from the PDF file and return a set of required skills."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        jd_text = " ".join(page.extract_text() for page in reader.pages)
    
    # Simulate extracting skills from the JD text
    required_skills = {"SQL", "ETL", "Data Engineering", "Python"}  # Example skills
    return required_skills

def clean_skills(skills_str):
    """Clean and convert the skills string into a set."""
    return set(map(str.strip, skills_str.split(',')))

def read_candidates_from_excel(excel_path):
    """Read the Excel file and return a DataFrame of candidates and their skills."""
    df = pd.read_excel(excel_path, usecols=["Name", "Tehcnical Skills"], engine="openpyxl")
    df.dropna(subset=["Name", "Tehcnical Skills"], inplace=True)
    df['Tehcnical Skills'] = df['Tehcnical Skills'].apply(clean_skills)
    return df

def match_skills(jd_skills, candidates_df):
    """Match JD skills with candidate skills and return qualified candidates."""
    matched_candidates = []
    for _, row in candidates_df.iterrows():
        candidate_name = row['Name']
        candidate_skills = row['Tehcnical Skills']
        if jd_skills & candidate_skills:  # Check for skill intersection
            matched_candidates.append(candidate_name)
    return matched_candidates

def main():
    jd_pdf_path = 'Assignment 16-Input.pdf'
    excel_path = 'Assignment 16-Input Excel.xlsx'
    
    jd_skills = extract_skills_from_pdf(jd_pdf_path)
    candidates_df = read_candidates_from_excel(excel_path)
    
    qualified_candidates = match_skills(jd_skills, candidates_df)
    
    print("Qualified Candidates:")
    for candidate in qualified_candidates:
        print(candidate)

if __name__ == "__main__":
    main()
