import unittest
from datetime import date
from unittest.mock import patch

from ml.resume_parser import (
    extract_experience_years,
    extract_projects_count,
    parse_resume,
)


class ResumeParserFeatureTests(unittest.TestCase):
    def test_skill_count_deduplicates_skills_across_categories(self):
        with patch('ml.resume_parser.extract_text', return_value='MongoDB Swift'):
            parsed = parse_resume('resume.pdf')

        self.assertEqual(parsed['skill_count'], 2)
        self.assertEqual(sum(map(len, parsed['skills'].values())), 4)

    def test_project_count_only_counts_project_titles_in_project_section(self):
        resume = '''WORK EXPERIENCE
- Coordinated a project team

PROJECTS
Personal Portfolio Website
- Developed responsive pages using CSS.
- Library Management System
- Built borrowing and return workflows.

EDUCATION
BTech'''

        self.assertEqual(extract_projects_count(resume), 2)
        self.assertEqual(
            extract_projects_count('EXPERIENCE\n- Built a website\n- Managed a project'),
            0,
        )

    def test_experience_date_ranges_merge_overlapping_jobs(self):
        resume = '''WORK EXPERIENCE
Engineer | Jan 2020 - Dec 2022
Developer | Jan 2022 - Dec 2024
EDUCATION
BTech'''

        self.assertEqual(extract_experience_years(resume), 5)

    def test_present_job_range_uses_current_date(self):
        resume = '''EMPLOYMENT HISTORY
Engineer | Jan 2020 - Present
EDUCATION
BTech'''
        expected_months = date.today().year * 12 + date.today().month - (2020 * 12)

        self.assertEqual(extract_experience_years(resume), expected_months // 12)

    def test_missing_project_and_experience_sections_return_zero(self):
        resume = 'EDUCATION\nBTech\nSKILLS\nPython'

        self.assertEqual(extract_projects_count(resume), 0)
        self.assertEqual(extract_experience_years(resume), 0)


if __name__ == '__main__':
    unittest.main()
