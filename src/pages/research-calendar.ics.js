import { deadlines, kindLabels } from '../data/deadlines.js';

// RFC 5545 wants CRLF line endings and lines folded at 75 octets, with the
// continuation indented by one space.
const fold = (line) => {
  const out = [];
  let rest = line;
  while (Buffer.byteLength(rest, 'utf8') > 75) {
    let cut = 75;
    while (Buffer.byteLength(rest.slice(0, cut), 'utf8') > 75) cut -= 1;
    out.push(rest.slice(0, cut));
    rest = ` ${rest.slice(cut)}`;
  }
  out.push(rest);
  return out;
};

const esc = (text) => String(text).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n');
const stamp = (y, m, d) => `${y}${String(m + 1).padStart(2, '0')}${String(d).padStart(2, '0')}`;
const slug = (text) => text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

export function GET() {
  const now = new Date();
  const dtstamp = `${now.toISOString().slice(0, 19).replace(/[-:]/g, '')}Z`;

  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Zhiqian Chen//Research Calendar//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'X-WR-CALNAME:Research Calendar — Zhiqian Chen',
    'X-WR-TIMEZONE:America/New_York',
  ];

  deadlines.forEach((mo) => {
    mo.items.forEach((item) => {
      // All-day event: DTEND is exclusive, so it points at the following day.
      const end = new Date(Date.UTC(mo.y, mo.m, item.d + 1));
      lines.push(
        'BEGIN:VEVENT',
        `UID:${stamp(mo.y, mo.m, item.d)}-${slug(item.name)}@zhiqian.ai`,
        `DTSTAMP:${dtstamp}`,
        `DTSTART;VALUE=DATE:${stamp(mo.y, mo.m, item.d)}`,
        `DTEND;VALUE=DATE:${stamp(end.getUTCFullYear(), end.getUTCMonth(), end.getUTCDate())}`,
        `SUMMARY:${esc(item.name)}${item.est ? ' (estimated)' : ''}`,
        `CATEGORIES:${esc(kindLabels[item.kind] ?? item.kind)}`,
        `DESCRIPTION:${esc(kindLabels[item.kind] ?? item.kind)}${item.est ? esc('. Date is an estimate; verify against the call.') : esc('. Verify against its own solicitation.')}`,
        'TRANSP:TRANSPARENT',
        'END:VEVENT',
      );
    });
  });

  lines.push('END:VCALENDAR');

  return new Response(lines.flatMap(fold).join('\r\n') + '\r\n', {
    headers: {
      'Content-Type': 'text/calendar; charset=utf-8',
      'Content-Disposition': 'attachment; filename="research-calendar.ics"',
    },
  });
}
