'''import kagglehub

# Download latest version
path = kagglehub.dataset_download("thanakomsn/glove6b300dtxt")

print("Path to dataset files:", path)'''
 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
wordlist = open('wordlist.txt', 'r')
wd = wordlist.readlines()
lines = [s.strip('\n') for s in wd]
word = random.choice(lines)
def load():
    vectors = open('glove.6B.300d.txt', 'r', encoding='utf-8', errors="ignore")    
    v = vectors.readlines()
    dict_embed = {}
    for i in v:
        parts = i.split()
        dict_embed[parts[0].lower()]=np.array(parts[1:], dtype=np.float32)
   
    
    return dict_embed
dict_embed = load()
def cos(word, user_word):
    z = cosine_similarity(word.reshape(1, -1), user_word.reshape(1, -1))
    if z < 0.4: 
        return "Cold"
    elif z > 0.4 and z < 0.6:
        return "Warm"
    elif z > 0.6 and z < 0.8:
        return "Hot"
    elif z > 0.8 and z < 0.95:
        return "Very Hot"
    elif z > 0.95:
        return "Done!"

        
    else:
        return "Error occurred"

def find_vector(term):
    
    return dict_embed.get(term.lower(), None)
print(word)
while True:   
    user_in = input("Type here: ")

    check = user_in.split()

    if len(check)>1:
        print("Only one word allowed in input")
    word_vector = np.array(find_vector(word))
    user_vector = np.array(find_vector(user_in))

    if user_vector is None:
        print("Word not found")
    
    res = cos(word_vector, user_vector)
        
    print(res)


