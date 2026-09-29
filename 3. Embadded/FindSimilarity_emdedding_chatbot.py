from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2')
documents=[
    "Artificial intelligence is transforming the way humans interact with technology",
    "Machine learning models can analyze large amounts of data efficiently.",
    "Natural language processing helps computers understand human language.",
    "Deep learning techniques are widely used in image recognition systems.",
    "Cloud computing provides scalable resources for modern software applications."
]

query = "in image processing we use depp learning"

docu_embedding=embeddings.embed_documents(documents)

query_embedding=embeddings.embed_query(query)

score=cosine_similarity([query_embedding],docu_embedding)[0]
sorted_results = sorted(list(enumerate(score)), key=lambda x: x[1], reverse=True)
index, similarity_score = sorted_results[0]

print(documents[index])
print("similarity score is ", similarity_score)

