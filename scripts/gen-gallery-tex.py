import json, os

BASE = os.path.expanduser('~/Downloads/hology/submission')
manifest_path = f'{BASE}/gallery/screenshots/full/_manifest.json'
out_path = f'{BASE}/gallery/gallery-body.tex'

with open(manifest_path) as f:
    manifest = json.load(f)

CATEGORY_LABELS = {
    'auth': 'Autentikasi dan Landing',
    'core': 'Dashboard, For Me, Notifikasi',
    'projects': 'Manajemen Proyek',
    'pmo': 'PMO: Kanban, List, Timeline, Catatan, Whiteboard',
    'chat': 'Obrolan Tim',
    'voice': 'Panggilan Suara',
    'godmode': 'Godmode: Panel Kendali Swa-hosting',
    'admin': 'Konsol Admin',
    'settings': 'Pengaturan Personal',
    'theme': 'Galeri Tema (24 Tema x Terang/Gelap)',
    'misc': 'Legal dan Status Sistem',
    'mobile': 'Responsif di Layar Ponsel',
}

order = ['auth', 'core', 'projects', 'pmo', 'chat', 'voice', 'godmode', 'admin', 'settings', 'theme', 'misc', 'mobile']

by_cat = {}
for item in manifest:
    if not item['ok']:
        continue
    by_cat.setdefault(item['category'], []).append(item)

lines = []
total = 0
for cat in order:
    items = by_cat.get(cat, [])
    if not items:
        continue
    label = CATEGORY_LABELS.get(cat, cat.title())
    lines.append(r'\clearpage')
    lines.append(r'\subsection*{%s}' % label.replace('&', r'\&'))
    lines.append(r'\vspace{0.3em}')
    lines.append(r'\noindent')
    n = len(items)
    for i, item in enumerate(items):
        total += 1
        rel = "screenshots/thumbs/" + item['file'].replace('.png', '.jpg')
        cap = item['name'].replace('_', ' ').replace('-', ' ')
        lines.append(r'\begin{minipage}[t]{0.315\linewidth}')
        lines.append(r'\includegraphics[width=\linewidth]{%s}\\[0.15em]' % rel)
        lines.append(r'{\ttfamily\scriptsize\color{cink3} %03d \quad %s}' % (total, cap))
        lines.append(r'\end{minipage}')
        if (i + 1) % 3 == 0 and i != n - 1:
            lines.append(r'\par\vspace{0.9em}')
            lines.append(r'\noindent')
        elif i != n - 1:
            lines.append(r'\hfill')
    lines.append('')

with open(out_path, 'w') as f:
    f.write('\n'.join(lines))

print(f'Wrote {out_path} with {total} images across {len([c for c in order if by_cat.get(c)])} categories')
