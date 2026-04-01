import os
import uuid
from io import BytesIO

from gtts import gTTS
from pydub import AudioSegment


def synthesise(text: str, params: dict, out_dir: str) -> str:
    """
    Synthesises speech, applies modulation, writes MP3 to out_dir.
    Returns the filename (UUID hex + '.mp3'), not the full path.
    Propagates gTTS exceptions to the caller.
    """
    # Step 1: Generate base audio using gTTS into a BytesIO buffer
    buffer = BytesIO()
    tts = gTTS(text=text, lang='en')
    tts.write_to_fp(buffer)
    buffer.seek(0)

    # Step 2: Load into pydub AudioSegment
    audio = AudioSegment.from_file(buffer, format='mp3')

    # Step 3: Apply volume_db (always apply, even if 0)
    audio = audio + params['volume_db']

    # Step 4: Apply rate (ONLY if params['rate'] != 1.0)
    if params['rate'] != 1.0:
        audio = audio.speedup(playback_speed=params['rate'])

    # Step 5: Apply pitch shift (ONLY if params['pitch'] != 0)
    if params['pitch'] != 0:
        semitones = params['pitch']
        new_frame_rate = int(audio.frame_rate * (2 ** (semitones / 12.0)))
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
        audio = audio.set_frame_rate(44100)

    # Step 6: Export to out_dir with a UUID hex filename
    filename = uuid.uuid4().hex + '.mp3'
    audio.export(os.path.join(out_dir, filename), format='mp3')

    # Step 7: Return ONLY the filename string (not the full path)
    return filename
