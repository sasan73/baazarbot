import re

def clean_text(text: str) -> str:
    url_pattern = r"\b(?:https?|ftp):\/\/(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(?:\/[^\s]*)?\b"
    email_pattern = r"\b[\w.+%-]+@[\w.-]+\.[a-zA-Z]{2,}"
    
    clean_text = re.sub(url_pattern, "<URL>", text)
    clean_text = re.sub(email_pattern, "<EMAIL>", clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text)
    return clean_text
