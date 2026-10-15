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

    # Attach the published funding rate before anything is serialized.
    for r in registry:
        info = funding_rate(r)
        if info:
            r['rate'] = info['rate']
            r['rate_basis'] = info['basis']
            r['rate_source'] = info['source']
            r['rate_source_name'] = info['source_name']

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
          f'({rated} with a published funding rate), {len(watchlist)} '
          f'watchlist rows')


if __name__ == '__main__':
    main()
