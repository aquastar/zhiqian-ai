"""Rebuild src/data/conferences.js from upstream sources.

Run from the repo root:  python3 scripts/build-conferences.py
It clones ccf-deadlines, pulls the official CORE2023 export and the
acceptance-rate table into .conf-cache/, then rewrites the data module.
"""
import yaml, glob, csv, re, json, datetime, collections, os, subprocess, urllib.request, unicodedata

TODAY = datetime.date.today()
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
    ('https://raw.githubusercontent.com/lixin4ever/Conference-Acceptance-Rate/master/README.md', 'ar.md'),
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
# The rate table and the CCF catalogue spell several venues differently;
# without these, KDD and friends silently lose their whole history.
AR_ALIAS={'TheWebConf':'WWW','NAACL-HLT':'NAACL','KDD':'SIGKDD','SIGKDD':'SIGKDD',
          'CCS':'CCS','S&P':'S&P','Oakland':'S&P','IEEE S&P':'S&P',
          'USENIX':'USENIX Security','USENIX Sec':'USENIX Security','SP':'S&P',
          'MM':'ACM MM','ACMMM':'ACM MM'}
rates=collections.defaultdict(dict)
# Remember which README section each venue sits under, so the page can link
# straight to the table the numbers came from instead of the repo root.
rate_section={}
_sec=''
for line in open('ar.md'):
    if line.startswith('### '):
        _sec=re.sub(r'[^a-z0-9]+','-',line[4:].strip().lower()).strip('-')
        continue
    if not line.startswith('|') or '---' in line or line.startswith('| Conference'): continue
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    m=re.match(r"([A-Za-z0-9&\-\. ]+?)[''](\d{2})(.*)", cells[0])
    if not m: continue
    name, yy, suffix = m.group(1).strip(), int(m.group(2)), m.group(3).strip()
    if 'finding' in suffix.lower(): continue      # Findings is a separate track
    pct=re.search(r'([\d.]+)%', cells[1] if len(cells)>1 else '')
    if not pct: continue
    year = 2000+yy
    key=AR_ALIAS.get(name, name)
    rates[key][year]=float(pct.group(1))
    rate_section.setdefault(key, _sec)

