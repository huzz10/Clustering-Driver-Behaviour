import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score
from scipy.cluster.hierarchy import dendrogram, linkage

file_path = "E:/Huzaifa E/Python/ML/reduced_data.csv"
df = pd.read_csv(file_path)
df.drop(columns=["Unnamed: 0", "class"], inplace=True, errors='ignore')
df.drop_duplicates(inplace=True)
scaler = StandardScaler()
data_scaled = scaler.fit_transform(df)

# K-Means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(data_scaled)
kmeans_silhouette = silhouette_score(data_scaled, kmeans_labels)
kmeans_db = davies_bouldin_score(data_scaled, kmeans_labels)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=data_scaled[:, 0], y=data_scaled[:, 1], hue=kmeans_labels, palette='viridis', alpha=0.6)
plt.title("K-Means Clustering")
plt.show()
print(f"K-Means Silhouette Score: {kmeans_silhouette:.4f}")
print(f"K-Means Davies-Bouldin Score: {kmeans_db:.4f}")

# DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=10)
dbscan_labels = dbscan.fit_predict(data_scaled)
if len(set(dbscan_labels)) > 1:  
    dbscan_silhouette = silhouette_score(data_scaled, dbscan_labels)
    dbscan_db = davies_bouldin_score(data_scaled, dbscan_labels)
else:
    dbscan_silhouette, dbscan_db = -1, -1  
plt.figure(figsize=(8, 6))
sns.scatterplot(x=data_scaled[:, 0], y=data_scaled[:, 1], hue=dbscan_labels, palette='viridis', alpha=0.6)
plt.title("DBSCAN Clustering")
plt.show()
print(f"DBSCAN Silhouette Score: {dbscan_silhouette:.4f}")
print(f"DBSCAN Davies-Bouldin Score: {dbscan_db:.4f}")

# Hierarchical Clustering
hierarchical = AgglomerativeClustering(n_clusters=3)
hierarchical_labels = hierarchical.fit_predict(data_scaled)
hierarchical_silhouette = silhouette_score(data_scaled, hierarchical_labels)
hierarchical_db = davies_bouldin_score(data_scaled, hierarchical_labels)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=data_scaled[:, 0], y=data_scaled[:, 1], hue=hierarchical_labels, palette='viridis', alpha=0.6)
plt.title("Hierarchical Clustering")
plt.show()
print(f"Hierarchical Silhouette Score: {hierarchical_silhouette:.4f}")
print(f"Hierarchical Davies-Bouldin Score: {hierarchical_db:.4f}")
plt.figure(figsize=(10, 6))
linkage_matrix = linkage(data_scaled, method='ward')
dendrogram(linkage_matrix)
plt.title("Dendrogram for Hierarchical Clustering")
plt.show()
