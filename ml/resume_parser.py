
import re
import os


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyPDF2 and pdfplumber as fallback."""
    text = ""
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass

    if len(text.strip()) < 50:
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            pass

    return text.strip()


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception:
        return ""


def extract_text(file_path):
    """Extract text based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    return ""


# ── Skill keywords organized by domain ──
SKILL_KEYWORDS = {
    'Programming': ['python', 'java', 'c++', 'javascript', 'typescript', 'r', 'sql',
                     'kotlin', 'swift', 'dart', 'go', 'rust', 'scala', 'ruby', 'php',
                     'c#', 'bash', 'matlab', 'perl'],
    'Machine Learning': ['machine learning', 'deep learning', 'tensorflow', 'pytorch',
                         'scikit-learn', 'keras', 'nlp', 'natural language processing',
                         'computer vision', 'neural network', 'cnn', 'rnn', 'lstm',
                         'transformer', 'bert', 'gpt', 'reinforcement learning',
                         'feature engineering', 'model deployment', 'mlops', 'mlflow'],
    'Data Science': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'statistics',
                     'data visualization', 'tableau', 'power bi', 'spark', 'hadoop',
                     'data analysis', 'data mining', 'data cleaning', 'etl',
                     'data warehousing', 'a/b testing', 'data modeling'],
    'Web Development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                        'mongodb', 'rest api', 'graphql', 'bootstrap', 'next.js',
                        'tailwind', 'webpack', 'sass', 'django', 'flask', 'fastapi'],
    'DevOps & Cloud': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform',
                       'ansible', 'jenkins', 'ci/cd', 'linux', 'nginx', 'prometheus',
                       'grafana', 'serverless', 'lambda', 'cloudformation',
                       'infrastructure as code'],
    'Database': ['mysql', 'postgresql', 'oracle', 'mongodb', 'redis', 'sqlite',
                 'database design', 'query optimization', 'nosql', 'cassandra',
                 'elasticsearch', 'dynamodb'],
    'Mobile': ['react native', 'flutter', 'ios development', 'android development',
               'xcode', 'android studio', 'firebase', 'swift', 'kotlin'],
    'Security': ['network security', 'penetration testing', 'encryption', 'siem',
                 'firewalls', 'vulnerability assessment', 'incident response',
                 'wireshark', 'nmap', 'metasploit', 'owasp', 'compliance'],
    'Soft Skills': ['communication', 'teamwork', 'leadership', 'problem solving',
                    'critical thinking', 'time management', 'agile', 'scrum',
                    'project management', 'mentoring', 'collaboration'],
    'Mechanical Engineering': ['autocad', 'solidworks', 'catia', 'thermodynamics',
                    'fluid mechanics', 'cad/cam', 'manufacturing', 'material science',
                    'fea', 'product design', 'hvac', 'ansys', 'mechatronics',
                    'gd&t', 'six sigma', 'lean manufacturing', 'pro-e',
                    'robotics', 'quality control', '3d printing', 'cnc',
                    'creo', 'unigraphics', 'nx', 'tolerance analysis'],
    'Civil Engineering': ['structural analysis', 'revit', 'construction management',
                    'surveying', 'concrete design', 'staad.pro', 'geotechnical',
                    'autocad civil 3d', 'etabs', 'primavera p6', 'bim',
                    'sap2000', 'urban planning', 'estimation', 'quantity surveying',
                    'gis', 'soil mechanics', 'hydrology', 'transportation engineering',
                    'project planning', 'risk management'],
    'Electrical Engineering': ['circuit design', 'pcb design', 'microcontrollers',
                    'power systems', 'simulink', 'plc', 'embedded systems',
                    'control systems', 'scada', 'high voltage', 'switchgear',
                    'labview', 'pspice', 'transformer design', 'electrical autocad',
                    'fpga', 'power electronics', 'relay protection', 'motor drives',
                    'electrical machines', 'instrumentation'],
    'Electronics & Communication': ['vlsi', 'vhdl', 'verilog', 'signal processing',
                    'analog circuits', 'digital circuits', 'antenna design',
                    'rf engineering', 'communication systems', 'microprocessors',
                    'wireless communication', 'iot', 'arm', 'dsp',
                    'pcb layout', 'oscilloscope', 'spectrum analyzer',
                    'telecommunications', 'optical communication', '5g', 'lte']
}

EDUCATION_PATTERNS = [
    r'(?i)(ph\.?d|doctorate)',
    r'(?i)(master|m\.?s\.?|m\.?tech|m\.?sc|mca|mba|m\.?arch|m\.?des|m\.?com|pgdm)',
    r'(?i)(bachelor|b\.?s\.?|b\.?tech|b\.?e\.?|b\.?sc|bca|bba|b\.?arch|b\.?des|b\.?com|b\.?a)',
    r'(?i)(diploma|associate)',
    r'(?i)(intermediate|12th|hsc|plus two|higher secondary)',
    r'(?i)(10th|ssc|high school|secondary school|matriculation)'
]

# Maps pattern index → Indian standard education label
EDUCATION_LEVELS = {
    0: 'PhD',
    1: 'MTech',
    2: 'BTech',
    3: 'BTech',
    4: 'Intermediate',
    5: '10th'
}