# cs-conf-stats carries accepted/submitted counts per year and is current to
# 2026 for most venues, so it is the primary source; the older compilation is
# kept only to fill venues it does not cover.
CSC_ALIAS={'KDD':'SIGKDD','IEEE S&P':'S&P','Interspeech':'InterSpeech'}
csc_rates={}; csc_slug={}; csc_ordinal={}
for c in json.load(open('cs-conf-stats/data/conf.json'))['conferences']:
    t=CSC_ALIAS.get(c['series'], c['series'])
    hist={}
    for y in c.get('yearly_data') or []:
        mt=y.get('main_track') or {}
        a,sb=mt.get('num_acc'), mt.get('num_sub')
        if a and sb: hist[y['year']]=round(100*a/sb, 1)
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
 'amsterdam': 'Rijksmuseum, Van Gogh Museum, canal belt',
 'athens': 'Acropolis, Ancient Agora, Plaka',
 'atlanta': 'Georgia Aquarium, MLK Historic Site, BeltLine',
 'austin': 'live music on 6th Street, Barton Springs, Texas Capitol',
 'barcelona': 'Sagrada Familia, Park Guell, Gothic Quarter',
 'bari': 'Basilica di San Nicola, Bari Vecchia, Adriatic seafront',
 'beijing': 'Forbidden City, Great Wall at Mutianyu, Temple of Heaven',
 'bellevue': 'Bellevue Botanical Garden, Seattle 20 minutes west, Cascade day trips',
 'bengaluru': 'Lalbagh Botanical Garden, Bangalore Palace, Cubbon Park',
 'berlin': 'Museum Island, Brandenburg Gate, East Side Gallery',
 'bremen': 'Town Musicians statue, Schnoor quarter, Bottcherstrasse',
 'brisbane': 'South Bank Parklands, Story Bridge climb, Moreton Island',
 'bruges': 'Markt and Belfry, canal boats, Groeningemuseum',
 'budapest': 'Szechenyi baths, Buda Castle, Parliament on the Danube',
 'buenos aires': 'Recoleta Cemetery, Teatro Colon, San Telmo tango',
 'cancun': 'Chichen Itza, cenotes, Isla Mujeres',
 'cape town': 'Table Mountain, Cape Point, Robben Island',
 'chania': 'Venetian harbour, Samaria Gorge, Balos lagoon',
 'chengdu': 'giant panda base, Jinli street, Mount Qingcheng',
 'copenhagen': 'Nyhavn, Tivoli Gardens, Louisiana Museum',
 'dallas': 'Sixth Floor Museum, Dallas Arts District, Deep Ellum',
 'danang': 'Marble Mountains, Hoi An old town, My Khe beach',
 'delft': 'Vermeer sights, Oude Kerk, Delft Blue potteries',
 'denver': 'Red Rocks, Rocky Mountain National Park, Denver Art Museum',
 'dublin': 'Trinity College and the Book of Kells, Guinness Storehouse, Howth cliffs',
 'durham': 'Duke Chapel, Sarah P. Duke Gardens, Research Triangle',
 'edinburgh': 'Edinburgh Castle, Arthur Seat, the Royal Mile',
 'eindhoven': 'Van Abbemuseum, Strijp-S, Philips Museum',
 'florence': 'Uffizi, Duomo, Ponte Vecchio',
 'fukui': 'Fukui Dinosaur Museum, Eiheiji temple, Tojinbo cliffs',
 'guangzhou': 'Canton Tower, Shamian Island, Chen Clan Academy',
 'hangzhou': 'West Lake, Lingyin Temple, Longjing tea terraces',
 'hanoi': 'Old Quarter, Hoan Kiem Lake, Ha Long Bay day trip',
 'hefei': 'Lord Bao Park, Sanhe ancient town, Huangshan day trip',
 'hong kong': 'Victoria Peak, Star Ferry, Tian Tan Buddha',
 'honolulu': 'Waikiki, Pearl Harbor, Diamond Head',
 'huntington beach': 'the pier and surf break, Bolsa Chica wetlands, Pacific Coast Highway',
 'jinan': 'Baotu Spring, Daming Lake, Mount Tai day trip',
 'krakow': 'Wawel Castle, Main Market Square, Auschwitz-Birkenau',
 'kuala lumpur': 'Petronas Towers, Batu Caves, Jalan Alor night food',
 'kunming': 'Stone Forest, Dianchi Lake, Green Lake Park',
 'kyoto': 'Fushimi Inari, Kinkaku-ji, Arashiyama bamboo grove',
 'leiden': 'Rijksmuseum van Oudheden, Hortus Botanicus, canal walks',
 'lille': 'Vieux-Lille, Palais des Beaux-Arts, Braderie in September',
 'limassol': 'Kourion ruins, Limassol Marina, Troodos mountains',
 'london': 'British Museum, Tate Modern, Borough Market',
 'los angeles': 'Getty Center, Griffith Observatory, Santa Monica',
 'luxembourg': 'Bock Casemates, Old Quarter, Mullerthal trails',
 'maastricht': 'Vrijthof, Sint-Pietersberg caves, Bonnefanten Museum',
 'macau': 'Ruins of St Paul, Senado Square, Taipa Village',
 'madrid': 'Prado, Retiro Park, Reina Sofia',
 'mainz': 'Gutenberg Museum, Mainz Cathedral, Rhine valley',
 'malmo': 'Turning Torso, Malmo Castle, Copenhagen over the bridge',
 'marrakesh': 'Jemaa el-Fnaa, Majorelle Garden, Atlas Mountains',
 'melbourne': 'laneway coffee, NGV, Great Ocean Road',
 'milan': 'Duomo, Last Supper, Navigli',
 'montreal': 'Old Montreal, Mount Royal, Jean-Talon Market',
 'new delhi': 'Red Fort, Humayun Tomb, Taj Mahal day trip',
 'new york': 'the Met, Central Park, Broadway',
 'new york city': 'the Met, Central Park, Broadway',
 'newark': 'Newark Museum of Art, Branch Brook cherry blossoms, Manhattan 20 minutes away',
 'osaka': 'Osaka Castle, Dotonbori, Kyoto and Nara by train',
 'ottawa': 'Parliament Hill, National Gallery, Rideau Canal',
 'phoenix': 'Desert Botanical Garden, Camelback Mountain, Sedona day trip',
 'poznan': 'Old Market Square, Imperial Castle, Lake Malta',
 'rennes': 'medieval half-timbered centre, Parlement de Bretagne, Mont Saint-Michel day trip',
 'reykjavik': 'Blue Lagoon, Golden Circle, northern lights in winter',
 'rio de janeiro': 'Christ the Redeemer, Sugarloaf, Copacabana',
 'riverside': 'Mission Inn, Box Springs Mountain, Joshua Tree day trip',
 'rome': 'Colosseum, Vatican Museums, Trastevere',
 'saarbrucken': 'Saarschleife bend, Ludwigskirche, Volklingen Ironworks',
 'sacramento': 'Old Sacramento, State Capitol, Napa and Tahoe day trips',
 'salt lake city': 'Temple Square, Big Cottonwood Canyon, Great Salt Lake',
 'san diego': 'Balboa Park, La Jolla Cove, the zoo',
 'san francisco': 'Golden Gate Bridge, Alcatraz, Muir Woods',
 'san jose': 'Winchester Mystery House, Santana Row, Santa Cruz over the hill',
 'santa barbara': 'Santa Barbara Mission, Stearns Wharf, wine country',
 'sao paulo': 'MASP, Ibirapuera Park, Liberdade',
 'seattle': 'Pike Place Market, Chihuly Garden, Mount Rainier',
 'seoul': 'Gyeongbokgung, Bukchon Hanok Village, Han River parks',
 'shanghai': 'the Bund, Yu Garden, Power Station of Art',
 'shenyang': 'Mukden Palace, Zhaoling Tomb, Qipanshan',
 'singapore': 'Gardens by the Bay, hawker centres, Sentosa',
 'southampton': 'SeaCity Museum, Tudor House, New Forest',
 'sydney': 'Opera House, Bondi to Coogee walk, Blue Mountains',
 'taipei': 'Taipei 101, National Palace Museum, Jiufen',
 'tokyo': 'Senso-ji, teamLab, Tsukiji outer market',
 'toronto': 'CN Tower, Royal Ontario Museum, Niagara Falls day trip',
 'trento': 'Buonconsiglio Castle, MUSE science museum, Dolomites',
 'vancouver': 'Stanley Park, Granville Island, Grouse Mountain',
 'venice': "St Mark's Basilica, Grand Canal, Murano and Burano",
 'vilnius': 'Old Town, Gediminas Tower, Uzupis',
 'wellington': 'Te Papa, Mount Victoria, Zealandia',
 'yokohama': 'Minato Mirai, Chinatown, Sankeien Garden',
 'the hague': 'Mauritshuis, Peace Palace, Scheveningen beach',
 'pittsburgh': 'Andy Warhol Museum, Duquesne Incline, Carnegie Museums',
 'cleveland': 'Rock and Roll Hall of Fame, Cleveland Museum of Art, Lake Erie',
 'columbia': 'South Carolina State House, Riverbanks Zoo, Congaree National Park',
 'lancaster': 'Lancaster Castle, Williamson Park, Lake District an hour north',
 'buena vista': 'Walt Disney World, Universal Orlando, Kennedy Space Center',
 'barbados': 'Carlisle Bay, Harrison Cave, Bridgetown Garrison',
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
def flag(place):
    if not place: return ''
    tail=place.split(',')[-1]
    tail=re.sub(r'\(.*?\)|/.*$|and online', ' ', tail, flags=re.I)
    tail=re.sub(r'[^a-z ]', ' ', tail.lower()).strip()
    tail=re.sub(r'\s+', ' ', tail)
    return CC.get(tail, '')

