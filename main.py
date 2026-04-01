'''import kagglehub

# Download latest version
path = kagglehub.dataset_download("thanakomsn/glove6b300dtxt")

print("Path to dataset files:", path)'''
 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
import pickle
from pinecone import Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os
load_dotenv() 
pc = Pinecone(api_key=os.getenv("PINECONE"))
'''pc.create_index(name="semword-index", dimension=300, 
spec=ServerlessSpec(
cloud="aws",
region="us-east-1"
))'''
index = pc.Index("semword-index")
def gen_word():
    wordlist = open('wordlist.txt', 'r')
    wd = wordlist.readlines()
    lines = [s.strip('\n') for s in wd]
    word = random.choice(lines)
    return word

def get_vector(term):
    
    x= index.fetch(ids=[term])
    y=(x['vectors'].items())
    for vector_id, vector_data in y:
        return (vector_data['values'])
def load():
    index = pc.Index("semword-index")
    with open("embeddings_common.pkl", "rb") as f:
        return pickle.load(f)
    '''vectors = open('embeddings_common.pkl', 'rb', errors="ignore")    
    v = vectors.readlines()
    dict_embed = {}
    for i in v:
        parts = i.split()
        dict_embed[parts[0].lower()]=np.array(parts[1:], dtype=np.float32)
   
    with open("embeddings.pkl", "wb") as f:
        pickle.dump(dict_embed, vectors)
    return dict_embed'''
def cos(word, user_word):
    z = cosine_similarity(np.array(word).reshape(1, -1), np.array(user_word).reshape(1, -1))
    if z < 0.4: 
        return "Cold"
    elif z > 0.4 and z < 0.6:
        return "Warm"
    elif z > 0.6 and z < 0.8:
        return "Hot"
    elif z > 0.8 and z < 0.98:
        return "Very Hot"
    elif z > 0.98:
        return "Done!"

        
    else:
        return "Error occurred"
    
def get_hints(word, n=5):
    secret_vec = get_vector(word.lower())

    matches = index.query(
        vector=secret_vec,
        top_k=500
    )

    hints = [
        m["id"] for m in matches["matches"]
        if m["id"] != word.lower() and m["score"] > 0.6
    ]

    return random.sample(hints, min(n, len(hints)))

'''def find_vector(term):
    
    return dict_embed.get(term.lower(), None)'''
'''while True:   
    user_in = input("Type here: ")

    check = user_in.split()

    if len(check)>1:
        print("Only one word allowed in input")
    word_vector = np.array(find_vector(word))
    user_vector = np.array(find_vector(user_in))

    if user_vector is None:
        print("Word not found")
    
    res = cos(word_vector, user_vector)
        
    print(res)'''

