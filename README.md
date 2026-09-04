# 📄 AI Resume Analyzer & Job Matcher

Ever sent out dozens of resumes and wondered why you weren't hearing back? Most companies rely on Applicant Tracking Systems (ATS) to filter out resumes before a human ever sees them. 

I built this application to help job seekers bypass that black hole. It evaluates resume content against job postings, pinpoints missing keywords or skills, and provides personalized feedback to maximize interview callbacks.

Try the live app here:** [AI Resume Analyzer](https://ai-resume-analyzer-jpoqoth5dbjhw2bbfpm8jz.streamlit.app)

 What it Does

Text Extraction:Pulls text cleanly from PDF resumes without losing structure or key details.
Semantic Matching: Goes beyond basic keyword matching by using contextual embeddings (`all-MiniLM-L6-v2`) to see how well candidate experience aligns with job descriptions.
Skill Gap Analysis: Highlights exact skills found in the job requirements that are missing or weak in the resume.
AI Action Plan: Uses Google's Gemini API to generate tailored recommendations on how to rephrase bullet points and highlight relevant background.



 Tech Stack

Frontend & Deployment: Streamlit / Streamlit Cloud
Language:Python 3.10+
NLP & Embeddings: Sentence-Transformers, PyTorch, Scikit-Learn
LLM: Google Gemini API
PDF Parsing:** `pdfplumber`, `pypdf`

 How to Run Locally

If you'd like to run this project on your machine:

1.Clone the repo:
 bash
   git clone [https://github.com/abrarsaberahmed/Ai-Resume-Analyzer.git](https://github.com/abrarsaberahmed/Ai-Resume-Analyzer.git)
   cd Ai-Resume-Analyzer
