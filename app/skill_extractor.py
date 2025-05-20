import spacy
from sentence_transformers import SentenceTransformer, util
from collections import defaultdict
import numpy as np
import math
import os
from dotenv import load_dotenv

load_dotenv()

# path_to_skills = os.getenv("PATH_TO_SKILLS")
path_to_skills = "data/sample_skills.csv"

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

with open(path_to_skills, "r", encoding='utf-8') as f:
    raw_skills = [line.strip() for line in f if line.strip()]

known_skills = [f"proficient with {skill}" for skill in raw_skills] 
skill_embeddings = model.encode(known_skills, convert_to_tensor=True)

def extract_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

def extract_noun_phrase(text):
    doc = nlp(text)
    noun_phrases = [chunk.text.strip() for chunk in doc.noun_chunks]
    return noun_phrases

def extract_skills(text, sentence_threshold=0.35, score_threshold=0.4):
    sentences = extract_sentences(text)
    
    if not sentences:
        return []
    
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    
    skill_scores = defaultdict(list)

    for i, skill_emb in enumerate(skill_embeddings):
        similarities = util.cos_sim(skill_emb, sentence_embeddings)[0]
        valid_scores = similarities[similarities >= sentence_threshold]

        if len(valid_scores) > 0:
            score = valid_scores.mean().item()
            adjusted_score = math.sqrt(score) * math.log(1 + len(valid_scores)) # cosine similarity and frequency of mentions 
            if adjusted_score > score_threshold:
                skill_scores[raw_skills[i]] = adjusted_score

    return sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
