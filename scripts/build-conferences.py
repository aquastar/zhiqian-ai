"""Rebuild src/data/conferences.js from upstream sources.

Run from the repo root:  python3 scripts/build-conferences.py
It clones ccf-deadlines, pulls the official CORE2023 export and the
acceptance-rate table into .conf-cache/, then rewrites the data module.
"""
import yaml, glob, csv, re, json, datetime, collections, os, subprocess, urllib.request, urllib.error, unicodedata, time

TODAY = datetime.date.today()
# How far into the past an announced deadline still counts as belonging to
# the cycle now in play. Wide enough to hold a call that has just closed,
# narrow enough to exclude the previous edition.
ANNOUNCED_GRACE = datetime.timedelta(days=180)
CACHE = '.conf-cache'
os.makedirs(CACHE, exist_ok=True)
os.chdir(CACHE)

if not os.path.isdir('cs-conf-stats'):
    subprocess.run(['git','clone','--depth','1','-q',
                    'https://github.com/Xovee/cs-conf-stats.git'], check=True)
else:
    subprocess.run(['git','-C','cs-conf-stats','pull','-q'], check=True)

if not os.path.isdir('ccf-deadlines'):
    subprocess.run(['git','clone','--depth','1','-q',
                    'https://github.com/ccfddl/ccf-deadlines.git'], check=True)
else:
    subprocess.run(['git','-C','ccf-deadlines','pull','-q'], check=True)

for url, dest in [
    ('https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings.js', 'csrankings.js'),
    ('https://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2023&sort=atitle&page=1&do=Export', 'core2023.csv'),
]:
    with urllib.request.urlopen(url, timeout=120) as r, open(dest,'wb') as f:
        f.write(r.read())

# ---------- official CORE 2023 ----------
core_rows=[r for r in csv.reader(open('core2023.csv')) if len(r)>=5]
norm=lambda x: re.sub(r'[^a-z0-9]','',(x or '').lower())
toks=lambda x: set(re.findall(r'[a-z]{4,}',(x or '').lower()))
def canon(v):
    v=(v or '').strip()
    if v in ('A*','A','B','C'): return v
    if v.upper()=='TBR': return 'TBR'
    if 'journal' in v.lower(): return 'JP'
    return 'N'
by_title={norm(r[1]): r[4] for r in core_rows}
acr=collections.defaultdict(list)
for r in core_rows: acr[norm(r[2])].append(r)
def official(title, desc):
    v=by_title.get(norm(desc)) or by_title.get(norm(title))
    if v is not None: return canon(v)
    dt=toks(desc)
    for r in acr.get(norm(title), []):
        if dt and len(dt & toks(r[1]))>=2: return canon(r[4])
    return None

# ---------- acceptance rates ----------
# One source only: cs-conf-stats, which publishes accepted and submitted
# counts per year and is current to 2026. The older README compilation
# (lixin4ever/Conference-Acceptance-Rate) used to fill the gaps, but it
# carried percentages with no counts behind them, no submission series, and
# no way to check a number against anything. A venue cs-conf-stats does not
# cover now shows no rate rather than an unverifiable one.
# cs-conf-stats carries accepted/submitted counts per year and is current to
# 2026 for most venues, so it is the primary source; the older compilation is
# kept only to fill venues it does not cover.
CSC_ALIAS={'KDD':'SIGKDD','IEEE S&P':'S&P','Interspeech':'InterSpeech'}
csc_rates={}; csc_slug={}; csc_ordinal={}; csc_subs={}
for c in json.load(open('cs-conf-stats/data/conf.json'))['conferences']:
    t=CSC_ALIAS.get(c['series'], c['series'])
    hist={}
    for y in c.get('yearly_data') or []:
        mt=y.get('main_track') or {}
        a,sb=mt.get('num_acc'), mt.get('num_sub')
        if a and sb:
            hist[y['year']]=round(100*a/sb, 1)
            # The submission count alongside the rate. A rate cannot tell a
            # harder bar from a bigger pile; the two series together can.
            # Most venues grew acceptances in step with submissions and held
            # their rate near 25%, and the ones whose rate fell did not.
            csc_subs.setdefault(t, {})[y['year']]=sb
    if hist:
        csc_rates[t]=hist
        csc_slug[t]=c['series'].lower().replace(' ','-').replace('&','')
    ords={y['year']: y['ordinal'] for y in (c.get('yearly_data') or []) if y.get('ordinal')}
    if ords: csc_ordinal[t]=max(ords.items())
print('cs-conf-stats venues with rates:', len(csc_rates))

# Best-paper awards: Jeff Huang's compilation, the only maintained
# cross-conference list. Anchors verified against the live page.
BEST={'AAAI':'aaai','ACL':'acl','CIKM':'cikm','CVPR':'cvpr','ICCV':'iccv','ICML':'icml',
      'IJCAI':'ijcai','SIGKDD':'kdd','NeurIPS':'neurips','PODS':'pods','S&P':'s&p',
      'SIGIR':'sigir','SIGMOD':'sigmod','VLDB':'vldb','WWW':'www','FSE':'fse'}

# ---------- CSRankings ----------
# CSRankings counts publications only at a fixed venue list per area, which is
# the closest thing the field has to a statement of which venues "count".
# Match on the DBLP key, which both sides already use.
CSR_ALIAS={'oakland':'sp','usenixsec':'uss','chiconf':'chi','nips':'nips'}
# Upstream gives AsiaCCS the DBLP key of ACM CCS, which both sends its
# proceedings link to the wrong venue and makes it look like a CSRankings
# venue. It is the only duplicate key in the whole catalogue.
DBLP_FIX={'AsiaCCS':'asiaccs'}
_csr=open('csrankings.js', encoding='utf-8', errors='ignore').read()
_i=_csr.find('areaMap = ['); _j=_csr.find('];', _i)
_pairs=re.findall(r'\{\s*area:\s*"([^"]+)",\s*title:\s*"([^"]+)"\s*\}', _csr[_i:_j])
CSR={CSR_ALIAS.get(a, a): t for a, t in _pairs if a.lower() != t.lower()}
if len(CSR) < 50:
    raise SystemExit(f'CSRankings areaMap parse found only {len(CSR)} venues; '
                     'the upstream file changed shape, fix the parser rather '
                     'than shipping an empty column.')
print('CSRankings venues:', len(CSR))

def ordinal_for(title, year, period):
    """Project the edition number forward from the last one on record.

    cs-conf-stats records an ordinal per year. Only project a few editions
    ahead: past that a skipped or merged year makes the count wrong.
    """
    rec=csc_ordinal.get(title)
    if not rec or not year: return ''
    base_year, label = rec
    m=re.match(r'(\d+)', str(label))
    if not m: return ''
    ahead = round((year - base_year) / max(period, 1))
    if ahead < 0 or ahead > 3: return ''
    n = int(m.group(1)) + ahead
    suf = 'th' if 10 <= n % 100 <= 20 else {1:'st', 2:'nd', 3:'rd'}.get(n % 10, 'th')
    return f'{n}{suf}'

# ---------- what the host city is good for ----------
# Three things per city, hand written. There is no data source for this, so a
# city that is not in the map simply shows nothing rather than a guess.
CITY_SKIP = re.compile(r'hotel|hilton|marriott|hyatt|sheraton|university|college|'
                       r'campus|convention|conference|cent(er|re)|holloway|springs|'
                       r'^online$|^virtual$|^cordis$|^westin$|^sofitel$', re.I)
def city_key(place):
    if not place: return ''
    p = re.sub(r'\(.*?\)', '', place.split(';')[0])
    for part in [x.strip() for x in p.split(',') if x.strip()]:
        if CITY_SKIP.search(part): continue
        c = ''.join(ch for ch in unicodedata.normalize('NFD', part)
                    if unicodedata.category(ch) != 'Mn')
        c = re.sub(r'[^a-z ]', '', c.lower()).strip()
        c = re.sub(r' sar$', '', c)
        if c and c not in ('sar', 'usa', 'uk'): return c
    return ''

