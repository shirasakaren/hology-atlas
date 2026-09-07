import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FRONTEND = 'http://localhost:3001';
const BACKEND = 'http://localhost:3002/api/v1';
const OUT_DIR = path.resolve(__dirname, '../../gallery/screenshots/full');
fs.mkdirSync(OUT_DIR, { recursive: true });

const CREDS = { email: 'demo.admin@creations.ren', password: 'AtlasDemo!2026' };
const GODMODE_PASSPHRASE = 'godmode-local-dev';

const SLUG = 'demo-northstar-studio';
const LIST1 = '3fc2fa49-fb52-4057-a3fe-f69f4f60fe44'; // Product Delivery
const LIST2 = 'eebac7e0-5597-4cc7-afd9-eba30a5b102e'; // Research and Content
const CH_GENERAL = '62a4d230-549a-40c8-aeb3-04b2b91bc2c9';
const CH_DESIGN = '29a44323-e2c5-4c94-a235-04e440966e3c';
const CH_RELEASE = '155d6e6d-476f-49cb-a95d-7127593522a1';
const CH_GLOBAL_COMMUNITY = 'ccd01b07-dc2c-42fd-a934-985dc5a5be54';
const WB1 = '746426a0-44ea-4cea-a9bc-7cfc8d88661c';

const DESKTOP = { width: 1440, height: 900 };
const MOBILE = { width: 390, height: 844 };

let counter = 0;
const manifest = [];

async function login() {
  const res = await fetch(`${BACKEND}/auth/login/password`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(CREDS),
  });
  if (!res.ok) throw new Error(`login failed: ${res.status}`);
  const data = await res.json();
  return { sessionId: data.sessionId, user: data.user, expiresAt: data.expiresAt };
}

