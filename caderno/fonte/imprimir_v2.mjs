// Imprime caderno_hidraulica_v2.html em PDF A3 retrato (sem ajuste de escala) e gera PNGs de revisao.
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const aqui = path.dirname(new URL(import.meta.url).pathname);
const saida = process.argv[2] || path.join(aqui, '..');
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1123, height: 1587 }, deviceScaleFactor: Number(process.env.ESCALA_PREVIA || 2) });
const htmlFile = 'caderno_hidraulica_v2.html';
const pdf = 'CADERNO DE DETALHAMENTO HIDRAULICO - PONTOS EM PLANTA - R02.pdf';
const prev = 'v2';
const previaDir = path.join(aqui, 'previa_v2');
if (!fs.existsSync(previaDir)) fs.mkdirSync(previaDir);
await page.goto('file://' + path.join(aqui, htmlFile));
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: path.join(saida, pdf),
  width: '297mm', height: '420mm', printBackground: true, preferCSSPageSize: true });
const n = await page.locator('section.sheet').count();
for (let i = 0; i < n; i++) {
  await page.locator('section.sheet').nth(i).screenshot({ path: path.join(previaDir, `${prev}_${String(i + 1).padStart(2, '0')}.png`), scale: 'device' });
}
await browser.close();
console.log('ok', n);
