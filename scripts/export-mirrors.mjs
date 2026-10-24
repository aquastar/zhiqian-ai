// Write the public mirrors of the site's conference and funding data.
//
//   node scripts/export-mirrors.mjs <out>
//
// fills <out>/conferences and <out>/funding with what the two GitHub repos
// hold: the data as JSON and CSV, a README generated from it, a citation
// file, a licence and an issue form for corrections. The site stays the only
// place the data is edited; .github/workflows/mirror.yml runs this after
// every data change and pushes the result.
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { ranked, notable, journals } from '../src/data/conferences.js';
import { destinations } from '../src/data/destinations.js';
import { DOMAINS, GROUPS } from '../src/data/domains.js';

const OUT = process.argv[2];
if (!OUT) throw new Error('usage: node scripts/export-mirrors.mjs <out>');
const TODAY = new Date().toISOString().slice(0, 10);
const SITE = 'https://zhiqian.ai';
const AUTHOR = { family: 'Chen', given: 'Zhiqian', site: SITE };
const REPOS = { conferences: 'cross-field-conferences', funding: 'computing-research-funding' };

const write = (path, text) => {
  mkdirSync(join(path, '..'), { recursive: true });
  writeFileSync(path, text.endsWith('\n') ? text : text + '\n');
};
const json = (x) => JSON.stringify(x, null, 1);
const cell = (s) => String(s ?? '').replace(/\|/g, '\\|').replace(/\s+/g, ' ').trim();
const csv = (rows, cols) => [cols.join(','), ...rows.map((r) => cols.map((c) => {
  const v = Array.isArray(r[c]) ? r[c].join('; ') : String(r[c] ?? '');
  return /[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v;
}).join(','))].join('\n');

// The licence file is the official CC BY 4.0 text, so GitHub recognises it;
// the attribution line goes in the README.
const LEGALCODE = readFileSync(new URL('./cc-by-4.0.txt', import.meta.url), 'utf8');

const citation = (title, repo, abstract, keywords) => `cff-version: 1.2.0
message: "If you use this data, please cite it as below."
type: dataset
title: "${title}"
abstract: "${abstract}"
authors:
  - family-names: ${AUTHOR.family}
    given-names: ${AUTHOR.given}
    website: "${SITE}"
repository-code: "https://github.com/aquastar/${repo}"
url: "${SITE}"
license: CC-BY-4.0
date-released: "${TODAY}"
keywords:
${keywords.map((k) => `  - ${k}`).join('\n')}
`;

const issueForm = (kind, fields) => `name: Correction
description: Report a wrong or missing ${kind}
labels: [correction]
body:
  - type: markdown
    attributes:
      value: The data here is regenerated from ${SITE}, so pull requests that edit the files would be overwritten. An issue is the way in; fixes land in the next sync.
${fields.map(([id, label, req]) => `  - type: input
    id: ${id}
    attributes:
      label: ${label}
    validations:
      required: ${req}`).join('\n')}
  - type: textarea
    id: what
    attributes:
      label: What is wrong, and what is right
    validations:
      required: true
  - type: input
    id: source
    attributes:
      label: Official page that shows it
    validations:
      required: true
`;

const syncNote = (path) => `> Generated from [zhiqian.ai${path}](${SITE}${path}), which is where the data is
> kept. Do not edit the files here by hand; they are rewritten on every sync.
> Spotted a mistake? [Open a correction](../../issues/new/choose).`;

// ---------- Conferences ----------
{
  const dir = join(OUT, 'conferences');
  const field = Object.fromEntries(DOMAINS.map((d) => [d.id, d]));
  const venue = (v, kind) => ({
    acronym: v.title, name: v.desc, field: v.area, field_label: field[v.area]?.label || v.area, kind,
    next_deadline: v.nextDeadline || '', deadline_estimated: !!v.estimated, abstract_deadline: v.nextAbstract || '',
    conference_dates: v.date || '', place: v.place || '', link: v.link || '',
    ccf: v.ccf && v.ccf !== 'N' ? v.ccf : '', core: v.core && v.core !== 'N' ? v.core : '',
    proceedings: v.proceedings || '', note: v.note || v.why || '',
  });
  const venues = [...ranked.map((v) => venue(v, 'ranked')), ...notable.map((v) => venue(v, 'notable'))];
  const js = journals.map((j) => ({ acronym: j.title, name: j.name, field: j.area, publisher: j.pub || '', issn: j.issn || '',
    ccf: j.ccf || '', citations_per_paper: j.cites ?? '', h_index: j.h ?? '', link: j.link || '' }));
  const fields = DOMAINS.map((d) => ({ id: d.id, label: d.label, group: d.group, notes: d.notes || [] }));

  write(join(dir, 'data/conferences.json'), json(venues));
  write(join(dir, 'data/conferences.csv'), csv(venues, Object.keys(venues[0])));
  write(join(dir, 'data/journals.json'), json(js));
  write(join(dir, 'data/journals.csv'), csv(js, Object.keys(js[0])));
  write(join(dir, 'data/fields.json'), json(fields));
  write(join(dir, 'data/destinations.json'), json(destinations.items));

  const rank = (v) => [v.ccf && `CCF ${v.ccf}`, v.core && `CORE ${v.core}`].filter(Boolean).join(' · ');
  const when = (v) => !v.next_deadline ? 'not published'
    : v.next_deadline < TODAY ? `${v.next_deadline} (passed)`
    : `${v.deadline_estimated ? '~' : ''}${v.next_deadline}`;
  const order = (a, b) => {
    const ka = a.next_deadline >= TODAY ? 0 : a.next_deadline ? 1 : 2;
    const kb = b.next_deadline >= TODAY ? 0 : b.next_deadline ? 1 : 2;
    return ka - kb || a.next_deadline.localeCompare(b.next_deadline) || a.acronym.localeCompare(b.acronym);
  };
  const soon = venues.filter((v) => v.next_deadline >= TODAY && !v.deadline_estimated).sort(order).slice(0, 15);
  const sections = GROUPS.map((g) => {
    const fs = DOMAINS.filter((d) => d.group === g.id);
    return `## ${g.label}\n\n` + fs.map((d) => {
      const vs = venues.filter((v) => v.field === d.id).sort(order);
      if (!vs.length) return '';
      return `### ${d.label}\n\n| Venue | Next deadline | Meeting | Rank |\n|---|---|---|---|\n` +
        vs.map((v) => `| [**${cell(v.acronym)}**](${v.link}) ${cell(v.name)} | ${when(v)} | ${cell(v.conference_dates)}${v.place ? `, ${cell(v.place)}` : ''} | ${rank(v)} |`).join('\n') +
        `\n\n[See ${d.label} on the site](${SITE}/conferences#${d.id})\n`;
    }).filter(Boolean).join('\n');
  }).join('\n');

  write(join(dir, 'README.md'), `# Cross-field conference deadlines

Submission deadlines, meeting dates and places for **${venues.length} conferences and
${js.length} journals across ${DOMAINS.length} fields**, from AI and security to epidemiology,
sleep research, philosophy and theology. Most deadline lists cover computer science only; this
one follows the meetings a researcher working across fields actually needs.

**Browse it as a website:** [by field](${SITE}/conferences) · [on a world map](${SITE}/conferences/destinations)

${syncNote('/conferences')}

Last synced ${TODAY}. A \`~\` marks a deadline estimated from the previous edition; check the
venue's own page before you plan around it.

## Next deadlines

| Venue | Field | Deadline |
|---|---|---|
${soon.map((v) => `| [${cell(v.acronym)}](${v.link}) | ${cell(v.field_label)} | ${v.next_deadline} |`).join('\n')}

${sections}
## Data

| File | What it holds |
|---|---|
| [\`data/conferences.json\`](data/conferences.json) / [\`.csv\`](data/conferences.csv) | Every venue: deadline, dates, place, CCF and CORE rank, link |
| [\`data/journals.json\`](data/journals.json) / [\`.csv\`](data/journals.csv) | The journals each field publishes in, with citation figures |
| [\`data/destinations.json\`](data/destinations.json) | Upcoming editions with coordinates, as drawn on the map |
| [\`data/fields.json\`](data/fields.json) | The ${DOMAINS.length} fields and how each one publishes |

Sources: CCF ranks via [ccf-deadlines](https://github.com/ccfddl/ccf-deadlines), CORE ranks from
the [CORE portal](https://portal.core.edu.au), acceptance figures via
[cs-conf-stats](https://github.com/Xovee/cs-conf-stats), and each venue's own call for papers.

## Cite

If this saves you time, a star helps others find it. To cite the data, use the
"Cite this repository" button on the right, or:

> Zhiqian Chen. *Cross-field conference deadlines*. https://github.com/aquastar/${REPOS.conferences}, ${TODAY.slice(0, 4)}.

Data licensed [CC BY 4.0](LICENSE): reuse it freely, crediting "Cross-field conference deadlines, Zhiqian Chen, ${SITE}".
`);
  write(join(dir, 'LICENSE'), LEGALCODE);
  write(join(dir, 'CITATION.cff'), citation('Cross-field conference deadlines', REPOS.conferences,
    `Submission deadlines, dates and places for conferences and journals across ${DOMAINS.length} fields.`,
    ['conference deadlines', 'call for papers', 'academic conferences', 'interdisciplinary research']));
  write(join(dir, '.github/ISSUE_TEMPLATE/correction.yml'), issueForm('conference or deadline',
    [['venue', 'Conference or journal', true]]));
  write(join(dir, '.github/ISSUE_TEMPLATE/config.yml'), 'blank_issues_enabled: true\n');
}

// ---------- Funding ----------
{
  const dir = join(OUT, 'funding');
  const data = JSON.parse(readFileSync(new URL('../src/data/funding.json', import.meta.url)));
  const ISO = /\d{4}-\d{2}-\d{2}/g;
  // The same reading of the free-text deadline as src/pages/funding/index.astro.
  const read = (text) => {
    const raw = (text || '').trim();
    const dates = (raw.match(ISO) || []).sort();
    const next = dates.find((d) => d >= TODAY) || '';
    return { next, status: next ? 'open' : dates.length || /\bclosed\b|not accepting/i.test(raw) ? 'closed' : 'rolling' };
  };
  const opps = data.registry.map((r) => {
    const dl = read(r.deadline);
    return { sponsor: r.sponsor, program: r.program, category: r.category || '', deadline: r.deadline || '',
      next_deadline: dl.next, status: dl.status, award: r.award || '', summary: r.tldr || '', eligibility: r.eligibility || '',
      link: r.url || '', first_seen: r.first_seen_date || '' };
  });
  const ORDER = { open: 0, rolling: 1, closed: 2 };
  opps.sort((a, b) => ORDER[a.status] - ORDER[b.status] || a.next_deadline.localeCompare(b.next_deadline) || a.sponsor.localeCompare(b.sponsor));
  const watch = data.watchlist.map((w) => ({ funder: w.funder, category: w.category || '', link: w.opportunities_url || '',
    link_verified: (w.url_verified || '').toUpperCase() === 'Y', cycle: w.typical_cycle || '', access: w.access || '' }));

  write(join(dir, 'data/opportunities.json'), json(opps));
  write(join(dir, 'data/opportunities.csv'), csv(opps, Object.keys(opps[0])));
  write(join(dir, 'data/funders.json'), json(watch));
  write(join(dir, 'data/funders.csv'), csv(watch, Object.keys(watch[0])));

  const open = opps.filter((o) => o.status === 'open');
  const rolling = opps.filter((o) => o.status === 'rolling');
  const row = (o) => `| ${o.next_deadline || cell(o.deadline) || 'rolling'} | ${cell(o.sponsor)} | [${cell(o.program) || 'call'}](${o.link}) | ${cell(o.category)} | ${cell(o.award)} |`;
  const head = '| Deadline | Sponsor | Program | Type | Award |\n|---|---|---|---|---|';

  write(join(dir, 'README.md'), `# Computing research funding

Open calls for research funding in AI and computing, from federal agencies, foundations and
industry, swept twice a week. **${open.length} open now, ${rolling.length} rolling**, out of
${opps.length} tracked, plus a watchlist of ${watch.length} funders checked on every sweep.

**Browse it as a website:** [${SITE}/funding](${SITE}/funding)

${syncNote('/funding')}

Last synced ${TODAY} (brief of ${data.date}). ${data.caveat}

## Open calls, soonest first

${head}
${open.map(row).join('\n')}

## Rolling or undated

${head}
${rolling.map(row).join('\n')}

Closed calls stay in [\`data/opportunities.json\`](data/opportunities.json) for reference.

## Data

| File | What it holds |
|---|---|
| [\`data/opportunities.json\`](data/opportunities.json) / [\`.csv\`](data/opportunities.csv) | Every call seen: sponsor, program, deadline, status, award, link |
| [\`data/funders.json\`](data/funders.json) / [\`.csv\`](data/funders.csv) | The funder watchlist: where each posts calls and how often |

## Cite

If this helps, a star helps others find it. To cite the data, use the "Cite this repository"
button on the right, or:

> Zhiqian Chen. *Computing research funding*. https://github.com/aquastar/${REPOS.funding}, ${TODAY.slice(0, 4)}.

Data licensed [CC BY 4.0](LICENSE): reuse it freely, crediting "Computing research funding, Zhiqian Chen, ${SITE}".
`);
  write(join(dir, 'LICENSE'), LEGALCODE);
  write(join(dir, 'CITATION.cff'), citation('Computing research funding', REPOS.funding,
    'Open research funding calls in AI and computing, and a watchlist of funders, swept twice a week.',
    ['research funding', 'grants', 'artificial intelligence', 'computer science']));
  write(join(dir, '.github/ISSUE_TEMPLATE/correction.yml'), issueForm('funding call',
    [['program', 'Sponsor and program', true]]));
  write(join(dir, '.github/ISSUE_TEMPLATE/config.yml'), 'blank_issues_enabled: true\n');
}

console.log('wrote', join(OUT, 'conferences'), join(OUT, 'funding'));
