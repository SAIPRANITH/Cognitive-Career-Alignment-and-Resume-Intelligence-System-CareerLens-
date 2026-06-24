import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
CHARTS_FOLDER = os.path.join(BASE_DIR, 'static', 'charts')
MODELS_FOLDER = os.path.join(BASE_DIR, 'models')
DATASETS_FOLDER = os.path.join(BASE_DIR, 'datasets')

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# ── Job Categories (must match Kaggle label encoder classes exactly) ──
JOB_CATEGORIES = [
    'Advocate', 'Arts', 'Automation Testing', 'Blockchain', 'Business Analyst',
    'Civil Engineer', 'Data Science', 'Database', 'DevOps Engineer', 'DotNet Developer',
    'ETL Developer', 'Electrical Engineering', 'HR', 'Hadoop', 'Health and fitness',
    'Java Developer', 'Mechanical Engineer', 'Network Security Engineer',
    'Operations Manager', 'PMO', 'Python Developer', 'SAP Developer', 'Sales',
    'Testing', 'Web Designing',
    # Extended categories (not in Kaggle model but supported via skill matching)
    'Cybersecurity', 'AI/ML Engineer', 'Robotics', 'Electronics & Communication'
]

# ── Skills pools per category (keys match Kaggle labels exactly) ──
SKILLS_MAP = {
    'Data Science': ['Python','R','SQL','TensorFlow','PyTorch','Pandas','NumPy','Scikit-learn','Deep Learning','NLP','Computer Vision','Machine Learning','Data Visualization','Tableau','Power BI'],
    'HR': ['Recruitment','Onboarding','Employee Relations','Performance Management','HR Policies','Talent Acquisition','Payroll','Conflict Resolution','Communication','Interviews'],
    'Advocate': ['Legal Research','Drafting','Litigation','Corporate Law','Contracts','Court Procedures','Negotiation','Compliance','Case Management','Client Counseling'],
    'Arts': ['Graphic Design','Illustration','Adobe Creative Suite','Typography','Visual Arts','Color Theory','Layout Design','Creativity','Painting','Digital Art'],
    'Web Designing': ['HTML','CSS','JavaScript','UI/UX','Figma','Adobe XD','Responsive Design','Bootstrap','Tailwind','Web Typography','Wireframing','Prototyping'],
    'Mechanical Engineer': ['AutoCAD','SolidWorks','Thermodynamics','Fluid Mechanics','CAD/CAM','Manufacturing','Material Science','FEA','Product Design','HVAC','ANSYS','Mechatronics','GD&T','Six Sigma','Lean Manufacturing','Pro-E','MATLAB','Robotics','Problem Solving','Analytical Skills','Project Management','Teamwork','Communication','Quality Control'],
    'Sales': ['B2B Sales','Lead Generation','CRM','Cold Calling','Negotiation','Account Management','Sales Strategy','Customer Satisfaction','Closing','Presentation'],
    'Health and fitness': ['Personal Training','Nutrition','Anatomy','Kinesiology','Workout Planning','Dietetics','CPR','First Aid','Wellness Coaching','Sports Science'],
    'Civil Engineer': ['AutoCAD','Structural Analysis','Revit','Construction Management','Surveying','Project Planning','Concrete Design','STAAD.Pro','Geotechnical','AutoCAD Civil 3D','ETABS','Primavera P6','BIM','SAP2000','Urban Planning','Estimation','Quantity Surveying','Problem Solving','Analytical Skills','Team Leadership','Communication','Risk Management'],
    'Java Developer': ['Java','Spring Boot','Hibernate','REST APIs','Microservices','SQL','Git','Maven','JUnit','OOP','Data Structures','Tomcat'],
    'Business Analyst': ['Requirement Gathering','Agile','Scrum','SQL','Data Analysis','Tableau','Visio','Process Modeling','JIRA','UML','User Stories','Stakeholder Management'],
    'SAP Developer': ['ABAP','SAP Fiori','OData','SAP HANA','SAP ERP','BAPI','ALE/IDoc','Web Dynpro','SAP UI5','Data Dictionary'],
    'Automation Testing': ['Selenium','TestNG','JUnit','Cucumber','Appium','Java','Python','Jenkins','CI/CD','API Testing','Postman','Agile'],
    'Electrical Engineering': ['Circuit Design','PCB Design','MATLAB','Microcontrollers','Power Systems','Simulink','PLC','Embedded Systems','Control Systems','C/C++','SCADA','High Voltage Engineering','Switchgear','LabVIEW','PSpice','Transformer Design','Electrical AutoCAD','FPGA','Problem Solving','Analytical Skills','Project Management','Communication','Troubleshooting'],
    'Operations Manager': ['Process Improvement','Supply Chain Management','Logistics','Team Leadership','Budgeting','Quality Assurance','Six Sigma','Inventory Management','Vendor Management'],
    'Python Developer': ['Python','Django','Flask','FastAPI','REST APIs','SQL','Git','Docker','Data Structures','Pandas','Pytest','Linux'],
    'DevOps Engineer': ['Docker','Kubernetes','AWS','Azure','Terraform','Ansible','Jenkins','CI/CD','Linux','Bash','Monitoring','Git'],
    'Network Security Engineer': ['Firewalls','VPN','Cisco','Routing','Switching','Wireshark','IDS/IPS','Network Architecture','Penetration Testing','Encryption'],
    'PMO': ['Project Management','Risk Management','Agile','Scrum','JIRA','Budgeting','Resource Allocation','Stakeholder Communication','MS Project','PMP'],
    'Database': ['SQL','MySQL','PostgreSQL','Oracle','MongoDB','Database Design','Query Optimization','ETL','Performance Tuning','Stored Procedures'],
    'Hadoop': ['Hadoop','Spark','Hive','Pig','Scala','Big Data','Kafka','MapReduce','HDFS','Sqoop','Flume'],
    'ETL Developer': ['Informatica','Data Warehousing','SQL','Talend','Data Modeling','Data Integration','Python','SSIS','Data Cleansing','Redshift'],
    'DotNet Developer': ['C#','.NET Core','ASP.NET','Entity Framework','SQL Server','MVC','Web API','LINQ','Visual Studio','Azure'],
    'Blockchain': ['Solidity','Ethereum','Smart Contracts','Web3.js','Cryptography','Blockchain Architecture','Hyperledger','Truffle','DeFi','Go'],
    'Testing': ['Manual Testing','Test Cases','JIRA','Bug Tracking','Agile','Regression Testing','Quality Assurance','API Testing','SQL','SDLC'],
    'Cybersecurity': ['Network Security','Penetration Testing','SIEM','Vulnerability Assessment','Incident Response','Python','Linux','Malware Analysis','OWASP','Cryptography'],
    'AI/ML Engineer': ['Python','TensorFlow','PyTorch','Scikit-learn','Docker','Kubernetes','MLOps','Deep Learning','NLP','Computer Vision','Model Deployment'],
    'Robotics': ['ROS','C++','Python','Computer Vision','Kinematics','Sensors','Control Systems','IoT','Machine Learning','Embedded Systems'],
    'Electronics & Communication': ['VLSI','VHDL','Verilog','Signal Processing','Analog Circuits','Digital Circuits','Antenna Design','RF Engineering','Communication Systems','Microprocessors','Wireless Communication','IoT','ARM','DSP','PCB Layout','Oscilloscope','Spectrum Analyzer','Telecommunications','Optical Communication','5G','LTE','Embedded Systems','MATLAB','C/C++']
}

