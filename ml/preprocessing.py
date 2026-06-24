"""
Data Preprocessing Module
Demonstrates: Pandas, NumPy, Data Cleaning, Missing Value Handling,
Label Encoding, Ordinal Encoding, One-Hot Encoding, GroupBy, Filtering.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from config import EDUCATION_LEVELS, JOB_CATEGORIES


class DataCleaner:
    """Handles all data cleaning operations with a full report."""

    def __init__(self, df):
        self.original_df = df.copy()
        self.df = df.copy()
        self.report = {
            'original_shape': df.shape,
            'duplicates_removed': 0,
            'missing_before': {},
            'missing_after': {},
            'outliers_handled': {},
            'steps': []
        }

    def remove_duplicates(self):
        before = len(self.df)
        # Drop duplicates based ONLY on 'skills' (which holds the full Kaggle resume text)
        # This prevents exact duplicate resumes from leaking into both train and test sets.
        self.df = self.df.drop_duplicates(subset=['skills'], keep='first')
        removed = before - len(self.df)
        self.report['duplicates_removed'] = removed
        self.report['steps'].append(f"Removed {removed} duplicate rows based on text content")
        return self

    def handle_missing_values(self):
        missing = self.df.isnull().sum()
        self.report['missing_before'] = missing[missing > 0].to_dict()

        # ── NumPy median fill for numeric columns ──
        if 'gpa' in self.df.columns:
            median_gpa = np.nanmedian(self.df['gpa'].values)
            self.df['gpa'] = self.df['gpa'].fillna(median_gpa)
            self.report['steps'].append(f"Filled GPA missing values with median: {median_gpa:.2f}")

        if 'publications_count' in self.df.columns:
            self.df['publications_count'] = self.df['publications_count'].fillna(0)
            self.report['steps'].append("Filled publications_count with 0")

        if 'salary_lpa' in self.df.columns:
            # ── GroupBy: fill salary by category median ──
            medians = self.df.groupby('job_category')['salary_lpa'].transform('median')
            self.df['salary_lpa'] = self.df['salary_lpa'].fillna(medians)
            overall_median = np.nanmedian(self.df['salary_lpa'].values)
            self.df['salary_lpa'] = self.df['salary_lpa'].fillna(overall_median)
            self.report['steps'].append("Filled salary with category-wise median (GroupBy)")

        if 'certifications' in self.df.columns:
            self.df['certifications'] = self.df['certifications'].fillna('None')
            self.report['steps'].append("Filled certifications with 'None'")

        self.report['missing_after'] = self.df.isnull().sum()[self.df.isnull().sum() > 0].to_dict()
        return self

    def handle_outliers(self, columns=None):
        if columns is None:
            columns = ['gpa', 'years_of_experience', 'salary_lpa', 'projects_count']
        for col in columns:
            if col not in self.df.columns:
                continue
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = ((self.df[col] < lower) | (self.df[col] > upper)).sum()
            self.df[col] = np.clip(self.df[col].values, lower, upper)
            self.report['outliers_handled'][col] = int(outliers)
            self.report['steps'].append(f"Clipped {outliers} outliers in '{col}' to [{lower:.2f}, {upper:.2f}]")
        return self

    def clean(self):
        return self.remove_duplicates().handle_missing_values().handle_outliers()

    def get_report(self):
        self.report['final_shape'] = self.df.shape
        return self.report

    def get_clean_data(self):
        return self.df


class DataEncoder:
    """Demonstrates Label, Ordinal, and One-Hot encoding."""

    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.ordinal_encoder = OrdinalEncoder(
            categories=[EDUCATION_LEVELS],
            handle_unknown='use_encoded_value',
            unknown_value=-1
        )
        self.onehot_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.tfidf = TfidfVectorizer(max_features=100, stop_words='english')
        self.is_fitted = False

    def fit(self, df):
        # ── Label Encoding on job_category ──
        self.label_encoder.fit(df['job_category'])

        # ── Ordinal Encoding on education_level ──
        self.ordinal_encoder.fit(df[['education_level']])

        # ── One-Hot Encoding on field_of_study ──
        self.onehot_encoder.fit(df[['field_of_study']])

        # ── TF-IDF on skills text ──
        self.tfidf.fit(df['skills'])

        self.is_fitted = True
        return self

    def transform(self, df):
        result = df.copy()

        # ── Label Encoding ──
        result['job_category_encoded'] = self.label_encoder.transform(result['job_category'])

        # ── Ordinal Encoding ──
        result['education_encoded'] = self.ordinal_encoder.transform(
            result[['education_level']]
        ).flatten()

        # ── One-Hot Encoding ──
        ohe_array = self.onehot_encoder.transform(result[['field_of_study']])
        ohe_cols = self.onehot_encoder.get_feature_names_out(['field_of_study'])
        ohe_df = pd.DataFrame(ohe_array, columns=ohe_cols, index=result.index)
        result = pd.concat([result, ohe_df], axis=1)

        # ── Derived features using NumPy ──
        result['skill_count'] = result['skills'].apply(lambda x: len(str(x).split(',')))
        result['cert_count'] = result['certifications'].apply(
            lambda x: 0 if str(x).strip() == 'None' else len(str(x).split(','))
        )
        result['lang_count'] = result['programming_languages'].apply(
            lambda x: len(str(x).split(','))
        )

        return result

    def fit_transform(self, df):
        return self.fit(df).transform(df)

    def get_tfidf_matrix(self, skills_series):
        return self.tfidf.transform(skills_series)

    def get_tfidf_features(self):
        return self.tfidf.get_feature_names_out()

    def get_encoding_demo(self, df):
        """Return a summary of all encoding operations for display."""
        sample = df.head(10)
        demo = {
            'label_encoding': {
                'description': 'Maps each job category to a unique integer',
                'mapping': dict(zip(
                    self.label_encoder.classes_,
                    self.label_encoder.transform(self.label_encoder.classes_).tolist()
                )),
                'sample': sample[['job_category']].copy()
            },
            'ordinal_encoding': {
                'description': 'Maps education levels to ordered integers (High School=0 < PhD=3)',
                'order': EDUCATION_LEVELS,
                'sample': sample[['education_level']].copy()
            },
            'onehot_encoding': {
                'description': 'Creates binary columns for each field of study',
                'columns': list(self.onehot_encoder.get_feature_names_out(['field_of_study'])),
                'sample': sample[['field_of_study']].copy()
            }
        }
        return demo


class FeatureEngineer:
    """Extract ML-ready feature matrix from processed DataFrame."""

    FEATURE_COLS = [
        'education_encoded', 'years_of_experience', 'gpa',
        'skill_count', 'cert_count', 'projects_count',
        'publications_count', 'lang_count', 'salary_lpa'
    ]

    @staticmethod
    def get_feature_matrix(df, tfidf_matrix=None):
        """Return X (features), y (labels) for classification."""
        features = []
        for col in FeatureEngineer.FEATURE_COLS:
            if col in df.columns:
                features.append(col)

        # Add one-hot encoded columns
        ohe_cols = [c for c in df.columns if c.startswith('field_of_study_')]
        features.extend(ohe_cols)

        X = df[features].values.astype(np.float64)
        
        # Merge TF-IDF into X
        if tfidf_matrix is not None:
            # tfidf_matrix is a sparse matrix, convert to dense and concatenate
            tfidf_dense = tfidf_matrix.toarray()
            X = np.hstack((X, tfidf_dense))

        y = df['job_category_encoded'].values.astype(np.int64)

        # Handle any remaining NaN
        X = np.nan_to_num(X, nan=0.0)
        return X, y, features

    @staticmethod
    def get_pandas_summary(df):
        """Demonstrate Pandas Series and DataFrame operations."""
        summary = {
            'shape': df.shape,
            'dtypes': df.dtypes.to_dict(),
            'describe': df.describe().to_dict(),
            'category_counts': df['job_category'].value_counts().to_dict(),
            'edu_counts': df['education_level'].value_counts().to_dict(),
            'avg_exp_by_category': df.groupby('job_category')['years_of_experience'].mean().to_dict(),
            'avg_salary_by_category': df.groupby('job_category')['salary_lpa'].mean().to_dict(),
            'top_locations': df['location'].value_counts().head(5).to_dict(),
            'correlation': df[['years_of_experience', 'gpa', 'projects_count',
                               'salary_lpa']].corr().to_dict()
        }
        return summary
