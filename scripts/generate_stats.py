"""Render real public-repository totals; no contribution heatmap or external image API."""
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USER = 'compromise729'


def fetch(url):
    headers = {'User-Agent': 'compromise729-profile', 'Accept': 'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer '+os.environ['GITHUB_TOKEN']
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return json.load(response)
        except (URLError, TimeoutError) as error:
            if isinstance(error, HTTPError) and error.code < 500:
                raise
            if attempt == 2:
                raise
            time.sleep(2**attempt)


def collect():
    repos = []
    for page in range(1, 101):
        batch = fetch(f'https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}')
        repos.extend(r for r in batch if not r['private'] and r['owner']['login'].lower() == USER.lower())
        if len(batch) < 100:
            break
    else:
        raise RuntimeError('Repository pagination limit exceeded')
    return {'repos': len(repos), 'stars': sum(r['stargazers_count'] for r in repos),
            'forks': sum(r['forks_count'] for r in repos)}


ICONS = [
    'M16 2L20 11L30 12L22 19L25 29L16 24L7 29L10 19L2 12L12 11Z',
    'M7 3H25V29H7Q3 29 3 25V7Q3 3 7 3M7 23H25M9 8H19M9 12H19',
    'M8 5V12Q8 17 16 17H24V5M16 17V28M5 2H11V8H5ZM21 2H27V8H21ZM13 25H19V31H13Z',
]


def render(stats, stamp, mobile=False):
    for key in ('stars', 'repos', 'forks'):
        if not isinstance(stats[key], int) or stats[key] < 0:
            raise ValueError('Invalid public-repository totals')
    width, height = (440, 560) if mobile else (1100, 254)
    chunks = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub public repository statistics">',
              '<title>GitHub public repository statistics</title>',
              f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16" fill="#0b1221" stroke="#2d3b53"/>',
              '<g font-family="Consolas,Menlo,monospace">',
              '<text x="25" y="35" font-size="12" letter-spacing="1.6" fill="#9fb3ce">GITHUB / PUBLIC REPOSITORIES</text>']
    for i, (key, label, color) in enumerate([('stars','STARS','#f2ce7b'),('repos','REPOSITORIES','#78e0ce'),('forks','FORKS','#b9a0f2')]):
        x, y, card_w = (20, 55+i*150, 400) if mobile else (20+i*360, 57, 340)
        chunks += [f'<g transform="translate({x} {y})">',
                   f'<rect width="{card_w}" height="135" rx="10" fill="#101c2e" stroke="{color}" stroke-opacity=".35"/>',
                   f'<path d="M16 0H60" stroke="{color}" stroke-width="2"/>',
                   f'<path transform="translate({card_w-55} 20)" d="{ICONS[i]}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>',
                   f'<text x="20" y="77" font-size="49" font-weight="bold" fill="#eef4fc">{stats[key]:,}</text>',
                   f'<text x="22" y="109" font-size="13" letter-spacing="1.7" fill="{color}">{label}</text></g>']
    chunks += [f'<text x="25" y="{height-24}" font-size="11" fill="#8095b2">UPDATED / {stamp}</text></g></svg>\n']
    return ''.join(chunks)


def generate(stats=None):
    if stats is None:
        stats = collect()
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    outputs = {'github-stats.svg': render(stats, stamp), 'github-stats-mobile.svg': render(stats, stamp, True)}
    for name, content in outputs.items():
        (ROOT/'assets'/name).write_text(content, encoding='utf-8')
    print('Generated public repository statistics:', stats)


if __name__ == '__main__':
    generate()
