import csv
import string

from src.anime import download_anime_details, download_anime_list
from src.anime_details import AnimeDetails


def download_anime_by_alpha_category(alpha_category: str) -> list[AnimeDetails]:
    results: list[AnimeDetails] = []
    print(f"Downloading anime list for '{alpha_category}' category...")
    anime_list = download_anime_list(alpha_category=alpha_category)
    for index, (title, url) in enumerate(anime_list):
        print(f"Downloading {title}...", index+1, len(anime_list))
        anime_details = download_anime_details(url)
        results.append(anime_details)
    return results


def save_anime_to_csv(alpha_category: str = "", filename: str = "anime.csv"):
    alpha_categories: list[str] = []
    results: list[AnimeDetails] = []
    if alpha_category:
        alpha_categories = [alpha_category]
    else:
        alpha_categories = list(string.ascii_lowercase)
        alpha_categories.append(".")
    for alpha_category in alpha_categories:
        results = results + download_anime_by_alpha_category(alpha_category=alpha_category)

    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for index, anime_details in enumerate(results):
            if index == 0:
                writer.writerow(anime_details.get_header())
            writer.writerow(list(anime_details))


if __name__ == "__main__":
    save_anime_to_csv(alpha_category="x")