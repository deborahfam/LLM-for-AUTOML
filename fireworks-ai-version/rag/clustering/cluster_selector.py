class ClusterSelector:
    def __init__(self, clustering_algorithm):
        self.clustering_algorithm = clustering_algorithm

    def select_representative_documents(self, documents, embeddings):
        clustered_docs = self.clustering_algorithm.get_clustered_documents(documents, embeddings)
        representative_docs = []
        for cluster, docs in clustered_docs.items():
            representative_docs.append(docs[0])
        return representative_docs