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


# One line a reader can take the whole row from, assembled from fields that
# are already checked rather than written by hand: what you get, who from,
# any restriction worth knowing before clicking, and when it shuts.
KIND_PHRASE = {
    'Federal': 'a federal agency',
    'State': 'New York State',
    'Foundation': 'a private foundation',
    'Industry': 'a company',
    'Nonprofit': 'a nonprofit',
    'University': 'a university',
    'Public (non-US)': 'a public funder outside the US',
}

# Eligibility lines worth repeating in a summary. "open" and "not listed" are
# not, since a one-liner ending "open to anyone" has told you nothing. The
# negative forms matter here: "not a limited submission" is the opposite of a
# restriction and must not be read as one.
TELLING = re.compile(
    r'\bESI\b|early career|bench-to-clinic|US institutions|PhD students|'
    r'postdocs|equipment only|open source|open-weight|appointment|'
    r'small business|undergraduate', re.I)
LIMITED = re.compile(r'(?<!not a )limited submission', re.I)


def tldr(row):
    money = (row.get('budget') or '').strip()
    money = money[0].upper() + money[1:] if money and money != 'not listed' else 'An unstated amount'
    parts = [f"{money} from {KIND_PHRASE.get(row.get('category', ''), 'this funder')}."]

    elig = (row.get('eligibility') or '').strip()
    if elig and (TELLING.search(elig) or LIMITED.search(elig)):
        parts.append(elig[0].upper() + elig[1:] + '.')

    raw = (row.get('deadline') or '').strip()
    if raw and raw.lower() not in ('n/a', 'none', 'none stated', 'tbd'):
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', raw):
            parts.append(f'Closes {raw}.')
        else:
            raw = re.sub(r'^est\b\.?', 'Estimated', raw, flags=re.I)
            parts.append(raw[0].upper() + raw[1:] + '.')
    return ' '.join(parts)

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
    if re.search(r'credits?|cluster|compute|GPU|NAIRR', prog, re.I):
        return 2, 'Estimated from the kind of call: compute allocations turn down far fewer applicants than cash does.'
    if re.search(r'\bBAA\b|rolling|Office-Wide', prog, re.I):
        return 3, 'Estimated from the kind of call: an open BAA takes white papers continuously rather than running one round.'
    if kind == 'Federal':
        return 4, 'Estimated from the kind of call: federal research solicitations typically fund well under a quarter of what they receive.'
    if kind in ('Foundation', 'Nonprofit', 'State'):
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
    tail = text.split('## 3. 早期信号', 1)
    if len(tail) == 2:
        for line in tail[1].split('\n'):
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
          f'logo across {logo_domains} domains), {len(watchlist)} '
          f'watchlist rows')


if __name__ == '__main__':
    main()
