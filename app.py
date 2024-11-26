from flask import Flask, request, jsonify
import spacy
from collections import Counter
import inflect

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
inflect_engine = inflect.engine()  # For singularizing words

def extract_keywords(text):
    # Process text with spaCy
    doc = nlp(text)

    # Extract nouns, proper nouns, and verbs longer than 2 characters
    keywords = [token.text.lower() for token in doc if token.pos_ in ("NOUN", "PROPN", "VERB") and len(token.text) > 2]

    # Singularize keywords using inflect
    singular_keywords = [inflect_engine.singular_noun(word) or word for word in keywords]

    # Count occurrences of each keyword
    keyword_counts = Counter(singular_keywords)

    # Sort keywords by frequency (descending order)
    weighted_keywords = [(keyword, count) for keyword, count in keyword_counts.items()]
    weighted_keywords.sort(key=lambda x: x[1], reverse=True)

    # Return the top 10 keywords
    top_keywords = [keyword for keyword, _ in weighted_keywords[:10]]
    return top_keywords

@app.route("/extract_keywords", methods=["POST"])
def keyword_extraction():
    try:
        # Parse JSON request
        data = request.get_json()
        text = data.get("text", "")
        
        if not text:
            return jsonify({"error": "Text is required"}), 400

        # Extract keywords
        keywords = extract_keywords(text)
        
        return jsonify({"keywords": keywords}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
