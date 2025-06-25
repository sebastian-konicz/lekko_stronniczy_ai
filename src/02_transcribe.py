import os
import time
import glob
import json
import shutil
import whisper

# ------------------------------------
# STEP 2: Transcribe videos with Whisper
# ------------------------------------

def transcribe_videos(input_dir: str, output_dir: str):
    # start time of function
    start_time = time.time()

    os.makedirs(output_dir, exist_ok=True)

    if shutil.which('ffmpeg') is None:
        raise EnvironmentError("ffmpeg is not installed or not found in PATH. Please install it or set the correct path.")

    if shutil.which('ffmpeg') is None:
        raise EnvironmentError("ffmpeg is not installed or not found in PATH.")

    print(f"Transcription started. Looking for mp4 in {input_dir}")
    files = glob.glob(os.path.join(input_dir, '*.mp4'))
    print(f"Found {len(files)} video(s): {files}")

    model = whisper.load_model('base')
    for video in files:
        print(f"Transcribing: {video}")
        result = model.transcribe(video)
        base = os.path.splitext(os.path.basename(video))[0]
        out_path = os.path.join(output_dir, f'{base}.json')
        with open(out_path, 'w') as f:
            json.dump(result, f)
        print(f"Saved transcript to {out_path}")

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    DOWNLOAD_DIR = './downloads'
    TRANSCRIPTS_DIR = './transcripts'
    transcribe_videos(DOWNLOAD_DIR, TRANSCRIPTS_DIR)

