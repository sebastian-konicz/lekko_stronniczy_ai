import os
import time
import json
import glob
import openai
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from openai import OpenAI
from config.config import OPENAI_API_KEY

# ------------------------------------
# STEP 3: Extract key frames for visual style
# ------------------------------------

def analyze_style(transcript_dir: str, frames_dir: str, output_path: str):
    start_time = time.time()
    print("[INFO] Start funkcji analyze_style")

    print("[INFO] Tworzenie klienta OpenAI...")
    client = OpenAI(api_key=OPENAI_API_KEY)

    print(f"[INFO] Wczytywanie transkryptów z katalogu: {transcript_dir}")
    transcripts = []
    for f in glob.glob(os.path.join(transcript_dir, '*.json')):
        transcripts.append(json.load(open(f))['text'])
    print(f"[INFO] Załadowano {len(transcripts)} transkryptów.")

    print("[INFO] Ładowanie modelu CLIP...")
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    print("[INFO] Model CLIP załadowany.")

    print(f"[INFO] Przetwarzanie obrazów z katalogu: {frames_dir}")
    visual_features = []
    img_paths = glob.glob(os.path.join(frames_dir, '*.jpg'))[:50]
    print(f"[INFO] Znaleziono {len(img_paths)} obrazów do analizy (max 50).")
    for i, img_path in enumerate(img_paths, 1):
        print(f"[INFO] Przetwarzanie obrazu {i}/{len(img_paths)}: {img_path}")
        image = Image.open(img_path)
        inputs = clip_processor(images=image, return_tensors="pt")
        features = clip_model.get_image_features(**inputs)
        visual_features.append(features.detach().numpy().tolist())

    print("[INFO] Przygotowywanie promptu i wysyłanie zapytania do OpenAI GPT-4o...")
    style_prompt = (
        "Analyze this channel's narrative style and visuals, "
        "then output a JSON profile describing tone, pacing, themes, and dominant visual motifs."
    )
    response = client.chat.completions.create(
        model="gpt-4o", messages=[
            {"role": "system", "content": "You are a style analysis assistant."},
            {"role": "user", "content": style_prompt + "\nTranscripts sample:\n" + json.dumps(transcripts[:5]) +
             "\nVisual features sample:\n" + json.dumps(visual_features[:5])}
        ]
    )
    print("[INFO] Otrzymano odpowiedź od modelu.")

    profile = response.choices[0].message.content

    print(f"[INFO] Zapis wyniku do pliku: {output_path}")
    with open(output_path, 'w') as f:
        f.write(profile)

    end_time = time.time()
    execution_time = int(end_time - start_time)
    print(f"[INFO] Zakończono funkcję analyze_style. Czas wykonania: {execution_time} sek.")

    return json.loads(profile)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    TRANSCRIPTS_DIR = './transcripts'
    FRAMES_DIR = './frames'
    STYLE_PROFILE_PATH = './style_profile.json'
    analyze_style(TRANSCRIPTS_DIR, FRAMES_DIR, STYLE_PROFILE_PATH)