EDUCATION_LEVELS = ['High School', "Bachelor's", "Master's", 'PhD']

EDUCATION_FIELDS = [
    'Computer Science','Information Technology','Data Science',
    'Electrical Engineering','Mathematics','Statistics',
    'Software Engineering','Cybersecurity','Business Analytics',
    'Mechanical Engineering','Physics','Economics'
]

CERTIFICATIONS_MAP = {
    'Data Science': ['AWS ML Specialty','TensorFlow Developer','Google Data Analytics','IBM Data Science','Microsoft Azure AI'],
    'Java Developer': ['Oracle Java SE','AWS Developer Associate','Spring Professional','Microsoft Azure Developer'],
    'Web Designing': ['Meta Front-End Developer','Google UX Design','MongoDB Developer','React Certification'],
    'DevOps Engineer': ['AWS Solutions Architect','CKA','Terraform Associate','Docker Certified Associate','Azure DevOps Engineer'],
    'Python Developer': ['PCAP','PCPP','AWS Developer Associate','Django Certification'],
    'Database': ['Oracle DBA','AWS Database Specialty','MongoDB DBA','Microsoft SQL Server','PostgreSQL Certified'],
    'Cybersecurity': ['CompTIA Security+','CEH','CISSP','OSCP','CISM'],
    'AI/ML Engineer': ['AWS ML Specialty','TensorFlow Developer','Google ML Engineer','Databricks ML Associate'],
    'Blockchain': ['Certified Blockchain Developer','Ethereum Developer','Hyperledger Certification'],
}

# Safety net: ensure all JOB_CATEGORIES have a SKILLS_MAP entry
for cat in JOB_CATEGORIES:
    if cat not in SKILLS_MAP:
        SKILLS_MAP[cat] = ['Communication', 'Teamwork', 'Problem Solving', 'Analytical Skills']
