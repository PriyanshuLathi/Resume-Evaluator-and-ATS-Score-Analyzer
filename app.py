import streamlit as st
import google.generativeai as genai
import fitz

api_key = st.secrets["API_KEY"]
genai.configure(api_key=api_key)

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_text] + [pdf_content] + [prompt])
    
    return response.text

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file using PyMuPDF (fitz)."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

st.set_page_config(page_title="ATS Resume Expert")
st.header("Resume Evaluator and ATS Score Analyzer")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("✅ PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Get ATS Score")

# Prompt for Resume Analysis
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

# Prompt for Percentage Match Calculation
input_prompt2 = """
You are an advanced ATS (Applicant Tracking System) specializing in resume-job description analysis.  
Evaluate the resume against the provided job description.  
Your response should include:
1. **Percentage match** (between 0% - 100%) based on skills, experience, and keywords.  
2. **List of missing or extra skills** from the resume.  
3. **Final thoughts on improvement suggestions**.

The percentage should be based on a detailed comparison rather than a fixed number.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("Resume Analysis:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload the resume")

if submit2:
    if uploaded_file is not None:
        pdf_content = extract_text_from_pdf(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("Percentage Match:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload the resume")
