#!/usr/bin/env python3
"""Turn the three Drive sources into public funding data.

Everything written here is served at zhiqian.ai/funding, so the one rule this
script enforces is that nothing personal survives the trip. The Drive brief is
written for one reader: it names him, it scores every opportunity against his
own research lines, and its headline section is strategy advice. None of that
belongs on a public page, and none of it is in the output.

Dropped on purpose, listed so the omission stays deliberate:

  - the "对象: <name>, <institution>" line
  - the 匹配度 column, a 1 to 10 personal fit score
  - the 本周头条 section, which is personal strategy end to end
  - the pointer to the private full report and its 低匹配项 count
  - the watchlist research_lines column, which keys rows to personal interests

What survives is the part that is true for anybody: who funds it, what it is
called, when it closes, how much, who may apply, how crowded it looks, and
where to read the call.

Usage: build-funding.py <brief.txt> <registry.txt> <watchlist.csv>
"""

import csv
import io
import json
import pathlib
import re
import sys
import html as html_mod
import struct
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'src' / 'data'
PUBLIC = ROOT / 'public' / 'funding'

# The brief's table, left to right. 'skip' is the personal fit score.
COLUMNS = ['sponsor', 'program', 'deadline', 'budget', 'eligibility',
           'skip', 'competition', 'source_tier', 'url']

CJK = re.compile(r'[\u4e00-\u9fff]')

# The Drive brief is written in Chinese. The page is not, so everything that
# crosses over gets translated here.
#
# Three layers, in order. EXACT covers the phrasings the brief actually uses,
# which is a small and formulaic vocabulary, and gives readable English.
# GLOSSARY is the fallback for wordings not seen before, applied longest
# phrase first so that 每年 is taken before 年. Whatever still carries a Chinese
# character after both is dropped from the output rather than published, and
# named in the run log so the term can be added. check_english() is the
# backstop that fails the run if anything slips past all three.
EXACT = {
    # competition
    '高': 'high', '中': 'medium', '低': 'low',
    '中到高': 'medium to high', '低到中': 'low to medium',
    # budget
    '未列': 'not listed',
    '无上限, 最长 5 年': 'no cap, up to 5 years',
    '最多 $1M, 最长 4 年': 'up to $1M, up to 4 years',
    '总额 $100M, 最长 5 年': '$100M total, up to 5 years',
    '总额 $110M, 最长 5 年': '$110M total, up to 5 years',
    '约 $245K 到 $250K 每年, 36 个月': 'about $245K to $250K per year, 36 months',
    '$150K 到 $350K 每年': '$150K to $350K per year',
    '年直接费用低于 $500K': 'annual direct costs under $500K',
    '每年最多 $903,954': 'up to $903,954 per year',
    '单项 $3M 到 $35M': '$3M to $35M per award',
    '最多 $20,000 额度': 'up to $20,000 in credits',
    '起步 $5,000 额度': 'from $5,000 in credits',
    '$3,850 每周 4 个月加算力': '$3,850 per week for 4 months, plus compute',
    '12 个月算力': '12 months of compute',
    '奖金 $12,500': '$12,500 prize',
    '节点时': 'node hours',
    '随宿主项目': 'follows the host program',
    '最多 $50,000': 'up to $50,000',
    '最高 $10M': 'up to $10M',
    '$10K 到 $150K': '$10K to $150K',
    '$1M 到 $1.3M': '$1M to $1.3M',
    '$50K 到 $3M': '$50K to $3M',
    '$5K 到 $35K': '$5K to $35K',
    # eligibility
    '开放': 'open',
    '全开放': 'fully open',
    '高校可投': 'universities eligible',
    '高校可投, 非限额': 'universities eligible, not a limited submission',
    '无人数限制': 'no cap on applicants',
    '无人数或机构限制': 'no cap on applicants or institutions',
    '每人 12 个月内最多 2 份, 非限额': 'at most 2 per person in 12 months, not a limited submission',
    '限额, 每机构 3 份': 'limited submission, 3 per institution',
    '限额, 每校 2 份': 'limited submission, 2 per campus',
    '仅 ESI, 新方向, 禁止预实验数据': 'ESI only, genuinely new direction, no preliminary data',
    '早期研究者, ESI 7 年内': 'early career, within 7 years of ESI status',
    '仅设备': 'equipment only',
    '学术研究者': 'academic researchers',
    '美国机构研究者': 'researchers at US institutions',
    '适合博士生或博后': 'suited to PhD students and postdocs',
    '训练开源权重 LLM': 'training open-weight LLMs',
    '须开源': 'must be open source',
    '需注册 AUP': 'requires an AUP registration',
    '需基础到临床团队': 'requires a bench-to-clinic team',
    '以 AI 风险为框架': 'framed around AI risk',
    '列出 AI 与图模型': 'names AI and graph models',
    'PI 需 UR 主聘': 'PI must hold a primary UR appointment',
    '标题以 "Genesis Mission:" 开头': 'title must begin with "Genesis Mission:"',
    # sponsors and programme names
    'NIH (含 NIA NIDCD NLM)': 'NIH (NIA, NIDCD, NLM)',
    'NSF 跨学部': 'NSF cross-directorate',
    # early signals
    'NIDCD Strategic Plan 2028 到 2032 RFI, 评论截止 2026-10-26':
        'NIDCD strategic plan 2028 to 2032 RFI, comments due 2026-10-26',
    'NSF X-Labs 未来主题 RFI, 截止 2026-10-30':
        'NSF X-Labs future topics RFI, closes 2026-10-30',
    'NSF SINI (PCLNet 下, 最多 $75M 5 年) 即将发布':
        'NSF SINI, under PCLNet, up to $75M over 5 years, release expected',
    'AI Forge (DARPA, NSF, NIST CAISI) 尚无征集':
        'AI Forge (DARPA, NSF, NIST CAISI), no solicitation yet',
    'NIH DP2 New Innovator RFA-RM-28-002 预计 2027-08-19 截止':
        'NIH DP2 New Innovator RFA-RM-28-002, expected to close 2027-08-19',
    'NIH Bridge2AI Stage 2 RFA-RM-28-010 预计 2027-03-01 截止':
        'NIH Bridge2AI Stage 2 RFA-RM-28-010, expected to close 2027-03-01',
    'DARPA YFA 2027 尚未发布': 'DARPA YFA 2027 not released yet',
}

