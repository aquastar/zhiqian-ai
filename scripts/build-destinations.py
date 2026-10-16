"""Rebuild src/data/destinations.js: where the conferences actually are.

Run from the repo root:  python3 scripts/build-destinations.py
Expects .conf-cache/ccf-deadlines, so run build-conferences.py first.

Two clean axes, never mixed: city and country. A place like Hawaii is
neither, so it is reachable through the free-text search over the raw place
string instead of being wedged into one of the two lists.
"""
import yaml, glob, re, json, datetime, collections, unicodedata, calendar

TODAY = datetime.date.today()
CACHE = '.conf-cache/ccf-deadlines/conference'
# Only venues one of the two tables rates highly, plus anything added by hand
# below. The destination view is for deciding where to go, and a list padded
# with everything would bury the ones worth the flight.
def worth_listing(ccf, core):
    return ccf in ('A', 'B') or core in ('A*', 'A')

# Popular destinations, deliberately a mix of cities, countries and one
# region: these are places people pick, not a taxonomy. First match wins, so
# Hawaii is taken out of the United States before the country rule is reached.
DESTINATIONS = [
 # Cities first, then regions and countries. First match wins, so a city is
 # always taken out before the wider rule that would otherwise swallow it.
 ('Hawaii',          'umbrella-beach', r'hawaii|honolulu|maui|waikiki|waikoloa|kona|kauai|o ahu|oahu|hilo|big island|kohala'),
 ('Hong Kong',       'city',           r'hong kong'),
 # fa-maple-leaf does not exist in Font Awesome 6 Free, so these two rendered
 # with no icon at all until now.
 ('Montreal',        'snowflake',      r'montreal|montr al'),
 ('Toronto',         'tower-observation', r'toronto'),
 ('Orlando',         'rocket',         r'orlando'),
 ('Miami',           'umbrella-beach', r'miami'),
 # Regions and countries
 ('Japan',           'torii-gate',     r'japan|tokyo|kyoto|osaka|yokohama|fukui|nara|sapporo'),
 ('California',      'sun',            r'california|san francisco|los angeles|san diego|san jose|san jos|long beach|anaheim|palo alto|santa barbara|sacramento|riverside|huntington beach|berkeley|pasadena|oakland'),
 ('Italy',           'wine-glass',     r'italy|rome|milan|florence|venice|bari|trento|turin|bologna|naples'),
 ('Greece',          'landmark',       r'greece|athens|thessaloniki|chania|crete|rhodes'),
 ('Spain & Portugal','sun',            r'spain|portugal|barcelona|madrid|seville|valencia|lisbon|porto|malaga'),
 ('Netherlands',     'bicycle',        r'netherlands|amsterdam|delft|leiden|eindhoven|maastricht|rotterdam|nijmegen|utrecht|the hague|hague'),
 ('France',          'wine-bottle',    r'france|paris|lyon|lille|rennes|marseille|nice|toulouse|grenoble|bordeaux'),
 ('Germany',         'beer-mug-empty', r'germany|berlin|munich|hamburg|cologne|frankfurt|dresden|mainz|bremen|saarbrucken|leipzig|stuttgart'),
 ('UK & Ireland',    'crown',          r'united kingdom|\buk\b|england|scotland|wales|ireland|london|edinburgh|glasgow|manchester|oxford|cambridge|bristol|dublin|galway|cork|southampton|lancaster'),
 ('Australia & NZ',  'kiwi-bird',      r'australia|new zealand|sydney|melbourne|brisbane|auckland|wellington|perth|canberra|adelaide|hobart'),
 ('South America',   'mountain-sun',   r'brazil|argentina|chile|colombia|peru|uruguay|ecuador|sao paulo|rio de janeiro|buenos aires|santiago|bogota|lima|cuiaba|florianopolis'),
 ('Southeast Asia',  'leaf',           r'malaysia|thailand|vietnam|indonesia|philippines|cambodia|bali|hanoi|bangkok|jakarta|kuala lumpur|da nang|danang|depok'),
]

def destination_of(place):
    n = key(place)
    for name, icon, pat in DESTINATIONS:
        if re.search(pat, n): return name, icon
    return '', ''


def strip_accents(s):
    return ''.join(ch for ch in unicodedata.normalize('NFD', s)
                   if unicodedata.category(ch) != 'Mn')

def key(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z ]', ' ', strip_accents(s).lower())).strip()

# Venue names, not places. The upstream place field often leads with the hotel.
NOT_A_PLACE = re.compile(
    r'hotel|hilton|marriott|hyatt|sheraton|westin|cordis|sofitel|university|college'
    r'|campus|convention|conference|cent(er|re)|holloway|springs|palace|resort|\bhall\b', re.I)
