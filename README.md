# Career Lens

Hey there! Welcome to Career Lens, a smart resume analyzer and career alignment tool I built to help people figure out how well their skills match up with the jobs they actually want. 

Instead of just guessing if your resume is "good enough," Career Lens reads your resume, extracts your skills and experience, and runs it through a custom Machine Learning model to show you exactly where you stand against 20+ different tech and non-tech roles.

# What it actually does:
- Resume Parsing: Drop your PDF or DOCX resume in, and it automatically pulls out your skills, education (yep, it supports Indian CGPA and degrees like B.Tech/MCA!), and years of experience.
- Role Checking: Wondering if you're ready for a Data Scientist role? It'll give you a percentage match score and tell you exactly which skills you're missing.
- AI Feedback: It hooks into Google's Gemini AI to give you actual, readable advice on how to improve your resume based on your target role.
- Data Visualizations: Check out the interactive dashboard to see how salaries and experience levels stack up across different industries.



#  How to run it on your own machine

If you want to spin this up locally, it's super easy. Just follow these steps:

1. Clone the repository
Open up your terminal and grab the code:
```bash
git clone https://github.com/SAIPRANITH/Cognitive-Career-Alignment-and-Resume-Intelligence-System-CareerLens-.git
cd Cognitive-Career-Alignment-and-Resume-Intelligence-System-CareerLens-
```

2. Set up a Virtual Environment (Highly Recommended)
This keeps the project's packages from messing with your global Python setup.
```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

3. Install the packages
Now install everything the app needs to run (Flask, pandas, scikit-learn, etc.):
```bash
pip install -r requirements.txt
```

4. Hook up the AI (Optional but recommended)
To get the smart AI feedback working, you'll need a free Google Gemini API key.

A. Create a file called `.env` right in the main project folder.

B. Paste your API key in there like this:

   ```text
   GEMINI_API_KEY="your_api_key_here"
   ```
(If you don't add an API key, the app will still work, but it'll just use basic pre-written text instead of the AI.)

5. Fire it up!
Start the Flask server:
```bash
python app.py
```

6. Open it in your browser
Once the server says it's running, open your web browser and go to:
http://127.0.0.1:5000

---
Enjoy using Career Lens! Feel free to open issues or contribute if you find any bugs.