GLOSSARY = [
    ('每月 15 日', '15th of each month'), ('每月评审', 'reviewed monthly'),
    ('白皮书', 'white paper'), ('预告', 'forecast'), ('至 ', 'through '),
    ('年直接费用低于', 'annual direct costs under'), ('随宿主项目', 'follows the host program'),
    ('无人数或机构限制', 'no cap on applicants or institutions'), ('无人数限制', 'no cap on applicants'),
    ('高校可投', 'universities eligible'), ('学术研究者', 'academic researchers'),
    ('美国机构研究者', 'researchers at US institutions'), ('即将发布', 'release expected'),
    ('尚无征集', 'no solicitation yet'), ('尚未发布', 'not released yet'),
    ('评论截止', 'comments due'), ('未来主题', 'future topics'),
    ('个月算力', 'months of compute'), ('加算力', 'plus compute'),
    ('非限额', 'not a limited submission'), ('限额', 'limited submission'),
    ('无上限', 'no cap'), ('未列', 'not listed'), ('节点时', 'node hours'),
    ('每年', 'per year'), ('每周', 'per week'), ('每月', 'per month'),
    ('最多', 'up to'), ('最高', 'up to'), ('最长', 'up to'), ('起步', 'from'),
    ('总额', 'total'), ('单项', 'per award'), ('奖金', 'prize'), ('额度', 'in credits'),
    ('预计', 'expected'), ('截止', 'deadline'), ('开放', 'open'), ('同上', 'same as above'),
    ('滚动', 'rolling'), ('随时', 'anytime'), ('目标日', 'target date'),
    ('个月', ' months'), ('年', ' years'), ('约', 'about'), ('到', ' to '), ('含', 'including'),
    ('中到高', 'medium to high'), ('低到中', 'low to medium'),
    ('高', 'high'), ('中', 'medium'), ('低', 'low'),
]


def to_english(value):
    """Return English, or '' when a Chinese term survives translation."""
    v = (value or '').strip()
    if not v or not CJK.search(v):
        return v
    if v in EXACT:
        return EXACT[v]
    for zh, en in GLOSSARY:
        v = v.replace(zh, en)
    v = re.sub(r'\s+', ' ', v).replace(' ,', ',').strip()
    return '' if CJK.search(v) else v

CAVEAT = ('Entries marked unverified were not confirmed against a primary page. '
          'The sponsor site is the authority; this is only an index.')


# Published funding rates, and only published ones.
#
# A funding rate is the share of competitively reviewed proposals that get
# funded. It is worth showing because it is the one number that says how long
# the odds are, and it is dangerous to invent, so nothing here is estimated:
# each entry is a figure the funder itself publishes, with the arithmetic and
# the source alongside it.
#
# Checked 2026-10-15:
#
#   NIH  publishes success rates in the NIH Data Book, pulled here straight
#        from its own API (report 29, R01-equivalent). FY2025 is 5,471 awards
#        from 42,022 applications. All research project grants together, its
#        report 20, land on the same 13% from 8,161 of 62,592.
#
#   NSF  does not have a comparable published actual. Its Funding Profile
#        prints a funding rate, but that table is explicitly an estimate: the
#        FY2025 request projected 27%, while the year appears to have come in
#        far lower. NSF by the Numbers carries actuals, as a Tableau embed
#        with no queryable endpoint and no FY2025 data. So NSF rows say
#        nothing rather than repeat a projection as though it were a result.
#
#   Everyone else, DoD and DARPA through the foundations and the industry
#        programmes, publishes no rate at all.
#
# The honest consequence is that this column is mostly empty. An empty cell
# here means the funder does not publish the number, not that the odds are
# unknown to be bad.
FUNDING_RATES = [
    (re.compile(r'^NIH\b', re.I), re.compile(r'grants\.nih\.gov|simpler\.grants\.gov|federalregister', re.I), {
        'rate': '13%',
        'basis': 'NIH-wide R01-equivalent success rate, FY2025: 5,471 awards '
                 'from 42,022 applications. Not this call\'s odds, and '
                 'individual institutes differ.',
        'source': 'https://report.nih.gov/nihdatabook/category/10',
        'source_name': 'NIH Data Book',
    }),
]


def funding_rate(row):
    for sponsor_re, url_re, info in FUNDING_RATES:
        if sponsor_re.search(row.get('sponsor', '')) and url_re.search(row.get('url', '')):
            return info
    return None


# ---------------------------------------------------------------- logos ----
#
# Each row gets its funder's mark, fetched here at build time and served from
# this site. Hotlinking an icon service would put a request to a third party
# on every row of the page and hand them the reader's browsing, which is not a
# trade worth making for a favicon.
#
# The domain is taken from the call's own url, except where that url points at
# a portal. Twenty-two of the rows link through simpler.grants.gov, and the
# grants.gov logo on an NIH, DARPA and DoD row alike would be worse than no
# logo at all, so those resolve through the sponsor instead.
LOGO_DIR = ROOT / 'public' / 'funding' / 'logos'

PORTALS = {'simpler.grants.gov', 'grants.gov', 'sam.gov', 'federalregister.gov',
           'govcontractfinder.com', 'job-boards.greenhouse.io', 'greenhouse.io',
           # A trade-press write-up is not the funder either, and its masthead
           # on a DARPA or DOE row would be a plain error.
           'nextgov.com', 'analyticsinsight.net', 'builtin.com', 'bwcoconsulting.com'}

SPONSOR_DOMAIN = [
    (re.compile(r'^NIGMS', re.I), 'nigms.nih.gov'),
    (re.compile(r'^NIH|^FNIH', re.I), 'nih.gov'),
    (re.compile(r'^DARPA', re.I), 'darpa.mil'),
    (re.compile(r'^ARPA-H', re.I), 'arpa-h.gov'),
    (re.compile(r'^AFOSR|^AFRL', re.I), 'afrl.af.mil'),
    (re.compile(r'^ARL|^ARO\b', re.I), 'arl.army.mil'),
    (re.compile(r'^ONR\b', re.I), 'onr.navy.mil'),
    (re.compile(r'^DoD\b|^DOD\b', re.I), 'defense.gov'),
    (re.compile(r'^DOE\b', re.I), 'energy.gov'),
    (re.compile(r'^NOAA', re.I), 'noaa.gov'),
    (re.compile(r'^NASA', re.I), 'nasa.gov'),
    (re.compile(r'^NIST', re.I), 'nist.gov'),
    (re.compile(r'^NSF\b', re.I), 'nsf.gov'),
    (re.compile(r'^ACL\b', re.I), 'acl.gov'),
    (re.compile(r'^Anthropic', re.I), 'anthropic.com'),
    (re.compile(r'^Amazon', re.I), 'amazon.science'),
    (re.compile(r'^Google', re.I), 'google.com'),
    (re.compile(r'^Microsoft', re.I), 'microsoft.com'),
    (re.compile(r'^NVIDIA', re.I), 'nvidia.com'),
    (re.compile(r'^Genesis Mission', re.I), 'energy.gov'),
    (re.compile(r'^Mercor', re.I), 'mercor.com'),
    (re.compile(r'^AMD\b', re.I), 'amd.com'),
]

