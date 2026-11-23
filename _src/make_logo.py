"""Build Zenith logo SVGs (text converted to outlines, no font dependency).
Lockup: Z mark + ZENITH (bold) over ENGINEERING (letter-spaced, width-matched)."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = TTFont("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")
gs, cmap, upm = F.getGlyphSet(), F.getBestCmap(), F["head"].unitsPerEm
def run(text, size, track):
    """returns (svg path d, width) with baseline at y=0, y-down."""
    s = size / upm; x = 0; d = []
    for ch in text:
        g = gs[cmap[ord(ch)]]; pen = SVGPathPen(gs)
        g.draw(TransformPen(pen, (s, 0, 0, -s, x, 0))); d.append(pen.getCommands())
        x += g.width * s + track
    return " ".join(d), x - track
Z_SIZE = 46; z_track = 0.16 * Z_SIZE
zd, zw = run("ZENITH", Z_SIZE, z_track)
E_SIZE = 14.5
# choose tracking so ENGINEERING spans the same width as ZENITH
_, w0 = run("ENGINEERING", E_SIZE, 0); e_track = (zw - w0) / (len("ENGINEERING") - 1)
ed, ew = run("ENGINEERING", E_SIZE, e_track)
cap_z = 0.729 * Z_SIZE; cap_e = 0.729 * E_SIZE; gap = 11
stack = cap_z + gap + cap_e; top = 36 - stack / 2          # centre on mark (76x72 box)
tx = 76 + 22
def svg(bar, word, sub, bg=None):
    W = tx + zw + 4; H = 72
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H}" role="img" aria-label="Zenith Engineering">'
            + (f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else "")
            + f'<g transform="translate(-12,-14)"><rect x="12" y="14" width="76" height="17" fill="{bar}"/><rect x="12" y="69" width="76" height="17" fill="{bar}"/>'
              f'<polygon points="88,31 88,69 12,69" fill="#F2A900"/></g>'
            + f'<path transform="translate({tx},{top + cap_z:.2f})" fill="{word}" d="{zd}"/>'
            + f'<path transform="translate({tx},{top + cap_z + gap + cap_e:.2f})" fill="{sub}" d="{ed}"/></svg>')
out = os.path.join(R, "assets")
open(f"{out}/logo.svg", "w").write(svg("#0F2A43", "#0F2A43", "#F2A900"))
open(f"{out}/logo-white.svg", "w").write(svg("#FFFFFF", "#FFFFFF", "#F2A900"))
mark = lambda bar: (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 76 72"><g transform="translate(-12,-14)"><rect x="12" y="14" width="76" height="17" fill="{bar}"/>'
                    f'<rect x="12" y="69" width="76" height="17" fill="{bar}"/><polygon points="88,31 88,69 12,69" fill="#F2A900"/></g></svg>')
open(f"{out}/logo-mark.svg", "w").write(mark("#0F2A43"))
print("ok", round(zw, 1), round(ew, 1), round(e_track, 2))
