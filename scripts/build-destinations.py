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
MIN_CITY = 4        # editions needed before a city gets its own chip
MIN_COUNTRY = 4

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

def country_of(place):
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
            city, country = city_of(place), country_of(place)
            if not city and not country: continue
            deadlines = sorted({dstr(t.get('deadline')) for t in (ed.get('timeline') or [])
                                if dstr(t.get('deadline'))})
            ahead = [d for d in deadlines if d >= TODAY.isoformat()]
            items.append({
                'title': c['title'], 'desc': (c.get('description') or '').strip(),
                'year': year, 'place': place, 'date': ed.get('date') or '',
                'city': city, 'country': country, 'continent': continent_of(country),
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
    m['continent'] = continent_of(m['country'])
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
         if not ((i['title'], i['city']) in seen or seen.add((i['title'], i['city'])))]
items.sort(key=lambda x: (x['year'], x['title'].lower()))
cities = collections.Counter(i['city'] for i in items if i['city'])
countries = collections.Counter(i['country'] for i in items if i['country'])
continents = collections.Counter(i['continent'] for i in items if i['continent'])

def chips(counter, floor):
    return [{'name': n, 'n': v} for n, v in counter.most_common() if v >= floor]

out = {
    'items': items,
    'cities': chips(cities, MIN_CITY),
    'countries': chips(countries, MIN_COUNTRY),
    'continents': chips(continents, 1),
}
hdr = ('// Generated by scripts/build-destinations.py, do not edit by hand.\n'
       '// Every announced future edition from the CCF catalogue, indexed by\n'
       '// where it is rather than when its deadline is. City and country are\n'
       '// kept as separate axes; anything that is neither, Hawaii for one, is\n'
       '// reached through the search over the raw place string.\n'
       f'// Built {TODAY.isoformat()}.\n')
with open('src/data/destinations.js', 'w') as f:
    f.write(hdr + 'export const destinations = ' + json.dumps(out, indent=1, ensure_ascii=False) + ';\n')

print(f"editions {len(items)} | cities {len(cities)} ({len(out['cities'])} with {MIN_CITY}+)"
      f" | countries {len(countries)} ({len(out['countries'])} with {MIN_COUNTRY}+)")
print('top cities   :', ', '.join(f"{c['name']} {c['n']}" for c in out['cities'][:10]))
print('top countries:', ', '.join(f"{c['name']} {c['n']}" for c in out['countries'][:10]))
print('continents   :', ', '.join(f"{c['name']} {c['n']}" for c in out['continents']))
unplaced = sorted({i['country'] for i in items if i['country'] and not i['continent']})
print('country with no continent:', unplaced or 'none')
print('hawaii rows  :', sum(1 for i in items if re.search(r'hawaii|honolulu|maui|waikoloa|big island', i['place'], re.I)))