# Both services answer a miss with a generic globe rather than a 404 body, so
# the placeholder is recognised by content and discarded.
PLACEHOLDER_SIZES = {726, 1478}
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36 zhiqian.ai-logo-fetch')


# What kind of body is paying. A federal solicitation, a state programme, a
# private foundation and a company's credit grant are different animals with
# different rules, and the sponsor's name alone does not say which. Decided
# here from the name and the funder's own domain, most specific rule first.
CATEGORIES = [
    ('State',      re.compile(r'^nys\b|^nyserda|empire state', re.I), re.compile(r'\.ny\.gov$|\.state\.[a-z]{2}\.us$')),
    ('University', re.compile(r'^rit\b|ctsi|university', re.I), re.compile(r'\.edu$|\.ac\.uk$')),
    # A "Foundation for X" is private money even when X is a federal agency,
    # which is the whole point of FNIH, so this has to come before Federal.
    ('Foundation', re.compile(r'foundation|^fnih$|^blavatnik|^arnold ventures|^dana\b|^simons\b|^keck|^oticon|^humboldt|^iliad\b|^lightcone|^gtr\b', re.I),
                   re.compile(r'foundation|^wmkeck|^dana\.org|^thebrf|^rrf\.org|^alzdiscovery|^johnahartford|^blavatnikawards|^fnih|^simonsfoundation|^arnoldventures|^orau\.org|williamdemantfonden')),
    ('Federal',    re.compile(r'^(nsf|nih|darpa|arpa-h|doe|dod|onr|afosr|afrl|arl|aro|nasa|nist|noaa|nij|acl|nigms|iarpa|epa|usda|ahrq|cdc|fda|neh|genesis mission)\b', re.I),
                   re.compile(r'\.gov$|\.mil$')),
    ('Public (non-US)', re.compile(r'^aria$|^cifar$', re.I), re.compile(r'^aria\.org\.uk$|^cifar\.ca$')),
    ('Industry',   re.compile(r'^(amd|amazon|anthropic|google|microsoft|nvidia|openai|qualcomm|cisco|cohere|lambda|modal|nebius|mercor|thinking machines|astralis|humanity ai|unconventional ai)\b', re.I),
                   re.compile(r'\.(com|ai|io)$')),
]


def category_of(sponsor, domain):
    for label, name_re, dom_re in CATEGORIES:
        if name_re.search(sponsor or '') or dom_re.search(domain or ''):
            return label
    if (domain or '').endswith('.org'):
        return 'Nonprofit'
    return ''


def logo_domain(row):
    host = urllib.parse.urlparse(row.get('url', '')).netloc.lower()
    host = host[4:] if host.startswith('www.') else host
    if host and host not in PORTALS:
        return host
    for pat, dom in SPONSOR_DOMAIN:
        if pat.search(row.get('sponsor', '')):
            return dom
    return ''


# Domains that answered with nothing usable. Kept in the repo so a weekly run
# does not spend a minute re-asking the same dead hosts, and so a funder that
# later grows an icon can be picked up by deleting its line.
MISSES = LOGO_DIR / 'no-logo.txt'


def _dims(body):
    """Pixel size of a PNG, ICO or JPEG without pulling in an image library."""
    if body[:8] == b'\x89PNG\r\n\x1a\n':
        w, h = struct.unpack('>II', body[16:24])
        return w, h
    if body[:2] == b'\xff\xd8':
        i = 2
        while i + 9 < len(body):
            if body[i] != 0xFF:
                i += 1
                continue
            marker, length = body[i + 1], struct.unpack('>H', body[i + 2:i + 4])[0]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack('>HH', body[i + 5:i + 9])
                return w, h
            i += 2 + length
        return (0, 0)
    if body[:4] == b'\x00\x00\x01\x00':
        best = (0, 0)
        for i in range(struct.unpack('<H', body[4:6])[0]):
            e = 6 + 16 * i
            w, h = body[e] or 256, body[e + 1] or 256
            if w * h > best[0] * best[1]:
                best = (w, h)
        return best
    return (0, 0)


EXT = {'image/png': 'png', 'image/x-icon': 'ico', 'image/vnd.microsoft.icon': 'ico',
       'image/svg+xml': 'svg', 'image/jpeg': 'jpg', 'image/gif': 'gif', 'image/webp': 'webp'}


def _get(url, limit=400_000):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=6) as r:
            if r.status != 200:
                return None
            body = r.read(limit)
            ctype = (r.headers.get('Content-Type') or '').split(';')[0].strip().lower()
        return body, ctype
    except Exception:
        return None


def _candidates(domain):
    """Icon urls the site declares for itself, best first.

    Favicon services hand back whatever small bitmap they cached, which is how
    this page ended up with a 16x24 DARPA mark and a 32x32 NSF one. A site's
    own <link rel="icon"> usually points at something far better, and often at
    an SVG, which is the only thing that stays sharp at any size on any
    screen. So the site is asked first and the services are the fallback.
    """
    out = []
    got = _get(f'https://{domain}/', limit=300_000)
    if got:
        html = got[0].decode('utf-8', 'replace')
        for m in re.finditer(r'<link\b[^>]*>', html, re.I):
            tag = m.group(0)
            rel = re.search(r'rel\s*=\s*["\']([^"\']+)', tag, re.I)
            href = re.search(r'href\s*=\s*["\']([^"\']+)', tag, re.I)
            if not rel or not href:
                continue
            rels = rel.group(1).lower()
            if 'icon' not in rels:
                continue
            url = urllib.parse.urljoin(f'https://{domain}/', href.group(1))
            # An SVG icon beats every bitmap; after that, bigger is better, and
            # apple-touch-icon is normally the largest bitmap a site publishes.
            score = 3 if url.lower().endswith('.svg') else 2 if 'apple' in rels else 1
            size = re.search(r'sizes\s*=\s*["\'](\d+)', tag, re.I)
            out.append((score, int(size.group(1)) if size else 0, url))
        out.sort(key=lambda x: (-x[0], -x[1]))
    urls = [u for _, _, u in out][:4]
    urls += [f'https://www.google.com/s2/favicons?domain={domain}&sz=256',
             f'https://icons.duckduckgo.com/ip3/{domain}.ico']
    return urls


def _best_icon(domain):
    """Largest icon the domain offers, as (rank, bytes, extension) or None."""
    best = None
    for url in _candidates(domain):
        got = _get(url)
        if not got:
            continue
        body, ctype = got
        if len(body) in PLACEHOLDER_SIZES or len(body) < 100:
            continue
        ext = EXT.get(ctype)
        if not ext and url.lower().endswith('.svg') and b'<svg' in body[:600].lower():
            ext = 'svg'
        if not ext:
            continue
        if ext == 'svg':
            best = (10_000, body, ext)             # vector wins outright
            break
        w, h = _dims(body)
        rank = min(w, h)
        if best is None or rank > best[0]:
            best = (rank, body, ext)
        if rank >= 128:
            break
    return best


