
import re
import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

data = [
    ("I will hack your system tonight", 1),
    ("hello whats up how are you doing", 0),
    ("delete all files immediately", 1),
    ("come one lets hang out", 0),
    ("give me your password now", 1),
    ("project completed successfully", 0),
    ("I am going to destroy the server", 1),
    ("fine? come one lets hang", 0),
    ("I will track your IP address", 1),
    ("hello good morning have a nice day", 0),
    ("format c: /y", 1),
    ("rm -rf /", 1),
    ("sudo su", 1),
    ("access granted admin", 1),
    ("bypass security", 1),
    ("how was your day", 0),
    ("nice weather today", 0),
    ("working on project", 0),
    ("install malware", 1),
    ("crack password", 1),
    ("steal credentials", 1),
    ("overwrite system files", 1),
    ("disable firewall", 1),
    ("meeting at 3pm", 0),
    ("lunch break", 0),
]


def clean_text(s):
    if not isinstance(s, str):
        s = str(s)
    s = re.sub(r'[\x00-\x1f\x7f]+', ' ', s)  # remove control chars
    s = s.replace('\n', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s.lower()


def train_model():
    df = pd.DataFrame(data, columns=["text", "label"])
    df["cleaned"] = df["text"].apply(clean_text)
    
    X_train, X_test, y_train, y_test = train_test_split(
        df["cleaned"], df["label"], test_size=0.3, random_state=42, stratify=df["label"]
    )
    
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        max_features=20000
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_tfidf, y_train)
    
    # Save model and vectorizer
    pickle.dump(model, open("threat_model.pkl", "wb"))
    pickle.dump(vectorizer, open("threat_vectorizer.pkl", "wb"))
    
    # Evaluate
    y_pred = model.predict(X_test_tfidf)
    print("Model trained successfully!")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, vectorizer


def load_model():
    model_path = "threat_model.pkl"
    vectorizer_path = "threat_vectorizer.pkl"
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        try:
            model = pickle.load(open(model_path, "rb"))
            vectorizer = pickle.load(open(vectorizer_path, "rb"))
            return model, vectorizer
        except:
            pass
    
    return train_model()


def predict_threat(text, model=None, vectorizer=None):
    if model is None or vectorizer is None:
        model, vectorizer = load_model()
    
    cleaned = clean_text(text)
    X_new = vectorizer.transform([cleaned])
    prob = model.predict_proba(X_new)[0, 1]
    pred = "THREAT" if prob > 0.5 else "BENIGN"
    return pred, round(prob, 3), cleaned


def analyze_keylog_file(file_path):
    if not os.path.exists(file_path):
        return None, None, None
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if not content.strip():
            return "BENIGN", 0.0, "Empty file"
        
        model, vectorizer = load_model()
        label, prob, cleaned = predict_threat(content, model, vectorizer)
        
        return label, prob, cleaned
    except Exception as e:
        print(f"Error analyzing keylog: {e}")
        return None, None, str(e)


def analyze_text_chunks(text, chunk_size=100):
    model, vectorizer = load_model()
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    results = []
    for i, chunk in enumerate(chunks):
        if chunk.strip():
            label, prob, cleaned = predict_threat(chunk, model, vectorizer)
            results.append({
                'chunk': i,
                'label': label,
                'probability': prob,
                'text': chunk[:50] + "..." if len(chunk) > 50 else chunk
            })
    
 
    max_threat_prob = max([r['probability'] for r in results]) if results else 0.0
    overall_label = "THREAT" if max_threat_prob > 0.5 else "BENIGN"
    
    return overall_label, max_threat_prob, results


if __name__ == "__main__":
    print("Initializing threat detection model...")
    model, vectorizer = train_model()
    print("Model ready! Use analyze_keylog_file() to analyze keylog files.")