NOWHERE = re.compile(r'^(online|virtual|tbd|tba|hybrid)$', re.I)

CITY_ALIAS = {
    'hong kong sar': 'Hong Kong', 'hong kong': 'Hong Kong',
    'macao': 'Macau', 'macau sar': 'Macau',
    'new york city': 'New York', 'nyc': 'New York',
    'washington dc': 'Washington', 'washington d c': 'Washington',
    'waikiki': 'Honolulu', 'o ahu': 'Honolulu', 'oahu': 'Honolulu',
    'montreal': 'Montreal', 'sao paulo': 'Sao Paulo', 'zurich': 'Zurich',
    'malmo': 'Malmo', 'krakow': 'Krakow', 'poznan': 'Poznan',
    'dusseldorf': 'Dusseldorf', 'san jose': 'San Jose',
}
COUNTRY_ALIAS = {
    'usa': 'United States', 'united states': 'United States', 'united state': 'United States',
    'us': 'United States', 'uk': 'United Kingdom', 'united kingdom': 'United Kingdom',
    'england': 'United Kingdom', 'scotland': 'United Kingdom', 'wales': 'United Kingdom',
    'the netherlands': 'Netherlands', 'netherlands': 'Netherlands',
    'korea': 'South Korea', 'republic of korea': 'South Korea', 'south korea': 'South Korea',
    'hong kong sar': 'Hong Kong', 'hong kong': 'Hong Kong', 'mexico city': 'Mexico',
    'czechia': 'Czechia', 'czech republic': 'Czechia', 'turkiye': 'Turkiye',
    'uae': 'United Arab Emirates',
}
# Two-letter US state codes and the like, which are not countries.
TOO_SHORT_OK = {'uae'}

# Upstream place strings carry hybrid notes and a full-width comma now and
# then, and often end on a US state rather than a country.
HYBRID_TAIL = re.compile(r'\s*(and|&|/)\s*(online|virtual|hybrid|in person)\s*$', re.I)
US_STATES = {
 'alabama','alaska','arizona','arkansas','california','colorado','connecticut','delaware','florida',
 'georgia','hawaii','idaho','illinois','indiana','iowa','kansas','kentucky','louisiana','maine',
 'maryland','massachusetts','michigan','minnesota','mississippi','missouri','montana','nebraska',
 'nevada','new hampshire','new jersey','new mexico','new york','north carolina','north dakota','ohio',
 'oklahoma','oregon','pennsylvania','rhode island','south carolina','south dakota','tennessee','texas',
 'utah','vermont','virginia','washington','west virginia','wisconsin','wyoming','district of columbia'}
# Expanded into the search blob so "hawaii" finds "Honolulu, HI, USA".
STATE_CODE = {
 'hi':'hawaii','ca':'california','fl':'florida','ny':'new york','tx':'texas','wa':'washington',
 'ma':'massachusetts','co':'colorado','ga':'georgia','il':'illinois','pa':'pennsylvania',
 'az':'arizona','ut':'utah','or':'oregon','nc':'north carolina','sc':'south carolina','mi':'michigan',
 'oh':'ohio','nj':'new jersey','md':'maryland','va':'virginia','tn':'tennessee','mn':'minnesota',
 'mo':'missouri','in':'indiana','wi':'wisconsin','nv':'nevada','la':'louisiana','ok':'oklahoma',
 'qc':'quebec','on':'ontario','bc':'british columbia','ab':'alberta','nsw':'new south wales',
 'vic':'victoria','qld':'queensland','wa au':'western australia','mt':'mato grosso',
}
def expand(place):
    extra = [full for seg in re.split(r'[,\s]+', place)
             for code, full in STATE_CODE.items() if seg.lower() == code]
    return ' '.join(extra)

US_CITIES = {'san francisco','san jose','long beach','palo alto','los angeles','new york','seattle',
             'atlanta','denver','boston','chicago','austin','pittsburgh','cleveland','honolulu'}

# Same rule as the conference table: a Taiwanese venue is listed by its city
# alone. Nothing here depends on it today, since no Taiwanese city has a chip,
# but the rule should hold wherever a place string is printed.
TW_CITY = re.compile(r'\b(taipei|hsinchu|kaohsiung|tainan|taichung|taoyuan|keelung)\b', re.I)
def simplify_place(place):
    m = TW_CITY.search(place or '')
    return m.group(1).title() if m else place