def _measure(path):
    """Smaller side of a stored icon, 9999 for a vector."""
    body = path.read_bytes()
    if path.suffix == '.svg' or b'<svg' in body[:400].lower():
        return 9999
    w, h = _dims(body)
    return min(w, h)


def fetch_logo(domain, known_misses):
    """Save the funder's mark, returning (published path, pixel size)."""
    for existing in LOGO_DIR.glob(f'{domain}.*'):
        if existing.name != 'no-logo.txt':
            return f'/funding/logos/{existing.name}', _measure(existing)
    if domain in known_misses:
        return '', 0
    best = _best_icon(domain)
    # A department's own subdomain often ships nothing but a 16px favicon
    # inherited from a decade ago, which is why NIH and DARPA arrived as
    # blurred smudges. The parent domain is the same organisation and usually
    # keeps a modern one, so it is worth a second ask when the first is poor.
    if (not best or best[0] < 64) and domain.count('.') >= 2:
        parent = domain.split('.', 1)[1]
        if parent.count('.') >= 1 and len(parent.split('.')[0]) > 2:
            alt = _best_icon(parent)
            if alt and (not best or alt[0] > best[0]):
                best = alt
    if not best:
        return '', 0
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    (LOGO_DIR / f'{domain}.{best[2]}').write_bytes(best[1])
    return f'/funding/logos/{domain}.{best[2]}', best[0]


def attach_logos(rows):
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    known = set()
    if MISSES.exists():
        known = {ln.strip() for ln in MISSES.read_text(encoding='utf-8').splitlines() if ln.strip()}

    domains = sorted({d for d in (logo_domain(r) for r in rows) if d})
    # Seventy-odd hosts, most of them government sites that are slow or simply
    # do not answer. One at a time this took longer than the rest of the build
    # put together, so they go out together with a short timeout.
    with ThreadPoolExecutor(max_workers=12) as pool:
        found = dict(zip(domains, pool.map(lambda d: fetch_logo(d, known), domains)))

    missed = sorted(known | {d for d, (path, _) in found.items() if not path})
    MISSES.write_text('\n'.join(missed) + '\n', encoding='utf-8')

    for r in rows:
        dom = r.get('logo_domain') or logo_domain(r)
        r['logo_domain'] = dom
        path, px = found.get(dom, ('', 0))
        # A 16px favicon blown up to the size of two lines of text is a smear.
        # Below this the row is better off with clean initials than with a
        # recognisable logo rendered badly.
        r['logo'] = path if px >= 32 else ''
        r['logo_px'] = px
    got = sum(1 for r in rows if r.get('logo'))
    return got, len(domains)


# A one-line synopsis of what the award actually is.
#
# The registry has no description field, and scraping 134 funder sites for one
# would be slow and brittle. It does not need one: almost every row is a
# standard mechanism, and the mechanism is named in the programme title. An
# R21 is an exploratory project with no preliminary data wherever it appears,
# a DURIP buys equipment and nothing else, a BAA takes white papers all year.
# So the synopsis is looked up from the mechanism, most specific first, and a
# row whose title names no mechanism gets no sentence rather than a vague one.
SYNOPSIS = [
    (r'\bRFI\b',                  'A request for comment, not a funding call.'),
    (r'\bDURIP\b',                'Buys equipment only, with no salary or research costs.'),
    (r'\bMURI\b',                 'A multi-university team on one topic, usually five years.'),
    (r'\bCAREER\b',               'Five years for a pre-tenure faculty member, research and teaching together.'),
    (r'Young Investigator|\bYIP\b', 'A single-PI award for someone within a few years of the PhD.'),
    (r'New Innovator|\bDP2\b',     'A high-risk award for an early-career investigator, no preliminary data.'),
    (r'\bR01\b',                  'A full-scale research project, usually four to five years.'),
    (r'\bR21\b',                  'An exploratory project of up to two years, no preliminary data expected.'),
    (r'\bR03\b',                  'A small project of up to two years.'),
    (r'\bR15\b|\bAREA\b',        'Research at a campus that is not research-intensive, with undergraduates involved.'),
    (r'\bR35\b',                  'One long award in place of several separate grants.'),
    (r'\bRM1\b',                  'A team programme rather than a single-PI project.'),
    (r'\bK\d\d\b',               'A mentored career-development award for one person.'),
    (r'\bF3\d\b|\bT32\b',       'A training award for a student or postdoc.'),
    (r'\bU01\b|\bUM1\b|Cooperative', 'A cooperative agreement, with programme staff involved in the work.'),
    (r'\bR13\b|Conference|Workshop', 'Supports a meeting rather than research.'),
    (r'\bRET\b',                  'Summer research placements for K-12 teachers.'),
    (r'\bREU\b',                  'Research placements for undergraduates.'),
    (r'Expeditions|\bHubs\b|Institute\b', 'A center-scale award for a large multi-investigator team.'),
    (r'Office-Wide|\bBAA\b',       "A standing call across the office's whole portfolio, white paper first."),
    (r'Challenge|Prize|Competition', 'An open competition judged on results, not on a proposal.'),
    (r'credits?|compute|cluster|GPU|model access|Researcher Access|for Academics|allocation|node hours',
                                   'An allocation of compute or model access rather than money.'),
    (r'Graduate Fellowship|\bFellowship\b', 'Supports a named individual rather than a project.'),
    (r'\bPilot\b|\bSeed\b|Bridge', 'A small starter award, usually to produce preliminary data.'),
    (r'Research Award',            'An unrestricted gift to one PI, decided in a single global round.'),
    (r'Translation to Practice|Accelerator', 'Takes existing results toward deployment rather than funding new science.'),
    (r'\bLOI\b|preproposal|Call for Proposals|open call|\bRFP\b', 'An open call, with the funder setting the topic.'),
    # Agency-specific shapes, for the titles that name no generic mechanism
    (r'ARPA-H-SOL|Mission Office ISO', 'An ARPA-H solicitation, judged on a short solution summary first.'),
    (r'DARPA-PS-|DARPA-SN-|\bYFA\b', 'A DARPA programme call, narrow in scope and run to its own schedule.'),
    (r'\bRFA-[A-Z]{2}-', 'An NIH request for applications, one topic and a fixed pot.'),
    (r'\bPAR-\d\d|\bPA-\d\d', 'A standing NIH announcement, open to the usual activity codes.'),
    (r'\bMIRA\b', 'One award covering the whole lab, in place of project-by-project grants.'),
    (r'NSF \d\d-\d\d\d|\bOTA\b|\bDCL\b', 'An NSF solicitation with its own topic and deadline.'),
    (r'\bROSES\b', 'A NASA omnibus call, one element of many under a single solicitation.'),
    (r'\bFIP\b|NIDILRR', 'A disability and rehabilitation research project, three years.'),
    (r'solicitation', 'An agency solicitation.'),
]

