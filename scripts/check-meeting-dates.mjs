// Lists the meetings the By time calendar has to leave out because their
// date string cannot be read. Run by refresh-conferences.yml after the data
// rebuild; it prints a short Markdown report and never fails the job.
//   node scripts/check-meeting-dates.mjs
import { ranked, notable } from '../src/data/conferences.js';
import { destinations } from '../src/data/destinations.js';
import { parseMeetingDate } from '../src/lib/meeting-dates.js';

const seen = new Set();
const all = [];
for (const i of destinations.items) { seen.add(i.title); all.push({ title: i.title, date: i.date }); }
for (const c of [...ranked, ...notable]) if (!seen.has(c.title)) { seen.add(c.title); all.push({ title: c.title, date: c.date }); }

const blank = all.filter((i) => !i.date || /^tbd$/i.test(i.date.trim()));
const unread = all.filter((i) => i.date && !/^tbd$/i.test(i.date.trim()) && !parseMeetingDate(i.date));

console.log('## By time calendar');
console.log(`${all.length - blank.length - unread.length} of ${all.length} meetings are on the calendar. ${blank.length} have no announced date.`);
if (unread.length) {
  console.log(`\nThese ${unread.length} have a date the calendar cannot read. Rewrite it as "Month D-D, YYYY" in scripts/build-conferences.py:`);
  for (const i of unread) console.log(`- ${i.title}: "${i.date}"`);
} else {
  console.log('\nEvery announced date was read.');
}
