import os
import uuid
from io import BytesIO

from gtts import gTTS
from pydub import AudioSegment


def synthesise(text: str, params: dict, out_dir: str) -> str:
    """
    Synthesises speech, applies vocal modulation, writes MP3 to out_dir.
    Returns the filename (UUID hex + '.mp3'), not the full path.
    Propagates gTTS exceptions to the caller.

    Modulation strategy:
    - Rate and pitch are combined into a single frame-rate multiplication to
      avoid compounding distortion from two sequential resamples.
    - Combined multiplier = rate * 2^(semitones/12)
    - Volume is applied independently via pydub's gain operator.
    """
    # Step 1: Generate base audio via gTTS into an in-memory buffer (no disk I/O)
    buffer = BytesIO()
    tts = gTTS(text=text, lang='en')
    tts.write_to_fp(buffer)
    buffer.seek(0)

    # Step 2: Load into pydub AudioSegment
    audio = AudioSegment.from_file(buffer, format='mp3')

    # Step 3: Apply volume gain (always; pydub handles 0 dB as a no-op)
    audio = audio + params['volume_db']

    # Step 4: Combine rate + pitch into a single frame-rate pass
    # This avoids the distortion caused by two sequential resamples.
    rate = params['rate']
    semitones = params['pitch']

    rate_multiplier = rate * (2 ** (semitones / 12.0))

    if abs(rate_multiplier - 1.0) > 1e-6:
        new_frame_rate = int(audio.frame_rate * rate_multiplier)
        # Clamp to a safe range to avoid pydub errors
        new_frame_rate = max(1000, min(new_frame_rate, 192000))
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
        # Normalise back to 44100 Hz for consistent playback
        audio = audio.set_frame_rate(44100)

    # Step 5: Export as MP3 with a UUID hex filename
    filename = uuid.uuid4().hex + '.mp3'
    audio.export(os.path.join(out_dir, filename), format='mp3')

    return filename