CITY = {
 'amsterdam': "herring from a street cart, genever in a brown cafe, Van Gogh's own bedroom",
 'athens': 'rooftop dinner under the lit Acropolis, souvlaki on Mitropoleos, Sunday flea at Monastiraki',
 'atlanta': 'Busy Bee fried chicken, walking under the whale sharks, Ponce City Market rooftop',
 'austin': 'Franklin brisket worth the queue, 1.5 million bats off Congress Bridge at dusk, 68F Barton Springs',
 'barbados': 'Friday fish fry at Oistins, Mount Gay rum since 1703, swimming with wild turtles off Carlisle Bay',
 'barcelona': "vermut and bombas in Barceloneta, Gaudi's still-unfinished Sagrada Familia, 2am Gothic Quarter",
 'bari': 'orecchiette rolled by hand in the street, focaccia barese, swimming off the old town wall',
 'beijing': 'Peking duck carved tableside, tobogganing down the Great Wall at Mutianyu, hutong breakfast jianbing',
 'bellevue': 'Din Tai Fung soup dumplings, Snoqualmie Falls, Seattle twenty minutes west',
 'bengaluru': 'masala dosa at CTR, filter coffee by the glass, Nandi Hills above the clouds at sunrise',
 'berlin': "doner at Mustafa's, Sunday karaoke in Mauerpark, currywurst at 4am",
 'bremen': 'Beck\'s at the brewery, Knipp for breakfast, the Schnoor lanes barely two people wide',
 'brisbane': 'sandboarding Moreton Island, holding a koala at Lone Pine, Eat Street shipping-container markets',
 'bruges': 'frites with andalouse sauce, 300 beers at t Brugs Beertje, canals empty after the day trippers leave',
 'budapest': 'chess in the hot pools at Szechenyi, ruin bar Szimpla Kert, langos the size of your head',
 'buena vista': 'Disney World, a Space Coast rocket launch, Cuban sandwiches in Ybor City',
 'buenos aires': 'asado and malbec, a neighborhood milonga rather than a tango show, dulce de leche in everything',
 'cancun': 'swimming in a cenote, Chichen Itza at opening time, cochinita pibil tacos',
 'cape town': 'braai above Camps Bay, Stellenbosch wine an hour out, cable car up Table Mountain',
 'chania': 'the Venetian harbour at sunset, dakos and raki, Balos lagoon by boat',
 'chengdu': 'mala hotpot you will remember, pandas at morning feeding, ear cleaning in a Renmin Park teahouse',
 'columbia': 'mustard-sauce Carolina barbecue, boardwalk through the Congaree cypress, Riverbanks Zoo',
 'copenhagen': 'smorrebrod, Reffen street food on the water, Tivoli lit up after dark',
 'dallas': 'Texas brisket, the Sixth Floor Museum window, live music in Deep Ellum',
 'danang': 'mi quang and banh mi, the Golden Bridge hands, Hoi An lanterns an hour south',
 'delft': "Vermeer's exact view, painting your own Delft Blue, apple pie on the Markt",
 'denver': 'a show at Red Rocks, green chile smothered burritos, skiing two hours west',
 'dublin': 'a pint poured properly at the Gravity Bar, a trad session in a back room, fish and chips after the Howth cliff walk',
 'durham': 'whole-hog eastern NC barbecue, a Durham Bulls game, Duke Gardens',
 'edinburgh': 'whisky flights, Arthur Seat at sunrise, haggis done well enough to convert you',
 'eindhoven': 'Dutch Design Week, bitterballen with mustard, the Strijp-S factory district',
 'florence': 'bistecca alla fiorentina for two, gelato at Vivoli, the Uffizi first thing',
 'fort collins': 'New Belgium brewery tour, Horsetooth Reservoir, Rocky Mountain National Park',
 'fukui': 'Echizen snow crab in season, the dinosaur museum, an overnight stay at Eiheiji zen temple',
 'guangzhou': 'morning yum cha trolleys, late-night congee on Shamian, Canton Tower',
 'guiyang': 'suan tang yu sour fish soup, Huangguoshu Waterfall, Qingyan ancient town',
 'haining': 'the Qiantang tidal bore in autumn, leather markets, Hangzhou forty minutes away',
 'hangzhou': 'West Lake at dawn, picking Longjing tea, dongpo pork',
 'hanoi': 'pho and egg coffee, scooter chaos in the Old Quarter, an overnight junk on Ha Long Bay',
 'hefei': 'Huangshan sunrise as a day trip, Hui-style stewed fish, Sanhe water town',
 'hengqin': 'Chimelong Ocean Kingdom, Macau over the bridge, Hengqin seafood night market',
 'hong kong': 'dim sum off a trolley, the Peak tram after dark, Tai O stilt houses and shrimp paste',
 'honolulu': 'poke and shave ice, Diamond Head at sunrise, North Shore surf in winter',
 'hsinchu': 'Hsinchu rice noodles and pork meatballs, Beipu Hakka lei cha, Taipei forty minutes by rail',
 'huntington beach': 'the pier at sunset, fish tacos, the PCH down to Laguna',
 'jinan': 'Baotu Spring, climbing Mount Tai overnight for the sunrise, Shandong pancakes',
 'krakow': 'pierogi and zapiekanka, the Wieliczka salt mine, a trumpet cut off mid-note every hour',
 'kuala lumpur': 'nasi lemak at Village Park, 272 steps at Batu Caves, Jalan Alor at midnight',
 'kunming': 'crossing-the-bridge noodles, the Stone Forest, spring weather all year',
 'kyoto': 'a kaiseki dinner, Fushimi Inari before dawn and empty, matcha in Uji',
 'lancaster': 'the Lake District an hour north, sticky toffee pudding, Lancaster Castle',
 'leiden': 'the oldest botanical garden in the Netherlands, canal-side terraces, stroopwafels off the iron',
 'lille': 'moules-frites, waffles at Meert, the Braderie flea market in September',
 'limassol': 'meze by the sea that keeps coming, Troodos mountain villages, Kourion amphitheatre',
 'london': 'lunch at Borough Market, a West End show, Sunday roast in a proper pub',
 'los angeles': 'tacos al pastor off a truck, Griffith Observatory at dusk, the Getty for free',
 'luxembourg': 'the Bock casemates, Mullerthal hiking trails, judd mat gaardebounen',
 'maastricht': 'vlaai pie, the Sint-Pietersberg caves, a bookshop in a 13th-century church',
 'macau': "egg tarts at Lord Stow's, African chicken, the Ruins of St Paul lit at night",
 'madrid': 'jamon iberico at Mercado San Miguel, churros at 2am, the Prado',
 'mainz': 'Riesling in the Rheingau, the Gutenberg Bible, Mainz carnival if you time it',
 'malmo': 'falafel, the Turning Torso, Copenhagen 35 minutes over the bridge',
 'marrakesh': 'Jemaa el-Fnaa as the food stalls open, tagine in the souk, the Atlas Mountains in a day',
 'melbourne': 'laneway coffee that ruins other coffee, AFL at the MCG, the Great Ocean Road',
 'milan': 'aperitivo hour, risotto alla milanese, the Last Supper if you book early',
 'montreal': "smoked meat at Schwartz's, wood-fired bagels at 3am, Mount Royal lookout",
 'new delhi': 'street chaat in Chandni Chowk, Humayun Tomb, the Taj Mahal at sunrise',
 'new york': 'a slice at 2am, the Met, standing-room Broadway tickets',
 'new york city': 'a slice at 2am, the Met, standing-room Broadway tickets',
 'newark': 'Ironbound Portuguese grills, Branch Brook cherry blossoms, Manhattan twenty minutes away',
 'osaka': 'takoyaki and okonomiyaki, Dotonbori neon, Nara deer in a day',
 'ottawa': 'BeaverTails on the Rideau Canal, skating the canal in winter, the National Gallery',
 'phoenix': 'Sonoran hot dogs, Camelback at sunrise, Sedona red rocks',
 'poznan': 'St Martin croissants, two mechanical goats butting heads at noon, the colored houses on the square',
 'rennes': 'galettes and cider, the half-timbered old town, Mont Saint-Michel in a day',
 'reykjavik': 'the Blue Lagoon, northern lights in winter, the hot dog stand everyone queues at',
 'rio de janeiro': 'feijoada on Saturday, Christ the Redeemer, Ipanema at sunset',
 'riverside': 'the Mission Inn at Christmas, citrus groves, Joshua Tree stargazing',
 'rome': 'cacio e pepe in Trastevere, gelato at Giolitti, the Colosseum at opening',
 'saarbrucken': 'the Saarschleife bend, the Volklingen ironworks, Lyoner sausage',
 'sacramento': 'farm-to-fork dining, Old Sacramento boardwalks, Napa an hour west',
 'salt lake city': 'powder skiing within an hour, floating in the Great Salt Lake, Temple Square',
 'san diego': 'fish tacos in Old Town, La Jolla sea lions, Balboa Park',
 'san francisco': 'sourdough and Dungeness crab, a cable car over the hills, redwoods at Muir Woods',
 'san jose': 'Vietnamese food on Story Road, the Winchester Mystery House, the Santa Cruz boardwalk',
 'santa barbara': 'Funk Zone wine tasting, Stearns Wharf, a boat to the Channel Islands',
 'sao paulo': 'the mortadella sandwich at Mercado Municipal, Japanese-Brazilian food in Liberdade, MASP',
 'seattle': 'oysters at Elliott\'s, Pike Place and the first Starbucks, Mount Rainier on a clear day',
 'seoul': 'Korean barbecue and soju, Gwangjang market, palaces free if you rent a hanbok',
 'shanghai': 'xiaolongbao, the Bund lit at night, the lanes of Tianzifang',
 'shenyang': 'northeastern barbecue, Mukden Palace, skiing at Qipanshan',
 'singapore': 'chili crab, hawker chicken rice for a few dollars, the Gardens by the Bay light show',
 'southampton': 'New Forest ponies, the Titanic exhibit at SeaCity, cream tea',
 'sydney': 'the Opera House, the Bondi to Coogee coastal walk, Blue Mountains',
 'taipei': 'beef noodle soup, Shilin night market, tea houses at Jiufen',
 'tokyo': 'breakfast at the Tsukiji outer market, teamLab, standing sushi bars',
 'toronto': "peameal bacon at St Lawrence Market, the CN Tower EdgeWalk, Niagara in a day",
 'trento': 'canederli and Trentino wine, the Dolomites an hour away, MUSE',
 'vancouver': 'sushi as good as Japan, the Stanley Park seawall by bike, the Grouse Grind',
 'venice': 'cicchetti and spritz standing up, a gondola through the back canals, glassblowing on Murano',
 'vilnius': 'cepelinai, the self-declared republic of Uzupis, baroque old town',
 'wellington': 'flat whites where they were invented, Weta Workshop, Te Papa',
 'yokohama': 'the biggest Chinatown in Japan, the Cup Noodles Museum, Minato Mirai at night',
 'the hague': 'Girl with a Pearl Earring up close, raw herring held by the tail, Scheveningen beach',
 'pittsburgh': "a Primanti Brothers sandwich with the fries inside, the Duquesne Incline at night, the Warhol Museum",
 'cleveland': 'the Rock and Roll Hall of Fame, West Side Market, Lake Erie sunsets',
 'boca raton': 'Atlantic beaches, sea turtle rehab at Gumbo Limbo, Mizner Park',
 'linkoping': 'Gamla Linkoping, fika, boats stepping down the Gota Canal locks',
 'sooke': 'swimming the Sooke Potholes, West Coast seafood, Vancouver Island rainforest',
 'auckland': 'Waiheke Island wineries by ferry, a fish and chips sunset at Mission Bay, Hobbiton two hours south',
}
def city_note(place):
    return CITY.get(city_key(place), '')

# ---------- country flags ----------
# place strings are free text from the upstream catalogue, so normalize the
# trailing country token to an ISO 3166-1 alpha-2 code the flag sprite knows.
CC={'argentina':'ar','australia':'au','barbados':'bb','belgium':'be','brazil':'br',
    'canada':'ca','china':'cn','cyprus':'cy','denmark':'dk','france':'fr','germany':'de',
    'greece':'gr','hungary':'hu','iceland':'is','india':'in','ireland':'ie','italy':'it',
    'japan':'jp','korea':'kr','republic of korea':'kr','south korea':'kr','lithuania':'lt',
    'luxembourg':'lu','malaysia':'my','mexico':'mx','morocco':'ma','netherlands':'nl',
    'the netherlands':'nl','new zealand':'nz','poland':'pl','scotland':'gb','singapore':'sg',
    'south africa':'za','spain':'es','sweden':'se','taiwan':'tw','uk':'gb',
    'united kingdom':'gb','united state':'us','united states':'us','usa':'us','vietnam':'vn'}
TW_CITY = re.compile(r'\b(taipei|hsinchu|kaohsiung|tainan|taichung|taoyuan|keelung)\b', re.I)
def simplify_place(place):
    """A Taiwanese venue is listed by its city alone, with no flag.

    The upstream catalogue writes these several ways and the suffix is not
    something this page needs to take a position on. The city is the useful
    part and is not in dispute.
    """
    m = TW_CITY.search(place or '')
    return m.group(1).title() if m else place

def flag(place):
    if TW_CITY.search(place or ''): return 

    if not place: return ''
    tail=place.split(',')[-1]
    tail=re.sub(r'\(.*?\)|/.*$|and online', ' ', tail, flags=re.I)
    tail=re.sub(r'[^a-z ]', ' ', tail.lower()).strip()
    tail=re.sub(r'\s+', ' ', tail)
    return CC.get(tail, '')

# ---------- areas ----------
# The area is a field id from src/data/domains.js. AI, security and the
# databases come whole from their CCF sub-areas; every other field takes
# only the venues named here, because CCF's architecture or multimedia
# lists hold far more than one field's worth. Pure bioinformatics (RECOMB,
# ISMB) is left out: the field here is biomedicine.
AREA_BY_SUB={'AI':'ai','SC':'security','DB':'ai'}
# CCF files WWW under 交叉/综合/新兴 because of its history, but everyone
# submitting to it treats it as a web-mining venue.
AREA_OVERRIDE={'WWW':'ai', 'SIGSPATIAL':'ai'}
BY_TITLE={
    'DAC':'eda','ICCAD':'eda','DATE':'eda','ASP-DAC':'eda',
    'ISCA':'eda','MICRO':'eda','HPCA':'eda','ASPLOS':'eda',
    'ICASSP':'audio','InterSpeech':'audio',
    'MICCAI':'biomed','BIBM':'biomed',
    'CogSci':'psych',
}
def area(sub, title):
    if title in EXTRA: return EXTRA[title]
    if title in BY_TITLE: return BY_TITLE[title]
    if title in AREA_OVERRIDE: return AREA_OVERRIDE[title]
    if sub in AREA_BY_SUB: return AREA_BY_SUB[sub]
    return 'science'

# The field's own ranking, where it has one, read the way people in the
# field use it rather than taken from a catalogue. AI has none here on
# purpose: CCF and CORE are the ranking there.
FIELD_RANK={
    'S&P':'Big Four','CCS':'Big Four','USENIX Security':'Big Four','NDSS':'Big Four',
    'DAC':'EDA top two','ICCAD':'EDA top two','DATE':'EDA, Europe','ASP-DAC':'EDA, Asia',
    'ISCA':'architecture top four','MICRO':'architecture top four',
    'HPCA':'architecture top four','ASPLOS':'architecture top four',
    'ICASSP':'SPS flagship','InterSpeech':'speech flagship','ISMIR':'MIR flagship',
    'MICCAI':'imaging flagship','AMIA':'informatics flagship',
    'CDC':'CSS flagship','ACC':'AACC flagship','ECC':'EUCA flagship',
    'PES GM':'PES flagship','PSCC':'most selective',
}

def tier_of(ccf, core):
    """1 = top by either table, 2 = strong by either, 3 = the rest."""
    if ccf=='A' or core=='A*': return 1
    if ccf=='B' or core=='A':  return 2
    return 3

def latest_link(confs):
    e=max(confs, key=lambda e: e.get('year',0)) if confs else {}
    return e.get('link','') or ''

def dstr(s):
    m=re.match(r'(\d{4}-\d{2}-\d{2})', str(s or '')); return m.group(1) if m else ''

EXTRA={'ICWSM':'ai'}
# Deadlines read off the venue's own site, overriding ccfddl.
#
# ccfddl rolls last year's date forward when a venue has announced nothing,
# and marks the result an estimate. Those estimates are sometimes badly out,
# and the failure is quiet: a venue shows as open on a date it did not
# choose. Checked against each site with scripts/check-deadlines.py, and
# every entry here was then read by eye on the page named in `source`, with
# the sentence it came from kept in `quote` so the claim can be rechecked.
#
# Only the main paper track. A commitment deadline, a journal track or an
# industry track is a different door and does not belong in this column.
DEADLINE_FIX = {
  'NAACL': {'date':'2026-10-12', 'label':'ARR Submission',
            'source':'https://2027.naacl.org/',
            'quote':'Main submission deadline (ARR) October 12, 2026',
            'checked':'2026-10-15'},
  'AAMAS': {'date':'2026-10-08', 'label':'Main track paper submission',
            'source':'https://warwick.ac.uk/fac/sci/dcs/aamas2027/',
            'quote':'Main Track: Abstract submission: 1 Oct 2026 Paper submission: 8 Oct 2026',
            'checked':'2026-10-15'},
  'ECIR':  {'date':'2026-10-12', 'label':'Full paper submission',
            'source':'https://ecir2027.co.uk/',
            'quote':'Full paper submission 12 Oct 2026',
            'checked':'2026-10-15'},
  'COLING':{'date':'2026-10-12', 'label':'ARR Submission',
            'source':'https://2027.coling-iccl.org/',
            'quote':'Important Dates ARR submission deadline Monday October 12, 2026',
            'checked':'2026-10-15'},
  'ICDAR': {'date':'2027-02-28', 'label':'Full paper deadline',
            'source':'https://icdar2027.org/important-dates',
            'quote':'Main Paper Deadlines for ICDAR 2027 Full Paper Deadline: February 28, 2027',
            'checked':'2026-10-15'},
}


def apply_deadline_fix(title, rounds):
    """Replace the main submission round with the date the venue published."""
    fix = DEADLINE_FIX.get(title)
    if not fix:
        return rounds
    # Every main-track round goes, not just the first. ICDAR carried two,
    # an estimate and a stale announced date, and replacing only one left the
    # stale one in front of the verified date. The site is the authority for
    # this track, so it supplies the whole of it.
    #
    # Commitment rounds survive untouched: those are a different door, open
    # only to papers that already have reviews, and the site's main-track
    # date says nothing about them.
    keep = [r for r in rounds if 'commitment' in (r.get('label') or '').lower()]
    # No abstract deadline is carried across. The one on the round being
    # replaced came from the same rolled estimate the site has just
    # contradicted, and an abstract date sorts ahead of its paper date, so
    # keeping it would have the row ordered by a guess: ICDAR sorted on a
    # 2027-01-31 abstract that nobody published, in front of the 2027-02-28
    # the site actually states. An abstract goes in DEADLINE_FIX by hand or
    # not at all.
    keep.append({'d': fix['date'], 'label': fix['label'], 'est': False,
                 'abs': fix.get('abstract', ''), 'fixed': fix['source']})
    keep.sort(key=lambda x: x['d'])
    return keep

