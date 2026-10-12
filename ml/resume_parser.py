
import re
import os
from datetime import date


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
    r'(?i)\b(?:ph\.?\s*d|doctorate|doctoral degree)\b',
    r'(?i)\b(?:master(?:\'s)?(?: degree)?|m\.?\s*(?:tech|sc|ca|ba|com|arch|des)|m\.s|m\.e|mba|pgdm)\b',
    r'(?i)\b(?:bachelor(?:\'s)?(?: degree)?|b\.?\s*(?:tech|sc|ba|com|arch|des)|bca|bba|b\.e|b\.s)\b',
    r'(?i)\bdiploma\b',
    r'(?i)\bassociate(?:\'s)?(?: degree)?\b',
    r'(?i)\b(?:intermediate|12\s*(?:th|std|standard)|class\s*(?:xii|12)|grade\s*12|hsc|plus two|higher secondary)\b',
    r'(?i)\b(?:10\s*(?:th|std|standard)|class\s*(?:x|10)|grade\s*10|ssc|high school|secondary school|matriculation)\b'
]

# Maps pattern index → Indian standard education label
EDUCATION_LEVELS = {
    0: 'PhD',
    1: 'MTech',
    2: 'BTech',
    3: 'Diploma',
    4: 'Associate',
    5: 'Intermediate',
    6: '10th'
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
            pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'
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
    return 'Not detected'


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

    lines = text.splitlines()
    section_headers = re.compile(
        r'^\s*(?:(?:professional\s+)?(?:work\s+)?experience|'
        r'employment\s+history|work\s+history)\s*:?\s*$',
        re.IGNORECASE,
    )
    other_headers = re.compile(
        r'^\s*(?:education|skills|projects|certifications|summary|'
        r'objective|achievements|awards|references|employment\s+history|'
        r'work\s+history)\s*:?\s*$',
        re.IGNORECASE,
    )
    experience_lines = []
    in_experience = False
    for line in lines:
        if section_headers.match(line):
            in_experience = True
            continue
        if in_experience and other_headers.match(line):
            break
        if in_experience:
            experience_lines.append(line)

    months = {
        name.lower(): number
        for number, names in enumerate(
            (
                ('jan', 'january'), ('feb', 'february'), ('mar', 'march'),
                ('apr', 'april'), ('may',), ('jun', 'june'), ('jul', 'july'),
                ('aug', 'august'), ('sep', 'sept', 'september'),
                ('oct', 'october'), ('nov', 'november'), ('dec', 'december'),
            ),
            start=1,
        )
        for name in names
    }
    date_pattern = re.compile(
        r'(?i)\b(?:'
        r'(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|'
        r'jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|'
        r'oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+)?'
        r'(20\d{2}|19\d{2})\s*(?:[-–—]|to)\s*'
        r'(?:(present|current|now)|(?:'
        r'(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|'
        r'jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|'
        r'oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+)?'
        r'(20\d{2}|19\d{2}))\b'
    )
    intervals = []
    current_month = date.today().year * 12 + date.today().month - 1
    for line in experience_lines:
        for match in date_pattern.finditer(line):
            start_month_name, start_year, end_period, end_month_name, end_year = match.groups()
            start = int(start_year) * 12
            if start_month_name:
                start += months[start_month_name.strip().lower()] - 1
            if end_period and end_period.lower() in ('present', 'current', 'now'):
                end = current_month
            else:
                end = int(end_year) * 12 + 11
                if end_month_name:
                    end = int(end_year) * 12 + months[end_month_name.strip().lower()] - 1
            if end >= start:
                intervals.append((start, end))

    if not intervals:
        return 0

    intervals.sort()
    total_months = 0
    range_start, range_end = intervals[0]
    for start, end in intervals[1:]:
        if start <= range_end + 1:
            range_end = max(range_end, end)
        else:
            total_months += range_end - range_start + 1
            range_start, range_end = start, end
    total_months += range_end - range_start + 1
    return total_months // 12


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
    """Count project entries in a project section, not generic resume bullets."""
    lines = text.splitlines()
    section_headers = re.compile(
        r'^\s*(?:academic\s+|personal\s+)?projects?(?:\s+(?:and|&)\s+'
        r'(?:research|publications))?\s*:?\s*$',
        re.IGNORECASE,
    )
    other_headers = re.compile(
        r'^\s*(?:education|skills|experience|work\s+experience|'
        r'professional\s+experience|certifications|summary|objective|'
        r'achievements|awards|references)\s*:?\s*$',
        re.IGNORECASE,
    )
    entries = 0
    in_projects = False
    for line in lines:
        stripped = line.strip()
        if section_headers.match(stripped):
            in_projects = True
            continue
        if in_projects and other_headers.match(stripped):
            break
        if not in_projects or not stripped:
            continue

        is_bullet = bool(re.match(r'^(?:[-*•▪►]|\d+[.)])\s+\S', stripped))
        title = re.sub(r'^(?:[-*•▪►]|\d+[.)])\s+', '', stripped)
        starts_with_action = bool(re.match(
            r'(?i)^(?:built|created|designed|developed|implemented|'
            r'integrated|managed|optimized|used|utilized|leveraged|'
            r'collaborated|worked|responsible)\b',
            title,
        ))
        is_title = bool(
            re.search(r'\b(?:project\s*\d*|application|app|system|platform|'
                      r'website|dashboard|model|tool|portfolio|'
                      r'machine\s+learning|data\s+analysis)\b',
                      title, re.IGNORECASE)
        )
        title_length = len(title.split())
        if is_title and not starts_with_action and (
            (is_bullet and title_length <= 12)
            or (not is_bullet and title_length <= 12 and not title.endswith('.'))
        ):
            entries += 1

    return entries


def parse_resume(file_path):
    """Full resume parsing pipeline — returns structured dict."""
    text = extract_text(file_path)

    if not text:
        return None

    skills = extract_skills(text)
    all_skills = list(dict.fromkeys(
        skill for category_skills in skills.values() for skill in category_skills
    ))

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
