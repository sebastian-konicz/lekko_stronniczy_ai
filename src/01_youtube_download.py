import os
import time
import yt_dlp

# ------------------------------------
# STEP 1: Download all videos from channel
# ------------------------------------

def download_videos(video_urls: str, out_dir: str):
    # start time of function
    start_time = time.time()

    os.makedirs(out_dir, exist_ok=True)
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(out_dir, '%(id)s.%(ext)s')
        # 'format': 'bestvideo+bestaudio/best',  # Najlepsze wideo + najlepszy dźwięk
        # 'merge_output_format': 'mp4',          # Format wynikowy (połączony)
        # 'outtmpl': 'downloads/%(title)s.%(ext)s',  # Ścieżka i nazwa pliku
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_urls)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    YT_VIDEO_URLS = [
    'https://www.youtube.com/watch?v=_xv13uqrQnU',
    'https://www.youtube.com/watch?v=Gm9hsd_BAnc',
    'https://www.youtube.com/watch?v=fznRzBZFS50',
    'https://www.youtube.com/watch?v=0zXIPwwPSlc',
    'https://www.youtube.com/watch?v=49FDlR6bTks'
    ]
    DOWNLOAD_DIR = './downloads'
    download_videos(YT_VIDEO_URLS, DOWNLOAD_DIR)

