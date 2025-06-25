import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz klucz API z .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Opcjonalnie: Rzucaj wyjątkiem, jeśli klucz nie jest ustawiony
if not all([OPENAI_API_KEY]):
    raise ValueError("Brakuje danych uwierzytelniających do OpenAI. Sprawdź plik .env.")