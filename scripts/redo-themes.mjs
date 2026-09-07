import { chromium } from 'playwright';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FRONTEND = 'http://localhost:3001';
const BACKEND = 'http://localhost:3002/api/v1';
const OUT_DIR = path.resolve(__dirname, '../proposal/assets/screenshots/curated');

const CREDS = { email: 'demo.admin@creations.ren', password: 'AtlasDemo!2026' };

async function login() {
  const res = await fetch(`${BACKEND}/auth/login/password`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(CREDS),
  });
  const data = await res.json();
  return { sessionId: data.sessionId, user: data.user, expiresAt: data.expiresAt };
}

async function main() {
  const session = await login();
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  await page.goto(`${FRONTEND}/login`);
  await page.evaluate((s) => localStorage.setItem('atlas_session', JSON.stringify(s)), session);

  const themes = [
    ['atlas', 'light', 'theme-atlas.png'],
    ['ocean', 'light', 'theme-ocean.png'],
    ['sunset', 'light', 'theme-sunset.png'],
    ['rose', 'light', 'theme-rose.png'],
    ['lavender', 'light', 'theme-lavender.png'],
    ['mint', 'light', 'theme-mint.png'],
    ['midnight', 'dark', 'theme-midnight.png'],
    ['noir', 'dark', 'theme-noir.png'],
  ];

  for (const [id, mode, fname] of themes) {
    const r = await fetch(`${BACKEND}/users/me`, {
      method: 'PATCH',
      headers: { 'content-type': 'application/json', authorization: `Bearer ${session.sessionId}` },
      body: JSON.stringify({ themeId: id, themeMode: mode }),
    });
    if (!r.ok) console.error('PATCH failed', id, mode, r.status, await r.text());
    await page.goto(`${FRONTEND}/dashboard`, { waitUntil: 'networkidle', timeout: 20000 });
    await page.waitForTimeout(600);
    const htmlTheme = await page.evaluate(() => ({
      theme: document.documentElement.getAttribute('data-theme'),
      dark: document.documentElement.classList.contains('dark'),
    }));
    console.log(fname, '->', JSON.stringify(htmlTheme));
    await page.screenshot({ path: path.join(OUT_DIR, fname), fullPage: false });
  }

  await browser.close();
  console.log('DONE');
}

main().catch((e) => {
  console.error('FATAL', e);
  process.exit(1);
});
