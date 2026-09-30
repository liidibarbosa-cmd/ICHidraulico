// Gera o PDF A2 paisagem e as prévias PNG de cada folha.
// uso: node imprimir.mjs [saida.pdf]
import { chromium } from 'playwright';
import path from 'path';
const out = process.argv[2] || '../CADERNO DE DETALHAMENTO - FORRO DE GESSO - R01.pdf';
const exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch({ executablePath: exe });
const pg = await b.newPage({ viewport: { width: 2245, height: 1587 }, deviceScaleFactor: 1 });
await pg.goto('file://' + path.resolve('caderno_forro.html'));
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(400);
await pg.pdf({ path: out, width: '594mm', height: '420mm', printBackground: true, preferCSSPageSize: true });
await pg.emulateMedia({ media: 'print' });
const n = await pg.$$eval('section.sheet', s => s.length);
const shots = await pg.$$('section.sheet');
for (let i = 0; i < n; i++) {
  await shots[i].screenshot({ path: `previa/folha_${String(i + 1).padStart(2, '0')}.png` });
}
await b.close();
console.log('pdf', out, 'folhas', n);
