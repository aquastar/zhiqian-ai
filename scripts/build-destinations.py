"""Rebuild src/data/destinations.js: where the conferences actually are.

Run from the repo root:  python3 scripts/build-destinations.py
Expects .conf-cache/ccf-deadlines to exist, so run build-conferences.py first.

The conference table answers "when is the deadline". This answers the other
question people actually ask, which is "where would I be going". It indexes
every announced future edition by place, not just the next one, because a
conference in Kyoto in 2028 is the whole point of looking.
"""
import yaml, glob, re, json, datetime, collections, unicodedata, os

TODAY = datetime.date.today()
CACHE = '.conf-cache/ccf-deadlines/conference'

def norm(s):
    s = ''.join(ch for ch in unicodedata.normalize('NFD', s)
                if unicodedata.category(ch) != 'Mn')
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z ]', ' ', s.lower())).strip()

# Ordered: the first pattern that matches wins, so Hawaii and Florida are
# carved out of the United States before the catch-all US rule is reached.
PATTERNS = [
 ('Hawaii', 'umbrella-beach', r'hawaii|honolulu|maui|waikiki|waikoloa|kona|kauai|o ahu|oahu|hilo|big island|kohala'),
 ('Florida & Orlando', 'rocket', r'orlando|miami|tampa|florida|buena vista|boca raton|daytona|key west'),
 ('California', 'sun', r'california|san francisco|los angeles|san diego|san jose|san jos|long beach|anaheim|palo alto|santa barbara|sacramento|riverside|huntington beach|berkeley|pasadena|oakland'),
 ('Japan', 'torii-gate', r'japan|tokyo|kyoto|osaka|yokohama|fukui|nara|sapporo'),
 ('East Asia', 'dragon', r'china|korea|taiwan|hong kong|macau|macao|beijing|shanghai|seoul|taipei|shenzhen|hangzhou|guangzhou|chengdu'),
 ('Southeast Asia', 'leaf', r'singapore|malaysia|thailand|vietnam|indonesia|philippines|cambodia|hanoi|bangkok|jakarta|kuala lumpur|da nang|danang'),
 ('Canada', 'maple-leaf', r'canada|toronto|montreal|vancouver|ottawa|quebec|calgary|edmonton'),
 ('South America', 'mountain-sun', r'brazil|argentina|chile|colombia|peru|uruguay|ecuador|bolivia|sao paulo|rio de janeiro|buenos aires|santiago|bogota|lima'),
 ('Mexico, Central America & Caribbean', 'water', r'mexico|cancun|barbados|cuba|jamaica|bahamas|puerto rico|costa rica|panama|st kitts|saint kitts|belize|guatemala|dominican'),
 ('Mediterranean', 'wine-glass', r'italy|spain|portugal|greece|cyprus|malta|croatia|turkiye|turkey|slovenia|rome|milan|florence|venice|barcelona|madrid|lisbon|porto|athens|chania|limassol|bari|trento'),
 ('Western Europe', 'landmark', r'france|germany|netherlands|belgium|united kingdom|\buk\b|ireland|switzerland|austria|luxembourg|scotland|england|wales|paris|berlin|munich|amsterdam|brussels|london|dublin|zurich|vienna|delft|leiden|eindhoven|maastricht|bruges|lille|rennes|mainz|bremen|saarbrucken|the hague|hague|southampton|lancaster'),
 ('Nordic & Baltic', 'snowflake', r'sweden|denmark|norway|finland|iceland|estonia|latvia|lithuania|stockholm|copenhagen|oslo|helsinki|reykjavik|malmo|vilnius|linkoping'),
 ('Central & Eastern Europe', 'chess-rook', r'poland|czech|hungary|romania|bulgaria|slovakia|serbia|ukraine|prague|warsaw|krakow|budapest|poznan'),
 ('Oceania', 'kiwi-bird', r'australia|new zealand|sydney|melbourne|brisbane|auckland|wellington|perth|canberra|adelaide'),
 ('India & South Asia', 'archway', r'india|pakistan|bangladesh|sri lanka|nepal|delhi|mumbai|bengaluru|bangalore|hyderabad'),
 ('Africa & Middle East', 'khanda', r'south africa|morocco|egypt|israel|\buae\b|emirates|qatar|saudi|tunisia|kenya|cape town|marrakesh|dubai|abu dhabi'),
 ('United States, elsewhere', 'flag-usa', r'\busa\b|united states|united state|\bus\b|seattle|denver|atlanta|chicago|boston|new york|austin|phoenix|pittsburgh|cleveland|dallas|nashville|portland|minneapolis|salt lake city|boulder|colorado|washington|virginia|texas|georgia|arizona|utah|oregon|michigan|ohio|carolina|tennessee|pennsylvania|massachusetts|maryland|missouri|indiana|wisconsin|nevada|new jersey|newark|durham|columbia|fort collins|bellevue|sooke'),
]
NOWHERE = re.compile(r'^(virtual|online|tbd|tba|hybrid)$')

def destination(place):
    n = norm(place)
    if not n or NOWHERE.match(n): return None, None
    for name, icon, pat in PATTERNS:
        if re.search(pat, n): return name, icon
    return None, None

def dstr(s):
    m = re.match(r'(\d{4}-\d{2}-\d{2})', str(s or ''))
    return m.group(1) if m else ''

items = []
for f in sorted(glob.glob(f'{CACHE}/*/*.yml')):
    if f.endswith('types.yml'): continue
    for c in (yaml.safe_load(open(f)) or []):
        rank = c.get('rank') or {}
        for ed in c.get('confs') or []:
            year, place = ed.get('year'), str(ed.get('place') or '').strip()
            if not year or year < TODAY.year or not place: continue
            dest, icon = destination(place)
            if not dest: continue
            deadlines = sorted({dstr(t.get('deadline')) for t in (ed.get('timeline') or [])
                                if dstr(t.get('deadline'))})
            ahead = [d for d in deadlines if d >= TODAY.isoformat()]
            items.append({
                'title': c['title'], 'desc': (c.get('description') or '').strip(),
                'year': year, 'place': place, 'date': ed.get('date') or '',
                'dest': dest, 'icon': icon,
                'ccf': rank.get('ccf', 'N'), 'core': rank.get('core', 'N'),
                'deadline': ahead[0] if ahead else (deadlines[-1] if deadlines else ''),
                'open': bool(ahead),
                'link': ed.get('link', '') or '',
            })

# Hand-added, because the CS catalogue does not reach outside computer science
# and the whole point of this view is that a trip is a trip whatever the field.
MANUAL = []
for m in MANUAL:
    m['dest'], m['icon'] = destination(m['place'])
    items.append(m)

groups = collections.defaultdict(list)
for it in items: groups[it['dest']].append(it)
for g in groups.values():
    g.sort(key=lambda x: (x['year'], x['title'].lower()))

order = [name for name, _, _ in PATTERNS]
out = [{'dest': n, 'icon': dict((a, b) for a, b, _ in PATTERNS)[n],
        'n': len(groups[n]), 'items': groups[n]}
       for n in order if groups.get(n)]

hdr = ('// Generated by scripts/build-destinations.py, do not edit by hand.\n'
       '// Every announced future edition from the CCF catalogue, indexed by\n'
       '// where it is rather than when its deadline is.\n'
       f'// Built {TODAY.isoformat()}.\n')
with open('src/data/destinations.js', 'w') as f:
    f.write(hdr + 'export const destinations = ' + json.dumps(out, indent=1, ensure_ascii=False) + ';\n')

print('editions placed:', len(items), '| destinations:', len(out))
for g in out: print(f'  {g["dest"]:36s} {g["n"]}')
