// uso: node shot.mjs arquivo.html saida.png [largura_mm altura_mm] [escala]
import { chromium } from 'playwright';
import path from 'path';
const [,, inp, out, wmm='594', hmm='420', sc='1.6'] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: Math.round(wmm*96/25.4), height: Math.round(hmm*96/25.4) }, deviceScaleFactor: +sc });
await pg.goto('file://' + path.resolve(inp)); await pg.waitForTimeout(300);
await pg.screenshot({ path: out, fullPage: false });
await b.close();
