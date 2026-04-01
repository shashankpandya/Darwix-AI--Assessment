import os
import glob
from flask import Flask, render_template, request, jsonify
from engine.detector import detect
from engine.mapper import get_params
from engine.ssml_builder import build_ssml
from engine.tts import synthesise

app = Flask(__name__)

OUT_DIR = os.path.join('static', 'output')
os.makedirs(OUT_DIR, exist_ok=True)

# Keep at most this many generated MP3s on disk to avoid filling storage
MAX_CACHED_FILES = 20


def _prune_output_dir():
    """Remove oldest MP3s when the output folder exceeds MAX_CACHED_FILES."""
    files = sorted(
        glob.glob(os.path.join(OUT_DIR, '*.mp3')),
        key=os.path.getmtime
    )
    for old_file in files[:-MAX_CACHED_FILES]:
        try:
            os.remove(old_file)
        except OSError:
            pass


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
        ssml = build_ssml(text, emotion, intensity)
        filename = synthesise(text, params, OUT_DIR)
        _prune_output_dir()
        return jsonify({
            'emotion':   emotion,
            'intensity': round(intensity, 4),
            'params':    params,
            'ssml':      ssml,
            'audio_url': f'/static/output/{filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Port 7860 is required by Hugging Face Spaces; falls back to 5000 locally
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port, debug=False)
