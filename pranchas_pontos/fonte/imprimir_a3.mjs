// Imprime um HTML A3 retrato (297 x 420 mm) em PDF e gera PNGs de revisao.
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const aqui = path.dirname(new URL(import.meta.url).pathname);
const [saida, nome] = [process.argv[2], process.argv[3]];
const html = process.env.HTML || 'areas_molhadas.html';
const prefixo = process.env.PREFIXO || 'am';
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1123, height: 1587 }, deviceScaleFactor: Number(process.env.ESCALA_PREVIA || 1) });
await page.goto('file://' + path.join(aqui, html));
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: path.join(saida, nome), width: '297mm', height: '420mm', printBackground: true, preferCSSPageSize: true });
const dir = path.join(aqui, 'previa');
if (!fs.existsSync(dir)) fs.mkdirSync(dir);
const n = await page.locator('section.folha').count();
for (let i = 0; i < n; i++) {
  await page.locator('section.folha').nth(i).screenshot({ path: path.join(dir, `${prefixo}_${String(i + 1).padStart(2, '0')}.png`), scale: 'device' });
}
await browser.close();
console.log('ok', n);
