import os
import re
import time
import warnings
import json
import streamlit as st
import pdfplumber
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai

warnings.filterwarnings('ignore')

# ----------------------------------------------------
# 1. تهيئة الصفحة والنموذج السحابي
# ----------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# تحميل النموذج مجاناً من Hugging Face للعمل في السحاب
@st.cache_resource
def load_semantic_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_semantic_model()

# تحميل المفتاح المنسق من البيئة أو Streamlit Secrets
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ----------------------------------------------------
# 2. القواميس والدوال المساعدة
# ----------------------------------------------------
bilingual_skills = {
    "Python": ["python", "باثون", "بايثون"],
    "SQL": ["sql", "اس كيو ال", "قواعد بيانات"],
    "Git": ["git", "جيت"],
    "Machine Learning": ["machine learning", "تعلم الآلة", "التعلم الآلي"],
    "Scikit-learn": ["scikit-learn", "سايكيت ليرن"],
    "Docker": ["docker", "دوكر"],
    "PyTorch": ["pytorch", "باي تورش"],
    "TensorFlow": ["tensorflow", "تنسرفلو"],
    "NLP": ["nlp", "معالجة اللغات الطبيعية", "معالجة اللغة الطبيعية"],
    "Data Analysis": ["data analysis", "تحليل البيانات", "تحليل بيانات"],
    "Data Structures": ["data structures", "هياكل البيانات"]
}

def extract_text_from_pdf(uploaded_file):
    """استخراج النص وتنظيفه مباشرة من ملف الـ PDF المرفوع"""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        return cleaned_text
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
        return ""

def extract_bilingual_skills(text, skills_dict):
    """استخراج المهارات الثنائية (عربي/إنجليزي)"""
    found_skills = set()
    text_lower = text.lower()
    for canonical_name, aliases in skills_dict.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(canonical_name)
                break
    return found_skills

def generate_ai_resume_feedback(cv_text, job_text, api_key):
    """توليد التقرير الشامل باستخدام نموذج Gemini"""
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    أنت خبير توظيف واستشاري تطوير سير ذاتية متقدم.
    قم بتحليل السيرة الذاتية التالية ومقارنتها بالوصف الوظيفي المحدد، ثم قدم تقريراً شاملاً ومفصلاً باللغة العربية.

    --- نص السيرة الذاتية (Resume) ---
    {cv_text}

    --- الوصف الوظيفي (Job Description) ---
    {job_text}

    المطلوب في التقرير:
    1. **نقاط القوة (Strengths)**: ما الذي يجعل هذه السيرة مناسبة للوظيفة؟
    2. **نقاط الضعف والقصور (Weaknesses)**: ما الأجزاء التي تحتاج لتوضيح أو تعميق؟
    3. **المهارات والتقنيات الناقصة (Missing Skills)**: التقنيات المذكورة في الوصف وغير الموضحة في الـ CV.
    4. **اقتراحات التحسين والصياغة (Recommendations)**: اقتراحات عمل وصياغات أفضل لأقسام المشاريع والخبرة لزيادة فرص القبول.
    """

    preferred_models = ['gemini-2.5-flash', 'gemini-1.5-flash']
    for model_name in preferred_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception:
            continue

    return "❌ تعذر الاتصال بجميع النماذج المتاحة حالياً، يرجى المحاولة بعد لحظات."

# ----------------------------------------------------
# 3. واجهة المستخدم (Streamlit UI)
# ----------------------------------------------------
st.title("📄 AI Resume Analyzer 🤖")
st.subheader("محلل السيرة الذاتية ومطابقتها بالمتطلبات الوظيفية بالذكاء الاصطناعي")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📥 قم برفع السيرة الذاتية (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("📝 أدخل الوصف الوظيفي (Job Description) هنا:", height=180)

if st.button("🚀 بدء تحليل السيرة الذاتية", use_container_width=True):
    if uploaded_file is not None and job_description.strip() != "":
        with st.spinner("جاري قراءة الملف وتحليل البيانات..."):
            cv_text = extract_text_from_pdf(uploaded_file)
            
            if cv_text:
                # 1. استخراج المهارات والمطابقة
                cv_skills = extract_bilingual_skills(cv_text, bilingual_skills)
                job_skills = extract_bilingual_skills(job_description, bilingual_skills)
                
                matched_skills = cv_skills.intersection(job_skills)
                missing_skills = job_skills - cv_skills

                # 2. حساب التشابه الدلالي (Semantic Similarity)
                embeddings = model.encode([job_description, cv_text], show_progress_bar=False)
                semantic_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0] * 100

                st.write("## 📊 نتائج التحليل السريع")
                st.metric("نسبة التطابق الدلالي (Match Score)", f"{semantic_score:.1f}%")

                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.success("✅ المهارات المتطابقة (Matched Skills):")
                    if matched_skills:
                        for s in matched_skills:
                            st.write(f"- {s}")
                    else:
                        st.write("لا توجد مهارات متطابقة مباشرة.")

                with res_col2:
                    st.error("❌ المهارات المفقودة (Missing Skills):")
                    if missing_skills:
                        for s in missing_skills:
                            st.write(f"- {s}")
                    else:
                        st.write("لا توجد مهارات مفقودة!")

                # 3. تقرير Gemini الذكي
                st.write("---")
                st.write("## 🤖 تقرير الذكاء الاصطناعي الشامل (Gemini Feedback)")
                if API_KEY:
                    with st.spinner("جاري توليد التقرير المتقدم..."):
                        ai_report = generate_ai_resume_feedback(cv_text, job_description, API_KEY)
                        st.markdown(ai_report)
                else:
                    st.warning("⚠️ لم يتم ضبط GEMINI_API_KEY في ملف .env لعرض التقرير التوليدي.")
    else:
        st.warning("يرجى رفع ملف السيرة الذاتية وإدخال الوصف الوظيفي أولاً.")
