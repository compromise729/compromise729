"""Generate the profile's rectangular, repository-hosted badges."""
from pathlib import Path
from html import escape

BADGES = {
 'encrypted-db': ('DB', 'ENCRYPTED DATABASE', 'teal'),
 'rmdb': ('CORE', 'RMDB', 'purple'),
 'infosec': ('SEC', 'INFORMATION SECURITY', 'blue'),
 'opengauss': ('RESEARCH', 'openGauss', 'teal'),
 'semantic-security': ('SEC', 'SEMANTIC SECURITY', 'teal'),
 'encrypted-index': ('DB', 'ENCRYPTED INDEX', 'teal'),
 'query-optimization': ('DB', 'QUERY OPTIMIZATION', 'teal'),
 'storage': ('DB', 'STORAGE ENGINE', 'purple'),
 'transaction': ('DB', 'TRANSACTION', 'purple'),
 'recovery': ('DB', 'RECOVERY', 'purple'),
 'competition': ('PROJECT', 'DBMS DESIGN COMPETITION', 'purple'),
 'security-systems': ('FOCUS', 'SECURITY + SYSTEMS', 'blue'),
 'nku': ('NKU', 'INFORMATION SECURITY', 'blue'),
 'courseware': ('DOCS', 'COURSEWARE', 'blue'),
 'materials': ('DOCS', 'LEARNING MATERIALS', 'blue'),
 'notes': ('DOCS', 'NOTES', 'blue'),
 'review': ('DOCS', 'REVIEW MATERIALS', 'blue'),
 'cpp': ('LANG', 'C / C++', 'blue'),
 'python': ('LANG', 'PYTHON', 'blue'),
 'sql': ('LANG', 'SQL', 'blue'),
 'linux': ('SYS', 'LINUX', 'purple'),
 'git': ('TOOL', 'GIT', 'purple'),
 'cmake': ('BUILD', 'CMAKE', 'purple'),
 'gdb': ('DEBUG', 'GDB', 'purple'),
}
PALETTE = {'teal': ('#16443f','#73dccb'), 'purple': ('#35274f','#b99be9'), 'blue': ('#193d58','#86c8ef')}


def generate():
    folder = Path(__file__).resolve().parents[1] / 'assets' / 'badges'
    folder.mkdir(parents=True, exist_ok=True)
    for name, (category, label, theme) in BADGES.items():
        fill, accent = PALETTE[theme]
        left = len(category)*7+20
        right = len(label)*7+24
        width = left+right
        title = escape(category+' / '+label)
        content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28" role="img" aria-label="{title}">
<title>{title}</title>
<rect x=".5" y=".5" width="{width-1}" height="27" rx="3" fill="#101827" stroke="{accent}" stroke-opacity=".75"/>
<path d="M3 1H{left}V27H3Q1 27 1 25V3Q1 1 3 1" fill="{fill}"/>
<path d="M{left} 1V27" stroke="{accent}" stroke-opacity=".5"/>
<g font-family="Consolas,Menlo,monospace" font-size="11" text-anchor="middle">
<text x="{left/2}" y="18" fill="{accent}" font-weight="bold">{escape(category)}</text>
<text x="{left+right/2}" y="18" fill="#e2eaf4">{escape(label)}</text>
</g></svg>
'''
        (folder / (name+'.svg')).write_text(content, encoding='utf-8')
    print(f'Generated {len(BADGES)} badges.')


if __name__ == '__main__':
    generate()