CERTIFICATION_KEYWORDS = [
    'aws certified', 'google certified', 'microsoft certified', 'cisco',
    'comptia', 'pmp', 'cka', 'ckd', 'terraform', 'docker certified',
    'oracle certified', 'itil', 'prince2', 'scrum master', 'six sigma',
    'ceh', 'cissp', 'oscp', 'togaf', 'salesforce', 'hubspot',
    'certificate', 'certified', 'certification', 'professional'
]


def extract_skills(text):
    """Extract skills from resume text by matching against known keywords using word boundaries."""
    text_lower = text.lower()
    found_skills = {}

    for category, keywords in SKILL_KEYWORDS.items():
        matched = []
        for skill in keywords:
            # Escape the skill string, but handle c++ or c# specially since + and # are non-word chars
            skill_escaped = re.escape(skill.lower())
            
            # If the skill ends in non-word char (like c++), don't enforce trailing word boundary
            if not skill[-1].isalnum():
                pattern = r'\b' + skill_escaped
            # If the skill starts with non-word char (like .net), don't enforce leading word boundary
            elif not skill[0].isalnum():
                pattern = skill_escaped + r'\b'
            else:
                pattern = r'\b' + skill_escaped + r'\b'
                
            if re.search(pattern, text_lower):
                matched.append(skill.title() if len(skill) > 2 else skill.upper())
        
        if matched:
            found_skills[category] = matched

    return found_skills


def extract_education(text):
    """Extract education level from resume text using Indian education standards."""
    for i, pattern in enumerate(EDUCATION_PATTERNS):
        if re.search(pattern, text):
            return EDUCATION_LEVELS.get(i, 'BTech')
    return 'BTech'


def extract_experience_years(text):
    """Extract years of experience from resume text."""
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'experience\s*:?\s*(\d+)\s*years?',
        r'(\d+)\s*years?\s*(?:of\s*)?(?:professional|industry|work)',
        # LinkedIn specific pattern: e.g. "3 yrs 5 mos"
        r'(\d+)\s*yrs?\s*\d+\s*mos?'
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return 0


def extract_gpa(text):
    """Extract GPA or CGPA from resume text and normalize to 4.0 scale."""
    # Try 4.0 Scale GPA
    match = re.search(r'(?i)gpa\s*:?\s*([0-4]\.\d{1,2})', text)
    if match:
        return float(match.group(1))
    
    match = re.search(r'(?i)([0-4]\.\d{1,2})\s*(?:/|out of)?\s*(?:4\.0|4)?\s*gpa', text)
    if match:
        return float(match.group(1))
        
    # Try 10.0 Scale CGPA (common in India)
    match = re.search(r'(?i)cgpa\s*:?\s*([5-9]\.\d{1,2}|10\.0)', text)
    if match:
        cgpa = float(match.group(1))
        return round((cgpa / 10.0) * 4.0, 2)
        
    match = re.search(r'(?i)([5-9]\.\d{1,2}|10\.0)\s*(?:/|out of)?\s*(?:10\.0|10)?\s*cgpa', text)
    if match:
        cgpa = float(match.group(1))
        return round((cgpa / 10.0) * 4.0, 2)

    return 3.5  # Default sensible fallback


def extract_field_of_study(text):
    """Extract Field of Study from text using config values."""
    try:
        from config import EDUCATION_FIELDS
    except ImportError:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from config import EDUCATION_FIELDS
    
    text_lower = text.lower()
    for field in EDUCATION_FIELDS:
        if field.lower() in text_lower:
            return field
    return "Computer Science"  # Default fallback


def extract_certifications(text):
    """Extract certifications from resume text."""
    text_lower = text.lower()
    found = []
    for cert in CERTIFICATION_KEYWORDS:
        if cert in text_lower:
            # Try to extract the full line containing the certification
            for line in text.split('\n'):
                if cert in line.lower() and len(line.strip()) > 5:
                    found.append(line.strip()[:80])
                    break
    return found if found else ['None']


def extract_projects_count(text):
    """Estimate project count from text."""
    text_lower = text.lower()
    project_markers = [
        r'project\s*\d', r'project\s*:', r'project\s*title',
        r'•\s*\w+', r'►\s*\w+', r'▪\s*\w+'
    ]
    count = 0
    for pattern in project_markers:
        count += len(re.findall(pattern, text_lower))
    return max(count, 1)


def parse_resume(file_path):
    """Full resume parsing pipeline — returns structured dict."""
    text = extract_text(file_path)

    if not text:
        return None

    skills = extract_skills(text)
    all_skills = [s for cat_skills in skills.values() for s in cat_skills]

    return {
        'text': text,
        'skills': skills,
        'skills_flat': ', '.join(all_skills) if all_skills else 'None',
        'skill_count': len(all_skills),
        'education_level': extract_education(text),
        'field_of_study': extract_field_of_study(text),
        'gpa': extract_gpa(text),
        'years_of_experience': extract_experience_years(text),
        'certifications': extract_certifications(text),
        'projects_count': extract_projects_count(text),
        'programming_languages': ', '.join(skills.get('Programming', ['None'])),
    }
