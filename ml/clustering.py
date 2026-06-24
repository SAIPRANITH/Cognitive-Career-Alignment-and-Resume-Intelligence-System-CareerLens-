"""
K-Means Clustering Module
Demonstrates: K-Means Clustering, PCA for visualization, cluster labelling.
Categorizes users into Beginner / Intermediate / Advanced.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


class ResumeClusterer:
    """Cluster resumes into Beginner / Intermediate / Advanced using K-Means."""

    CLUSTER_LABELS = ['Beginner', 'Intermediate', 'Advanced']
    CLUSTER_FEATURES = ['years_of_experience', 'skill_count', 'projects_count',
                        'education_encoded', 'cert_count', 'gpa']

    def __init__(self, n_clusters=3, random_state=42):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state,
                             n_init=10, max_iter=300)
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.is_fitted = False

    def fit(self, df):
        """Fit K-Means on resume features."""
        features = [c for c in self.CLUSTER_FEATURES if c in df.columns]
        X = df[features].values.astype(np.float64)
        X = np.nan_to_num(X, nan=0.0)

        # ── Scale features ──
        self.X_scaled = self.scaler.fit_transform(X)

        # ── Fit K-Means ──
        self.kmeans.fit(self.X_scaled)

        # ── PCA for 2D visualization ──
        self.X_pca = self.pca.fit_transform(self.X_scaled)

        self.is_fitted = True
        self.feature_names = features
        return self

    def predict(self, df):
        """Predict cluster for new data."""
        features = [c for c in self.CLUSTER_FEATURES if c in df.columns]
        X = df[features].values.astype(np.float64)
        X = np.nan_to_num(X, nan=0.0)
        X_scaled = self.scaler.transform(X)
        return self.kmeans.predict(X_scaled)

    def get_cluster_label(self, cluster_id):
        """Map cluster ID to readable label based on centroid values."""
        return self.CLUSTER_LABELS[cluster_id % len(self.CLUSTER_LABELS)]

    def fit_predict_with_labels(self, df):
        """Fit and return DataFrame with cluster labels."""
        self.fit(df)
        labels = self.kmeans.labels_

        # ── Sort clusters by centroid mean (experience + skills) to assign labels ──
        centroids = self.kmeans.cluster_centers_
        # Use first two features (experience, skill_count) for ordering
        centroid_scores = centroids[:, 0] + centroids[:, 1]
        sorted_indices = np.argsort(centroid_scores)

        label_map = {}
        for rank, idx in enumerate(sorted_indices):
            label_map[idx] = self.CLUSTER_LABELS[rank]

        df = df.copy()
        df['cluster_id'] = labels
        df['cluster_label'] = [label_map[l] for l in labels]
        df['pca_x'] = self.X_pca[:, 0]
        df['pca_y'] = self.X_pca[:, 1]

        return df

    def get_cluster_stats(self, df):
        """Get statistics per cluster."""
        stats = {}
        for label in self.CLUSTER_LABELS:
            cluster_df = df[df['cluster_label'] == label]
            if len(cluster_df) == 0:
                continue
            stats[label] = {
                'count': len(cluster_df),
                'avg_experience': round(cluster_df['years_of_experience'].mean(), 1),
                'avg_skills': round(cluster_df['skill_count'].mean(), 1),
                'avg_projects': round(cluster_df['projects_count'].mean(), 1),
                'avg_gpa': round(cluster_df['gpa'].mean(), 2),
                'top_categories': cluster_df['job_category'].value_counts().head(3).to_dict()
            }
        return stats

    def get_elbow_data(self, X_scaled=None, max_k=10):
        """Compute inertia for elbow method chart."""
        if X_scaled is None:
            X_scaled = self.X_scaled
        inertias = []
        silhouettes = []
        K_range = range(2, max_k + 1)
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            inertias.append(km.inertia_)
            silhouettes.append(silhouette_score(X_scaled, km.labels_))
        return list(K_range), inertias, silhouettes

    def predict_single(self, features_dict):
        """Predict cluster for a single resume."""
        values = []
        for col in self.CLUSTER_FEATURES:
            values.append(features_dict.get(col, 0))
        X = np.array([values], dtype=np.float64)
        X_scaled = self.scaler.transform(X)
        cluster = self.kmeans.predict(X_scaled)[0]

        centroids = self.kmeans.cluster_centers_
        centroid_scores = centroids[:, 0] + centroids[:, 1]
        sorted_indices = np.argsort(centroid_scores)
        label_map = {idx: self.CLUSTER_LABELS[rank]
                     for rank, idx in enumerate(sorted_indices)}

        return label_map[cluster]
