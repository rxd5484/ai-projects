# Vector search is a database it is gonna be hosted locally on our own computer using something called Chromadb quickly look up relevant information
# that we can pass to our model

from langchain_ollama import OllamaEmbeddings
from
from langchain_core.documents import Document
import os
import pandas as pd

df=pd.read_csv("realistic_restaurant_reviews.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db_location='./chrome_langchain_db'
add_documents = not os.path.exists(db_location)
