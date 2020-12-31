#!/usr/bin/python3

import re
import requests
from bs4 import BeautifulSoup

class Mojim:
    def __init__(self, artist='', song=''):
        self.artist = artist
        self.song = song

    def _make_soup(self, url):
        resp = requests.get(url).text
        return BeautifulSoup(resp, 'html5lib')

    def _fetch_lyrics(self, url):
        soup = self._make_soup(url)
        spans = soup.findAll('span', {'class': 'mxsh_ss4'})
        pattern = re.compile(r'(.*?) ')
        url = ''
        for s in spans:
            link = s.find('a', {'title': pattern})
            if link:
                if self.artist in link.get('title'):
                    url = link.get('href')
        soup = self._make_soup(f'http://mojim.com{url}')
        return soup.find('dl', {'id': 'fsZx1'})

    def _clean(self, lyrics):
        cleaned = ''
        lyrics = [str(line) for line in lyrics.contents]
        for i in lyrics:
            if 'br' in i:
                i = '\n'
            if '[' in i or ':' in i or '：' in i or '<' in i or 'Mojim' in i:
                continue
            cleaned += i
        return cleaned.strip()

    def save(self, artist=None, song=None):
        self.artist = artist
        self.song = song
        simplified_url = f'https://mojim.com/{song}.html?g3'
        traditional_url = f'https://mojim.com/{song}.html?t3'
        
        lyrics = self._fetch_lyrics(simplified_url) or self._fetch_lyrics(traditional_url)
        if not lyrics:
            return None
        lyrics = self._clean(lyrics)

        with open(f'{artist} - {song}.txt', 'w', encoding='utf-8') as fout:
            fout.write(lyrics)
        
        print(f'{artist} - {song} saved.')
        return None


if __name__ == '__main__':
    artist = input('artist: ')
    song = input('song: ')

    mojim = Mojim()
    mojim.save(artist, song)
