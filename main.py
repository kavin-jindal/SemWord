'''import kagglehub

# Download latest version
path = kagglehub.dataset_download("thanakomsn/glove6b300dtxt")

print("Path to dataset files:", path)'''
 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
import pickle

def gen_word():
    wordlist = open('wordlist.txt', 'r')
    wd = wordlist.readlines()
    lines = [s.strip('\n') for s in wd]
    word = random.choice(lines)
    return word

def load():
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
    z = cosine_similarity(word.reshape(1, -1), user_word.reshape(1, -1))
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
    
def get_hints(dict_embed, word, n=5):
    '''secret = dict_embed[word.lower()]
    #print(secret)
    hints = []
    for i in dict_embed:
        h_word = dict_embed[i]
        sim = cos(h_word, secret)
        if sim=="Very Hot" or sim=="Hot":
            print(i)
            hints.append(i)
        
    return random.choice(hints)'''
    words = list(dict_embed.keys())
    matrix = np.stack([dict_embed[w] for w in words])
    secret_vec = dict_embed[word.lower()].reshape(1, -1)
    scores = cosine_similarity(secret_vec, matrix)[0]
    top_indices = np.argsort(scores)[::-1][1:n+1]
    return [words[i] for i in top_indices]

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

