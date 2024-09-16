import requests
import time
from dataclasses import dataclass

@dataclass
class TikTokStats:
    cache: bool
    success: bool
    followerCount: int
    likeCount: int
    followingCount: int
    videoCount: int

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
        old_stats.followingCount != new_stats.followingCount or
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

    previous_stats = None  # Przechowuje poprzedni stan danych

    attempt_count = 0  # Licznik prób
    while True:
        # Wysłanie żądania GET z nagłówkami
        response = requests.get(api_url, headers=headers)

        # Sprawdzenie odpowiedzi
        if response.status_code == 200:
            response_json = response.json()  # Parsowanie JSON z odpowiedzi
            current_stats = map_response_to_object(response_json)  # Mapowanie JSON na obiekt

            if previous_stats is not None and has_stats_changed(previous_stats, current_stats):
                on_change_detected(previous_stats, current_stats)

            # Aktualizacja poprzednich danych na bieżące
            previous_stats = current_stats

            print("Zmapowane dane:")
            print(current_stats)
        else:
            attempt_count += 1
            print(f"Błąd HTTP: {response.status_code}, Próba: {attempt_count}")

        time.sleep(3)  # Odstęp między kolejnymi żądaniami (np. 3 sekundy)

# Funkcja główna
def main():
    fetch_tiktok_stats()

# Standardowy blok Python do uruchamiania skryptu
if __name__ == "__main__":
    main()
