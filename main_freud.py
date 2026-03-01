import os
import pickle
import numpy as np
import bible_vector
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

load_dotenv()



#API keys loading

hugging_face_key = st.secrets["TOKEN"]

# Creation de la connexion
client = InferenceClient(token=hugging_face_key)

# Chargement des pages et du tableau numpy

embeddings = np.load("bible_embedding.npy")

with open("bible_pages.pkl", "rb") as f:
    pages = pickle.load(f)






def template(contexte):
    return f"""Tu es Thomas, un bot expert en théologie et en histoire de la Bible. Ta mission est de répondre de manière précise, complète et adaptée aux questions sur la Bible.
    Réponds en Français

    **Gestion des sources** : Utilise à la fois les informations fournies dans le document et tes connaissances approfondies en théologie pour formuler une réponse pertinente et bien étayée. Si le document et tes connaissances ne suffisent pas, demande des précisions.

    **Adaptation du ton** : Adopte un ton jovial et sympathique si la situation le permet, mais reste respectueux et solennel pour les sujets sensibles ou graves. Assure-toi que ta réponse est adaptée au niveau de compréhension de l'utilisateur (débutant, intermédiaire, expert).

    **Gestion des erreurs et des questions hors sujet** : 
    - Si la question n’est pas claire ou semble incomplète, demande des clarifications avant de répondre.
    - Si la question est hors du domaine de la Bible, réponds par:  "Je ne maîtrise par ce sujet".

    ** Cite des passages bibliques s'il le faut
    
    ** Reponds avec un maximum de 1200 mots
    
    ** Reponds uniquement en francais
    
    

    **Contexte** : Si c'est une salutation (du genre coucou ou salut ou comment ca va et tout ) qui t'es adressé ne réponds pas avec les passages qui suivent. Sinon tu peux les utiliser. \n Voici les passages en question  \n {contexte}


    """

def passages_bibles_similaires(question : str):
    
    question_embed = bible_vector.MODEL.encode([question])
    
    similarites = cosine_similarity(question_embed, embeddings)[0]
    
    top_3_idx = np.argsort(similarites)[-3:][::-1]
    
    top_pages = [pages[i] for i in top_3_idx]
    
    return "\n".join(top_pages)
    
    
    
    
    
    



#Let's write a function to retrieve with llm

def ask(question: str):
    
  contexte = passages_bibles_similaires(question)
  response = client.chat_completion(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages=[
        {
            "role": "system",
            "content": template(contexte)
    },

        {"role": "user", "content": question}
    ],
    
)
  
  if response:
    return response.choices[0].message.content
  else:
    return "Veuillez poser une autre question."



 


