#!/usr/bin/env python3
"""Translate the funding brief's leftover Chinese phrases with the Claude API.

build-funding.py drops any field its phrasebook cannot translate and lists it
in scripts/untranslated.json. This script sends that list to Claude in one
call and merges the answers into scripts/translation-cache.json, which the
build reads on every run, including the unattended one on GitHub Actions.

Run locally, then rebuild:
  ~/.config/harness/run ~/tools/claude-env/bin/python scripts/translate-funding.py
  python3 scripts/build-funding.py brief.txt registry.txt watchlist.csv

Needs HARNESS_API_KEY (the launcher provides it). Logs the call to
~/.config/harness/ledger.csv when that file exists.
"""
import csv, datetime, json, os, pathlib, re, socket, sys
import anthropic

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODO = ROOT / 'scripts' / 'untranslated.json'
CACHE = ROOT / 'scripts' / 'translation-cache.json'
LEDGER = pathlib.Path.home() / '.config' / 'harness' / 'ledger.csv'
MODEL = 'claude-sonnet-5-5'
PRICE = (3, 15)                     # USD per million tokens, input and output
CJK = re.compile(r'[㐀-鿿豈-﫿]')

RULES = """You translate short fields from a Chinese research-funding brief into English for a public web page.
Rules:
- Translate faithfully. Add nothing, drop nothing, no commentary.
- Keep every number, date, amount, ID and proper name exactly. Dates stay as written (2026-11-20).
- Money: "250k USD" becomes "$250K", "1M USD" becomes "$1M", "500K 到 2M/项" becomes "$500K to $2M per award".
- "未核实" means "unverified", "未列" means "not listed", "滚动" means "rolling", "同上" means "same as above".
- Ranges use "to". No em dashes, no en dashes, no semicolons. American spelling. Short, plain wording.
- The output must contain no Chinese characters.
Reply with only a JSON object mapping each input string to its English translation."""


def main():
    todo = json.loads(TODO.read_text(encoding='utf-8')) if TODO.exists() else []
    cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}
    todo = [t for t in todo if t not in cache]
    if not todo:
        print('nothing to translate')
        return

    client = anthropic.Anthropic(api_key=os.environ['HARNESS_API_KEY'])
    msg = client.messages.create(
        model=MODEL, max_tokens=16000, system=RULES,
        messages=[{'role': 'user', 'content': json.dumps(todo, ensure_ascii=False, indent=1)}])
    tin, tout = msg.usage.input_tokens, msg.usage.output_tokens
    cost = (tin * PRICE[0] + tout * PRICE[1]) / 1e6
    if LEDGER.exists():
        with LEDGER.open('a', newline='') as f:
            csv.writer(f).writerow([datetime.date.today().isoformat(), socket.gethostname(),
                                    'translate-funding.py', msg.model, 1, tin, tout, f'{cost:.6f}'])
    # The reply can open with a thinking block, so read the text blocks only.
    text = ''.join(b.text for b in msg.content if b.type == 'text').strip()
    text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text)
    out = json.loads(text)

    added, bad = 0, []
    for zh in todo:
        en = (out.get(zh) or '').strip()
        if not en or CJK.search(en) or re.search(r'[–—;]', en):
            bad.append(zh)
            continue
        cache[zh] = en
        added += 1
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1, sort_keys=True) + '\n',
                     encoding='utf-8')

    print(f'translated {added} of {len(todo)}, {len(bad)} rejected, ${cost:.4f}')
    for zh in bad:
        print(f'  rejected: {zh}')


if __name__ == '__main__':
    sys.exit(main())