# ---------- areas ----------
BIO={'APBC','BIBM','ISMB','ISBRA','RECOMB','MICCAI','EMBC'}
AREA_BY_SUB={'AI':'AI / ML / Data Mining','SC':'Security & Privacy','DB':'AI / ML / Data Mining'}
# CCF files WWW under 交叉/综合/新兴 because of its history, but everyone
# submitting to it treats it as a web-mining venue.
AREA_OVERRIDE={'WWW':'AI / ML / Data Mining'}
def area(sub, title):
    if title in EXTRA: return EXTRA[title]
    if title in AREA_OVERRIDE: return AREA_OVERRIDE[title]
    if sub in AREA_BY_SUB: return AREA_BY_SUB[sub]
    if title in BIO: return 'Medicine, Biology & Genetics'
    return 'Science & Interdisciplinary'

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

EXTRA={'ICASSP':'AI / ML / Data Mining','InterSpeech':'AI / ML / Data Mining',
       'ICWSM':'AI / ML / Data Mining'}
out=[]
for sub in ['AI','SC','DB','MX','CG','HI']:
    for f in sorted(glob.glob(f'ccf-deadlines/conference/{sub}/*.yml')):
        for c in yaml.safe_load(open(f)):
            r=c.get('rank') or {}; t=c['title']; d=(c.get('description') or '').strip()
            if sub in ('CG','HI') and t not in EXTRA: continue
            confs=c.get('confs') or []
            # next deadline still ahead of today, across every published edition
            upcoming=[]
            for ed in confs:
                for tl in (ed.get('timeline') or []):
                    ds=dstr(tl.get('deadline'))
                    if ds and datetime.date.fromisoformat(ds) >= TODAY:
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
                rs=[(dstr(t.get('deadline')), (t.get('comment') or '').strip())
                    for t in (ed.get('timeline') or []) if dstr(t.get('deadline'))]
                seen=set(); rs=[r for r in rs if not (r[0] in seen or seen.add(r[0]))]
                if len(rs) > len(ref_rounds): ref_rounds=rs
            rounds=[]
            for ds, label in ref_rounds:
                d0=datetime.date.fromisoformat(ds)
                if d0 >= TODAY:
                    rounds.append({'d':ds,'label':label,'est':False})
                    continue
                # Keep stepping by the venue's own period until the date is
                # ahead of today. Every venue gets a date, however far out.
                for k in range(1, 13):
                    bump=period*k
                    try: cand=d0.replace(year=d0.year+bump)
                    except ValueError: cand=d0.replace(year=d0.year+bump, day=28)
                    if cand >= TODAY:
                        rounds.append({'d':cand.isoformat(),'label':label,'est':True,'from':ds})
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
                             'year':u_yr,'link':u_lk,'abstract':u_ab})
            real_labels={norm_lab(r['label']) for r in real if r['label']}
            real_days=sorted(datetime.date.fromisoformat(r['d']) for r in real)
            # Proximity window scales with how close together the rounds sit.
            # VLDB runs monthly, so a flat 45 days would swallow its neighbours.
            ref_days=sorted(datetime.date.fromisoformat(d) for d, _ in ref_rounds)
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
                keep.append(e)
            keep.sort(key=lambda x: x['d'])
            cap=max(len(ref_rounds), len(real))
            rounds = real + keep[:max(0, cap - len(real))]
            rounds.sort(key=lambda x: x['d'])
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
            # Count rounds only within the edition being shown. Taking the max
            # across every edition flagged AAAI, whose old NeurIPS fast track
            # looks like a second cycle but no longer exists.
            ref = next((e for e in confs if e.get('year')==(nxt[1] if nxt else None)), latest if confs else {})
            tl_ref = ref.get('timeline') or []
            labels=[(t.get('comment') or '').strip() for t in tl_ref]
            deadlines_in_ref={dstr(t.get('deadline')) for t in tl_ref if dstr(t.get('deadline'))}
            cycles=len(deadlines_in_ref) if len(deadlines_in_ref)>1 else 1
            roundLabels=[l for l in labels if l] if cycles>1 else []
            hist=sorted((csc_rates.get(t) or rates.get(t, {})).items())
            rsrc='csc' if t in csc_rates else ('ar' if t in rates else '')
            off=official(t,d); mirror=canon(r.get('core','N'))
            out.append({
                'title':t, 'desc':d, 'area':area(sub,t),
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
                'date': latest.get('date',''), 'place': latest.get('place',''),
                'cc': flag(latest.get('place','')),
                'city': city_note(latest.get('place','')),
                'cycles': cycles, 'roundLabels': roundLabels,
                'proceedings': 'full',
                'rates': [{'y':y,'r':v} for y,v in hist],
                'rateSection': rate_section.get(t,''),
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
  'date':'November 1-4, 2026','place':'San Francisco, California, USA',
  'note':'The main annual gathering for operations research and analytics, around 6,000 attendees. The date shown is the abstract deadline.',
  'link':'https://meetings.informs.org/'},
 {'title':'SIAM MDS','desc':'SIAM Conference on Mathematics of Data Science',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-05-18','period':2,
  'date':'November 16-20, 2026','place':'Salt Lake City, Utah, USA',
  'note':'Biennial, even years. Where the mathematical side of data science meets. The date shown is the abstract deadline.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/mds26/'},
 {'title':'SIAM CSE','desc':'SIAM Conference on Computational Science and Engineering',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-08-25','period':2,
  'date':'February 22-26, 2027','place':'Pittsburgh, Pennsylvania, USA',
  'note':'Biennial, odd years. The largest SIAM meeting and the main venue for scientific machine learning. The date shown is the abstract deadline.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/cse27/'},
 {'title':'SIAM UQ','desc':'SIAM Conference on Uncertainty Quantification',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2025-09-22','period':2,
  'note':'Biennial, even years. The central applied-maths meeting for UQ. UQ26 ran March 2026 in Minneapolis and UQ28 is not yet announced. The date shown is the abstract deadline.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/uq26/'},
 {'title':'SIAM Annual Meeting','desc':'SIAM Annual Meeting (AN)',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-02-16','period':1,
  'note':'Yearly, all of applied mathematics in one room. AN26 ran July 2026 in Cleveland and AN27 is not yet announced. The date shown is the abstract deadline.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/an26/'},
 {'title':'SIAM OP','desc':'SIAM Conference on Optimization',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2025-11-13','period':3,
  'note':'Triennial. OP26 ran June 2026 in Edinburgh, so the next edition falls around 2029. The date shown is the abstract deadline.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/op26/'},
 {'title':'ICIAM','desc':'International Congress for Industrial and Applied Mathematics',
  'area':'Society meetings','proceedings':'none','lastDeadline':'2026-12-07','period':4,
  'date':'July 12-16, 2027','place':'The Hague, Netherlands',
  'note':'Every four years, the field-wide congress of applied mathematics, around 4,000 participants. The date shown is the abstract deadline, which is published.',
  'link':'https://iciam2027.org/'},

 # Full proceedings, but too new or too far outside the catalogues to carry
 # a CCF or CORE rank. lastDeadline is the most recent published deadline;
 # the page rolls it forward and marks the result as an estimate.
 {'title':'COLM', 'equivalent':'CCF B / CORE A','desc':'Conference on Language Modeling','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Full proceedings. Founded 2024, too new for either ranking table.',
  'lastDeadline':'2026-03-31','link':'https://colm.cc/'},
 {'title':'MLSys', 'equivalent':'CCF B / CORE A','desc':'Conference on Machine Learning and Systems','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Full proceedings. Unranked by both CCF and CORE despite being the main ML-systems venue.',
  'lastDeadline':'2025-10-30','link':'https://mlsys.org/'},
 {'title':'AMIA', 'equivalent':'CCF B / CORE A','desc':'AMIA Annual Symposium','area':'Medicine, Biology & Genetics',
  'proceedings':'full','note':'Full proceedings, indexed in PubMed. The central US biomedical-informatics meeting.',
  'lastDeadline':'2026-03-10','link':'https://amia.org/education-events/amia-annual-symposium'},
 {'title':'ASONAM', 'ccfManual':'C','coreManual':'B','desc':'IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Ranked CCF C / CORE B, so below this page\'s usual bar, but it is the dedicated social-network analysis venue.',
  'lastDeadline':'2026-05-10','link':'https://asonam.cpsc.ucalgary.ca/2026/CFP.php'},
]

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
    nd, ny, est = roll(n.get('lastDeadline',''), n.get('period',1))
    n.update({'ccf':n.get('ccfManual','N'),'core':n.get('coreManual','N'),'coreVerified':False,'nextAbstract':'',
              'cycles':1,'roundLabels':[],'rates':[],'rateSection':'','rateSrc':'','rateSlug':'','rounds':[],'dblp':'','best':'','csr':'','edition':'',
              'estimated':est,'estFrom':n.get('lastDeadline','') if est else '',
              # For a society meeting the deadline year is not the edition
              # year, so do not print one. The date string names the edition.
              'nextDeadline':nd,'nextYear':(None if n['proceedings']=='none' else ny),
              'notable':True})
    n.setdefault('date',''); n.setdefault('place','')
    n['cc']=flag(n['place'])
    n['city']=city_note(n['place'])
    # An emerging venue carries a stated equivalence so it sorts with its peers;
    # a society meeting has no proceedings, so no tier is claimed for it.
    n['tier'] = 2 if n['equivalent'] else tier_of(n['ccf'], n['core'])