def segments(place):
    place = re.sub(r'\(.*?\)', '', re.split(r'[;]', place)[0])
    place = place.replace('\uff0c', ',')
    return [HYBRID_TAIL.sub('', p).strip() for p in place.split(',') if p.strip()]

def city_of(place):
    for seg in segments(place):
        if NOT_A_PLACE.search(seg) or NOWHERE.match(seg): continue
        k = key(seg)
        if not k or k in ('usa', 'uk', 'us', 'sar'): continue
        return CITY_ALIAS.get(k, seg.strip())
    return ''

# ISO 3166-1 is a list of countries AND territories, and it carries separate
# entries for CN, HK, MO and TW. Following it keeps this axis consistent no
# matter how an upstream contributor wrote the suffix, and means the page is
# citing a standard rather than making a call of its own. ccfddl itself has
# no convention here: its README asks only for "city, country" and the
# catalogue contains Hong Kong written five different ways.
ISO_TERRITORY = {
    'taiwan': 'Taiwan', 'hong kong': 'Hong Kong', 'macau': 'Macau', 'macao': 'Macau',
}

def country_of(place):
    # A territory named anywhere in the string wins over a trailing country,
    # so "Hsinchu, Taiwan, China" and "Taipei, Taiwan" land in the same place.
    for seg in segments(place):
        k = re.sub(r'\s*sar\s*$', '', key(seg))
        if k in ISO_TERRITORY: return ISO_TERRITORY[k]
    return _country_tail(place)

def _country_tail(place):
    for seg in reversed(segments(place)):
        k = re.sub(r' sar$', '', key(seg))
        if not k or NOWHERE.match(k): continue
        if k in COUNTRY_ALIAS: return COUNTRY_ALIAS[k]
        if len(k) <= 3 and k not in TOO_SHORT_OK: continue   # CA, HI, NY
        if k in US_STATES or k in US_CITIES: return 'United States'
        if NOT_A_PLACE.search(seg) or k.endswith(' expo') or k.endswith(' disneyland'): continue
        if k.endswith(' china'): return 'China'
        return seg.strip().title()
    return ''

CONTINENT = {
 'North America': ['united states','canada','mexico','costa rica','panama','guatemala','belize',
                   'cuba','jamaica','bahamas','barbados','puerto rico','dominican republic','st kitts','saint kitts'],
 'South America': ['brazil','argentina','chile','colombia','peru','uruguay','ecuador','bolivia','paraguay','venezuela'],
 'Europe': ['united kingdom','ireland','france','germany','netherlands','belgium','luxembourg','switzerland',
            'austria','italy','spain','portugal','greece','cyprus','malta','croatia','slovenia','poland',
            'czechia','hungary','romania','bulgaria','slovakia','serbia','ukraine','sweden','denmark','norway',
            'finland','iceland','estonia','latvia','lithuania','turkiye','turkey'],
 'Asia': ['china','japan','south korea','taiwan','hong kong','macau','singapore','malaysia','thailand',
          'vietnam','indonesia','philippines','cambodia','india','pakistan','bangladesh','sri lanka','nepal',
          'israel','united arab emirates','qatar','saudi arabia','jordan','kazakhstan'],
 'Oceania': ['australia','new zealand','fiji'],
 'Africa': ['south africa','morocco','egypt','tunisia','kenya','nigeria','ghana','ethiopia','rwanda'],
}
TO_CONTINENT = {c: k for k, v in CONTINENT.items() for c in v}
def continent_of(country):
    return TO_CONTINENT.get(key(country), '')