out=[]
for sub in ['AI','SC','DB','MX','CG','HI','DS']:
    for f in sorted(glob.glob(f'ccf-deadlines/conference/{sub}/*.yml')):
        for c in yaml.safe_load(open(f)):
            r=c.get('rank') or {}; t=c['title']; d=(c.get('description') or '').strip()
            if sub in ('CG','HI','DS') and t not in EXTRA and t not in BY_TITLE: continue
            confs=c.get('confs') or []
            # Announced deadlines for the edition now in play, across every
            # published edition.
            #
            # The window reaches back, which it did not used to, and that was
            # the bug behind NAACL, AAMAS and ECIR all showing invented dates
            # in October 2026. ccfddl had every one of those deadlines
            # correctly recorded. They had simply passed within the last few
            # days, this filter dropped them for being in the past, and the
            # code below then rolled some *other* round forward to fill the
            # gap. A real date three days old was replaced by a guess, which
            # is the worst trade available.
            #
            # A date that has just passed is still the truth about this
            # cycle, and the page knows what to do with it: the live-date
            # rule rolls it forward itself and sinks the row. Half a year is
            # wide enough to hold a cycle that has just closed and narrow
            # enough to exclude the previous edition.
            upcoming=[]
            for ed in confs:
                for tl in (ed.get('timeline') or []):
                    ds=dstr(tl.get('deadline'))
                    if ds and datetime.date.fromisoformat(ds) >= TODAY - ANNOUNCED_GRACE:
                        upcoming.append((ds, ed.get('year'), ed.get('link',''),
                                         dstr(tl.get('abstract_deadline')),
                                         (tl.get('comment') or '').strip()))
            upcoming.sort()
            # Every round the venue runs, not just the soonest. The reference
            # edition is whichever recent one publishes the most rounds; a
            # round whose date has passed is rolled forward like any other
            # estimate, so a two-round venue always shows two.
            yrs=sorted({e.get('year') for e in confs if e.get('year')})
            gaps=[b-a for a,b in zip(yrs, yrs[1:])] if len(yrs)>1 else []
            period=collections.Counter(gaps).most_common(1)[0][0] if gaps else 1
            period=max(1, min(period, 4))
            # Only editions that actually carry a date. MICCAI publishes two
            # future editions with TBD timelines, which would otherwise be
            # picked as the reference and leave the venue with no rounds.
            dated_eds=[e for e in confs
                       if any(dstr(t.get('deadline')) for t in (e.get('timeline') or []))]
            recent=sorted(dated_eds, key=lambda e: e.get('year',0))[-2:]
            ref_rounds=[]
            for ed in recent:
                rs=[(dstr(t.get('deadline')), (t.get('comment') or '').strip(),
                     dstr(t.get('abstract_deadline')))
                    for t in (ed.get('timeline') or []) if dstr(t.get('deadline'))]
                seen=set(); rs=[r for r in rs if not (r[0] in seen or seen.add(r[0]))]
                if len(rs) > len(ref_rounds): ref_rounds=rs
            rounds=[]
            for ds, label, abs_ds in ref_rounds:
                d0=datetime.date.fromisoformat(ds)
                if d0 >= TODAY:
                    rounds.append({'d':ds,'label':label,'est':False,'abs':abs_ds})
                    continue
                # Keep stepping by the venue's own period until the date is
                # ahead of today. Every venue gets a date, however far out.
                for k in range(1, 13):
                    bump=period*k
                    try: cand=d0.replace(year=d0.year+bump)
                    except ValueError: cand=d0.replace(year=d0.year+bump, day=28)
                    if cand >= TODAY:
                        # The abstract deadline rolls with its paper deadline,
                        # keeping the gap that the venue actually runs.
                        a = ''
                        if abs_ds:
                            a0 = datetime.date.fromisoformat(abs_ds)
                            a = (cand - (d0 - a0)).isoformat()
                        rounds.append({'d':cand.isoformat(),'label':label,'est':True,
                                       'from':ds,'abs':a})
                        break
            # Announced beats estimated. The moment a conference publishes a
            # round, that date replaces the rolled one. Matching is by round
            # label first, then by proximity, because an announced date often
            # moves a few weeks from where last year's fell.
            norm_lab=lambda x: re.sub(r'[^a-z0-9]', '', (x or '').lower())
            real=[]
            for u_ds, u_yr, u_lk, u_ab, u_lab in upcoming:
                if any(r['d']==u_ds for r in real): continue
                real.append({'d':u_ds,'label':u_lab,'est':False,
                             'year':u_yr,'link':u_lk,'abs':u_ab})
            real_labels={norm_lab(r['label']) for r in real if r['label']}
            real_days=sorted(datetime.date.fromisoformat(r['d']) for r in real)
            # Proximity window scales with how close together the rounds sit.
            # VLDB runs monthly, so a flat 45 days would swallow its neighbours.
            ref_days=sorted(datetime.date.fromisoformat(r[0]) for r in ref_rounds)
            min_gap=min((b-a).days for a, b in zip(ref_days, ref_days[1:])) if len(ref_days)>1 else 365
            window=max(10, min(45, min_gap // 2))
            keep=[]
            for e in rounds:
                if norm_lab(e['label']) and norm_lab(e['label']) in real_labels: continue
                ed_=datetime.date.fromisoformat(e['d'])
                if any(abs((ed_-rd).days) <= window for rd in real_days): continue
                # An estimate exists to fill out the edition that is already
                # under way. Once it lands more than a year past the first
                # announced round it belongs to a later edition, and the
                # announced rounds are the authority on how many there are.
                if real_days and (ed_ - real_days[0]).days > 365: continue
                # An estimate never outranks an announced date. ICDAR had its
                # 2027 conference track announced for 2027-02-20 and still led
                # with 2026-11-14, which was its *journal* track rolled a year
                # forward. A guess that sorts ahead of a fact decides the row.
                if real_days and ed_ < real_days[0]: continue
                keep.append(e)
            keep.sort(key=lambda x: x['d'])
            cap=max(len(ref_rounds), len(real))
            rounds = real + keep[:max(0, cap - len(real))]
            rounds.sort(key=lambda x: x['d'])
            rounds = apply_deadline_fix(t, rounds)
            # The soonest round is the headline date, whether it is published
            # or rolled forward.
            nxt=None; est=False
            if rounds:
                r0=rounds[0]
                if r0['est']:
                    src=r0.get('from','')
                    base=next((e.get('year') for e in confs
                               if any(dstr(t.get('deadline'))==src for t in (e.get('timeline') or []))), None)
                    bumped=datetime.date.fromisoformat(r0['d']).year - datetime.date.fromisoformat(src).year if src else 1
                    nxt=(r0['d'], (base+bumped) if base else None, latest_link(confs), '')
                    est=True
                else:
                    nxt=(r0['d'], r0.get('year'), r0.get('link',''), r0.get('abstract',''))
            latest=max(confs, key=lambda e: e.get('year',0)) if confs else {}
            # Where and when the meeting is only belongs to the edition the
            # next deadline points at. Carrying last year's city over to an
            # estimated date is simply wrong: the venue moves every year.
            this_ed=next((e for e in confs if e.get('year')==(nxt[1] if nxt else None)), {})
            # Count rounds only within the edition being shown. Taking the max
            # across every edition flagged AAAI, whose old NeurIPS fast track
            # looks like a second cycle but no longer exists.
            ref = next((e for e in confs if e.get('year')==(nxt[1] if nxt else None)), latest if confs else {})
            tl_ref = ref.get('timeline') or []
            labels=[(t.get('comment') or '').strip() for t in tl_ref]
            deadlines_in_ref={dstr(t.get('deadline')) for t in tl_ref if dstr(t.get('deadline'))}
            cycles=len(deadlines_in_ref) if len(deadlines_in_ref)>1 else 1
            roundLabels=[l for l in labels if l] if cycles>1 else []
            hist=sorted(csc_rates.get(t, {}).items())
            subs=sorted(csc_subs.get(t, {}).items())
            rsrc='csc' if t in csc_rates else ''
            off=official(t,d); mirror=canon(r.get('core','N'))
            out.append({
                'title':t, 'desc':d, 'area':area(sub,t), 'sub':sub, 'frank':FIELD_RANK.get(t,''),
                'ccf':r.get('ccf','N'), 'core': off if off is not None else mirror,
                'coreVerified': off is not None,
                'nextDeadline': nxt[0] if nxt else '',
                'nextYear': nxt[1] if nxt else None,
                'nextAbstract': nxt[3] if nxt else '',
                'estimated': est,
                'estFrom': (rounds[0].get('from','') if rounds else '') if est else '',
                'rounds': rounds,
                'dblp': DBLP_FIX.get(t, c.get('dblp','')),
                'csr': CSR.get(DBLP_FIX.get(t, c.get('dblp','')), ''),
                'edition': ordinal_for(t, nxt[1] if nxt else None, period),
                'best': BEST.get(t,''),
                'link': (nxt[2] if nxt else latest.get('link','')) or '',
                'date': this_ed.get('date','') or '', 'place': simplify_place(this_ed.get('place','') or ''),
                'cc': flag(this_ed.get('place','')),
                'city': city_note(this_ed.get('place','')),
                'cycles': cycles, 'roundLabels': roundLabels,
                'proceedings': 'full',
                'rates': [{'y':y,'r':v} for y,v in hist],
                'subs': [{'y':y,'n':n} for y,n in subs],
                'rateSrc': rsrc, 'rateSlug': csc_slug.get(t,''),
            })
json.dump(out, open('built.json','w'))
print('conferences:', len(out))
print('with a FUTURE deadline:', sum(1 for c in out if c['nextDeadline']))
print('with acceptance history:', sum(1 for c in out if c['rates']))
print('areas:', dict(collections.Counter(c['area'] for c in out)))
print('multi-cycle venues:', [(c['title'],c['cycles']) for c in out if c['cycles']>1])

# ---------- hand-maintained: venues the ranking tables simply do not cover ----------
# CCF and CORE only index conferences with archival proceedings, so society
# meetings and brand-new venues fall through. Edit this list by hand.
NOTABLE=[
 # Society meetings: abstract- or minisymposium-driven, no archival
 # proceedings, so neither CCF nor CORE can index them at all. lastDeadline
 # is the abstract deadline, read off each society's own page, and period is
 # how many years apart the editions run.
 {'title':'INFORMS Annual Meeting','desc':'Institute for Operations Research and the Management Sciences',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-05-20','period':1,
  'date':'October 24-27, 2027','place':'Seattle, Washington, USA','estIsForDate':True,
  'note':'The main annual gathering for operations research and analytics, around 6,000 attendees. The 2027 meeting is in Seattle; its abstract deadline is not announced, so the date shown is last year\'s rolled forward.',
  'field':'operations research','kind':'flagship, yearly','why':'optimization and analytics at scale',
  'link':'https://meetings.informs.org/'},
 {'title':'SIAM MDS','desc':'SIAM Conference on Mathematics of Data Science',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-05-18','period':2,
  'date':'November 16-20, 2026','place':'Salt Lake City, Utah, USA',
  'note':'Biennial, even years. Where the mathematical side of data science meets. The date shown is the abstract deadline.',
  'field':'data science theory','kind':'biennial, even years','why':'the mathematics under data science',
  'link':'https://www.siam.org/conferences-events/siam-conferences/mds26/'},
 {'title':'SIAM CSE','desc':'SIAM Conference on Computational Science and Engineering',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-08-25','period':2,
  'date':'February 22-26, 2027','place':'Pittsburgh, Pennsylvania, USA',
  'note':'Biennial, odd years. The largest SIAM meeting and the main venue for scientific machine learning. The date shown is the abstract deadline.',
  'field':'computational science','kind':'biennial, odd years','why':'scientific machine learning',
  'link':'https://www.siam.org/conferences-events/siam-conferences/cse27/'},
 {'title':'SIAM UQ','desc':'SIAM Conference on Uncertainty Quantification',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2025-09-22','period':2,
  'note':'Biennial, even years. The central applied-maths meeting for UQ. UQ26 ran March 2026 in Minneapolis and UQ28 is not yet announced. The date shown is the abstract deadline.',
  'field':'uncertainty quantification','kind':'biennial, even years','why':'UQ methods',
  'link':'https://www.siam.org/conferences-events/siam-conferences/uq26/'},
 {'title':'SIAM Annual Meeting','desc':'SIAM Annual Meeting (AN)',
  'area':'Society meetings','proceedings':'none','period':1,
  'date':'August 7-11, 2028','place':'Minneapolis, Minnesota, USA',
  'note':'All of applied mathematics in one room. There is no AN27: ICIAM takes its place in 2027. AN28 is in Minneapolis, and SIAM plans to post its call in September 2027.',
  'field':'applied mathematics','kind':'yearly, skips ICIAM years','why':'the whole field in one room',
  'link':'https://www.siam.org/conferences-events/siam-conferences/an28/'},
 {'title':'SIAM OP','desc':'SIAM Conference on Optimization',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2025-11-13','period':3,
  'note':'Triennial. OP26 ran June 2026 in Edinburgh, so the next edition falls around 2029. The date shown is the abstract deadline.',
  'field':'optimization','kind':'triennial','why':'optimization theory',
  'link':'https://www.siam.org/conferences-events/siam-conferences/op26/'},
 {'title':'ICIAM','desc':'International Congress for Industrial and Applied Mathematics',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-12-07','period':4,
  'date':'July 12-16, 2027','place':'The Hague, Netherlands',
  'note':'Every four years, the field-wide congress of applied mathematics, around 4,000 participants. The date shown is the abstract deadline, which is published.',
  'field':'applied mathematics','kind':'every four years','why':'field-wide congress',
  'link':'https://iciam2027.org/'},

 # --- added 2026-10-11, each checked against the society's own site ---
 {'title':'APS Global Physics Summit','desc':'American Physical Society Global Physics Summit',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-10-22','period':1,
  'date':'April 11-16, 2027','place':'Atlanta, Georgia, USA',
  'note':'The largest physics meeting in the world, around 14,000 attendees and over 10,000 abstracts a year. Formed by merging the March and April meetings, so the name March Meeting is retired. The date shown is the contributed abstract deadline.',
  'field':'physics','kind':'flagship, yearly','why':'physics-informed modelling',
  'link':'https://summit.aps.org/attend/abstracts'},
 {'title':'SfN','desc':'Society for Neuroscience Annual Meeting','area':'Society meetings',
  'proceedings':'none','lastDeadline':'2026-06-11','period':1,
  'date':'October 23-27, 2027','place':'Chicago, Illinois, USA',
  'note':'The largest neuroscience meeting worldwide, 21,093 attendees in 2025, poster driven. Abstracts appear only in the online meeting planner, and preprints are explicitly allowed. The date shown is the regular abstract deadline, with late breaking abstracts closing in September.',
  'field':'neuroscience','kind':'flagship, yearly','why':'the largest neuroscience meeting',
  'estIsForDate':True,
  'link':'https://www.sfn.org/meetings/neuroscience-2026/general-information/dates-and-deadlines'},
 {'title':'COSYNE','desc':'Computational and Systems Neuroscience','area':'Society meetings',
  'proceedings':'none','lastDeadline':'2026-10-18','period':1,
  'date':'March 11-14, 2027','place':'Montreal, Quebec, Canada',
  'note':'The main venue for computational and theoretical neuroscience, with double blind review of two page abstracts and heavy dynamical systems content. Its own call states the accepted summaries are not full length proceedings and do not prevent later publication.',
  'field':'computational neuroscience','kind':'flagship, yearly','why':'dynamical systems in neural data',
  'link':'https://www.cosyne.org/abstracts'},
 # --- added 2026-10-18: psychology, neuroscience, sleep and dreams.
 # Every date below was read off the society's own 2027 page on 2026-10-18.
 # Named in full: the physics card below is also an APS, for a different
 # society, and two bare acronyms in one grid is a trap.
 {'title':'APS Annual Convention','desc':'Association for Psychological Science',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-12-01','period':1,
  'date':'May 27-30, 2027','place':'Seattle, Washington, USA',
  'field':'psychology','kind':'flagship, yearly','why':'the research side of psychology, broadly',
  'note':'The main convention of the research wing of psychology, as distinct from the clinically oriented APA. Submissions are abstracts for posters and symposia, nothing archival. The date shown is the submission deadline, 5pm Eastern.',
  'link':'https://www.psychologicalscience.org/conventions/2027-aps-annual-convention'},
 {'title':'APA Convention','desc':'American Psychological Association Annual Convention',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-01-14','period':1,
  'date':'August 12-14, 2027','place':'San Francisco, California, USA','estIsForDate':True,
  'field':'psychology','kind':'flagship, yearly','why':'the practice side, and the larger of the two',
  'note':'The largest gathering of psychologists in the world, and the professional counterpart to the research-led APS convention: divisions, practice, policy and continuing education alongside the science. Proposals go to the divisions. The 2027 call has not opened, so the date shown is the 2026 deadline rolled a year forward.',
  'link':'https://convention.apa.org/proposals'},
 {'title':'World Sleep','desc':'World Sleep Congress',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2027-05-15','period':2,
  'date':'September 10-15, 2027','place':'Montreal, Quebec, Canada',
  'field':'sleep and circadian','kind':'biennial, odd years','why':'the international counterpart to SLEEP',
  'note':'The World Sleep Society congress, held every two years and the international counterpart to the American SLEEP meeting. Four doors, all published: symposium proposals and fast-track abstracts close on 20 January 2027, oral abstracts on 15 May and posters on 15 July. The date shown is the oral abstract deadline.',
  'link':'https://worldsleepcongress.com/'},
 {'title':'Psychonomics','desc':'Psychonomic Society Annual Meeting',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-06-01','period':1,
  'field':'cognitive psychology','kind':'flagship, yearly','why':'how the mind works, by behavioral methods',
  'note':'The premier international meeting for cognitive psychology, close to 2,000 people from more than 35 countries and over 1,000 presentations across three days, focused on fundamental questions studied behaviorally. The 68th meeting is at the Sheraton New Orleans. The date shown is the last call rolled a year forward, since the 2027 call has not opened.',
  'date':'November 18-21, 2027',
  'place':'New Orleans, Louisiana, USA',
  'estIsForDate':True,
  'link':'https://www.psychonomic.org/page/futuremeetings'},
 {'title':'OHBM','desc':'Organization for Human Brain Mapping Annual Meeting',
  'area':'Society meetings','proceedings':'none','period':1,
  'date':'June 26-30, 2027','place':'Toronto, Ontario, Canada',
  'field':'brain imaging','kind':'flagship, yearly','why':'neuroimaging methods and their statistics',
  'note':'The meeting for human neuroimaging, where fMRI, MEG and EEG methodology is argued out. Its 2027 page gives December 2026 for the content submission deadline without naming a day, which is why no date is shown here rather than a guessed one.',
  'link':'https://www.humanbrainmapping.org/ohbm-2027/'},
 {'title':'CCN','desc':'Cognitive Computational Neuroscience',
  'area':'Society meetings','proceedings':'optin','lastDeadline':'2027-02-01','period':1,
  'field':'computational neuroscience','kind':'yearly','why':'where neuroscience and machine learning meet',
  'note':'Built around the overlap between neural computation and machine learning, which makes it the closest of these meetings to this site. Two tracks: a two page contribution for presentation, due 1 April 2027, or an eight page paper with a competitive acceptance rate published with a DOI in the CCN Proceedings, whose abstract is due 1 February and whose full paper is due 4 February. The date shown is the first of those. The 10th edition is at the Edinburgh International Conference Centre.',
  'date':'July 26-29, 2027',
  'place':'Edinburgh, United Kingdom',
  'link':'https://2027.ccneuro.org/dates-and-deadlines/'},
 {'title':'ASSC','desc':'Association for the Scientific Study of Consciousness',
  'area':'Society meetings','proceedings':'none','period':1,
  'date':'June 16-19, 2027','place':'Beijing, China',
  'field':'consciousness','kind':'flagship, yearly','why':'consciousness as an empirical question, dreaming included',
  'note':'The 30th annual meeting, at the Beijing International Convention Center, drawing cognitive science, neuroscience, medicine and philosophy. Dreaming sits inside its remit as a state of consciousness. The organizers say details are still to come, so no submission date is published yet.',
  'link':'https://theassc.org/assc-30/'},
 {'title':'SLEEP','desc':'APSS Annual Meeting, AASM and SRS',
  'area':'Society meetings','proceedings':'abstracts','lastDeadline':'2026-12-07','period':1,
  'date':'June 6-9, 2027','place':'Denver, Colorado, USA',
  'field':'sleep and circadian','kind':'flagship, yearly','why':'where sleep and dream data is presented',
  'note':'The joint meeting of the American Academy of Sleep Medicine and the Sleep Research Society, over 6,000 attendees and more than 1,500 abstracts, covering clinical sleep medicine and circadian research together. Accepted abstracts are published in a supplement to the journal SLEEP. The date shown is the abstract deadline, 11:59pm Eastern.',
  'link':'https://www.sleepmeeting.org/call-for-abstracts/'},
 {'title':'IASD','desc':'International Association for the Study of Dreams',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-12-18','period':1,
  'date':'May 29 - June 2, 2027','place':'Atlanta, Georgia, USA',
  'field':'dream research','kind':'flagship, yearly','why':'the one meeting given over entirely to dreaming',
  'note':'The 44th annual conference, five days and over 100 presentations from as many as 20 countries, and the only international meeting devoted wholly to dreams. It mixes dream science with clinical practice, lucid dreaming and the arts, so it is a wider room than the other cards here. The date shown is the deadline for presentation proposals.',
  'link':'https://iasdconferences.org/2027/'},

 # --- added 2026-10-17, checked against the society's own pages ---
 {'title':'CNS','desc':'Cognitive Neuroscience Society Annual Meeting','area':'Society meetings',
  'proceedings':'abstracts','lastDeadline':'2026-11-03','period':1,
  'date':'March 20-23, 2027','place':'Boston, Massachusetts, USA',
  'note':'Where cognitive neuroscience meets psychology and computational modelling, four days built around poster sessions, invited symposia and award lectures. The 33rd meeting ran in Vancouver in March 2026. Abstracts are 250 words and are published by default in the Proceedings of the Annual Meeting of the Cognitive Neuroscience Society, so this is not a no-proceedings venue, but the proceedings are the abstracts themselves. The Sketchpad Series takes work in progress and is left out of them. Submission requires society membership. The date shown is the poster abstract deadline, which the society says will not be extended.',
  'field':'cognitive neuroscience','kind':'yearly','why':'cognition, modelling and imaging',
  'link':'https://www.cogneurosociety.org/submit-a-poster/'},
 {'title':'NetSci','desc':'International School and Conference on Network Science',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-12-01','period':1,
  'note':'The flagship conference of the Network Science Society and the closest society meeting to graph machine learning. One page abstracts. Hosted by TU Dresden, with satellites and the school on 17 and 18 May, whose own proposals closed on 15 November 2026. The date shown is the abstract deadline.',
  'field':'network science','kind':'flagship, yearly','why':'the closest society meeting to graph ML',
  'date':'May 17-21, 2027',
  'place':'Dresden, Germany',
  'link':'https://netsci2027.github.io/'},
 # Control theory, which neither CCF nor CORE indexes because both are
 # computing catalogues. The absence is not a judgement on the venue, so
 # both ranks read n/a rather than being invented. Dates and both deadlines
 # read off cdc2027.ieeecss.org on 2026-10-17.
 {'title':'CDC','desc':'IEEE Conference on Decision and Control',
  'area':'Control','proceedings':'full','lastDeadline':'2027-03-17','period':1,
  'date':'December 14-17, 2027','place':'Lisbon, Portugal','badge':'control',
  'dblp':'cdc','cycles':2,
  'roundLabels':['L-CSS and CDC','CDC only'],
  'rounds':[{'d':'2027-03-17','label':'L-CSS and CDC','est':False},
            {'d':'2027-03-31','label':'CDC only','est':False}],
  'note':'The main conference of the IEEE Control Systems Society and the premier venue of the field, 66th edition, with full archival proceedings. Papers may be submitted jointly to L-CSS, the society letters journal, on the earlier of the two deadlines. Neither CCF nor CORE indexes it, because both catalogue computing rather than control.',
  'link':'https://cdc2027.ieeecss.org/'},
 # The rest of control's conference calendar. Dates read off each venue's
 # own site on 2026-10-19.
 {'title':'ACC','desc':'American Control Conference',
  'area':'Control','proceedings':'full','lastDeadline':'2026-09-11','period':1,
  'date':'July 7-9, 2027','place':'Philadelphia, Pennsylvania, USA','badge':'control',
  'dblp':'amcc','cycles':2,
  'roundLabels':['L-CSS and ACC','ACC only'],
  'rounds':[{'d':'2026-09-11','label':'L-CSS and ACC','est':False},
            {'d':'2026-10-02','label':'ACC only','est':False}],
  'note':'The American Automatic Control Council conference, the US counterpart to CDC, with full archival proceedings on IEEE Xplore. Eight pages at submission, six in the final version. As at CDC, a paper can go to L-CSS and be presented here, on the earlier deadline. The date shown for ACC only is the firm deadline.',
  'link':'https://acc2027.a2c2.org/'},
 {'title':'ECC','desc':'European Control Conference',
  'area':'Control','proceedings':'full','lastDeadline':'2026-10-31','period':1,
  'date':'July 13-16, 2027','place':'Brussels, Belgium','badge':'control',
  'dblp':'eucc',
  'note':'The conference of the European Control Association, 25th edition, at the UCLouvain campus in Woluwe. Full archival proceedings on IEEE Xplore.',
  'link':'https://ecc27.euca-ecc.org/'},
 {'title':'L4DC','desc':'Learning for Dynamics and Control Conference',
  'area':'Control','proceedings':'full','lastDeadline':'2026-11-13','period':1,
  'date':'June 16-18, 2027','place':'Stockholm, Sweden','badge':'control',
  'dblp':'l4dc',
  'note':'Where machine learning and control meet, run since 2019, with proceedings in PMLR. Smaller and more selective than CDC or ACC. The 2027 edition is at KTH and reviews on OpenReview for the first time.',
  'link':'https://l4dc2027.control.ee.ethz.ch/'},

 {'title':'CompleNet','desc':'International Conference on Complex Networks',
  'area':'Society meetings','proceedings':'optin','lastDeadline':'2026-10-17','period':1,
  'field':'network science','kind':'yearly','why':'plenary only, with a Springer paper track',
  'note':'Smaller and more personal than NetSci, running since 2009, with every talk in a single plenary session rather than parallel tracks. Two kinds of submission: an abstract for presentation only, or a paper that goes into the Springer conference volume. The 18th edition is at the University of Rochester. The date shown is the abstract and paper deadline, Anywhere on Earth.',
  'date':'March 9-12, 2027',
  'place':'Rochester, New York, USA',
  'link':'https://complenet.github.io/index.html'},

 {'title':'Complex Systems (CCS)','desc':'Conference on Complex Systems','area':'Society meetings',
  'proceedings':'none','lastDeadline':'2026-05-15','period':1,
  'date':'September 17-24, 2027','place':'Wroclaw, Poland',
  'note':'The annual meeting of the Complex Systems Society, covering networks, dynamical systems and complexity applied to epidemics, traffic and infrastructure. One page extended abstracts. Not to be confused with ACM CCS in security.',
  'field':'complex systems','kind':'flagship, yearly','why':'networks, epidemics and traffic',
  'estIsForDate':True,
  'link':'https://cssociety.org/ccs'},
 {'title':'IC2S2','desc':'International Conference on Computational Social Science',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-03-03','period':1,
  'note':'The main venue for computational social science, heavy on network analysis and large scale data methodology. Its call states submissions are non archival, so work published or in preparation elsewhere may be submitted.',
  'field':'computational social science','kind':'flagship, yearly','why':'non-archival, network heavy',
  'link':'https://easychair.org/cfp/IC2S2_2026'},
 {'title':'Sunbelt','desc':'INSNA Social Networks Conference','area':'Society meetings',
  'proceedings':'none','lastDeadline':'2026-02-27','period':1,
  'note':'The annual conference of the International Network for Social Network Analysis and the oldest continuing venue for social network analysis, where much of the methodology now used in network science originated.',
  'field':'social networks','kind':'flagship, yearly','why':'where network methodology began',
  'date':'June 21-26, 2027',
  'place':'Montreal, Quebec, Canada',
  'estIsForDate':True,
  'link':'https://www.insna.org/events/sunbelt-2027-montreal'},
 {'title':'JSM','desc':'Joint Statistical Meetings','area':'Society meetings',
  'proceedings':'optin','lastDeadline':'2027-02-01','period':1,
  'note':'The largest annual gathering of North American statisticians, over 5,000 attendees from 52 countries, run jointly by the ASA, IMS and allied societies. Presentation is abstract only, but the ASA also publishes an opt-in, non peer reviewed JSM Proceedings volume, which is why this one is not a clean no-proceedings case. Topic-contributed session proposals close earlier, on 10 December 2026. The date shown is the abstract deadline.',
  'field':'statistics','kind':'flagship, yearly','why':'statistical methodology',
  'link':'https://ww2.amstat.org/meetings/jsm/2027/submissions.cfm'},
 {'title':'JMM','desc':'Joint Mathematics Meetings','area':'Society meetings',
  'proceedings':'none','lastDeadline':'2026-09-15','period':1,
  'date':'January 12-15, 2027','place':'Chicago, Illinois, USA',
  'note':'The largest mathematics meeting in the world and the main annual US gathering across pure and applied mathematics, hosted by the AMS with partner societies. The date shown is the general abstract deadline.',
  'field':'mathematics','kind':'flagship, yearly','why':'breadth across pure and applied',
  'link':'https://meetings.ams.org/math/jmm2027/cfp.cgi'},
 {'title':'EURO','desc':'European Conference on Operational Research','area':'Society meetings',
  'proceedings':'none','lastDeadline':'2027-02-28','period':1,
  'date':'July 11-14, 2027','place':'Athens, Greece',
  'note':'The flagship annual conference of the Association of European Operational Research Societies, the European counterpart to the INFORMS Annual Meeting. Abstract only, organized into streams.',
  'field':'operations research','kind':'flagship, yearly','why':'the European counterpart to INFORMS',
  'link':'https://euro2027athens.com/'},
 {'title':'AGU','desc':'American Geophysical Union Annual Meeting','area':'Society meetings',
  'proceedings':'none','lastDeadline':'2026-08-05','period':1,
  'date':'December 7-11, 2026','place':'San Francisco, California, USA',
  'note':'The largest Earth and space science meeting, 25,000 or more attendees from over 100 countries. AGU26 runs 7 to 11 December 2026 in San Francisco and its late-breaking abstracts close on 20 October 2026. The date shown is the regular abstract deadline for the cycle after it.',
  'field':'Earth and space science','kind':'flagship, yearly','why':'geoscience data at scale',
  'link':'https://www.agu.org/annual-meeting'},
 {'title':'Epidemics','desc':'International Conference on Infectious Disease Dynamics',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2027-06-18','period':2,
  'date':'December 5-8, 2027','place':'Singapore',
  'note':'The main international meeting for infectious disease modelling and epidemic dynamics, directly relevant to network based epidemic models. Run by a publisher rather than a learned society, which makes it the odd one out in this list.',
  'field':'epidemic modelling','kind':'biennial','why':'network models of disease spread',
  'link':'https://www.elsevier.com/events/conferences/international-conference-on-infectious-disease-dynamics'},

 # Full proceedings, but too new or too far outside the catalogues to carry
 # a CCF or CORE rank. lastDeadline is the most recent published deadline;
 # the page rolls it forward and marks the result as an estimate.
 {'title':'COLM', 'equivalent':'CCF B / CORE A','desc':'Conference on Language Modeling','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Full proceedings. Founded 2024, too new for either ranking table.',
  'lastDeadline':'2026-03-31','link':'https://colm.cc/'},
 {'title':'MLSys', 'equivalent':'CCF B / CORE A','desc':'Conference on Machine Learning and Systems','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Full proceedings. Unranked by both CCF and CORE despite being the main ML-systems venue.',
  'lastDeadline':'2025-10-30','link':'https://mlsys.org/'},
 {'title':'AMIA', 'equivalent':'CCF B / CORE A','badge':'informatics','desc':'AMIA Annual Symposium','area':'Health & Bio',
  'proceedings':'full','note':'Full proceedings, indexed in PubMed. The central US biomedical-informatics meeting.',
  'lastDeadline':'2026-03-10','link':'https://amia.org/education-events/amia-annual-symposium'},
 {'title':'ASONAM', 'ccfManual':'C','coreManual':'B','desc':'IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Ranked CCF C / CORE B, so below this page\'s usual bar, but it is the dedicated social-network analysis venue.',
  'lastDeadline':'2026-05-10','link':'https://asonam.cpsc.ucalgary.ca/2026/CFP.php'},

 # ---- Added 2026-10-19 with the per-field tabs. Every date below was read
 # off the venue's own site that day; "tentative" is the venue's word.
 # Music & Audio
 {'title':'ISMIR','desc':'International Society for Music Information Retrieval Conference',
  'area':'audio','proceedings':'full','lastDeadline':'2026-04-27','period':1,
  'date':'November 8-12, 2026','place':'Abu Dhabi, United Arab Emirates','badge':'MIR','dblp':'ismir',
  'note':'The music-information-retrieval community\'s own conference. Papers are 6 pages plus references, double-blind, published open access. The 2027 edition is not announced yet.',
  'link':'https://ismir2026.ismir.net/'},
 {'title':'DCASE','desc':'Detection and Classification of Acoustic Scenes and Events Workshop',
  'area':'audio','proceedings':'full','lastDeadline':'2026-07-12','period':1,
  'date':'October 27-29, 2026','place':'Medford, Massachusetts, USA','badge':'audio','dblp':'dcase',
  'note':'The workshop of the DCASE challenge, 4 pages plus a page of references, open proceedings. The 2027 workshop is not announced yet.',
  'link':'https://dcase.community/workshop2026'},
 {'title':'WASPAA','desc':'IEEE Workshop on Applications of Signal Processing to Audio and Acoustics',
  'area':'audio','proceedings':'full','lastDeadline':'2027-04-21','period':2,
  'date':'September 19-22, 2027','place':'Levi, Finland','badge':'audio','dblp':'waspaa',
  'rounds':[{'d':'2027-04-21','abs':'2027-04-14','label':'tentative','est':False}],
  'note':'Every other year, small and single track, 4 pages plus references. The first WASPAA held in Europe; it spent most of its history at Mohonk in New York. The dates are the venue\'s tentative schedule.',
  'link':'https://waspaa.com/'},
 # Biomedical
 {'title':'CHIL','desc':'AHLI Conference on Health, Inference, and Learning',
  'area':'biomed','proceedings':'full','lastDeadline':'2027-02-03','period':1,
  'date':'June 28-30, 2027','place':'Chicago, Illinois, USA','badge':'ML for health','dblp':'chil',
  'note':'Machine learning for health, 8 to 10 pages, double-blind on OpenReview, proceedings in PMLR. One co-author per paper reviews three. Create OpenReview accounts for every author by 15 January. Meeting dates are tentative.',
  'link':'https://chil.ahli.cc/'},
 {'title':'ML4H','desc':'Machine Learning for Health Symposium',
  'area':'biomed','proceedings':'full','lastDeadline':'2026-09-10','period':1,
  'date':'December 6-7, 2026','place':'Sydney, Australia','badge':'ML for health','dblp':'ml4h',
  'note':'Formerly a NeurIPS workshop, now a standalone symposium. Two tracks: Proceedings, 8 pages and archival in PMLR, and Findings, 4 pages and non-archival.',
  'link':'https://ml4h.ahli.cc/'},
 {'title':'MIDL','desc':'Medical Imaging with Deep Learning',
  'area':'biomed','proceedings':'full','lastDeadline':'2026-12-04','period':1,
  'date':'July 14-16, 2027','place':'Porto, Portugal','badge':'imaging','dblp':'midl',
  'rounds':[{'d':'2026-12-04','abs':'2026-11-30','label':'full papers','est':False}],
  'note':'Full papers archival in PMLR, 10 pages in the main track; a new clinical-translation track takes 14 and does not require novelty. Short papers come later and are not archived.',
  'link':'https://2027.midl.io/'},
 {'title':'ISBI','desc':'IEEE International Symposium on Biomedical Imaging',
  'area':'biomed','proceedings':'full','lastDeadline':'2026-10-26','period':1,
  'date':'May 25-28, 2027','place':'Lausanne, Switzerland','badge':'imaging','dblp':'isbi',
  'rounds':[{'d':'2026-10-26','label':'4-page paper','est':False},
            {'d':'2027-02-01','label':'1-page abstract, poster only','est':False}],
  'note':'Four-page papers, single-blind, presented in person or withdrawn. Deadlines are 11:59pm US Eastern, not Anywhere on Earth. One-page abstracts are posters and are not in the proceedings.',
  'link':'https://biomedicalimaging.org/2027/'},
 # Time series
 {'title':'ISF','desc':'International Symposium on Forecasting',
  'area':'ts','proceedings':'none','lastDeadline':'2027-03-07','period':1,
  'date':'June 20-23, 2027','place':'Paphos, Cyprus',
  'field':'forecasting','kind':'flagship, yearly','why':'the forecasting community',
  'note':'The International Institute of Forecasters\' yearly meeting, 47th edition. One abstract per person, 350 words, presented in person. The institute\'s journal is the International Journal of Forecasting.',
  'link':'https://isf.forecasters.org/'},
 # Dynamical systems
 {'title':'SIAM DS','desc':'SIAM Conference on Applications of Dynamical Systems',
  'area':'dynsys','proceedings':'none','lastDeadline':'2026-11-23','period':2,
  'date':'May 23-27, 2027','place':'Atlanta, Georgia, USA',
  'rounds':[{'d':'2026-10-26','label':'minisymposium proposal','est':False},
            {'d':'2026-11-23','label':'talk and poster abstracts','est':False}],
  'field':'dynamical systems','kind':'flagship, odd years','why':'applied dynamics, the big one',
  'note':'Every other year. One presentation per person, fully in person. Propose a minisymposium of four talks first, or send a contributed abstract by the later date.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/ds27/'},
 {'title':'Dynamics Days US','desc':'Dynamics Days US',
  'area':'dynsys','proceedings':'none','lastDeadline':'2026-11-22','period':1,
  'place':'La Jolla, California, USA',
  'field':'dynamical systems','kind':'yearly','why':'single track, nonlinear science',
  'note':'Single track with no parallel sessions; a few abstracts are picked as talks and the rest are posters. The 2027 meeting is at the Scripps Seaside Forum; its calendar dates are not posted yet.',
  'link':'https://www.ddays.org/2027/'},
 {'title':'Dynamics Days Europe','desc':'Dynamics Days Europe',
  'area':'dynsys','proceedings':'none','lastDeadline':'2026-04-27','period':1,
  'field':'dynamical systems','kind':'yearly','why':'the European counterpart',
  'note':'The European single-track meeting, 46th edition in Lisbon in July 2026. The 2027 host is not announced, so the date shown is last year\'s abstract deadline rolled forward.',
  'link':'https://sites.google.com/view/ddayseurope'},
 # UQ & statistics
 {'title':'UNCECOMP','desc':'ECCOMAS Conference on Uncertainty Quantification in Computational Sciences and Engineering',
  'area':'uq','proceedings':'optin','lastDeadline':'2026-10-30','period':2,
  'date':'June 13-16, 2027','place':'Hersonissos, Crete, Greece',
  'rounds':[{'d':'2026-10-30','label':'one-page abstract','est':False},
            {'d':'2027-02-28','label':'optional full paper','est':False}],
  'field':'uncertainty quantification','kind':'odd years','why':'engineering UQ, optional papers',
  'note':'The engineering side of UQ, held with COMPDYN. A one-page abstract gets you on the programme; a full paper, optional, goes into the ECCOMAS proceedings.',
  'link':'https://2027.uncecomp.org/'},
 # Optimization & OR
 {'title':'ISMP','desc':'International Symposium on Mathematical Programming',
  'area':'opt','proceedings':'none','lastDeadline':'2027-01-15','period':3,
  'date':'July 25-30, 2027','place':'Amsterdam, Netherlands',
  'field':'optimization','kind':'flagship, every three years','why':'all of mathematical optimization',
  'note':'The Mathematical Optimization Society\'s symposium, 26th edition, every three years. One talk per person. Contributed abstracts and invited-session proposals share the deadline.',
  'link':'https://ismp2027.mathopt.nl/'},

 # Power & energy
 {'title':'PES GM','desc':'IEEE Power & Energy Society General Meeting',
  'area':'power','proceedings':'full','lastDeadline':'2026-11-10','period':1,
  'date':'July 25-29, 2027','place':'San Francisco, California, USA','badge':'power','dblp':'pesgm',
  'note':'The power society\'s large yearly meeting. One round, 5-page papers, about 800 accepted, archived on IEEE Xplore only if presented. Part 1 and Part 2 papers are not accepted.',
  'link':'https://pes-gm.org/2027-san-francisco/'},
 {'title':'PSCC','desc':'Power Systems Computation Conference',
  'area':'power','proceedings':'full','lastDeadline':'2025-06-15','period':2,
  'date':'June 26-30, 2028','place':'Delft, Netherlands','badge':'power','estIsForDate':True,
  'note':'Every two years and selective. Two stages: a one-page abstract first, then a full paper by invitation only, published in a special issue of Electric Power Systems Research. The 2028 dates are not announced; the date shown is the 2026 abstract deadline rolled forward two years.',
  'link':'https://pscc2028.dryfta.com/'},
 {'title':'SmartGridComm','desc':'IEEE International Conference on Communications, Control, and Computing Technologies for Smart Grids',
  'area':'power','proceedings':'full','lastDeadline':'2026-05-03','period':1,
  'date':'October 26-29, 2026','place':'College Station, Texas, USA','badge':'smart grid','dblp':'smartgridcomm',
  'note':'Six-page papers on IEEE Xplore, presented in person. The 2027 edition is not announced.',
  'link':'https://sgc2026.ieee-smartgridcomm.org/'},
 {'title':'e-Energy','desc':'ACM International Conference on Future and Sustainable Energy Systems',
  'area':'power','proceedings':'full','lastDeadline':'2027-01-15','period':1,
  'date':'June 5-11, 2027','place':'Atlanta, Georgia, USA','badge':'energy','dblp':'eenergy',
  'rounds':[{'d':'2027-01-15','abs':'2027-01-08','label':'winter round','est':False}],
  'note':'ACM\'s energy-systems conference, part of ACM Sustainability Week at FCRC 2027. Two rounds a year with revisions; the fall round has closed, and a paper rejected in fall cannot go to winter.',
  'link':'https://energy.acm.org/conferences/eenergy/2027/'},
 # Materials
 {'title':'MRS Spring','desc':'Materials Research Society Spring Meeting & Exhibit',
  'area':'materials','proceedings':'none','lastDeadline':'2026-10-14','period':1,
  'date':'April 5-9, 2027','place':'Seattle, Washington, USA',
  'field':'materials','kind':'flagship, yearly','why':'dozens of parallel symposia',
  'note':'Abstracts go to one symposium inside a topical cluster. The 2027 call closed on 14 October 2026, so the date shown is the next one, estimated.',
  'link':'https://www.mrs.org/meetings-events/annual-meetings/2027-mrs-spring-meeting-exhibit'},
 {'title':'MRS Fall','desc':'Materials Research Society Fall Meeting & Exhibit',
  'area':'materials','proceedings':'none','lastDeadline':'2026-06-17','period':1,
  'date':'November 28 - December 3, 2027','place':'Boston, Massachusetts, USA','estIsForDate':True,
  'field':'materials','kind':'flagship, yearly','why':'the larger of the two MRS meetings',
  'note':'Always in Boston. The 2027 abstract call is not out, so the date shown is the 2026 regular deadline rolled forward; 2026 also had a later Breaking News round.',
  'link':'https://www.mrs.org/meetings-events/annual-meetings/2027-mrs-fall-meeting-exhibit'},
 {'title':'TMS','desc':'TMS Annual Meeting & Exhibition',
  'area':'materials','proceedings':'optin','lastDeadline':'2026-07-01','period':1,
  'date':'March 14-18, 2027','place':'Orlando, Florida, USA',
  'field':'materials','kind':'yearly','why':'metals and processing, 100+ symposia',
  'note':'The Minerals, Metals & Materials Society meeting, over 4,000 attendees. Mostly abstracts, with full-paper proceedings volumes for some symposia. The 2027 abstract call has closed, so the date shown is the next one, estimated.',
  'link':'https://www.tms.org/TMS2027'},
 {'title':'AI4Mat','desc':'AI for Accelerated Materials Design, NeurIPS workshop',
  'area':'materials','proceedings':'none','lastDeadline':'2026-08-29','period':1,
  'date':'December 12, 2026','place':'Sydney, Australia',
  'field':'materials','kind':'yearly, at NeurIPS','why':'where ML meets materials',
  'note':'Non-archival, so a 4-page paper here can grow into a journal article; selected papers are invited to a Wiley collection. The 2026 deadline has passed.',
  'link':'https://sites.google.com/view/ai4mat'},
 # Epidemics, sleep, complex systems, network science
 {'title':'ESCAIDE','desc':'European Scientific Conference on Applied Infectious Disease Epidemiology',
  'area':'epi','proceedings':'none','lastDeadline':'2026-05-18','period':1,
  'date':'November 18-20, 2026','place':'Stockholm, Sweden',
  'field':'public health','kind':'yearly','why':'applied epidemiology, run by ECDC',
  'note':'Run by the European Centre for Disease Prevention and Control, free to attend, hybrid. Abstracts in May, with a late-breaker window in September.',
  'link':'https://www.escaide.eu/en'},
 {'title':'Sleep Europe','desc':'European Sleep Research Society Congress',
  'area':'sleep','proceedings':'none','lastDeadline':'2026-04-01','period':2,
  'date':'October 20-23, 2026','place':'Maastricht, Netherlands',
  'field':'sleep and circadian','kind':'flagship, even years','why':'European sleep research',
  'note':'The ESRS congress, every two years, 28th edition. 350-word structured abstracts. The 2028 edition is not announced.',
  'link':'https://esrs.eu/sleep-congress/'},
 {'title':'ALIFE','desc':'Conference on Artificial Life',
  'area':'complex','proceedings':'full','lastDeadline':'2026-03-30','period':1,
  'date':'July 19-23, 2027','place':'Prague, Czech Republic','estIsForDate':True,'badge':'artificial life',
  'field':'artificial life','kind':'flagship, yearly','why':'artificial life and emergence',
  'note':'The ISAL conference. Full papers of 3 to 8 pages go into open-access MIT Press proceedings; two-page summaries of published work are also taken. The 2027 call is not out, so the date shown is the 2026 deadline rolled forward.',
  'link':'https://2027.alife.org/'},
 {'title':'Complex Networks','desc':'International Conference on Complex Networks and their Applications',
  'area':'netsci','proceedings':'optin','lastDeadline':'2026-09-13','period':1,
  'date':'December 2-4, 2026','place':'Granada, Spain',
  'field':'network science','kind':'yearly','why':'papers in a Springer volume',
  'note':'Two kinds of submission: a 12-page paper in the Springer proceedings, or a 4-page extended abstract that is not archived. Accepted papers can be invited to journal special issues. The 2026 deadline has passed.',
  'link':'https://complexnetworks.org/'},
]

# Society meetings used to be one tab. They are spread over their fields
# now, keyed on the field label each card already carried.
FIELD_DOMAIN={
    'applied mathematics':'amath','computational science':'amath','data science theory':'amath','mathematics':'amath',
    'brain imaging':'neuro','cognitive neuroscience':'neuro','computational neuroscience':'neuro','neuroscience':'neuro',
    'cognitive psychology':'psych','psychology':'psych','consciousness':'psych',
    'dream research':'sleep','sleep and circadian':'sleep',
    'complex systems':'complex','physics':'complex','artificial life':'complex',
    'network science':'netsci','social networks':'netsci','computational social science':'netsci',
    'epidemic modelling':'epi','public health':'epi',
    'operations research':'opt','optimization':'opt',
    'statistics':'uq','uncertainty quantification':'uq',
    'Earth and space science':'dynsys','dynamical systems':'dynsys',
    'forecasting':'ts','materials':'materials',
}
AREA_RENAME={'AI / ML / Data Mining':'ai','Control':'control','Health & Bio':'biomed'}
for n in NOTABLE:
    if n['area']=='Society meetings':
        n['area']=FIELD_DOMAIN[n['field']]
    else:
        n['area']=AREA_RENAME.get(n['area'], n['area'])
    n['frank']=FIELD_RANK.get(n['title'],'')

def roll(ds, period=1):
    """Last published deadline -> next plausible one, same month and day."""
    if not ds: return '', None, False
    d0=datetime.date.fromisoformat(ds)
    if d0 >= TODAY: return ds, d0.year, False   # already published and ahead
    for bump in (period*k for k in range(1, 13)):
        try: cand=d0.replace(year=d0.year+bump)
        except ValueError: cand=d0.replace(year=d0.year+bump, day=28)
        if cand >= TODAY: return cand.isoformat(), cand.year, True
    return ('', None, False) if d0 < TODAY else (ds, d0.year, False)

for n in NOTABLE:
    n.setdefault('equivalent', None)   # editorial, not an official rank
    # The chip beside the name. "emerging" is the common case, a venue too
    # new for the catalogues; CDC is on the list for the opposite reason.
    n.setdefault('badge', 'emerging')
    for k in ('field', 'kind', 'why'):
        n.setdefault(k, '')
    n.setdefault('estIsForDate', False)
    nd, ny, est = roll(n.get('lastDeadline',''), n.get('period',1))
    n.update({'ccf':n.get('ccfManual','N'),'core':n.get('coreManual','N'),'coreVerified':False,'nextAbstract':'',
              'cycles':n.get('cycles',1),'roundLabels':n.get('roundLabels',[]),
              'rates':[],'rateSrc':'','rateSlug':'','rounds':n.get('rounds',[]),
              'dblp':n.get('dblp',''),'best':'','csr':'','edition':'','sub':'',
              'estimated':est,'estFrom':n.get('lastDeadline','') if est else '',
              # The deadline year is not the edition year for any of these:
              # MLSys closes in October for the following year's conference.
              # The date string, where there is one, names the edition.
              'nextDeadline':nd,'nextYear':None,
              'notable':True})
    n.setdefault('date',''); n.setdefault('place','')
    if est and n['date'] and not n.get('estIsForDate'):
        # The meeting on record is not the one this estimated deadline belongs
        # to. Both are worth showing, so both stay and the note says which is
        # which, rather than one of them being deleted to avoid the question.
        n['note']=n['note'].rstrip() + ' The meeting shown is the next one to attend, which is a cycle ahead of the estimated deadline beside it.'
    n['cc']=flag(n['place'])
    n['city']=city_note(n['place'])
    # An emerging venue carries a stated equivalence so it sorts with its peers;
    # a society meeting has no proceedings, so no tier is claimed for it.
    n['tier'] = 2 if n['equivalent'] else tier_of(n['ccf'], n['core'])

for c in out: c['tier']=tier_of(c['ccf'], c['core'])

CORE_ORDER={'A*':0,'A':1,'B':2,'C':3,'TBR':4,'JP':5,'N':6}
CCF_ORDER={'A':0,'B':1,'C':2,'N':3}
# Security keeps only the four everyone means by "the top tier". The
# interdisciplinary bucket keeps nothing: SIGSPATIAL, the one worth having,
# moved to AI. Everything dropped here lands in the folded Others section.
BIG_FOUR = {'CCS', 'S&P', 'USENIX Security', 'NDSS'}
def listed(c):
    if c['area'] == 'science': return False
    # A venue named into a field is there on purpose, whatever its tier.
    if c['title'] in BY_TITLE: return True
    if not (c['core'] in ('A*','A') or c['ccf'] in ('A','B')): return False
    if c['sub'] == 'SC' and c['title'] not in BIG_FOUR: return False
    return True
# inside an area, soonest deadline first; anything without one trails behind
def dkey(c): return (0, c['nextDeadline']) if c['nextDeadline'] else (1, c['title'].lower())
emerging=[n for n in NOTABLE if n['proceedings']=='full']
society=[n for n in NOTABLE if n['proceedings'] in ('none','optin','abstracts')]
# One list, ordered by date alone — the reader filters by field in the page.
ranked=sorted([c for c in out if listed(c)] + emerging, key=dkey)
# The folded "Others" list is gone: everything below the bar used to land
# there in one alphabetical heap with no field. The fields now carry their
# journals instead, which is the second half of how a field publishes.
# Grouped by field rather than alphabetically: the field chip is the first
# thing on a card, so the neighbours of a card should share it.
notable=sorted(society, key=lambda c:(c.get('field','') or 'zz', c['title'].lower()))


# ---------- journals ----------
# Conferences are only half of how most fields publish, and in control and
# medicine the smaller half. The list is chosen by hand, one handful per
# field; everything measured about each journal is pulled at build time.
#
# OpenAlex gives papers per year and the two-year mean citations per paper,
# which is the impact factor's formula on an open index, so it runs close
# to the JCR number without being it. CCF tiers come from the CCF catalogue
# as mirrored by CCFrank4dblp, keyed on the DBLP stream. Control journals
# have no CCF tier because CCF catalogues computing; that reads n/a, not a
# judgement.
JOURNALS=[
 # ai
 {'title':'TPAMI','name':'IEEE Transactions on Pattern Analysis and Machine Intelligence','issn':'0162-8828','dblp':'pami','area':'ai','pub':'IEEE','why':"vision and learning, the field's top transactions",'rank':''},
 {'title':'JMLR','name':'Journal of Machine Learning Research','issn':'1532-4435','dblp':'jmlr','area':'ai','pub':'JMLR','why':'long-form ML theory and methods, open access','rank':''},
 {'title':'TMLR','name':'Transactions on Machine Learning Research','issn':'2835-8856','dblp':'tmlr','area':'ai','pub':'OpenReview','why':'rolling review, judged on correctness rather than novelty','rank':''},
 {'title':'AIJ','name':'Artificial Intelligence','issn':'0004-3702','dblp':'ai','area':'ai','pub':'Elsevier','why':'the oldest general AI journal','rank':''},
 {'title':'JAIR','name':'Journal of Artificial Intelligence Research','issn':'1076-9757','dblp':'jair','area':'ai','pub':'AI Access Foundation','why':'general AI, open access','rank':''},
 {'title':'IJCV','name':'International Journal of Computer Vision','issn':'0920-5691','dblp':'ijcv','area':'ai','pub':'Springer','why':'computer vision','rank':''},
 {'title':'TKDE','name':'IEEE Transactions on Knowledge and Data Engineering','issn':'1041-4347','dblp':'tkde','area':'ai','pub':'IEEE','why':'data mining and databases','rank':''},
 {'title':'TKDD','name':'ACM Transactions on Knowledge Discovery from Data','issn':'1556-4681','dblp':'tkdd','area':'ai','pub':'ACM','why':'data mining, the SIGKDD journal','rank':''},
 {'title':'DMKD','name':'Data Mining and Knowledge Discovery','issn':'1384-5810','dblp':'datamine','area':'ai','pub':'Springer','why':'data mining, with an ECML PKDD journal track','rank':''},
 {'title':'TNNLS','name':'IEEE Transactions on Neural Networks and Learning Systems','issn':'2162-237X','dblp':'tnn','area':'ai','pub':'IEEE','why':'neural networks, high volume','rank':''},
 {'title':'TACL','name':'Transactions of the Association for Computational Linguistics','issn':'2307-387X','dblp':'tacl','area':'ai','pub':'ACL','why':'NLP, papers presented at ACL conferences','rank':''},
 # security
 {'title':'TDSC','name':'IEEE Transactions on Dependable and Secure Computing','issn':'1545-5971','dblp':'tdsc','area':'security','pub':'IEEE','why':'systems security and dependability','rank':'top'},
 {'title':'TIFS','name':'IEEE Transactions on Information Forensics and Security','issn':'1556-6013','dblp':'tifs','area':'security','pub':'IEEE','why':'forensics, biometrics, privacy','rank':'top'},
 {'title':'JoC','name':'Journal of Cryptology','issn':'0933-2790','dblp':'joc','area':'security','pub':'Springer (IACR)','why':'the cryptography journal','rank':'IACR journal'},
 {'title':'TOPS','name':'ACM Transactions on Privacy and Security','issn':'2471-2566','dblp':'tissec','area':'security','pub':'ACM','why':"security and privacy, ACM's journal",'rank':''},
 {'title':'Computers & Security','name':'Computers & Security','issn':'0167-4048','dblp':'compsec','area':'security','pub':'Elsevier','why':'applied security, high volume','rank':''},
 {'title':'JCS','name':'Journal of Computer Security','issn':'0926-227X','dblp':'jcs','area':'security','pub':'IOS Press','why':'formal and systems security','rank':''},
 # eda
 {'title':'TCAD','name':'IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems','issn':'0278-0070','dblp':'tcad','area':'eda','pub':'IEEE','why':'long versions of DAC and ICCAD papers','rank':'journal of record'},
 {'title':'TC','name':'IEEE Transactions on Computers','issn':'0018-9340','dblp':'tc','area':'eda','pub':'IEEE','why':'computer architecture and systems','rank':''},
 {'title':'TODAES','name':'ACM Transactions on Design Automation of Electronic Systems','issn':'1084-4309','dblp':'todaes','area':'eda','pub':'ACM','why':"design automation, ACM's journal",'rank':''},
 {'title':'TVLSI','name':'IEEE Transactions on Very Large Scale Integration Systems','issn':'1063-8210','dblp':'tvlsi','area':'eda','pub':'IEEE','why':'circuits and VLSI design','rank':''},
 # audio
 {'title':'TASLP','name':'IEEE/ACM Transactions on Audio, Speech, and Language Processing','issn':'2329-9290','dblp':'taslp','area':'audio','pub':'IEEE / ACM','why':'audio, speech and language, long form','rank':'top'},
 {'title':'TISMIR','name':'Transactions of the International Society for Music Information Retrieval','issn':'2514-3298','dblp':'tismir','area':'audio','pub':'Ubiquity Press','why':'music information retrieval, open access','rank':'ISMIR journal'},
 {'title':'EURASIP JASMP','name':'EURASIP Journal on Audio, Speech, and Music Processing','issn':'1687-4714','dblp':'ejasmp','area':'audio','pub':'Springer','why':'audio and music processing, open access','rank':''},
 {'title':'JAES','name':'Journal of the Audio Engineering Society','issn':'1549-4950','dblp':'','area':'audio','pub':'AES','why':'audio engineering, the AES journal','rank':''},
 # ts
 {'title':'IJF','name':'International Journal of Forecasting','issn':'0169-2070','dblp':'','area':'ts','pub':'Elsevier (IIF)','why':"forecasting, the IIF's journal",'rank':'IIF journal'},
 {'title':'JTSA','name':'Journal of Time Series Analysis','issn':'0143-9782','dblp':'','area':'ts','pub':'Wiley','why':'time-series statistics','rank':''},
 # control
 {'title':'TAC','name':'IEEE Transactions on Automatic Control','issn':'0018-9286','dblp':'tac','area':'control','pub':'IEEE CSS','why':'theory first','rank':'flagship'},
 {'title':'Automatica','name':'Automatica','issn':'0005-1098','dblp':'automatica','area':'control','pub':'Elsevier (IFAC)','why':"IFAC's journal, level with TAC",'rank':'flagship'},
 {'title':'SICON','name':'SIAM Journal on Control and Optimization','issn':'0363-0129','dblp':'siamco','area':'control','pub':'SIAM','why':'mathematical control theory','rank':''},
 {'title':'TCST','name':'IEEE Transactions on Control Systems Technology','issn':'1063-6536','dblp':'tcst','area':'control','pub':'IEEE CSS','why':'control applied to real systems','rank':''},
 {'title':'TCNS','name':'IEEE Transactions on Control of Network Systems','issn':'2325-5870','dblp':'tcns','area':'control','pub':'IEEE CSS','why':'networked and multi-agent control','rank':''},
 {'title':'L-CSS','name':'IEEE Control Systems Letters','issn':'2475-1456','dblp':'lcsys','area':'control','pub':'IEEE CSS','why':'six-page letters, presentable at CDC or ACC','rank':'CDC / ACC track'},
 {'title':'SCL','name':'Systems & Control Letters','issn':'0167-6911','dblp':'scl','area':'control','pub':'Elsevier','why':'short theory papers','rank':''},
 {'title':'ARC','name':'Annual Reviews in Control','issn':'1367-5788','dblp':'arc','area':'control','pub':'Elsevier (IFAC)','why':'invited surveys, so citations run high','rank':''},
 # dynsys
 {'title':'SIADS','name':'SIAM Journal on Applied Dynamical Systems','issn':'1536-0040','dblp':'siamads','area':'dynsys','pub':'SIAM','why':'applied dynamics, the SIAM journal','rank':''},
 {'title':'Chaos','name':'Chaos: An Interdisciplinary Journal of Nonlinear Science','issn':'1054-1500','dblp':'','area':'dynsys','pub':'AIP','why':'nonlinear science across fields','rank':''},
 {'title':'Physica D','name':'Physica D: Nonlinear Phenomena','issn':'0167-2789','dblp':'','area':'dynsys','pub':'Elsevier','why':'nonlinear phenomena, mathematical','rank':''},
 {'title':'Nonlinearity','name':'Nonlinearity','issn':'0951-7715','dblp':'','area':'dynsys','pub':'IOP / LMS','why':'pure and applied dynamics','rank':''},
 {'title':'Nonlinear Dyn.','name':'Nonlinear Dynamics','issn':'0924-090X','dblp':'','area':'dynsys','pub':'Springer','why':'engineering dynamics, high volume','rank':''},
 # complex
 {'title':'PRE','name':'Physical Review E','issn':'1539-3755','dblp':'','area':'complex','pub':'APS','why':'statistical, nonlinear and soft-matter physics','rank':''},
 {'title':'Physica A','name':'Physica A: Statistical Mechanics and its Applications','issn':'0378-4371','dblp':'','area':'complex','pub':'Elsevier','why':'statistical physics applied widely','rank':''},
 {'title':'JPhys Complexity','name':'Journal of Physics: Complexity','issn':'2632-072X','dblp':'','area':'complex','pub':'IOP','why':'complex systems, open access','rank':''},
 {'title':'Artificial Life','name':'Artificial Life','issn':'1064-5462','dblp':'','area':'complex','pub':'MIT Press','why':"ISAL's journal",'rank':'ISAL journal'},
 {'title':'Complexity','name':'Complexity','issn':'1076-2787','dblp':'','area':'complex','pub':'Wiley','why':'broad complex systems, open access','rank':''},
 # netsci
 {'title':'Network Science','name':'Network Science','issn':'2050-1242','dblp':'netsci','area':'netsci','pub':'Cambridge','why':"the Network Science Society's journal",'rank':'society journal'},
 {'title':'J. Complex Netw.','name':'Journal of Complex Networks','issn':'2051-1310','dblp':'compnet','area':'netsci','pub':'Oxford','why':'network theory and methods','rank':''},
 {'title':'Appl. Netw. Sci.','name':'Applied Network Science','issn':'2364-8228','dblp':'ans','area':'netsci','pub':'Springer','why':'applied networks, open access','rank':''},
 {'title':'Social Networks','name':'Social Networks','issn':'0378-8733','dblp':'socnet','area':'netsci','pub':'Elsevier','why':"social network analysis, INSNA's journal",'rank':'INSNA journal'},
 {'title':'EPJ Data Sci.','name':'EPJ Data Science','issn':'2193-1127','dblp':'epjds','area':'netsci','pub':'Springer','why':'computational social science, open access','rank':''},
 # uq
 {'title':'JUQ','name':'SIAM/ASA Journal on Uncertainty Quantification','issn':'2166-2525','dblp':'juq','area':'uq','pub':'SIAM / ASA','why':'UQ, the joint SIAM and ASA journal','rank':'SIAM / ASA'},
 {'title':'IJUQ','name':'International Journal for Uncertainty Quantification','issn':'2152-5080','dblp':'','area':'uq','pub':'Begell House','why':'UQ in engineering','rank':''},
 {'title':'JASA','name':'Journal of the American Statistical Association','issn':'0162-1459','dblp':'','area':'uq','pub':'ASA / Taylor & Francis','why':"statistics, the ASA's flagship",'rank':'ASA flagship'},
 {'title':'AoS','name':'The Annals of Statistics','issn':'0090-5364','dblp':'','area':'uq','pub':'IMS','why':'mathematical statistics','rank':'IMS flagship'},
 # opt
 {'title':'Math. Prog.','name':'Mathematical Programming','issn':'0025-5610','dblp':'mp','area':'opt','pub':'Springer (MOS)','why':"optimization theory, MOS's journal",'rank':'MOS flagship'},
 {'title':'SIOPT','name':'SIAM Journal on Optimization','issn':'1052-6234','dblp':'siamjo','area':'opt','pub':'SIAM','why':'continuous optimization','rank':''},
 {'title':'OR','name':'Operations Research','issn':'0030-364X','dblp':'ior','area':'opt','pub':'INFORMS','why':'operations research','rank':'INFORMS flagship'},
 {'title':'MS','name':'Management Science','issn':'0025-1909','dblp':'mansci','area':'opt','pub':'INFORMS','why':'OR meets business and economics','rank':''},
 {'title':'IJOC','name':'INFORMS Journal on Computing','issn':'0899-1499','dblp':'informs','area':'opt','pub':'INFORMS','why':'computation in OR','rank':''},
 # amath
 {'title':'SIAM Review','name':'SIAM Review','issn':'0036-1445','dblp':'siamrev','area':'amath','pub':'SIAM','why':'surveys and expository papers','rank':''},
 {'title':'SISC','name':'SIAM Journal on Scientific Computing','issn':'1064-8275','dblp':'siamsc','area':'amath','pub':'SIAM','why':'numerical methods and computing','rank':''},
 {'title':'SIMODS','name':'SIAM Journal on Mathematics of Data Science','issn':'2577-0187','dblp':'simods','area':'amath','pub':'SIAM','why':'mathematics of data science','rank':''},
 {'title':'JCP','name':'Journal of Computational Physics','issn':'0021-9991','dblp':'jcphy','area':'amath','pub':'Elsevier','why':'computational physics and numerics','rank':''},
 # neuro
 {'title':'Neuron','name':'Neuron','issn':'0896-6273','dblp':'','area':'neuro','pub':'Cell Press','why':'neuroscience, broad and top','rank':'top'},
 {'title':'Nat. Neurosci.','name':'Nature Neuroscience','issn':'1097-6256','dblp':'','area':'neuro','pub':'Nature Portfolio','why':'neuroscience, broad and top','rank':'top'},
 {'title':'JOCN','name':'Journal of Cognitive Neuroscience','issn':'0898-929X','dblp':'','area':'neuro','pub':'MIT Press','why':'cognitive neuroscience itself','rank':''},
 {'title':'NeuroImage','name':'NeuroImage','issn':'1053-8119','dblp':'','area':'neuro','pub':'Elsevier','why':'brain imaging methods and studies','rank':''},
 {'title':'HBM','name':'Human Brain Mapping','issn':'1065-9471','dblp':'','area':'neuro','pub':'Wiley','why':'brain mapping','rank':''},
 {'title':'PLOS Comp Bio','name':'PLOS Computational Biology','issn':'1553-734X','dblp':'ploscb','area':'neuro','pub':'PLOS','why':'computational neuroscience and biology','rank':''},
 {'title':'eLife','name':'eLife','issn':'2050-084X','dblp':'','area':'neuro','pub':'eLife','why':'life sciences, reviewed preprints','rank':''},
 # psych
 {'title':'Psych. Review','name':'Psychological Review','issn':'0033-295X','dblp':'','area':'psych','pub':'APA','why':"theory, the field's top theory journal",'rank':'top'},
 {'title':'Psych. Science','name':'Psychological Science','issn':'0956-7976','dblp':'','area':'psych','pub':'SAGE (APS)','why':"short empirical papers, APS's flagship",'rank':'APS flagship'},
 {'title':'TiCS','name':'Trends in Cognitive Sciences','issn':'1364-6613','dblp':'','area':'psych','pub':'Cell Press','why':'reviews and opinion, so citations run high','rank':''},
 {'title':'JEP: General','name':'Journal of Experimental Psychology: General','issn':'0096-3445','dblp':'','area':'psych','pub':'APA','why':'broad experimental psychology','rank':''},
 {'title':'Cognition','name':'Cognition','issn':'0010-0277','dblp':'','area':'psych','pub':'Elsevier','why':'cognitive science, experimental','rank':''},
 {'title':'Cognitive Science','name':'Cognitive Science','issn':'0364-0213','dblp':'cogsci','area':'psych','pub':'Wiley','why':"the Cognitive Science Society's journal",'rank':'society journal'},
 {'title':'PB&R','name':'Psychonomic Bulletin & Review','issn':'1069-9384','dblp':'','area':'psych','pub':'Springer','why':"the Psychonomic Society's journal",'rank':'society journal'},
 # sleep
 {'title':'SLEEP','name':'SLEEP','issn':'0161-8105','dblp':'','area':'sleep','pub':'Oxford (SRS)','why':'sleep research; publishes the SLEEP meeting abstracts, which drag the citation mean down','rank':'SRS journal'},
 {'title':'Sleep Med. Rev.','name':'Sleep Medicine Reviews','issn':'1087-0792','dblp':'','area':'sleep','pub':'Elsevier','why':'reviews, so citations run high','rank':''},
 {'title':'JSR','name':'Journal of Sleep Research','issn':'0962-1105','dblp':'','area':'sleep','pub':'Wiley (ESRS)','why':'the ESRS journal','rank':'ESRS journal'},
 {'title':'Dreaming','name':'Dreaming','issn':'1053-0797','dblp':'','area':'sleep','pub':'APA (IASD)','why':"dream research, IASD's journal",'rank':'IASD journal'},
 {'title':'IJoDR','name':'International Journal of Dream Research','issn':'1866-7953','dblp':'','area':'sleep','pub':'Heidelberg University','why':'dream research, open access','rank':''},
 # biomed
 {'title':'JAMIA','name':'Journal of the American Medical Informatics Association','issn':'1067-5027','dblp':'jamia','area':'biomed','pub':'Oxford (AMIA)','why':'clinical informatics','rank':'AMIA journal'},
 {'title':'Lancet Digit. Health','name':'The Lancet Digital Health','issn':'2589-7500','dblp':'','area':'biomed','pub':'Elsevier','why':'digital health for clinicians','rank':''},
 {'title':'npj Digit. Med.','name':'npj Digital Medicine','issn':'2398-6352','dblp':'','area':'biomed','pub':'Nature Portfolio','why':'digital health and clinical AI, open access','rank':''},
 {'title':'MedIA','name':'Medical Image Analysis','issn':'1361-8415','dblp':'mia','area':'biomed','pub':'Elsevier','why':'medical imaging methods','rank':'MICCAI journal'},
 {'title':'TMI','name':'IEEE Transactions on Medical Imaging','issn':'0278-0062','dblp':'tmi','area':'biomed','pub':'IEEE','why':'medical imaging','rank':'top'},
 {'title':'TBME','name':'IEEE Transactions on Biomedical Engineering','issn':'0018-9294','dblp':'tbe','area':'biomed','pub':'IEEE','why':'biomedical engineering','rank':''},
 {'title':'JBHI','name':'IEEE Journal of Biomedical and Health Informatics','issn':'2168-2194','dblp':'titb','area':'biomed','pub':'IEEE','why':'health informatics and sensing','rank':''},
 {'title':'JBI','name':'Journal of Biomedical Informatics','issn':'1532-0464','dblp':'jbi','area':'biomed','pub':'Elsevier','why':'biomedical informatics methods','rank':''},
 # epi
 {'title':'Epidemics','name':'Epidemics','issn':'1755-4365','dblp':'','area':'epi','pub':'Elsevier','why':'infectious disease dynamics','rank':'conference journal'},
 {'title':'Lancet Inf. Dis.','name':'The Lancet Infectious Diseases','issn':'1473-3099','dblp':'','area':'epi','pub':'Elsevier','why':'infectious disease, clinical and public health','rank':'top'},
 {'title':'Eurosurveillance','name':'Eurosurveillance','issn':'1025-496X','dblp':'','area':'epi','pub':'ECDC','why':'surveillance and outbreak reports, fast','rank':''},
 {'title':'AJE','name':'American Journal of Epidemiology','issn':'0002-9262','dblp':'','area':'epi','pub':'Oxford','why':'epidemiological methods','rank':''},
 {'title':'IDM','name':'Infectious Disease Modelling','issn':'2468-0427','dblp':'','area':'epi','pub':'KeAi','why':'modelling, open access','rank':''},
 # materials
 {'title':'Nat. Mater.','name':'Nature Materials','issn':'1476-1122','dblp':'','area':'materials','pub':'Nature Portfolio','why':'materials science, broad and top','rank':'top'},
 {'title':'npj Comput. Mater.','name':'npj Computational Materials','issn':'2057-3960','dblp':'','area':'materials','pub':'Nature Portfolio','why':'computational and ML materials','rank':''},
 {'title':'Digital Discovery','name':'Digital Discovery','issn':'2635-098X','dblp':'','area':'materials','pub':'RSC','why':'ML and automation for chemistry and materials','rank':''},
 {'title':'Acta Mater.','name':'Acta Materialia','issn':'1359-6454','dblp':'','area':'materials','pub':'Elsevier','why':'structural and metallic materials','rank':''},
 {'title':'Chem. Mater.','name':'Chemistry of Materials','issn':'0897-4756','dblp':'','area':'materials','pub':'ACS','why':'materials chemistry','rank':''},
 # power
 {'title':'TPWRS','name':'IEEE Transactions on Power Systems','issn':'0885-8950','dblp':'','area':'power','pub':'IEEE PES','why':'power systems','rank':'top'},
 {'title':'TSG','name':'IEEE Transactions on Smart Grid','issn':'1949-3053','dblp':'','area':'power','pub':'IEEE PES','why':'smart grids and data','rank':'top'},
 {'title':'TSTE','name':'IEEE Transactions on Sustainable Energy','issn':'1949-3029','dblp':'','area':'power','pub':'IEEE PES','why':'renewables and storage','rank':''},
 {'title':'EPSR','name':'Electric Power Systems Research','issn':'0378-7796','dblp':'','area':'power','pub':'Elsevier','why':'power systems; carries PSCC papers','rank':'PSCC journal'},
 {'title':'Applied Energy','name':'Applied Energy','issn':'0306-2619','dblp':'','area':'power','pub':'Elsevier','why':'energy systems, broad, high volume','rank':''},
]

# Anything a fetch misses comes from the copy kept beside the script, so a
# bad week upstream degrades to last week's numbers instead of blanks.
JCACHE='../scripts/journal-cache.json'
jcache=json.load(open(JCACHE)) if os.path.exists(JCACHE) else {}
try:
    with urllib.request.urlopen('https://raw.githubusercontent.com/WenyanLiu/CCFrank4dblp/master/data/ccfRankUrl.js', timeout=60) as r:
        _ccfj=r.read().decode('utf-8','ignore')
    CCF_J={k: v.strip() for k, v in re.findall(r'"/journals/([^/"]+)/[^"]*":\s*"([^"]+)"', _ccfj)}
except Exception as e:
    print('CCF journal table unavailable:', e); CCF_J=None
journals=[]
for j in JOURNALS:
    key=j['issn']
    try:
        # Single-record lookups cost no OpenAlex credits, but a burst of a
        # hundred still trips the per-second limit, so pace and retry.
        src=None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(f'https://api.openalex.org/sources/issn:{key}?mailto=site@zhiqian.ai', timeout=60) as r:
                    src=json.load(r)
                break
            except urllib.error.HTTPError as e:
                if e.code != 429 or attempt == 3: raise
                time.sleep(5 * (attempt + 1))
        time.sleep(0.25)
        st=src.get('summary_stats') or {}
        # The current year is still filling in, so it is left out rather than
        # drawn as a cliff at the end of every line.
        per=sorted((c['year'], c['works_count']) for c in src.get('counts_by_year') or []
                   if c['year'] < TODAY.year)
        jcache[key]={'subs':[{'y':y,'n':n} for y,n in per][-10:],
                     'cites':round(st.get('2yr_mean_citedness') or 0, 1),
                     'h':st.get('h_index') or 0, 'oa':src.get('id','')}
    except Exception as e:
        print('OpenAlex miss, using cache:', j['title'], e)
    m=jcache.get(key, {'subs':[], 'cites':0, 'h':0, 'oa':''})
    if CCF_J is not None:
        j['ccf']=CCF_J.get(j['dblp'], 'N') if j['dblp'] else 'N'
        jcache.setdefault(key, {})['ccf']=j['ccf']
    else:
        j['ccf']=jcache.get(key, {}).get('ccf', 'N')
    # A journal OpenAlex barely indexes (TMLR, and JMLR's citations) would
    # otherwise show a confident zero. Zero here means "not measured".
    # JMLR is the subtle case: OpenAlex has its early years and almost none
    # of the recent ones, so its citation mean reads zero and its output
    # line falls off a cliff that never happened. A zero mean is the tell.
    indexed=sum(p['n'] for p in m['subs']) >= 50 and m['cites'] > 0
    journals.append({**j, 'subs': m['subs'] if indexed else [],
                     'cites': m['cites'] if indexed else None,
                     'h': m['h'] if indexed else None, 'oa': m.get('oa',''),
                     'link': f"https://dblp.org/db/journals/{j['dblp']}/index.html" if j['dblp'] else ''})
json.dump(jcache, open(JCACHE,'w'), indent=1, sort_keys=True)
# The hand order within a field is the editorial ranking (TAC before a survey
# journal whose citations are high by construction), so the sort only lifts
# CCF tiers above it and is otherwise stable.
journals.sort(key=lambda j: CCF_ORDER.get(j['ccf'],3) if j['area'] == 'ai' else 0)
print('journals:', len(journals), dict(collections.Counter(j['area'] for j in journals)))

hdr=("// Generated by scripts/build-conferences.py — do not edit by hand.\n"
     "// CCF ranks mirror the CCF catalogue via github.com/ccfddl/ccf-deadlines.\n"
     "// CORE ranks are cross-checked against the official CORE2023 export from\n"
     "// portal.core.edu.au. Acceptance rates and submission counts come from\n"
     "// github.com/Xovee/cs-conf-stats (main track only).\n"
     f"// Built {TODAY.isoformat()}.\n")
body=(hdr + "export const ranked = %s;\n\n"
      "// Hand-maintained; the ranking tables do not reach these.\nexport const notable = %s;\n\n"
      "// Journal list by hand; output, citations and CCF tier pulled each build.\nexport const journals = %s;\n"
      % tuple(json.dumps(x, indent=2, ensure_ascii=False) for x in (ranked, notable, journals)))
open('../src/data/conferences.js','w').write(body)
import collections as _c
print('\nwritten | listed', len(ranked), '| journals', len(journals), '| society', len(notable))
print('tiers:', dict(sorted(_c.Counter(c['tier'] for c in ranked).items())))
print('areas:', dict(_c.Counter(c['area'] for c in ranked)))
