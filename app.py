from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
# Enable CORS so the frontend can communicate with the backend, especially when deployed separately
CORS(app)

# Configure the Gemini API securely using environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY environment variable not set.")

# Using the recommended free model for text generation
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/api/study', methods=['POST'])
def study_assistant():
    data = request.json
    action = data.get('action')
    payload = data.get('payload')

    if not payload:
        return jsonify({"error": "Input is required"}), 400

    # Constructing targeted prompts based on the requested feature
    if action == 'explain':
        prompt = f"Explain this concept for a school student. Include a simple explanation, detailed explanation, real-life example, important points, and a mnemonic: {payload}"
    elif action == 'quiz':
        prompt = f"Generate 3 multiple-choice questions, 2 true/false, and 1 short answer question based on this topic: {payload}"
    elif action == 'plan':
        prompt = f"Create a structured weekly study planner based on these details: {payload}. Format as a clear, readable text table."
    else:
        prompt = f"You are StudySphere, an AI tutor. Answer this doubt clearly and concisely for a student: {payload}"

    try:
        response = model.generate_content(prompt)
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render will automatically assign a PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