KIND_FALLBACK = {
    'Federal': 'A federal research call.',
    'State': 'A New York State programme.',
    'Foundation': 'A private foundation grant.',
    'Industry': 'A company programme.',
    'Nonprofit': 'A nonprofit grant.',
    'University': 'An internal university programme.',
    'Public (non-US)': 'A call from a public funder outside the US.',
}


def tldr(row):
    text = f"{row.get('sponsor', '')} {row.get('program', '')}"
    line = next((s for pat, s in SYNOPSIS if re.search(pat, text, re.I)), '')
    if not line:
        line = KIND_FALLBACK.get(row.get('category', ''), '')
    # Money only when there is a figure. A row that says "an unstated amount"
    # has spent a line telling the reader nothing.
    return line


def award_size(row):
    """What one project gets, kept apart from the programme's whole pot.

    A figure like "$110M total" is what the agency has to spend across every
    award it will make, and printing it against a single call would read as
    the award size. Those go to the note instead, and the per-project cell
    says nothing, which is the true answer.
    """
    money = (row.get('budget') or '').strip()
    if not money or money.lower() in ('not listed', 'same as above'):
        return '', ''
    if re.search(r'\btotal\b', money, re.I):
        pot = re.sub(r'\s*\btotal\b\s*,?\s*', ' ', money, flags=re.I).strip(' ,')
        return '', f'{pot} across the whole programme. Not a per-project figure.'
    if re.search(r'follows the host|per host', money, re.I):
        return '', 'Set by whichever programme hosts the work.'
    return money[0].upper() + money[1:], ''


# ------------------------------------------------- what one award is worth --
#
# The weekly brief carries a budget for the 27 calls it picks out. The other
# hundred-odd rows had nothing, so the column read "not stated" almost all the
# way down, which is false: a federal solicitation always says what an award
# is worth. It is on grants.gov, in structured form, for everything posted
# there.
#
# grants.gov defines awardCeiling and awardFloor as the largest and smallest
# single award, which is precisely this column, and estimatedFunding as the
# whole programme, which is precisely not. Only the first two are used.
#
# Rows are matched by the opportunity number printed in their own title. That
# is exact: no fuzzy name matching, and a hit is accepted only when the
# number comes back identical.
GG_SEARCH = 'https://api.grants.gov/v1/api/search2'
GG_FETCH = 'https://api.grants.gov/v1/api/fetchOpportunity'
AWARD_CACHE = ROOT / 'scripts' / 'award-cache.json'

OPP_PATTERNS = [
    r'\bNSF\s+(\d\d-\d{3})\b',
    r'\b((?:PAR|PA|RFA|NOT)-[A-Z]{2}-\d\d-\d{3})\b',
    r'\b(HHS-\d{4}-[A-Z]+-[A-Z]+-[A-Z]+-\d{4})\b',
    r'\b(DE-FOA-\d{7})\b',
    r'\b(ARPA-H-SOL-\d\d-\d{3})\b',
    r'\b(DARPA-[A-Z]{2}-\d\d-\d{3})\b',
    r'\b(HR\d{9,12})\b',
    r'\b([NW]\d{8,12}[A-Z]{1,3}\d{1,4})\b',
    r'\b(FA\d{6,}[A-Z]\d{4})\b',
    r'\b(W911NF-\d\d-[A-Z]-\d{4})\b',
]


def opp_numbers(row):
    text = f"{row.get('program', '')}"
    out = []
    for pat in OPP_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            n = m.group(1).upper()
            if n not in out:
                out.append(n)
    return out


def _gg_post(url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', 'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def _money(v):
    """grants.gov sends amounts as strings, and 'none' for unspecified."""
    try:
        n = int(float(v))
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def _fmt(n):
    if n >= 1_000_000:
        s = f'{n / 1_000_000:.1f}'.rstrip('0').rstrip('.')
        return f'${s}M'
    if n >= 10_000:
        s = f'{n / 1000:.0f}'
        return f'${s}K'
    return f'${n:,}'


def lookup_award(number):
    """Per-award floor and ceiling from grants.gov, or None."""
    try:
        hits = _gg_post(GG_SEARCH, {'keyword': number, 'rows': 5})['data']['oppHits']
    except Exception:
        return None
    hit = next((h for h in hits if (h.get('number') or '').upper() == number), None)
    if not hit:
        return None
    try:
        data = _gg_post(GG_FETCH, {'opportunityId': int(hit['id'])})['data']
    except Exception:
        return None
    for blk in ('synopsis', 'forecast'):
        b = data.get(blk) or {}
        lo, hi = _money(b.get('awardFloor')), _money(b.get('awardCeiling'))
        if lo or hi:
            return {'floor': lo, 'ceiling': hi,
                    'awards': _money(b.get('numberOfAwards')),
                    'pot': _money(b.get('estimatedFunding')),
                    'number': number}
    return None


def attach_grants_gov(rows):
    cache = {}
    if AWARD_CACHE.exists():
        cache = json.loads(AWARD_CACHE.read_text(encoding='utf-8'))

    wanted = []
    for r in rows:
        for n in opp_numbers(r):
            if n not in cache and n not in wanted:
                wanted.append(n)
    if wanted:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for n, res in zip(wanted, pool.map(lookup_award, wanted)):
                cache[n] = res            # None is cached too, so misses cost once
        AWARD_CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + '\n',
                               encoding='utf-8')

    found = 0
    for r in rows:
        if r.get('award'):
            continue                      # the brief's own figure wins
        for n in opp_numbers(r):
            a = cache.get(n)
            if not a:
                continue
            lo, hi = a.get('floor'), a.get('ceiling')
            if lo and hi and lo != hi:
                r['award'] = f'{_fmt(lo)} to {_fmt(hi)}'
            elif hi:
                r['award'] = f'Up to {_fmt(hi)}'
            elif lo:
                r['award'] = f'From {_fmt(lo)}'
            else:
                continue
            bits = [f"grants.gov lists this per award for {a['number']}."]
            if a.get('awards'):
                bits.append(f"About {a['awards']} awards expected.")
            if a.get('pot'):
                bits.append(f"{_fmt(a['pot'])} for the whole programme.")
            r['award_note'] = ' '.join(bits)
            r['award_src'] = 'grants.gov'
            found += 1
            break
    return found


