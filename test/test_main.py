from src.anime import download_anime_details, download_anime_list


def test_download_anime_list():
    anime_list = download_anime_list(alpha_category="a", limit=1)
    assert len(anime_list) >= 20
    title, url = anime_list[0]
    assert len(title) > 0
    assert len(url) > 0


def test_download_anime_details():
    anime_list = download_anime_list(alpha_category="a", limit=1)
    _, url = anime_list[0]
    anime_details = download_anime_details(url=url)
    assert len(anime_details.title) > 0
    assert len(anime_details.type) > 0
