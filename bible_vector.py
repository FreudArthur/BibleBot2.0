# Objectif transformer la bible en vecteur d'embedding et le stocker pour eviter de le charger dès le lancement de l'appication

import os
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from pypdf import PdfReader


MODEL = SentenceTransformer("all-MiniLM-L6-v2")
# Extraction des pages de la bible et stockage dans une liste / pandas

def extract_text_from_pdf(path):
    """
    Renvoie une liste de texte avec chaque élément représentant le contenu d'une page
    """
    reader = PdfReader(path)
    liste_page = []

    for page in tqdm(reader.pages):
        liste_page.append(page.extract_text())
    return liste_page


def encode_and_save(path):
    
    """
    Pour encoder et sauvegarder le vecteur d'embedding et sérialiser les pages de la bible pour les rendre accessible
    """
    
    
    pages = extract_text_from_pdf(path)
    
    with open("bible_pages.pkl", "wb") as f:
        pickle.dump(pages, f)
    
    
        
        # Pour faire une petite initialisation avant le chargement des batchs
    MODEL.encode(["warmup"])
        
    pages_embeddings = MODEL.encode(
            pages ,
            batch_size=32,
            show_progress_bar=True)
        
    np.save("bible_embedding" , pages_embeddings)
        
    

if __name__ == "__main__":
    encode_and_save("OpenBible.fr-FR.pdf")