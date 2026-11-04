// Reads a hand-written meeting date ("Dec 1-4, 2026", "May 31 - June 4,
// 2027", "December 8-10 (Sydney), December 9-11 (Atlanta and Paris), 2026")
// into UTC start and end times. Only the first range and the first year are
// used. Returns null when the string has no usable date, so a caller can
// leave the meeting out instead of guessing.
//
// Shared by the By time page and scripts/check-meeting-dates.mjs, which the
// daily refresh runs to report any date this cannot read.
const MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
const monthOf = (w) => (w.length >= 3 ? MONTHS.findIndex((m) => m.startsWith(w.toLowerCase().slice(0, 3))) : -1);

export const parseMeetingDate = (s) => {
  if (!s) return null;
  const y = s.match(/\b(20\d\d)\b/);
  const m = s.match(/([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:\s*-\s*(?:([A-Za-z]{3,9})\.?\s+)?(\d{1,2}))?/);
  if (!y || !m) return null;
  const m1 = monthOf(m[1]);
  if (m1 < 0) return null;
  const m2 = m[3] ? monthOf(m[3]) : m1;
  if (m2 < 0) return null;
  const d1 = +m[2];
  const d2 = m[4] ? +m[4] : d1;
  const y1 = +y[1];
  const y2 = m2 < m1 ? y1 + 1 : y1;
  const start = Date.UTC(y1, m1, d1);
  const end = Date.UTC(y2, m2, d2);
  // A range longer than three weeks is a misread, not a meeting.
  if (Number.isNaN(start) || end < start || (end - start) / 864e5 > 20) return null;
  return { start, end };
};
