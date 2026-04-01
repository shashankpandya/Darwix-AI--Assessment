import os
from flask import Flask, render_template, request, jsonify
from engine.detector import detect
from engine.mapper import get_params
from engine.ssml_builder import build_ssml
from engine.tts import synthesise

app = Flask(__name__)

OUT_DIR = os.path.join('static', 'output')
os.makedirs(OUT_DIR, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/synthesise', methods=['POST'])
def synthesise_route():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'text field is required and must be non-empty'}), 400
    try:
        emotion, intensity = detect(text)
        params = get_params(emotion, intensity)
        build_ssml(text, emotion, intensity)
        filename = synthesise(text, params, OUT_DIR)
        return jsonify({
            'emotion': emotion,
            'intensity': intensity,
            'params': params,
            'audio_url': f'/static/output/{filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
