from datetime import datetime

import imgkit


from jinja2 import Template
import requests
import time
from dataclasses import dataclass
import os
from PIL import Image

RUN_RPI = os.getenv('RUN_RPI', '').lower() in ['1', 'true', 'yes']

if RUN_RPI:
    from waveshare_epd import epd2in13b_V4


previous_stats = None

@dataclass
class TikTokStats:
    cache: bool
    success: bool
    followerCount: int
    likeCount: int
    followingCount: int
    videoCount: int

def render_html_to_image(html_content, output_image, width, height):
    options = {
        'width': width,
        'height': height,
        'format': 'png',
        'crop-w': width,
        'crop-h': height
    }
    imgkit.from_string(html_content, output_image, options=options)




def generate_image(stats):
    try:
        # Wczytaj HTML z pliku
        with open('template.html', 'r') as file:
            template_content = file.read()

        print("Wczytano zawartość szablonu HTML.")

        # Tworzenie szablonu Jinja2
        template = Template(template_content)

        # Dane do szablonu
        html_content = template.render(
            name="@final_notmi",
            fC=stats.followerCount,
            lC=stats.likeCount,
            followingCount=stats.followingCount,
            videoCount=stats.videoCount
        )

        output_image = "output.png"
        width = 250
        height = 122

        print(f"Generowanie obrazu z danymi: {stats}")

        # Renderowanie HTML na obraz
        render_html_to_image(html_content, output_image, width, height)
        print(f"Obraz zapisany jako {output_image} o rozmiarze {width}x{height}.")

    except Exception as e:
        print(f"Błąd podczas generowania obrazu: {e}")


# Funkcja do zamiany JSON na obiekt
def map_response_to_object(response_json):
    return TikTokStats(
        cache=response_json["cache"],
        success=response_json["success"],
        followerCount=response_json["followerCount"],
        likeCount=response_json["likeCount"],
        followingCount=response_json["followingCount"],
        videoCount=response_json["videoCount"]
    )

# Funkcja wywoływana w momencie wykrycia zmiany
def on_change_detected(old_stats, new_stats):
    print("Wykryto zmianę danych!!!!!!!!!!!!!!!!!!!!")
    print(f"Poprzednie dane: {old_stats}")
    print(f"Nowe dane: {new_stats}")
    # Możesz dodać tutaj dalszą logikę, np. wysyłanie powiadomień itp.

# Funkcja do porównywania obiektów TikTokStats
def has_stats_changed(old_stats, new_stats):
    return (
        old_stats.followerCount != new_stats.followerCount or
        old_stats.likeCount != new_stats.likeCount or
        old_stats.videoCount != new_stats.videoCount
    )

# Funkcja do wysłania żądania HTTP i monitorowania odpowiedzi
def fetch_tiktok_stats():
    # URL API
    api_url = "https://tiktok.livecounts.io/user/stats/7408301119661687841"

    # Nagłówki HTTP
    headers = {
        "Origin": "https://tokcounter.com",
        "Priority": "u=4",
        "Accept-Encoding": "application/json",
        "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
    }

    global previous_stats  # Przechowuje poprzedni stan danych

    attempt_count = 0  # Licznik prób
    while True:
        # Wysłanie żądania GET z nagłówkami
        response = requests.get(api_url, headers=headers)

        # Sprawdzenie odpowiedzi
        if response.status_code == 200:
            response_json = response.json()  # Parsowanie JSON z odpowiedzi
            current_stats = map_response_to_object(response_json)  # Mapowanie JSON na obiekt

            if previous_stats is None or has_stats_changed(previous_stats, current_stats):
                on_change_detected(previous_stats, current_stats)
                previous_stats = current_stats

                print("change detected!")
                return current_stats

            # Aktualizacja poprzednich danych na bieżące

            previous_stats = current_stats
            print("Zmapowane dane:")
            print(current_stats)
        else:
            attempt_count += 1
            print(f"Błąd HTTP: {response.status_code}, Próba: {attempt_count}")

        time.sleep(3)  # Odstęp między kolejnymi żądaniami (np. 3 sekundy)

def display_image_on_eink(image_path):
    if not RUN_RPI:
        print("Uruchomione na komputerze - pomijanie wyświetlania na e-ink.")
        return

    try:
        # Inicjalizacja sterownika
        epd = epd2in13b_V4.EPD()
        epd.init()

        # Załadowanie obrazu i konwersja do trybu e-ink (1-bit color)
        if os.path.exists(image_path):
            image = Image.open(image_path)

            # Dostosowanie obrazu do rozmiaru wyświetlacza
            width, height = epd.width, epd.height

            red_image = Image.new('1', (width, height), 255)  # Całkowicie biały obraz (bez czerwonych pikseli)

            # Wyświetlenie obrazów na wyświetlaczu
            epd.display(epd.getbuffer(image), epd.getbuffer(red_image))

            epd.sleep()
        else:
            print(f"Błąd: Plik {image_path} nie istnieje.")
    except Exception as e:
        print(f"Błąd podczas wyświetlania obrazu: {e}")

# Funkcja główna
def main():
    while True:
        current_time = datetime.now()
        if current_time.hour == 2 and current_time.minute == 0:
            print("Rebooting system at 2 AM...")
            os.system('sudo reboot')

        stats = fetch_tiktok_stats()
        generate_image(stats)
        display_image_on_eink("output.png")
        time.sleep(180)


# Standardowy blok Python do uruchamiania skryptu
if __name__ == "__main__":
    main()
