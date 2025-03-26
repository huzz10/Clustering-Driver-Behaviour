import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns


file_path = "E:/Huzaifa E/Python/ML/reduced_data.csv"
data = pd.read_csv(file_path)


data_clean = data.drop(columns=['Unnamed: 0'])


le = LabelEncoder()
data_clean['class'] = le.fit_transform(data_clean['class'])

features = ['accelX', 'accelY', 'accelZ', 'gyroX', 'gyroY', 'gyroZ']
X_cluster = data_clean[features]


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)


inertia = []
k_values = range(1, 11)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)


plt.figure(figsize=(8, 5))
plt.plot(k_values, inertia, marker='o', linestyle='--', color='b')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal K')
plt.show()


optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

data_clean['Cluster'] = clusters

sns.pairplot(data_clean, hue='Cluster', diag_kind='kde', palette='Set1')
plt.show()


cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
cluster_df = pd.DataFrame(cluster_centers, columns=features)
print("\nCluster Centers:\n", cluster_df)

risk_analysis = data_clean.groupby('Cluster')[features].mean()
print("\nCluster-wise Risk Analysis:\n", risk_analysis)

