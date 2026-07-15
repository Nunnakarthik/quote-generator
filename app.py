from flask import Flask, jsonify
import random

app = Flask(__name__)

quotes = [
    {"id": 1, "quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"id": 2, "quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"id": 3, "quote": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
    {"id": 4, "quote": "Success is not final, failure is not fatal.", "author": "Winston Churchill"},
    {"id": 5, "quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
]

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Quote Generator API!", "endpoints": ["/quote", "/quote/<id>"]})

@app.route("/quote")
def random_quote():
    return jsonify(random.choice(quotes))

@app.route("/quote/<int:quote_id>")
def quote_by_id(quote_id):
    for q in quotes:
        if q["id"] == quote_id:
            return jsonify(q)
    return jsonify({"error": "Quote not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)