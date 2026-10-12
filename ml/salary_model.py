def estimate_salary(education_encoded, years_of_experience, skill_count, cluster_label):
    capped_skills = min(skill_count, 25)
    capped_exp = min(years_of_experience, 15)
    base_salary = round(
        education_encoded * 2.0 + capped_exp * 1.5 + capped_skills * 0.3 + 4.0,
        1,
    )
    cluster_mult = {'Entry-Level': 1.0, 'Intermediate': 1.3, 'Senior': 1.8}
    return max(3.0, round(base_salary * cluster_mult.get(cluster_label, 1.0), 1))
