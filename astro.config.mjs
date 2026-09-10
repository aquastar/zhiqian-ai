// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // /grant's content moved into /research when the two pages merged; the route
  // itself became /agenda, so an old link must not land on the calendar.
  redirects: {
    '/grant': '/research',
  },
});
