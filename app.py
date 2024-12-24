from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from openai import ChatCompletion
import os
import random


app = Flask(__name__, static_folder='../frontend')

DATABASE = 'carebridge.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn



SCENARIOS = [
    "A patient arrives with severe chest pain. What would you do?",
    "An elderly patient has trouble remembering medications. How can you assist?",
    "A child presents with a high fever and rash. What steps would you take?",
    "A patient reports sudden loss of vision in one eye. What is your response?",
    "A pregnant woman experiences early contractions. How do you handle it?",
    "A patient with diabetes complains of persistent fatigue. What could be the issue?",
    "A person collapses in the waiting room. What actions do you take?",
    "A patient is diagnosed with cancer and is very emotional. How do you support them?",
    "A teenager reports difficulty breathing after eating. What iss your approach?",
    "A patient is experiencing a severe allergic reaction. What immediate steps are necessary?"
]



@app.route('/')
def index():
    # Serve the frontend HTML file
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    # Serve other static files (CSS, JS)
    return send_from_directory(app.static_folder, path)

@app.route('/scenario', methods=['GET'])
def get_scenario():
    conn = get_db_connection()
    scenario = conn.execute('SELECT * FROM scenarios ORDER BY RANDOM() LIMIT 1').fetchone()
    conn.close()
    if scenario:
        return jsonify({'id': scenario['id'], 'text': scenario['text']})
    return jsonify({'error': 'No scenarios found'}), 404

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    scenario_id = data.get('scenario_id')
    feedback = data.get('feedback')
    improvement = data.get('improvement')
    if not scenario_id or not feedback or not improvement:
        return jsonify({'error': 'Invalid data'}), 400
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO feedback (scenario_id, feedback, improvement) VALUES (?, ?, ?)',
        (scenario_id, feedback, improvement)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Feedback submitted successfully'})


@app.route('/generate-scenario', methods=['POST'])
def generate_scenario():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    try:
    #     import openai
    #     openai.api_key = "xyz"  # Replace "your_api_key" with your actual OpenAI API key

    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": prompt}
    #         ]
    #     )
    #     scenario_text = response['choices'][0]['message']['content']
    #     conn = get_db_connection()
    #     conn.execute('INSERT INTO scenarios (text) VALUES (?)', (scenario_text,))
    #     conn.commit()
    #     conn.close()
    #     return jsonify({'message': 'Scenario generated successfully', 'text': scenario_text})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
    # Select a random scenario
        scenario_text = random.choice(SCENARIOS)
        
        # Simulate saving to the database (optional)
        # You can uncomment the following lines if a database is connected:
        # conn = get_db_connection()
        # conn.execute('INSERT INTO scenarios (text) VALUES (?)', (scenario_text,))
        # conn.commit()
        # conn.close()

        return jsonify({'message': 'Scenario generated successfully', 'text': scenario_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
