#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os

# المجلدات المطلوب إنشاؤها
directories = ['data', 'notebooks', 'src']

# إنشاء المجلدات
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# إنشاء ملف README.md وعرض محتوى مبدئي فيه
with open('README.md', 'w', encoding='utf-8') as f:
    f.write("# AI Resume Analyzer 🤖\n\nمشروع تحليل السيرة الذاتية ومقارنتها بالمتطلبات الوظيفية باستعمال الذكاء الاصطناعي.")

# إنشاء ملف requirements.txt وحفظ المكتبات الأساسية
with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write("pypdf\nstreamlit\n")

print("✅ تم إنشاء هيكل المشروع بنجاح!")


# In[9]:




# In[16]:


# 1. تثبيت مكتبة إنشاء ملفات الـ PDF (إذا لم تكن موجودة)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# 2. التأكد من وجود مجلد data وإنشائه إذا كان مفقوداً
os.makedirs('data', exist_ok=True)

# 3. إنشاء ملف PDF وهمي للتجربة
pdf_path = "data/resume.pdf"
c = canvas.Canvas(pdf_path, pagesize=letter)
c.drawString(100, 750, "Abrar Saber Al-Awadhi")
c.drawString(100, 730, "Artificial Intelligence Student")
c.drawString(100, 710, "Skills: Python, SQL, Machine Learning, Data Structures, Git")
c.save()

print("✅ تم إنشاء ملف resume.pdf وتجهيزه داخل مجلد data بنجاح!")


# In[14]:


import pypdf
import re

def extract_and_clean_pdf(pdf_path):
    """
    دالة تقرأ ملف PDF وتستخرج النص وتنظفه من الأسطر والمسافات الزائدة
    """
    try:
        # 1. فتح وقراءة ملف الـ PDF
        reader = pypdf.PdfReader(pdf_path)
        raw_text = ""
        
        # 2. المرور على كافة الصفحات واستخراج النصوص
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                raw_text += page_text + " "
                
        # 3. تنظيف النص (Text Cleaning)
        # إزالة الأسطر والمسافات الزائدة واستبدالها بمسافة واحدة
        cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
        
        return cleaned_text

    except FileNotFoundError:
        print(f"❌ الخطأ: الملف {pdf_path} غير موجود داخل مجلد data!")
        return None
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
        return None

# --- تجربة الدالة ---
file_path = "data/resume.pdf"
cv_text = extract_and_clean_pdf(file_path)

if cv_text:
    print("✅ تم استخراج النص وتنظيفه بنجاح!\n")
    print(f"📊 إجمالي عدد الكلمات: {len(cv_text.split())} كلمة.")
    print("--------------------------------------------------")
    print("📝 عينة من النص المنظف (أول 300 حرف):")
    print(cv_text[:300])


# In[19]:


import re

def parse_resume(text):
    """
    دالة تفكك نص الـ CV وتستخرج الأقسام الأساسية وتخزنها في Dictionary
    """
    # 1. القاموس الفارغ للهيكل
    resume_data = {
        "name": "",
        "skills": [],
        "education": [],
        "experience": [],
        "projects": []
    }
    
    # 2. استخراج الاسم (افتراضياً السطر أو الكلمات الأولى)
    words = text.split()
    if len(words) >= 4:
        resume_data["name"] = " ".join(words[:4]) # أخذ أول 4 كلمات كالاسم واللقب
    
    # 3. قائمة بالمهارات الشائعة للبحث عنها داخل النص
    skill_keywords = ["python", "sql", "machine learning", "data structures", "git", "pytorch", "tensorflow"]
    
    found_skills = []
    for skill in skill_keywords:
        # البحث عن المهارة داخل النص بغض النظر عن حالة الأحرف (حالة مكبرة/مصغرة)
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill.capitalize())
            
    resume_data["skills"] = found_skills
    
    # 4. البحث عن أقسام التعليم والخبرة والمشاريع باستخدام Regular Expressions
    # نحدد للنموذج العثور على ما بين الكلمة المفتاحية والكلمة التي تليها
    education_match = re.search(r'(education|degree|university)(.*?)(experience|skills|projects|$)', text, re.IGNORECASE)
    if education_match:
        resume_data["education"] = [education_match.group(2).strip()]
        
    experience_match = re.search(r'(experience|work history)(.*?)(skills|projects|education|$)', text, re.IGNORECASE)
    if experience_match:
        resume_data["experience"] = [experience_match.group(2).strip()]

    projects_match = re.search(r'(projects|portfolio)(.*?)(skills|education|experience|$)', text, re.IGNORECASE)
    if projects_match:
        resume_data["projects"] = [projects_match.group(2).strip()]

    return resume_data

# --- تجربة الدالة على النص الذي استخرجناه من المرحلة 1 ---
parsed_resume = parse_resume(cv_text)

# طباعة النتيجة بشكل منظم
import json
print("✅ تم تفكيك الـ CV وتنظيم البيانات بنجاح:\n")
print(json.dumps(parsed_resume, indent=4, ensure_ascii=False))


