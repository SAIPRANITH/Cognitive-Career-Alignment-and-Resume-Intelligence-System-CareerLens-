"""
Flask Web Application — Career Lens
"""
import os, uuid
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, jsonify)
from werkzeug.utils import secure_filename
import joblib

from config import (UPLOAD_FOLDER, CHARTS_FOLDER, MODELS_FOLDER,
                    DATASETS_FOLDER, ALLOWED_EXTENSIONS, JOB_CATEGORIES, SKILLS_MAP)
from ml.resume_parser import parse_resume
from ml.visualizations import (plot_role_probabilities, plot_skill_distribution,
                                plot_salary_estimation)
from ml.ai_generator import generate_resume_feedback


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

for folder in [UPLOAD_FOLDER, CHARTS_FOLDER, MODELS_FOLDER, DATASETS_FOLDER]:
    os.makedirs(folder, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_models():
    models = {}
    try:
        models['classifier'] = joblib.load(os.path.join(MODELS_FOLDER, 'classifier.pkl'))
    except Exception as e:
        print(f"[Warning] Classifier not loaded: {e}")

    try:
        models['vectorizer'] = joblib.load(os.path.join(MODELS_FOLDER, 'vectorizer.pkl'))
    except Exception as e:
        print(f"[Warning] Vectorizer not loaded: {e}")

    try:
        models['encoder'] = joblib.load(os.path.join(MODELS_FOLDER, 'label_encoder.pkl'))
    except Exception as e:
        print(f"[Warning] Encoder not loaded: {e}")

    try:
        models['clusterer'] = joblib.load(os.path.join(MODELS_FOLDER, 'clusterer.pkl'))
    except Exception:
        pass

    return models


MODELS = load_models()


@app.route('/')
def index():
    """Main Landing Page."""
    return render_template('index.html')

@app.route('/chart/<filename>')
def serve_chart(filename):
    from flask import send_from_directory
    return send_from_directory(CHARTS_FOLDER, filename)

@app.route('/dashboard')
def dashboard():
    """Main dashboard (Hub)."""
    return render_template('dashboard.html', categories=JOB_CATEGORIES)



@app.route('/role-checker-tool')
def role_checker_tool():
    return render_template('role_checker.html', categories=JOB_CATEGORIES)


@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('dashboard'))

    file = request.files['resume']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload PDF or DOCX.', 'error')
        return redirect(url_for('dashboard'))

    filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    parsed = parse_resume(filepath)
    if not parsed:
        flash('Could not extract text from resume. Please try a different file.', 'error')
        return redirect(url_for('dashboard'))

    if 'classifier' not in MODELS or 'encoder' not in MODELS or 'vectorizer' not in MODELS:
        flash('Models not trained yet. Run train_model.py first.', 'error')
        return redirect(url_for('dashboard'))

    clusterer = MODELS.get('clusterer')

    edu_map = {'10th': 0, 'Intermediate': 1, 'BTech': 2, 'MTech': 3, 'PhD': 4}
    resume_data = {
        'education_encoded': edu_map.get(parsed['education_level'], 1),
        'cert_count': len([c for c in parsed['certifications'] if c != 'None']),
    }
    
    resume_text = parsed.get('text', parsed.get('skills_flat', ''))
    
    if len(resume_text) < 50:
        resume_text += " " + parsed.get('skills_flat', '')

    vectorizer = MODELS.get('vectorizer')
    classifier = MODELS.get('classifier')
    encoder = MODELS.get('encoder')

    if vectorizer and classifier and encoder:
        X = vectorizer.transform([resume_text])
        ml_probs = classifier.predict_proba(X)[0]
        
        all_roles = []
        for i, prob in enumerate(ml_probs):
            all_roles.append({
                'role': encoder.inverse_transform([i])[0],
                'probability': round(float(prob * 100), 1) # Raw percentage rounded to 1 decimal
            })
    else:
        all_roles = [{'role': 'Data Science', 'probability': 85.0}]
    user_skills = set(s.strip().lower() for cat in parsed['skills'].values() for s in cat)
    
    blended_roles = []
    for role_info in all_roles:
        r_name = role_info['role']
        ml_prob = role_info['probability']
        
        orig_role_skills = SKILLS_MAP.get(r_name, [])
        if not orig_role_skills:
            orig_role_skills = ['Programming', 'Analysis', 'Communication', 'Problem Solving']

        missing = []
        matched = []
        for orig_s in orig_role_skills:
            if orig_s.lower() in user_skills:
                matched.append(orig_s)
            else:
                if len(missing) < 10:
                    missing.append(orig_s)
        
        role_skills_len = len(orig_role_skills)

        match_ratio = min(1.0, len(matched) / min(8, max(1, role_skills_len)))
        
        if len(matched) == 0:
            final_prob = min(ml_prob, 15.0)
        else:
            final_prob = round((ml_prob * 0.3) + (match_ratio * 100 * 0.7), 1)
            if match_ratio >= 0.8:
                final_prob = round(min(98.5, final_prob * 1.35), 1)
            elif match_ratio >= 0.5:
                final_prob = round(min(85.0, final_prob * 1.2), 1)
                
        blended_roles.append({
            'role': r_name,
            'probability': round(final_prob, 1),
            'missing_skills': missing,
            'matched_skills': matched
        })

    blended_roles.sort(key=lambda x: x['probability'], reverse=True)
    top_roles = blended_roles[:5]

    roles = [r['role'] for r in top_roles]
    probs = [r['probability'] for r in top_roles]
    plot_role_probabilities(roles, probs, 'user_role_probs.png')
    plot_skill_distribution(parsed['skills'], 'user_skill_dist.png')

    cluster_label = 'Intermediate'
    if clusterer and vectorizer:
        try:
            cluster_pred = clusterer.predict(vectorizer.transform([resume_text]))[0]
            cluster_map = {0: 'Entry-Level', 1: 'Intermediate', 2: 'Senior'}
            cluster_label = cluster_map.get(cluster_pred, 'Intermediate')
        except Exception:
            pass

    skill_pts = min(40, parsed['skill_count'] * 2)
    exp_pts = min(25, parsed['years_of_experience'] * 4)
    proj_pts = min(15, parsed['projects_count'] * 3)
    cert_pts = min(10, resume_data['cert_count'] * 5)
    edu_pts = min(10, edu_map.get(parsed['education_level'], 1) * 3)
    
    score = int(skill_pts + exp_pts + proj_pts + cert_pts + edu_pts)

    capped_skills = min(parsed['skill_count'], 25)
    capped_exp = min(parsed['years_of_experience'], 15)
    pred_salary = round(resume_data['education_encoded'] * 2.0 +
                        capped_exp * 1.5 +
                        capped_skills * 0.3 + 4.0, 1)
    
    # Adjust salary based on cluster to add ML context
    cluster_mult = {'Entry-Level': 1.0, 'Intermediate': 1.3, 'Senior': 1.8}
    pred_salary = round(pred_salary * cluster_mult.get(cluster_label, 1.0), 1)
    pred_salary = max(3.0, pred_salary)
    
    max_market = max(35.0, pred_salary + 5.0)
    plot_salary_estimation(3.0, 12.0, max_market, pred_salary, 'user_salary.png')


    result = {
        'filename': file.filename,
        'parsed': parsed,
        'top_roles': top_roles,
        'score': score,
        'cluster_label': cluster_label,
        'salary_estimate': pred_salary,
        'top_3_roles': blended_roles[:3],
    }

    response = render_template('analysis.html', result=result, categories=JOB_CATEGORIES)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception:
            pass
    return response


