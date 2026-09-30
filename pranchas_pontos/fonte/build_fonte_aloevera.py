# -*- coding: utf-8 -*-
"""Reconstroi uma fonte Aloevera Display Bold utilizavel a partir dos subconjuntos
embutidos nos PDFs do proprio escritorio (cadernos Tomadas, Hidraulica Detalhe,
Portas e Janelas, Ar condicionado). Os subconjuntos nao tem tabela cmap: o mapa
glifo->caractere vem do ToUnicode de cada PDF. Resultado: fonts/aloevera-bold-dup.ttf
(uso interno, apenas para reproduzir os titulos no mesmo padrao das pranchas existentes)."""
import pymupdf as fitz, io, re, glob, sys, copy
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import cmap_format_4

def tumap(d, tu):
    cm = d.xref_stream(tu).decode('latin1'); pairs = {}
    for blk in re.findall(r'beginbfchar(.*?)endbfchar', cm, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            pairs[int(a, 16)] = chr(int(b[:4], 16))
    for blk in re.findall(r'beginbfrange(.*?)endbfrange', cm, re.S):
        for a, b, c in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            for i in range(int(a, 16), int(b, 16) + 1):
                pairs[i] = chr(int(c, 16) + i - int(a, 16))
    return pairs

def subsets(files):
    for fn in files:
        d = fitz.open(fn)
        for x in range(1, d.xref_length()):
            try: o = d.xref_object(x)
            except Exception: continue
            if '/Type0' in o and 'Aloevera' in o and '/ToUnicode' in o:
                desc = int(re.search(r'/DescendantFonts\s*\[\s*(\d+)', o).group(1))
                do = d.xref_object(desc); fd = int(re.search(r'/FontDescriptor\s+(\d+)', do).group(1))
                m = re.search(r'/FontFile2\s+(\d+)', d.xref_object(fd))
                if not m: continue
                f = TTFont(io.BytesIO(d.xref_stream(int(m.group(1)))))
                pairs = tumap(d, int(re.search(r'/ToUnicode\s+(\d+)', o).group(1)))
                go = f.getGlyphOrder(); g = f['glyf']
                have = {ch: go[cid] for cid, ch in pairs.items()
                        if cid < len(go) and g[go[cid]].numberOfContours != 0 and len(ch) == 1 and ord(ch) < 0x2100}
                yield f, have

def main(files, out):
    subs = sorted(subsets(files), key=lambda s: -len(s[1]))
    base, bhave = subs[0]
    glyf, hmtx = base['glyf'], base['hmtx']
    order = list(base.getGlyphOrder())
    cmap = {ord(ch): gn for ch, gn in bhave.items()}
    n = 0
    for f, have in subs[1:]:
        for ch, gn in have.items():
            if ord(ch) in cmap: continue
            def copy_glyph(name):
                nonlocal n
                src = f['glyf'][name]
                new = 'g%d_%s' % (n, name); n += 1
                gl = copy.deepcopy(src)
                if gl.isComposite():
                    for comp in gl.components:
                        comp.glyphName = copy_glyph(comp.glyphName)
                glyf.glyphs[new] = gl; order.append(new)
                hmtx.metrics[new] = f['hmtx'].metrics[name]
                return new
            cmap[ord(ch)] = copy_glyph(gn)
    if 32 not in cmap:  # espaco
        sp = [gn for gn in order if glyf[gn].numberOfContours == 0 and hmtx.metrics[gn][0] > 0]
        if sp: cmap[32] = sp[0]
    base.setGlyphOrder(order); glyf.glyphOrder = order
    base['maxp'].numGlyphs = len(order)
    t = newTable('cmap'); t.tableVersion = 0
    sub = cmap_format_4(4); sub.platformID, sub.platEncID, sub.language = 3, 1, 0; sub.cmap = cmap
    t.tables = [sub]; base['cmap'] = t
    post = newTable('post'); post.formatType = 3.0; post.italicAngle = 0; post.underlinePosition = -100
    post.underlineThickness = 50; post.isFixedPitch = 0; post.minMemType42 = post.maxMemType42 = 0
    post.minMemType1 = post.maxMemType1 = 0; base['post'] = post
    base['hhea'].numberOfHMetrics = len(order)
    base.save(out)
    print('glifos:', ''.join(sorted(chr(c) for c in cmap)))

if __name__ == '__main__':
    files = sys.argv[2:]
    main(files, sys.argv[1])
