from bs4 import BeautifulSoup
import requests
import json
import os


def get_concerts(file_name = 'playlist.html'):
    res = {}
    with open(file_name) as f:
        soup = BeautifulSoup(f, 'html.parser')

    titles = soup.find_all('div', class_='title')

    for title in titles:
        a_tag = title.find('a')
        res[a_tag.text] = {'url': a_tag['href']}
    return res

def get_songs(concerts):
    for name in concerts:
        url = concerts[name]['url']
        concerts[name]['playlist'] = []
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find('div', class_='content-tracks').find_all('li')
        for row in rows:
            song = row.select_one('div.song > a')
            if not song:
                continue
            artist = row.select_one('div.artist-album > a')
            if not artist:
                continue
            song = song.text
            artist = artist.text
            concerts[name]['playlist'].append({'song': song, 'artist': artist})
    return concerts

def to_json(data, file_name='concerts.json'):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def from_json(file_name='concerts.json'):
    with open(file_name, 'r', encoding='utf-8') as f:
        concerts = json.load(f)
    return concerts

if __name__ == '__main__':
    if not os.path.isfile('concerts.json'):
        concerts = get_concerts('playlist.html')
        concerts = get_songs(concerts)
        to_json(concerts)
    else:
        concerts = from_json(file_name='concerts.json')
    print(concerts)