@app.route('/check-role', methods=['POST'])
def check_role():
    """Check probability for a specific target role from manual input."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
        
    target_role = data.get('role', '')
    skills = data.get('skills', '')
    try:
        experience = int(data.get('experience', 0))
    except (ValueError, TypeError):
        experience = 0
    education = data.get('education', "BTech")

    result = _calculate_role_eligibility(target_role, skills, experience, education, resume_text=None)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)

@app.route('/api/check-role-file', methods=['POST'])
def check_role_file():
    """Check probability for a target role using an uploaded resume file."""
    target_role = request.form.get('role', '')
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file uploaded'}), 400
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Upload PDF or DOCX'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        parsed = parse_resume(filepath)
        if not parsed:
            return jsonify({'error': 'Could not extract text from resume'}), 400
        
        parsed_skills = parsed.get('skills', [])
        if isinstance(parsed_skills, dict):
            skills_list = [s for cat in parsed_skills.values() for s in cat]
        else:
            skills_list = parsed_skills
        skills = ", ".join(skills_list)
        
        resume_text = parsed.get('text', parsed.get('skills_flat', ''))
        if len(resume_text) < 50:
            resume_text += " " + parsed.get('skills_flat', '')
        
        education = parsed.get('education_level', 'BTech')
                    
        experience = parsed.get('years_of_experience', 0)
        
        result = _calculate_role_eligibility(target_role, skills, experience, education, resume_text=resume_text)
        if 'error' in result:
            return jsonify(result), 400
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass

def _calculate_role_eligibility(target_role, skills, experience, education, resume_text=None):
    """Core logic to evaluate a candidate against a target role."""

    if 'classifier' not in MODELS or 'encoder' not in MODELS or 'vectorizer' not in MODELS:
        return {'error': 'Models not trained'}

    skill_list = [s.strip() for s in skills.split(',') if s.strip()]

    vectorizer = MODELS.get('vectorizer')
    classifier = MODELS.get('classifier')
    encoder = MODELS.get('encoder')

    user_skills_lower = set(s.lower() for s in skill_list)

    def get_blended_prob(raw_prob, role_name):
        role_skills = SKILLS_MAP.get(role_name, [])
        if not role_skills:
            return round(raw_prob, 1)
        
        matched_count = sum(1 for s in role_skills if s.lower() in user_skills_lower)
        match_ratio = min(1.0, matched_count / min(8, max(1, len(role_skills))))
        
        if matched_count == 0:
            return min(round(raw_prob, 1), 15.0)
            
        prob = (raw_prob * 0.3) + (match_ratio * 100 * 0.7)
        if match_ratio >= 0.8:
            prob = min(98.5, prob * 1.35)
        elif match_ratio >= 0.5:
            prob = min(85.0, prob * 1.2)
            
        return round(prob, 1)

    probability = 15.0
    top_roles = []
    
    if vectorizer and classifier and encoder:
        if resume_text and len(resume_text) > 50:
            X = vectorizer.transform([resume_text])
        else:
            context_skills = f"experienced professional specializing in {skills} i have built extensive projects utilizing {skills} dedicated to continuous learning"
            X = vectorizer.transform([context_skills])
            
        ml_probs = classifier.predict_proba(X)[0]
        
        target_idx = -1
        for i, c in enumerate(encoder.classes_):
            if target_role.lower() == c.lower():
                target_idx = i
                break
                
        if target_idx != -1:
            probability = get_blended_prob(float(ml_probs[target_idx] * 100), target_role)
            
        top_indices = ml_probs.argsort()[::-1]
        top_roles = []
        for i in top_indices:
            role_name = encoder.inverse_transform([i])[0]
            if role_name.lower() != target_role.lower():
                top_roles.append({
                    'role': role_name,
                    'probability': get_blended_prob(float(ml_probs[i] * 100), role_name)
                })
        
        top_roles.sort(key=lambda x: x['probability'], reverse=True)
        top_roles = top_roles[:5]

    orig_role_skills = SKILLS_MAP.get(target_role, [])
    if not orig_role_skills:
        orig_role_skills = ['Communication', 'Teamwork', 'Problem Solving']

    missing = []
    matched = []
    for orig_s in orig_role_skills:
        if orig_s.lower() in user_skills_lower:
            matched.append(orig_s)
        else:
            if len(missing) < 10:
                missing.append(orig_s)

    suggestions = []
    if probability < 30:
        suggestions.append("Consider taking online courses in the missing skills listed above")
        suggestions.append("Build at least 3-5 projects demonstrating these skills")
        suggestions.append("Earn relevant certifications to strengthen your profile")
    elif probability < 60:
        suggestions.append("You're on the right track! Focus on the missing skills")
        suggestions.append("Consider contributing to open-source projects in this domain")
        suggestions.append("Network with professionals in this field")
    else:
        suggestions.append("Great profile match! Focus on interview preparation")
        suggestions.append("Consider specializing in a niche area within this role")
        suggestions.append("Build a portfolio showcasing your best projects")

    return {
        'role': target_role,
        'probability': probability,
        'top_roles': top_roles,
        'missing_skills': missing,
        'matched_skills': matched,
        'suggestions': suggestions
    }


@app.route('/api/generate-feedback', methods=['POST'])
def api_generate_feedback():
    """API: Generate AI feedback for resume."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400
    resume_text = data.get('resume_text', '')
    if not resume_text.strip():
        return jsonify({'error': 'Resume text is required'}), 400
    target_role = data.get('role', 'General')
    feedback = generate_resume_feedback(resume_text, target_role)
    return jsonify({'markdown': feedback})


@app.route('/ai-feedback')
def ai_feedback_tool():
    """Render AI Feedback Tool page."""
    return render_template('ai_feedback.html', categories=JOB_CATEGORIES)


@app.route('/api/generate-feedback-file', methods=['POST'])
def api_generate_feedback_file():
    """API: Generate AI feedback using an uploaded resume file."""
    target_role = request.form.get('role', 'General')
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file uploaded'}), 400
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Upload PDF or DOCX'}), 400
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        parsed = parse_resume(filepath)
        if not parsed:
            return jsonify({'error': 'Could not extract text from resume'}), 400
        resume_text = parsed.get('text', '')
        if not resume_text.strip():
            # Fallback to skills_flat if full text extraction failed
            resume_text = parsed.get('skills_flat', '')
            
        if not resume_text.strip():
            return jsonify({'error': 'Could not extract text from the resume'}), 400
            
        feedback = generate_resume_feedback(resume_text, target_role)
        return jsonify({'markdown': feedback})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass




if __name__ == '__main__':
    print("\nStarting Career Lens...")
    print("   Visit: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