MONTHS = {m: i for i, m in enumerate(
    ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'], 1)}

def ends_after_today(date_text, year):
    """Has this edition finished? Dates are free text, so be generous.

    Takes the last month named, because a run like "September 26 - October 1"
    ends in the later one, and treats the end of that month as the finish.
    Unparseable dates fall back to the year, which keeps the current year in.
    """
    if not date_text:
        return year >= TODAY.year
    months = [MONTHS[m] for m in re.findall(r'[a-z]{3}', date_text.lower()) if m in MONTHS]
    yrs = [int(y) for y in re.findall(r'\b(20\d{2})\b', date_text)]
    y = max(yrs) if yrs else year
    if not months:
        return y >= TODAY.year
    m = max(months) if len(set(months)) > 1 else months[0]
    return datetime.date(y, m, calendar.monthrange(y, m)[1]) >= TODAY

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
            if not ends_after_today(ed.get('date') or '', year): continue
            if NOWHERE.match(key(place)): continue
            if not worth_listing(rank.get('ccf', 'N'), rank.get('core', 'N')): continue
            dest, icon = destination_of(place)
            if not dest: continue   # no chip, and no search box, so no way in
            city, country = city_of(place), country_of(place)
            deadlines = sorted({dstr(t.get('deadline')) for t in (ed.get('timeline') or [])
                                if dstr(t.get('deadline'))})
            ahead = [d for d in deadlines if d >= TODAY.isoformat()]
            items.append({
                'title': c['title'], 'desc': (c.get('description') or '').strip(),
                'year': year, 'place': simplify_place(place), 'date': ed.get('date') or '',
                'city': city, 'country': country, 'dest': dest, 'icon': icon,
                'ccf': rank.get('ccf', 'N'), 'core': rank.get('core', 'N'),
                'deadline': ahead[0] if ahead else (deadlines[-1] if deadlines else ''),
                'open': bool(ahead), 'link': ed.get('link', '') or '',
                # Precomputed here rather than in the template: 550 template
                # literals is enough to blow the Astro compiler's WASM heap.
                'q': f"{place} {city} {country} {expand(place)}".lower(),
            })

# Hand-added, because the catalogue is computer science only and a trip is a
# trip whatever the field. Each needs title, desc, year, place, date,
# deadline, open, link; city and country are derived.
MANUAL = [
 # Hawaii. PSB is the anchor: the same hotel on the Big Island six years
 # running, 2022 through 2027, each verified on psb.stanford.edu.
 {'title':'PSB','desc':'Pacific Symposium on Biocomputing','year':2027,
  'place':'Kohala Coast, Big Island, Hawaii, USA','date':'January 3-7, 2027',
  'deadline':'2026-12-01','open':True,'link':'https://psb.stanford.edu/'},
 # CDC is in neither ccfddl nor the CORE export, both of which are
 # computing, so nothing upstream knows it exists and it has to be named
 # here. The 65th is at the Hilton Hawaiian Village; its paper deadline was
 # 31 March 2026 and has long gone, so the call shows as closed. The 66th
 # has no announced venue yet, which is why only this edition is listed.
 {'title':'CDC','desc':'IEEE Conference on Decision and Control','year':2026,
  'place':'Honolulu, Hawaii, USA','date':'December 15-18, 2026',
  'deadline':'2026-03-31','open':False,'link':'https://cdc2026.ieeecss.org/'},
 {'title':'AMOS','desc':'Advanced Maui Optical and Space Surveillance Technologies Conference','year':2027,
  'place':'Maui, Hawaii, USA','date':'September 14-17, 2027',
  'deadline':'','open':False,'link':'https://amostech.com/'},
 {'title':'ICLDC','desc':'International Conference on Language Documentation and Conservation','year':2027,
  'place':'Honolulu, Hawaii, USA','date':'March 4-7, 2027',
  'deadline':'2026-09-30','open':False,'link':'https://ling.lll.hawaii.edu/sites/icldc/'},
 {'title':'HARC','desc':'Hawaii Accounting Research Conference','year':2027,
  'place':'Honolulu, Hawaii, USA','date':'January 2-5, 2027',
  'deadline':'2026-07-31','open':False,'link':'https://manoa.hawaii.edu/harc/'},
 {'title':'IICE','desc':'IAFOR International Conference on Education, Hawaii','year':2027,
  'place':'Honolulu, Hawaii, USA','date':'January 8-11, 2027',
  'deadline':'2026-09-24','open':False,'link':'https://iicehawaii.iafor.org/'},
 # Florida
 {'title':'FLAIRS','desc':'Florida Artificial Intelligence Research Society Conference','year':2027,
  'place':'St. Pete Beach, Florida, USA','date':'May 24-27, 2027',
  'deadline':'2027-01-22','open':True,'link':'https://www.flairs-40.info/'},
 {'title':'AIAA SciTech','desc':'AIAA Science and Technology Forum and Exposition','year':2027,
  'place':'Orlando, Florida, USA','date':'January 11-15, 2027',
  'deadline':'','open':False,'link':'https://scitech.aiaa.org/'},
 {'title':'SoutheastCon','desc':'IEEE SoutheastCon','year':2027,
  'place':'Daytona Beach, Florida, USA','date':'April 15-18, 2027',
  'deadline':'','open':False,'link':'https://ieeesoutheastcon.org/'},
 # Canada
 {'title':'CASCON','desc':'IEEE International Conference on Collaborative Advances in Software and Computing','year':2026,
  'place':'Toronto, Ontario, Canada','date':'November 9-12, 2026',
  'deadline':'2026-07-13','open':False,'link':'https://conf.researchr.org/home/cascon-2026'},
 # Japan
 {'title':'SICE ISCS','desc':'SICE International Symposium on Control Systems','year':2027,
  'place':'Tokyo, Japan','date':'March 2-5, 2027',
  'deadline':'','open':False,'link':'https://iscs2027.sice-ctrl.jp'},
 # South America
 {'title':'BRACIS','desc':'Brazilian Conference on Intelligent Systems','year':2026,
  'place':'Cuiaba, Mato Grosso, Brazil','date':'October 19-22, 2026',
  'deadline':'2026-05-04','open':False,'link':'https://bracis.sbc.org.br/2026/'},
 # Southeast Asia
 {'title':'ACIIDS','desc':'Asian Conference on Intelligent Information and Database Systems','year':2027,
  'place':'Bali, Indonesia','date':'April 5-7, 2027',
  'deadline':'2026-10-31','open':True,'link':'https://aciids.pwr.edu.pl/'},
 {'title':'IEEM','desc':'IEEE International Conference on Industrial Engineering and Engineering Management','year':2026,
  'place':'Singapore','date':'December 2-5, 2026',
  'deadline':'2026-09-30','open':False,'link':'https://www.ieem.org/'},
 # Australia and New Zealand
 {'title':'ANZIAM','desc':'Australian and New Zealand Industrial and Applied Mathematics Conference','year':2027,
  'place':'Auckland, New Zealand','date':'February 1-5, 2027',
  'deadline':'','open':False,'link':'https://www.anziam.org.au/events'},
 {'title':'MODSIM','desc':'International Congress on Modelling and Simulation','year':2027,
  'place':'Perth, Western Australia, Australia','date':'December 5-9, 2027',
  'deadline':'','open':False,'link':'https://mssanz.org.au/modsim2027/'},
 {'title':'AJCAI','desc':'Australasian Joint Conference on Artificial Intelligence','year':2026,
  'place':'Auckland, New Zealand','date':'November 27-30, 2026',
  'deadline':'','open':False,'link':'https://ajcai26.org/'},
 {'title':'AusDM','desc':'Australasian Data Science and Machine Learning Conference','year':2026,
  'place':'Sydney, New South Wales, Australia','date':'December 2-4, 2026',
  'deadline':'2026-07-26','open':False,'link':'https://ausdm26.ausdm.org/'},
]
for m in MANUAL:
    if not ends_after_today(m.get('date', ''), m['year']): continue
    m['city'], m['country'] = city_of(m['place']), country_of(m['place'])
    m['dest'], m['icon'] = destination_of(m['place'])
    if not m['dest']:
        print('  DROPPED, hand-added venue matches no destination:', m['title'], m['place'])
        continue
    m['q'] = f"{m['place']} {m['city']} {m['country']} {expand(m['place'])}".lower()
    m.setdefault('ccf', 'N'); m.setdefault('core', 'N')
    items.append(m)

# Editions that have already happened are gone, so a conference appears once
# per city: its next visit there. Deduping by title alone would be wrong here,
# because RecSys 2026 somewhere else would hide RecSys 2027 in Honolulu, and
# the whole point of this view is to find the latter.
items.sort(key=lambda x: (x['year'], x['date'], x['title'].lower()))
seen = set()
items = [i for i in items
         if not ((i['title'], i['dest']) in seen or seen.add((i['title'], i['dest'])))]
items.sort(key=lambda x: (x['year'], x['title'].lower()))

counts = collections.Counter(i['dest'] for i in items)
order = [n for n, _, _ in DESTINATIONS if counts[n]]
icons = {n: ic for n, ic, _ in DESTINATIONS}
out = {
    'items': items,
    'places': [{'name': n, 'icon': icons[n], 'n': counts[n]} for n in order],
}
hdr = ('// Generated by scripts/build-destinations.py, do not edit by hand.\n'
       '// Upcoming editions worth travelling for, grouped by destination.\n'
       '// Only CCF A or B, or CORE A* or A, plus the venues added by hand in\n'
       '// the script. Destinations deliberately mix cities, countries and\n'
       '// regions, because that is how people choose where to go.\n'
       f'// Built {TODAY.isoformat()}.\n')
with open('src/data/destinations.js', 'w') as f:
    f.write(hdr + 'export const destinations = ' + json.dumps(out, indent=1, ensure_ascii=False) + ';\n')

print('editions', len(items), '| destinations', len(out['places']))
for pl in out['places']: print(f"  {pl['name']:18s} {pl['n']}")
print('hawaii rows  :', sum(1 for i in items if re.search(r'hawaii|honolulu|maui|waikoloa|big island', i['place'], re.I)))