# In[21]:


import re

# 1. إدخال النص الخاص بالوصف الوظيفي
job_description = """
We are looking for a Junior Machine Learning Engineer.

Requirements:
- Python
- SQL
- Machine Learning
- Scikit-learn
- Git
"""

def extract_job_skills(job_text):
    """
    دالة تقرأ الوصف الوظيفي وتستخرج المهارات المطلوبة فقط
    """
    # قائمة بالمهارات التقنية المطلوبة في مجالات الـ AI و ML
    skill_keywords = [
        "python", "sql", "machine learning", "scikit-learn", 
        "git", "pytorch", "tensorflow", "data structures", "docker"
    ]
    
    required_skills = []
    
    # البحث عن المهارات داخل نص الوصف الوظيفي
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', job_text, re.IGNORECASE):
            # الحفاظ على شكل المهارة المنسق
            if skill.lower() == "scikit-learn":
                required_skills.append("Scikit-learn")
            elif skill.lower() == "sql":
                required_skills.append("SQL")
            else:
                required_skills.append(skill.capitalize())
                
    return required_skills

# --- تجربة استخراج مهارات الوظيفة ---
required_skills = extract_job_skills(job_description)

print("🎯 المهارات المستخرجة من الوصف الوظيفي (Required Skills):\n")
for skill in required_skills:
    print(f"• {skill}")


# In[23]:


def compare_skills(cv_skills, required_skills):
    """
    دالة تقارن بين مهارات الـ CV والمهارات المطلوبة للوظيفة
    وتحسب نسبة التوافق والمهارات المتطابقة والناقصة
    """
    # 1. تحويل القوائم إلى Sets لسهولة المقارنة
    cv_set = set(cv_skills)
    job_set = set(required_skills)
    
    # 2. استخراج المهارات المتطابقة (Intersection)
    matched_skills = list(cv_set.intersection(job_set))
    
    # 3. استخراج المهارات الناقصة (Difference)
    missing_skills = list(job_set - cv_set)
    
    # 4. حساب نسبة التوافق (Match Score %)
    if job_set:
        match_score = (len(matched_skills) / len(job_set)) * 100
    else:
        match_score = 0.0
        
    return {
        "match_score": round(match_score, 1),
        "matched": matched_skills,
        "missing": missing_skills
    }

# --- تجربة المقارنة باستخدام البيانات السابقة ---
comparison = compare_skills(parsed_resume["skills"], required_skills)

# طباعة النتيجة بشكل احترافي
print("🎯 نتيجة المقارنة بين الـ CV والوظيفة:\n")
print(f"📊 Match Score: {comparison['match_score']}% Match\n")

print("✅ Matched Skills:")
for skill in comparison['matched']:
    print(f"  • {skill}")

print("\n❌ Missing Skills:")
for skill in comparison['missing']:
    print(f"  • {skill}")
# إنشاء الملف الخفي وتخزين المفتاح داخله مباشرة
with open(".env", "w") as f:
    f.write('GEMINI_API_KEY="AQ.Ab8RN6IuotW3cXcc1vUYRSyDfFDGNk-2QLROq4NA26E3WKpHfw"\n')

print("✅ تم حفظ المفتاح بأمان داخل ملف .env الخفي!")


# In[47]:


import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def generate_ai_resume_feedback(cv_text, job_text, api_key):
    client = genai.Client(api_key=api_key)
    
    # 1. جلب قائمة الموديلات المتاحة لحسابكِ ديناميكياً
    available_models = []
    try:
        for m in client.models.list():
            # تصفية الموديلات التي تدعم توليد النصوص فقط
            if "generateContent" in getattr(m, 'supported_generation_methods', []):
                available_models.append(m.name)
    except Exception as e:
        pass

    # ترتيب النماذج المفضلة مع استخدام المتاح فعلياً بحسابك
    preferred_models = ['gemini-2.5-flash', 'gemini-3.6-flash', 'gemini-1.5-flash']
    target_models = [m for m in preferred_models if m in available_models] or available_models
    
    if not target_models:
        # خيار احتياطي في حال عدم إمكانية سرد الموديلات
        target_models = ['gemini-2.5-flash', 'gemini-3.6-flash']

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

    # 2. التجربة على الموديلات المتاحة تباعاً
    for model_name in target_models:
        for attempt in range(1, 3):
            try:
                # تنظيف اسم الموديل من أي بادقة زائدة
                clean_name = model_name.replace("models/", "")
                response = client.models.generate_content(
                    model=clean_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                if "503" in str(e) and attempt < 2:
                    time.sleep(2)
                    continue
                # تجربة الموديل التالي عند الفشل
                break

    return "❌ تعذر الاتصال بجميع النماذج المتاحة حالياً، يرجى المحاولة بعد لحظات."

if API_KEY:
    print("⏳ جاري الكشف عن النماذج المتاحة وتحليل الـ CV...\n")
    ai_feedback = generate_ai_resume_feedback(cv_text, job_description, API_KEY)
    print("🤖 **تقرير الذكاء الاصطناعي الشامل:**\n")
    print(ai_feedback)
else:
    print("❌ لم يتم العثور على المفتاح في ملف .env")


# In[1]:


import sys
print(sys.executable)


# In[3]:


import warnings
warnings.filterwarnings('ignore')

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. تحميل النموذج من المجلد المحلي (يعمل بدون إنترنت)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. نص تجريبي للسيرة الذاتية ومتطلبات الوظيفة
job_description = "Looking for a Data Scientist skilled in Python, Machine Learning, and NLP."
cv_text = "Experienced AI Specialist proficient in Python, PyTorch, and Data Analysis."

# 3. حساب التشابه الدلالي
embeddings = model.encode([job_description, cv_text], show_progress_bar=False)
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

print(f"✅ نسبة التشابه الدلالي: {similarity * 100:.2f}%")


# In[3]:


import os
import re
import warnings
import pdfplumber
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

# 1. تحميل النموذج متعدد اللغات محلياً (يدعم العربية والإنجليزي)
model_path = 'C:/Users/hp/my_multilingual_model'
model = SentenceTransformer(model_path)

# 2. دالة استخراج النص من ملف الـ PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    if os.path.exists(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    return text

# 3. قاموس المهارات ثنائي اللغة (Bilingual Skills Database)
bilingual_skills = {
    "Python": ["python", "باثون", "بايثون"],
    "SQL": ["sql", "اس كيو ال", "قواعد بيانات"],
    "Git": ["git", "جيت"],
    "Machine Learning": ["machine learning", "تعلم الآلة", "التعلم الآلي"],
    "Docker": ["docker", "دوكر"],
    "PyTorch": ["pytorch", "باي تورش"],
    "NLP": ["nlp", "معالجة اللغات الطبيعية", "معالجة اللغة الطبيعية"],
    "Data Analysis": ["data analysis", "تحليل البيانات", "تحليل بيانات"]
}

# 4. دالة استخراج المهارات الثنائية
def extract_bilingual_skills(text, skills_dict):
    found_skills = set()
    text_lower = text.lower()
    for canonical_name, aliases in skills_dict.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(canonical_name)
                break
    return found_skills

# 5. الـ Pipeline الرئيسي للمطابقة متعددة اللغات
def analyze_cv_multilingual(cv_text, job_description, skills_dict):
    # أ. استخراج المهارات المترادفة للـ CV والـ Job Description
    cv_skills = extract_bilingual_skills(cv_text, skills_dict)
    job_skills = extract_bilingual_skills(job_description, skills_dict)
    
    # ب. المطابقة والمهارات المفقودة
    matched_skills = cv_skills.intersection(job_skills)
    missing_skills = job_skills - cv_skills
    
    # ج. التحليل الدلالي العابر للغات (Cross-lingual Semantic Matching)
    embeddings = model.encode([job_description, cv_text], show_progress_bar=False)
    semantic_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0] * 100
    
    # هـ. طباعة التقرير التفاعلي
    print("\n" + "="*45)
    print(f"📊 نسبة التطابق (Resume Match): {semantic_score:.0f}%")
    print("="*45)
    
    print("\n🔍 المهارات المطلوبة (Skills Match):")
    for skill in job_skills:
        if skill in matched_skills:
            print(f"  ✅ {skill}")
        else:
            print(f"  ❌ {skill}")
            
    print("\n💪 نقاط القوة (Strengths):")
    if cv_skills:
        print(f"  • خلفية قوية في: {', '.join(cv_skills)}")
    
    print("\n⚠️ المهارات المفقودة (Missing Skills):")
    if missing_skills:
        for skill in missing_skills:
            print(f"  • {skill}")
    else:
        print("  • لا يوجد مهارات مفقودة")
        
    print("\n💡 توصيات التطوير (AI Recommendations):")
    if missing_skills:
        print(f"  • إضافة مشاريع تغطي: {', '.join(missing_skills)}")
    print("  • إبراز المشاريع العملية المنجزة")
    print("="*45)

# ==========================================
# 6. تجربة الحالة الأقوى: CV عربي + Job Description إنجليزي
# ==========================================

# نص السيرة الذاتية باللغة العربية
cv_arabic = """
أخصائي ذكاء اصطناعي وتحليل البيانات. أمتلك خبرة ممتازة في بايثون وقواعد بيانات SQL،
بالإضافة إلى إطار العمل باي تورش واستخدام نظام جيت للتحكم بالإصدارات.
"""

# نص الوظيفة باللغة الإنجليزية
job_english = """
Looking for a Data Scientist skilled in Python, SQL, Machine Learning, Git, and Docker. 
Experience with NLP and PyTorch is required.
"""

# تشغيل التحليل التبادلي
analyze_cv_multilingual(cv_arabic, job_english, bilingual_skills)
