import os
import time
import glob
import subprocess

# ------------------------------------
# STEP 3: Extract key frames for visual style
# ------------------------------------

def extract_frames(input_dir: str, output_dir: str, interval: int = 10):
    # start time of function
    start_time = time.time()

    os.makedirs(output_dir, exist_ok=True)
    for video in glob.glob(os.path.join(input_dir, '*.mp4')):
        base = os.path.splitext(os.path.basename(video))[0]
        out_pattern = os.path.join(output_dir, base + '_%03d.jpg')
        subprocess.run([
            'C:/ffmpeg/bin/ffmpeg.exe', '-i', video,
            '-vf', f"fps=1/{interval}", '-qscale:v', '2', out_pattern
        ])

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    DOWNLOAD_DIR = './downloads'
    FRAMES_DIR = './frames'
    extract_frames(DOWNLOAD_DIR, FRAMES_DIR)

