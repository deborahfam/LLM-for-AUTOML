import numpy as np
from sklearn.cluster import KMeans

class ClusteringAlgorithm:
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters

    def fit(self, embeddings):
        kmeans = KMeans(n_clusters=self.n_clusters)
        kmeans.fit(embeddings)
        return kmeans.labels_, kmeans.cluster_centers_

    def get_clustered_documents(self, documents, embeddings):
        labels, centers = self.fit(embeddings)
        clustered_docs = {}
        for label, doc in zip(labels, documents):
            if label not in clustered_docs:
                clustered_docs[label] = []
            clustered_docs[label].append(doc)
        return clustered_docs