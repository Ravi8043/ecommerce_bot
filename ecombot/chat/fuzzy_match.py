import json
from rapidfuzz import fuzz, process

with open("ecombot/chat/faq.json", "r") as f:
    faqs = json.load(f)

def fuzzy_lookup(user_query: str, threshold: int = 70):
 from rapidfuzz import fuzz, process

def hybrid_faq_lookup(user_query: str, threshold: int = 70):
    query = user_query.lower().strip()
    questions = [faq["question"] for faq in faqs]

    # 1. QRatio
    best_match = process.extractOne(query, questions, scorer=fuzz.QRatio)
    if best_match:
        matched_question, score, idx = best_match
        if score >= threshold:
            return faqs[idx]["answer"]

    # 2. token_sort_ratio
    best_match = process.extractOne(query, questions, scorer=fuzz.token_sort_ratio)
    if best_match:
        matched_question, score, idx = best_match
        if score >= threshold:
            return faqs[idx]["answer"]

    # 3. token_set_ratio
    best_match = process.extractOne(query, questions, scorer=fuzz.token_set_ratio)
    if best_match:
        matched_question, score, idx = best_match
        if score >= threshold:
            return faqs[idx]["answer"]

    # 4. Fall back to LLM
    return None