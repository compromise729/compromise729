"""Render public GitHub data as self-hosted SVGs; Python standard library only."""
import json
import os
import time
from collections import Counter
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
USER = 'compromise729'


def fetch(url):
    headers = {'User-Agent': 'compromise729-profile', 'Accept-Language': 'en-US'}
    if url.startswith('https://api.github.com/') and os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return response.read().decode('utf-8')
        except (URLError, TimeoutError) as error:
            if isinstance(error, HTTPError) and error.code < 500:
                raise
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-date' in attrs and 'data-level' in attrs:
            self.days[attrs['data-date']] = int(attrs['data-level'])


def text(x, y, value, size=15, color='#c9d1d9'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(str(value))}</text>'


def svg(title, body, height):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" '
            f'viewBox="0 0 960 {height}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title><rect x="1" y="1" width="958" height="{height-2}" '
            'rx="18" fill="#0d1117" stroke="#26344b"/>'
            '<g font-family="ui-monospace, SFMono-Regular, Consolas, monospace">'
            + body + '</g></svg>\n')


def generate():
    repos = []
    for page in range(1, 101):
        batch = json.loads(fetch(f'https://api.github.com/users/{USER}/repos?per_page=100&page={page}'))
        repos.extend(r for r in batch if not r['private'])
        if len(batch) < 100:
            break
    else:
        raise RuntimeError('Repository pagination limit reached')
    profile = json.loads(fetch(f'https://api.github.com/users/{USER}'))
    languages = Counter()
    for repo in repos:
        if not repo['fork']:
            languages.update(json.loads(fetch(repo['languages_url'])))
    calendar = Calendar()
    calendar.feed(fetch(f'https://github.com/users/{USER}/contributions'))
    days = sorted(calendar.days.items())
    if len(days) < 350 or any(level not in range(5) for _, level in days):
        raise ValueError('GitHub calendar changed; keeping previous SVGs')
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    body = text(30, 36, 'PUBLIC SIGNAL / ' + USER, 18, '#22d3ee')
    metrics = [(len(repos), 'PUBLIC REPOS'),
               (sum(r['stargazers_count'] for r in repos), 'REPO STARS'),
               (profile['followers'], 'FOLLOWERS'),
               (sum(level > 0 for _, level in days), 'ACTIVE DAYS / YEAR')]
    for i, (value, label) in enumerate(metrics):
        body += text(30 + i*235, 91, value, 34, '#f0f6fc')
        body += text(30 + i*235, 119, label, 12, '#8b9bb4')
    body += text(30, 166, 'LANGUAGES / public non-fork repositories', 14, '#a78bfa')
    if languages:
        total = sum(languages.values())
        for i, (language, count) in enumerate(languages.most_common(6)):
            body += text(30+(i%3)*310, 199+(i//3)*27, f'{language}: {count/total:.1%}', 14)
    else:
        body += text(30, 199, 'No language bytes reported for public repositories yet.', 14)
    body += text(30, 272, 'Snapshot: ' + stamp + ' / GitHub public data', 12, '#8b9bb4')
    stats = svg('GitHub public repository statistics', body, 295)
    body = text(30, 36, 'CONTRIBUTION SIGNAL / LAST YEAR', 18, '#22d3ee')
    colors = ['#161f30', '#263d70', '#4752aa', '#8561d5', '#22d3ee']
    for i, (date, level) in enumerate(days):
        body += (f'<rect x="{30+i//7*17}" y="{65+i%7*17}" width="13" height="13" '
                 f'rx="3" fill="{colors[level]}"><title>{date}: contribution level {level}/4</title></rect>')
    body += text(30, 210, days[0][0] + ' - ' + days[-1][0], 13, '#8b9bb4')
    body += text(630, 210, 'Less', 12, '#8b9bb4')
    for i, color in enumerate(colors):
        body += f'<rect x="{675+i*20}" y="198" width="13" height="13" rx="3" fill="{color}"/>'
    body += text(785, 210, 'More', 12, '#8b9bb4')
    body += text(30, 246, 'Updated / ' + stamp, 11, '#8b9bb4')
    graph = svg('GitHub contribution calendar', body, 268)
    # All requests and rendering must succeed before replacing last-known-good images.
    output = ROOT / 'assets'
    output.mkdir(exist_ok=True)
    for name, content in {'github-telemetry.svg': stats, 'contribution-calendar.svg': graph}.items():
        (output / name).write_text(content, encoding='utf-8')
    print(f'Generated statistics for {len(repos)} public repositories and {len(days)} calendar days.')


if __name__ == '__main__':
    generate()