# NSF states, in two labelled fields on every solicitation page, the whole
# programme's budget and how many awards it expects. It does not state the
# size of one award in any machine-readable way: that lives in prose which
# differs per solicitation, and parsing it was tried and abandoned, because
# on nsf24-569 and nsf24-503 it returned the programme total as though it
# were the award. Publishing that would be a worse answer than none.
#
# What is safe is the division. Total over count is an average award, it is
# arithmetic on two figures NSF itself publishes, and it is labelled as an
# average everywhere it appears rather than being passed off as the award.
NSF_CACHE = ROOT / 'scripts' / 'nsf-cache.json'
NSF_POT = re.compile(r'Anticipated Funding Amount:\s*\$([\d,]+)(?:\s*to\s*\$([\d,]+))?', re.I)
NSF_N = re.compile(r'Estimated Number of Awards:\s*([\d,]+)(?:\s*to\s*([\d,]+))?', re.I)


def nsf_figures(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read(900_000).decode('utf-8', 'replace')
    except Exception:
        return None
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', raw, flags=re.S)
    text = re.sub(r'\s+', ' ', html_mod.unescape(re.sub(r'<[^>]+>', ' ', body)))
    pot, n = NSF_POT.search(text), NSF_N.search(text)
    if not pot or not n:
        return None
    num = lambda x: int(x.replace(',', '')) if x else None
    return {'pot_lo': num(pot.group(1)), 'pot_hi': num(pot.group(2)),
            'n_lo': num(n.group(1)), 'n_hi': num(n.group(2))}


def attach_nsf(rows):
    cache = json.loads(NSF_CACHE.read_text(encoding='utf-8')) if NSF_CACHE.exists() else {}
    urls = sorted({r['url'] for r in rows
                   if not r.get('award')
                   and re.search(r'nsf\.gov/funding/opportunities/.+/nsf\d\d-\d{3}', r.get('url', ''))
                   and r['url'] not in cache})
    if urls:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for u, res in zip(urls, pool.map(nsf_figures, urls)):
                cache[u] = res
        NSF_CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + '\n', encoding='utf-8')

    found = 0
    for r in rows:
        if r.get('award'):
            continue
        f = cache.get(r.get('url'))
        if not f or not f.get('pot_lo') or not f.get('n_lo'):
            continue
        pot_lo, pot_hi = f['pot_lo'], f['pot_hi'] or f['pot_lo']
        n_lo, n_hi = f['n_lo'], f['n_hi'] or f['n_lo']
        lo, hi = pot_lo / max(n_hi, 1), pot_hi / max(n_lo, 1)
        r['award'] = (f'~{_fmt(int(lo))}' if round(lo) == round(hi)
                      else f'~{_fmt(int(lo))} to {_fmt(int(hi))}')
        pot = _fmt(pot_lo) if pot_lo == pot_hi else f'{_fmt(pot_lo)} to {_fmt(pot_hi)}'
        cnt = n_lo if n_lo == n_hi else f'{n_lo} to {n_hi}'
        r['award_note'] = (f'An average, not a stated award size: NSF expects {cnt} '
                           f'awards from {pot} for the whole programme. The '
                           f'solicitation gives the size of one award only in prose.')
        r['award_src'] = 'nsf-average'
        found += 1
    return found


# ------------------------------------------------- who a call is aimed at ---
#
# The sparse funding-rate column is gone. What a reader actually needs before
# clicking is whether the call is even aimed at them, and that is recoverable
# from the row: activity codes and programme names encode the shape of the
# award, institute names encode the subject, and the eligibility line encodes
# who may apply. None of this is guessed; each tag below fires on a token the
# funder itself put in the name.
FIT_RULES = [
    # shape of the award, from the activity code or programme type
    (r'\bR01\b|Parent R01',            'full research project'),
    (r'\bR21\b',                       'exploratory, no preliminary data'),
    (r'\bR03\b',                       'small and short'),
    (r'\bR15\b|\bAREA\b',             'undergraduate-serving campus'),
    (r'\bK\d\d\b',                    'mentored career award'),
    (r'\bDP2\b|New Innovator',         'early-career, high risk'),
    (r'\bF3\d\b|\bT32\b',            'trainee fellowship'),
    (r'\bMURI\b',                      'multi-university team'),
    (r'Young Investigator|\bYIP\b',     'within a few years of the PhD'),
    (r'\bDURIP\b',                     'equipment only'),
    (r'\bBAA\b',                       'white paper first'),
    (r'Expeditions|\bCenter\b|\bHubs\b', 'large multi-PI team'),
    (r'Fellowship',                     'for an individual, not a lab'),
    (r'\bSBIR\b|\bSTTR\b',            'small business partner'),
    (r'Challenge|Prize|Competition',    'contest, not a proposal'),
    (r'credits?|cluster|compute|GPU|NAIRR', 'compute, not cash'),
    (r'\bPilot\b|\bSeed\b|Bridge',    'pilot scale'),
    (r'\bRET\b|Teacher',               'K-12 teacher partners'),
    (r'\bREU\b',                       'undergraduate researchers'),
    (r'\(limited\)|limited submission', 'your institution nominates'),
    # subject, from the institute or directorate
    (r'NIDCD',          'hearing and communication'),
    (r'\bNIA\b|Alzheimer|dementia|ADRD', 'aging and dementia'),
    (r'NCCIH',          'complementary health'),
    (r'NHGRI|genom',    'genomics'),
    (r'\bNLM\b',       'biomedical informatics'),
    (r'NIBIB',          'bioimaging and bioengineering'),
    (r'BRAIN|neuro',    'neuroscience'),
    (r'NIGMS',          'basic biomedical'),
    (r'\bCISE\b',      'core computing'),
    (r'NSF ENG|\bECCS\b|\bCMMI\b', 'engineering'),
    (r'ARPA-H',         'health, high risk'),
    (r'DARPA',          'defense, high risk'),
    (r'\bONR\b|AFOSR|AFRL|\bARL\b|\bARO\b|\bDoD\b', 'defense basic research'),
    (r'\bDOE\b|Genesis Mission', 'energy and scientific computing'),
    (r'NOAA',           'environment and satellites'),
    (r'\bNIJ\b',       'criminal justice'),
    (r'NIST|CHIPS',     'standards and microelectronics'),
    (r'NYSERDA|\bNYS\b|Empire', 'New York State work'),
    # themes that appear in the name itself rather than in an agency code
    (r'AI safety|alignment|existential|corrigibility|Safeguarded|AI risk', 'AI safety and alignment'),
    (r'model access|Researcher Access|API', 'model access, not cash'),
    (r'[Ss]emiconductor|CHIPS|microelectronic|Reliability', 'semiconductors'),
    (r'Digital Health|health technolog', 'digital health'),
    (r'Software', 'research software'),
    (r'\bK-12\b|Teacher', 'K-12 education'),
    (r'Mitochondria|Music as Medicine|SenNet|Precision', 'specific biomedical topic'),
    (r'Collaborat|Consortium|Node', 'team award'),
    (r'Scholars|Faculty Award|National Awards', 'named award for an individual'),
    (r'Global|European|International', 'international scope'),
    (r'\bRFI\b', 'comment, not a proposal'),
    (r'\bLOI\b|preproposal|pre-proposal', 'letter of intent first'),
    (r'\bRFP\b|Call for Proposals|open call|open application|Open Call', 'open call'),
]