async function main() {
  const session = await login();
  console.log('Logged in as', session.user.email);

  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: DESKTOP });
  const page = await context.newPage();

  await page.goto(`${FRONTEND}/login`);
  await page.evaluate((s) => {
    localStorage.setItem('atlas_session', JSON.stringify(s));
  }, session);

  async function shot(category, name, urlPath, opts = {}) {
    counter++;
    const idx = String(counter).padStart(3, '0');
    const fname = `${idx}-${category}-${name}.png`;
    try {
      await page.setViewportSize(opts.viewport || DESKTOP);
      if (urlPath !== null) {
        await page
          .goto(`${FRONTEND}${urlPath}`, { waitUntil: 'networkidle', timeout: 20000 })
          .catch(() => {});
      }
      if (opts.waitFor) {
        await page.waitForSelector(opts.waitFor, { timeout: 8000 }).catch(() => {});
      }
      if (opts.clickText) {
        await page
          .getByText(opts.clickText, { exact: true })
          .first()
          .click({ timeout: 5000 })
          .catch(() => {});
        await page.waitForTimeout(500);
      }
      if (opts.clickSelector) {
        await page.locator(opts.clickSelector).first().click({ timeout: 5000 }).catch(() => {});
        await page.waitForTimeout(500);
      }
      if (opts.before) await opts.before(page);
      await page.waitForTimeout(opts.settle ?? 450);
      await page.screenshot({ path: path.join(OUT_DIR, fname), fullPage: opts.fullPage !== false });
      manifest.push({ file: fname, category, name, path: urlPath, ok: true });
      console.log(`OK   ${fname}`);
    } catch (e) {
      manifest.push({ file: fname, category, name, path: urlPath, ok: false, error: String(e).slice(0, 200) });
      console.log(`FAIL ${fname}: ${String(e).slice(0, 150)}`);
    }
  }

  // ---------- Public / auth ----------
  await context.clearCookies();
  await page.evaluate(() => localStorage.clear());
  await shot('auth', 'landing', '/');
  await shot('auth', 'login', '/login');
  await shot('auth', 'register', '/register');
  await shot('auth', 'forgot-password', '/auth/forgot-password');
  await shot('auth', 'magic-link', '/auth/magic-link');

  // re-seed session for everything after this point
  await page.evaluate((s) => localStorage.setItem('atlas_session', JSON.stringify(s)), session);

  // ---------- Core ----------
  await shot('core', 'dashboard', '/dashboard');
  await shot('core', 'for-me', '/for-me');
  await shot('core', 'notifications', '/notifications');
  await shot('core', 'notif-bell-open', '/dashboard', {
    clickSelector: 'button[aria-label*="otif" i]',
  });
  await shot('core', 'my-profile', '/me');
  await shot('core', 'saved', '/me/saved');

  // ---------- Projects ----------
  await shot('projects', 'grid', '/projects');
  await shot('projects', 'new', '/projects/new');
  await shot('projects', 'overview', `/projects/${SLUG}`);
  await shot('projects', 'manage', `/projects/${SLUG}/manage`);
  await shot('projects', 'manage-requests', `/projects/${SLUG}/manage/requests`);
  await shot('projects', 'lists', `/projects/${SLUG}/lists`);
  await shot('projects', 'team', `/projects/${SLUG}/lists/${LIST1}/team`);

  // ---------- PMO ----------
  await shot('pmo', 'list-view', `/projects/${SLUG}/lists/${LIST1}/list`);
  await shot('pmo', 'kanban', `/projects/${SLUG}/lists/${LIST1}/kanban`, { waitFor: 'a[href*="/tasks/"]' });
  await shot('pmo', 'timeline', `/projects/${SLUG}/lists/${LIST1}/timeline`);
  await shot('pmo', 'task-new', `/projects/${SLUG}/lists/${LIST1}/tasks/new`);
  await shot('pmo', 'notes', `/projects/${SLUG}/lists/${LIST1}/notes`, { settle: 900 });
  await shot('pmo', 'whiteboards-list', `/projects/${SLUG}/lists/${LIST1}/whiteboards`);
  await shot('pmo', 'whiteboard-canvas', `/projects/${SLUG}/lists/${LIST1}/whiteboards/${WB1}`, { settle: 1200 });
  await shot('pmo', 'files', `/projects/${SLUG}/lists/${LIST1}/files`);
  await shot('pmo', 'list2-kanban', `/projects/${SLUG}/lists/${LIST2}/kanban`);
  await shot('pmo', 'task-detail-modal', `/projects/${SLUG}/lists/${LIST1}/kanban`, {
    waitFor: 'a[href*="/tasks/"]',
    clickSelector: 'a[href*="/tasks/"]',
    settle: 700,
  });

  // ---------- Chat ----------
  await shot('chat', 'global-landing', '/chat');
  await shot('chat', 'global-community', `/chat/global/${CH_GLOBAL_COMMUNITY}`, { settle: 900 });
  await shot('chat', 'project-landing', `/projects/${SLUG}/chat`);
  await shot('chat', 'project-general', `/projects/${SLUG}/chat/${CH_GENERAL}`, { settle: 900 });
  await shot('chat', 'project-design-review', `/projects/${SLUG}/chat/${CH_DESIGN}`, { settle: 900 });
  await shot('chat', 'project-release-room', `/projects/${SLUG}/chat/${CH_RELEASE}`, { settle: 900 });

  // ---------- Voice (discover a channel through the sidebar) ----------
  await shot('voice', 'project-sidebar-entry', `/projects/${SLUG}`, {
    clickSelector: 'a[href*="/voice/"]',
    settle: 1500,
  });

  // ---------- Godmode ----------
  await page.evaluate(() => localStorage.removeItem('atlas_godmode_token'));
  await shot('godmode', 'unlock-screen', '/godmode', { waitFor: '#gm-passphrase' });
  {
    const tokenRes = await fetch(`${BACKEND}/godmode/unlock`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ passphrase: GODMODE_PASSPHRASE }),
    });
    const tokenData = await tokenRes.json();
    await page.evaluate((t) => localStorage.setItem('atlas_godmode_token', t), tokenData.token);
  }
  await shot('godmode', 'overview', '/godmode', { settle: 900 });
  const godmodeSections = [
    ['users', 'Users'],
    ['roles', 'Roles'],
    ['site', 'Site'],
    ['appearance', 'Appearance'],
    ['registration', 'Registration'],
    ['authentication', 'Authentication'],
    ['sessions-policy', 'Sessions'],
    ['oauth', 'OAuth providers'],
    ['sso', 'SSO (OIDC / SAML)'],
    ['storage', 'Storage'],
    ['modules', 'Modules'],
    ['legal', 'Legal'],
  ];
  for (const [name, label] of godmodeSections) {
    await shot('godmode', name, '/godmode', { clickText: label, settle: 700 });
  }

  // ---------- Admin console ----------
  const adminTabs = ['tags', 'featured', 'roles', 'users', 'stickers', 'chat', 'flags'];
  for (const tab of adminTabs) {
    await shot('admin', tab, `/admin?tab=${tab}`, { settle: 600 });
  }

  // ---------- Settings ----------
  await shot('settings', 'hub', '/settings');
  await shot('settings', 'profile', '/settings/profile');
  await shot('settings', 'account', '/settings/account');
  await shot('settings', 'appearance', '/settings/appearance');
  await shot('settings', 'notifications', '/settings/notifications');
  await shot('settings', 'privacy', '/settings/privacy');

  // ---------- Theme gallery ----------
  const themeShots = [
    ['atlas', 'light'],
    ['ocean', 'light'],
    ['sunset', 'light'],
    ['rose', 'light'],
    ['lavender', 'light'],
    ['mint', 'light'],
    ['midnight', 'dark'],
    ['noir', 'dark'],
  ];
  for (const [themeId, mode] of themeShots) {
    await fetch(`${BACKEND}/me`, {
      method: 'PATCH',
      headers: { 'content-type': 'application/json', authorization: `Bearer ${session.sessionId}` },
      body: JSON.stringify({ themeId, themeMode: mode }),
    }).catch(() => {});
    await shot('theme', `${themeId}-${mode}`, '/dashboard', { settle: 700 });
  }
  // reset to instance default
  await fetch(`${BACKEND}/me`, {
    method: 'PATCH',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${session.sessionId}` },
    body: JSON.stringify({ themeId: null, themeMode: 'system' }),
  }).catch(() => {});

  // ---------- Legal + health ----------
  await shot('misc', 'legal-terms', '/legal/terms');
  await shot('misc', 'legal-privacy', '/legal/privacy');
  await shot('misc', 'health', '/health');

  // ---------- Mobile responsive pass ----------
  await shot('mobile', 'dashboard', '/dashboard', { viewport: MOBILE });
  await shot('mobile', 'kanban', `/projects/${SLUG}/lists/${LIST1}/kanban`, { viewport: MOBILE });
  await shot('mobile', 'chat', `/projects/${SLUG}/chat/${CH_GENERAL}`, { viewport: MOBILE, settle: 800 });
  await shot('mobile', 'godmode', '/godmode', { viewport: MOBILE, settle: 700 });
  await shot('mobile', 'settings', '/settings', { viewport: MOBILE });
  await shot('mobile', 'projects', '/projects', { viewport: MOBILE });

  await browser.close();

  fs.writeFileSync(path.join(OUT_DIR, '_manifest.json'), JSON.stringify(manifest, null, 2));
  const ok = manifest.filter((m) => m.ok).length;
  console.log(`\nDONE: ${ok}/${manifest.length} captured -> ${OUT_DIR}`);
}

main().catch((e) => {
  console.error('FATAL', e);
  process.exit(1);
});
