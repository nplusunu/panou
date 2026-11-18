# Incarcarea variabilelor de mediu (.env)

import os
from dotenv import load_dotenv

load_dotenv()

CHEIE_OPEN_WEATHER = os.getenv("OPEN_WEATHER_API_KEY")
NUME = os.getenv("NUME")