# Straight from the eligibility line, which says who may apply in so many words
FIT_FROM_ELIGIBILITY = [
    (r'\bESI\b|early career',      'early-stage investigator only'),
    (r'limited submission',         'your institution nominates'),
    (r'bench-to-clinic',            'clinical partner needed'),
    (r'US institutions',            'US institutions only'),
    (r'PhD students|postdocs',      'for students and postdocs'),
    (r'open source|open-weight',    'must publish openly'),
    (r'equipment only',             'equipment only'),
    (r'primary .* appointment',     'host-institution appointment'),
]

MAX_FIT = 3


def fit_tags(row):
    text = f"{row.get('sponsor', '')} {row.get('program', '')}"
    tags = []
    for pat, tag in FIT_RULES:
        if re.search(pat, text, re.I) and tag not in tags:
            tags.append(tag)
    for pat, tag in FIT_FROM_ELIGIBILITY:
        if re.search(pat, row.get('eligibility', ''), re.I) and tag not in tags:
            tags.append(tag)
    return tags[:MAX_FIT]


# -------------------------------------------------------- how crowded it is -
#
# Every row gets a 1 to 5 reading, because "no estimate" is not useful to
# anyone, but the basis is carried with it and shown on hover. A published
# success rate is not the same kind of claim as a guess from the shape of the
# call, and the page should not let the two look alike.
def _band(pct):
    return 5 if pct < 10 else 4 if pct < 20 else 3 if pct < 35 else 2 if pct < 55 else 1


# An allocation of machine time or model access, as opposed to money.
ACCESS = (r'credits?|cluster|compute|GPU|NAIRR|model access|Researcher Access|'
          r'allocation|node hours|for Academics|API')
# A named, single-round award with a fixed and small number of places.
NAMED_AWARD = r'Award|Fellowship|Grant|Scholar|Catalyst|Innovation|Prize'
# Facts the company does publish, so the estimate is not pulled from nowhere.
AWARD_NOTES = {
    'Amazon': ('Amazon publishes recipients but not applications: 68 awards '
               'worldwide in the Fall 2025 cycle and 75 the year before, across '
               'every topic it funds.'),
}

BRIEF_SCORE = {'high': 4, 'medium to high': 4, 'medium': 3, 'low to medium': 2, 'low': 1}


def competition(row):
    elig = row.get('eligibility', '')
    # An institutional cap means you compete at home before you compete at all.
    if re.search(r'limited submission', elig, re.I) or '(limited)' in row.get('program', ''):
        return 5, 'Limited submission: your institution runs its own competition first.'
    if row.get('rate'):
        pct = float(re.sub(r'[^0-9.]', '', row['rate']) or 0)
        return _band(pct), f"From the funder's published success rate of {row['rate']}. {row.get('rate_basis', '')}"
    graded = (row.get('competition') or '').lower().strip()
    if graded in BRIEF_SCORE:
        return BRIEF_SCORE[graded], f'Graded "{graded}" in this week\'s brief, not a published rate.'
    kind = row.get('category', '')
    prog = row.get('program', '')
    money = row.get('budget', '')
    # What is on offer, not who is paying. Treating every company programme as
    # easy was wrong: Amazon Research Awards, the Microsoft and NVIDIA
    # fellowships and the Qualcomm Innovation Fellowship are single global
    # rounds, and are at least as contested as a federal solicitation. What is
    # genuinely softer is an allocation of credits or model access, which is
    # reviewed on a rolling basis and costs the company little to grant.
    if re.search(ACCESS, prog, re.I) or re.search(ACCESS, money, re.I):
        return 2, ('Estimated from what is on offer: an allocation of compute or '
                   'model access is reviewed as it arrives and turns down far '
                   'fewer applicants than a cash award. No rate is published.')
    if re.search(r'\bBAA\b|rolling|Office-Wide', prog, re.I):
        return 3, ('Estimated from the kind of call: an open BAA takes white papers '
                   'continuously rather than running one round.')
    if kind == 'Industry' and re.search(NAMED_AWARD, prog, re.I):
        note = AWARD_NOTES.get(row.get('sponsor', '').split()[0], '')
        return 4, ('Estimated from what is on offer: a named company award is one '
                   'global round for a fixed and small number of places. ' + note
                   ).strip()
    if kind == 'Federal':
        return 4, ('Estimated from the kind of call: federal research solicitations '
                   'typically fund well under a quarter of what they receive.')
    if kind == 'Industry':
        return 3, 'Estimated from the kind of call, not a published rate.'
    if kind in ('Foundation', 'Nonprofit', 'State'):
        return 3, 'Estimated from the kind of call, not a published rate.'
    return 3, 'Estimated from the kind of call, not a published rate.'
    if kind == 'Industry':
        return 2, 'Estimated from the kind of call: company programmes are usually smaller and less contested than federal ones.'
    return 3, 'Estimated from the kind of call, not a published rate.'


def load(path):
    text = pathlib.Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    if text.lstrip().lower().startswith(('<!doctype', '<html')):
        sys.exit(f"{path}: got an HTML page, the Drive file is probably not "
                 f"shared as 'Anyone with the link'")
    return text