for c in out: c['tier']=tier_of(c['ccf'], c['core'])

CORE_ORDER={'A*':0,'A':1,'B':2,'C':3,'TBR':4,'JP':5,'N':6}
CCF_ORDER={'A':0,'B':1,'C':2,'N':3}
def listed(c): return c['core'] in ('A*','A') or c['ccf'] in ('A','B')
# inside an area, soonest deadline first; anything without one trails behind
def dkey(c): return (0, c['nextDeadline']) if c['nextDeadline'] else (1, c['title'].lower())
emerging=[n for n in NOTABLE if n['proceedings']=='full']
society=[n for n in NOTABLE if n['proceedings']=='none']
# One list, ordered by date alone — the reader filters by field in the page.
ranked=sorted([c for c in out if listed(c)] + emerging, key=dkey)
others=sorted([c for c in out if not listed(c)], key=lambda c:(CORE_ORDER[c['core']], CCF_ORDER[c['ccf']], c['title'].lower()))
notable=sorted(society, key=lambda c:(c['area'], c['title']))

hdr=("// Generated by scripts/build-conferences.py — do not edit by hand.\n"
     "// CCF ranks mirror the CCF catalogue via github.com/ccfddl/ccf-deadlines.\n"
     "// CORE ranks are cross-checked against the official CORE2023 export from\n"
     "// portal.core.edu.au. Acceptance rates come from\n"
     "// github.com/lixin4ever/Conference-Acceptance-Rate (main track only).\n"
     f"// Built {TODAY.isoformat()}.\n")
body=(hdr + "export const ranked = %s;\n\nexport const others = %s;\n\n"
      "// Hand-maintained; the ranking tables do not reach these.\nexport const notable = %s;\n"
      % tuple(json.dumps(x, indent=2, ensure_ascii=False) for x in (ranked, others, notable)))
open('../src/data/conferences.js','w').write(body)
import collections as _c
print('\nwritten | listed', len(ranked), '| folded', len(others), '| society', len(notable))
print('tiers:', dict(sorted(_c.Counter(c['tier'] for c in ranked).items())))
print('areas:', dict(_c.Counter(c['area'] for c in ranked)))
