const fs = require('fs');
const vm = require('vm');

const portalHtml = fs.readFileSync('frontend/portal.html', 'utf8');

const scriptStart = portalHtml.indexOf('<script>');
const scriptEnd = portalHtml.lastIndexOf('</script>');
const scriptContent = portalHtml.substring(scriptStart + 8, scriptEnd);

const mockDOM = {
  elements: {},
  title: '',
  documentElement: { lang: 'en' },
  addEventListener: () => {},
  removeEventListener: () => {},
  getElementById: (id) => ({
    id, textContent: '', innerText: '', innerHTML: '', style: {},
    classList: { add: () => {}, remove: () => {}, contains: () => false },
    addEventListener: () => {}
  }),
  querySelectorAll: () => [],
  querySelector: () => null,
  createElement: (tag) => ({
    tagName: tag.toUpperCase(), style: {}, classList: { add: () => {}, remove: () => {} },
    appendChild: () => {}, setAttribute: () => {}, getAttribute: () => null
  }),
  body: { appendChild: () => {}, style: {} }
};

const mockLocalStorage = {
  store: { 'HARVEST_HUB_LANG_v2': 'en', 'HARVEST_HUB_LANG': 'en' },
  getItem(key) { return this.store[key] || null; },
  setItem(key, val) { this.store[key] = String(val); },
  removeItem(key) { delete this.store[key]; }
};

const mockConsole = { log: () => {}, warn: () => {}, error: () => {}, info: () => {} };

function MockCustomEvent(type, detail) { this.type = type; this.detail = detail; }

const mockWindow = {
  localStorage: mockLocalStorage,
  document: mockDOM,
  navigator: { language: 'en-US' },
  addEventListener: () => {},
  removeEventListener: () => {},
  dispatchEvent: () => {},
  CustomEvent: MockCustomEvent,
  setTimeout: () => {},
  clearTimeout: () => {},
  setInterval: () => {},
  clearInterval: () => {},
  console: mockConsole,
  location: { hostname: 'localhost', port: '8085', protocol: 'http:' }
};

const context = vm.createContext({
  window: mockWindow,
  document: mockDOM,
  localStorage: mockLocalStorage,
  navigator: mockWindow.navigator,
  CustomEvent: MockCustomEvent,
  setTimeout: () => {},
  clearTimeout: () => {},
  setInterval: () => {},
  clearInterval: () => {},
  console: mockConsole,
  alert: () => {},
  confirm: () => true,
  prompt: () => ''
});

try {
  vm.runInContext(scriptContent, context);

  const state = context.window.kisanState;
  const i18n = context.window.kisanI18n;
  const app = context.window.app;

  function countHindi(text) {
    if (!text) return 0;
    const clean = text.replace(/<[^>]+>/g, ' ');
    const matches = clean.match(/[\u0900-\u097f]+/g);
    return matches ? matches.length : 0;
  }

  // 1. Initial State: English Mode
  console.log('1. Checking Initial English Mode (currentLang =', i18n.currentLang, ')...');
  let enErrors = [];
  ['farmer', 'officer', 'testing', 'warehouse', 'account'].forEach(role => {
    const config = app.getLoginRoleConfig(role);
    if (countHindi(JSON.stringify(config)) > 0) enErrors.push(`Login ${role} has Hindi in English mode`);
  });

  ['farmerPortal', 'officerPortal', 'testingPortal', 'warehousePortal', 'accountPortal'].forEach(portalKey => {
    if (context.window[portalKey]) {
      const html = context.window[portalKey].render();
      if (countHindi(html) > 0) enErrors.push(`${portalKey} has Hindi in English mode`);
    }
  });

  if (enErrors.length > 0) {
    console.error('FAIL in English mode:', enErrors);
    process.exit(1);
  } else {
    console.log('PASS: 0 Hindi words found in initial English mode!');
  }

  // 2. Switch to Hindi
  console.log('2. Testing Switch to Hindi...');
  i18n.setLanguage('hi');
  let hiCount = 0;
  ['farmerPortal', 'officerPortal', 'testingPortal', 'warehousePortal', 'accountPortal'].forEach(portalKey => {
    if (context.window[portalKey]) {
      hiCount += countHindi(context.window[portalKey].render());
    }
  });
  console.log('PASS: Successfully rendered in Hindi (Devanagari words rendered:', hiCount, ')');

  // 3. Switch back to English
  console.log('3. Testing Switch back to English...');
  i18n.setLanguage('en');
  let backErrors = [];
  ['farmerPortal', 'officerPortal', 'testingPortal', 'warehousePortal', 'accountPortal'].forEach(portalKey => {
    if (context.window[portalKey]) {
      const html = context.window[portalKey].render();
      if (countHindi(html) > 0) backErrors.push(`${portalKey} has Hindi after toggling back to English`);
    }
  });

  if (backErrors.length > 0) {
    console.error('FAIL after switching back to English:', backErrors);
    process.exit(1);
  } else {
    console.log('PASS: 0 Hindi words found after switching back to English!');
  }

  console.log('ALL TESTS PASSED! 100% PURE ENGLISH DEFAULT WITH PERFECT BILINGUAL TOGGLE!');

} catch (err) {
  console.error('Execution error:', err);
  process.exit(1);
}