def parse_brief(text):
    """Pull the date, the window and the opportunity table out of the brief."""
    m = re.search(r'AI Funding Brief (\d{4}-\d{2}-\d{2})', text)
    if not m:
        sys.exit("brief heading 'AI Funding Brief YYYY-MM-DD' not found")
    date = m.group(1)

    # The window is a fact about the search, not about the person, so it is
    # lifted out of the 对象 line before that line is discarded.
    window = {}
    w = re.search(r'窗口:\s*(\d{4}-\d{2}-\d{2})\s*以来新发布,\s*或\s*(\d{4}-\d{2}-\d{2})\s*前截止', text)
    if w:
        window = {'new_since': w.group(1), 'deadline_before': w.group(2)}

    rows = []
    for line in text.split('\n'):
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != len(COLUMNS):
            continue
        if cells[0] in ('机构', '') or set(cells[0]) <= set('-: '):
            continue        # header and the --- separator
        row = {k: v for k, v in zip(COLUMNS, cells) if k != 'skip'}
        # 同上 means "as the row above". Resolve it against the real value
        # before translation, or the cell would read "same as above" on a page
        # whose sort order no longer puts that row above it.
        for k, v in row.items():
            if v.strip() == '同上' and rows:
                row[k] = rows[-1][k]
        rows.append(row)

    signals = []
    # The section number moves between brief layouts (3 in the short one, 6 in
    # the full routine report), so match the title and stop at the next heading.
    m = re.search(r'^## \d+\. 早期信号[^\n]*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if m:
        for line in m.group(1).split('\n'):
            line = line.strip()
            if not line.startswith('- '):
                continue
            body = line[2:].strip()
            u = re.search(r'(https?://\S+)$', body)
            signals.append({
                'note': body[:u.start()].rstrip(' :') if u else body,
                'url': u.group(1) if u else '',
            })

    dropped = []
    for r in rows:
        for k, v in list(r.items()):
            if k == 'url':
                continue
            en = to_english(v)
            if not en and v:
                dropped.append(v)
            r[k] = en
    for sig in signals:
        en = to_english(sig['note'])
        if not en and sig['note']:
            dropped.append(sig['note'])
        sig['note'] = en
    signals[:] = [sig for sig in signals if sig['note']]

    return date, window, rows, signals, dropped


def parse_registry(text):
    rows = []
    for line in text.split('\n'):
        if not re.match(r'^\s*\d{4}-\d{2}-\d{2}\s*\|', line):
            continue
        parts = [x.strip() for x in line.split('|')]
        # Anything past the fifth field is part of the url, which can itself
        # contain a pipe. Rejoin rather than truncate.
        parts = parts[:4] + ['|'.join(parts[4:]).strip()]
        rows.append(dict(zip(
            ['first_seen_date', 'sponsor', 'program', 'deadline', 'url'], parts)))
    return rows


def parse_watchlist(text):
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for r in reader:
        r.pop('research_lines', None)       # keys rows to personal interests
        rows.append({k: (v or '').strip() for k, v in r.items() if k})
    return rows


def main():
    brief_p, registry_p, watchlist_p = sys.argv[1:4]
    date, window, opps, signals, dropped = parse_brief(load(brief_p))
    registry = parse_registry(load(registry_p))
    watchlist = parse_watchlist(load(watchlist_p))

    for d in (DATA, PUBLIC):
        d.mkdir(parents=True, exist_ok=True)

    # Every opportunity in the weekly table is also a registry row, so the page
    # can show one list instead of two and the brief's extra columns ride along
    # on the row they belong to. The url alone is not enough of a key: three
    # sponsors list two separate programs behind a single landing page, and
    # matching on url would copy one programme's budget onto the other. Where a
    # url is shared, the programme names have to agree as well.
    def norm(x):
        return [t for t in re.split(r'[^a-z0-9]+', (x or '').lower()) if t]

    by_url = {}
    for r in registry:
        by_url.setdefault(r.get('url', ''), []).append(r)

    for o in opps:
        rows = by_url.get(o.get('url', ''), [])
        if not rows:
            continue
        if len(rows) > 1:
            want = set(norm(o.get('program')))
            scored = sorted(rows, key=lambda r: len(want & set(norm(r.get('program')))),
                            reverse=True)
            best = len(want & set(norm(scored[0].get('program'))))
            if best == 0:
                continue                      # same page, different programme
            rows = [scored[0]]
        target = rows[0]
        target['pick'] = True
        for k in ('budget', 'eligibility', 'competition', 'source_tier'):
            if o.get(k):
                target[k] = o[k]

    logos_found, logo_domains = attach_logos(registry)
    for r in registry:
        r['category'] = category_of(r.get('sponsor', ''), r.get('logo_domain', ''))

    # Attach the published funding rate before anything is serialized.
    for r in registry:
        info = funding_rate(r)
        if info:
            r['rate'] = info['rate']
            r['rate_basis'] = info['basis']
            r['rate_source'] = info['source']
            r['rate_source_name'] = info['source_name']

    # Both of these read the rate and the category, so they run last of the
    # enrichment steps and, like all of it, before anything is serialized.
    for r in registry:
        r['fit'] = fit_tags(r)
        r['comp_score'], r['comp_basis'] = competition(r)
        r['tldr'] = tldr(r)
        r['award'], r['award_note'] = award_size(r)
    gg = attach_grants_gov(registry)
    nsf = attach_nsf(registry)

    data = {
        'date': date,
        'window': window,
        'caveat': CAVEAT,
        'counts': {'opportunities': len(opps), 'early_signals': len(signals),
                   'registry': len(registry), 'watchlist': len(watchlist)},
        'opportunities': opps,
        'early_signals': signals,
        'registry': registry,
        'watchlist': watchlist,
    }
    blob = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    (PUBLIC / 'data.json').write_text(blob, encoding='utf-8')
    (PUBLIC / f'{date}.json').write_text(blob, encoding='utf-8')
    # The page imports this one. Keeping it in src means a missing or malformed
    # brief breaks the build loudly instead of rendering an empty table.
    (DATA / 'funding.json').write_text(blob, encoding='utf-8')

    with open(PUBLIC / 'registry.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['first_seen_date', 'sponsor', 'program',
                                          'deadline', 'url'], extrasaction='ignore')
        w.writeheader()
        w.writerows(registry)

    if watchlist:
        with open(PUBLIC / 'watchlist.csv', 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(watchlist[0].keys()))
            w.writeheader()
            w.writerows(watchlist)

    # A last sweep over everything that will be served. The personal lines are
    # removed structurally above; this is the check that says so out loud, and
    # fails the run rather than publishing a name by accident.
    banned = ['Zhiqian', 'RIT CS', '对象:', '匹配度', '本周头条', 'research_lines']
    for p in list(PUBLIC.glob('*')) + [DATA / 'funding.json']:
        if p.is_dir():
            continue
        body = p.read_text(encoding='utf-8')
        hit = [b for b in banned if b in body]
        if hit:
            sys.exit(f'{p}: personal content leaked into a public file: {hit}')
        # The page is in English. Anything the translation missed should have
        # been dropped above, so a Chinese character here is a bug, not a
        # wording to argue with. Fail rather than publish it.
        zh = sorted(set(CJK.findall(body)))
        if zh:
            sample = [ln.strip() for ln in body.splitlines() if CJK.search(ln)][:3]
            sys.exit(f'{p}: untranslated Chinese reached a public file: '
                     f'{"".join(zh)[:40]} ... e.g. {sample}')

    if dropped:
        print(f'  dropped {len(dropped)} field(s) with no translation, add them '
              f'to EXACT or GLOSSARY in this script:')
        for v in sorted(set(dropped)):
            print(f'    {v}')

    picks = sum(1 for r in registry if r.get('pick'))
    rated = sum(1 for r in registry if r.get('rate'))
    print(f'brief {date}: {len(opps)} opportunities ({picks} matched into the '
          f'registry), {len(signals)} signals, {len(registry)} registry rows '
          f'({rated} with a published funding rate, {logos_found} with a '
          f'logo across {logo_domains} domains, {gg} sized from grants.gov, '
          f'{nsf} averaged from NSF), '
          f'{len(watchlist)} '
          f'watchlist rows')


if __name__ == '__main__':
    main()
