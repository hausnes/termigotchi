"""
Pikselgrafikk for Termigotchi, laget med rich-pixels.
Installer først: pip install rich-pixels

I dungeon crawler-eksempelet brukte vi Pixels.from_image_path() for å vise et bilde.
Her bruker vi Pixels.from_ascii(): vi "tegner" med bokstaver, og hver bokstav
blir byttet ut med en farget rute.
"""

from rich.segment import Segment
from rich.style import Style
from rich_pixels import Pixels

# Tegningene. Hver bokstav er én piksel:
#   .  gjennomsiktig      k  kroppen (fargen til dyret)
#   o  øye                n  nese / munn
#   r  tunge (rød)        h  horn (bare drage)
TEGNINGER = {
    "hund": """\
.nn........nn.
nnnk......knnn
nnkkkkkkkkkknn
nnkkkkkkkkkknn
n.kkokkkkokk.n
..kkkkkkkkkk..
..kkkknnkkkk..
...kkkrrkkk...
....kkkkkk....
...kkkkkkkk...
..kkkkkkkkkk..
..kk.kk..kk.kk
""",
    "katt": """\
.k..........k.
.kk........kk.
.kkk......kkk.
.kkkkkkkkkkkk.
.kkokkkkkkokk.
.kkkkkkkkkkkk.
.kkkkknnkkkkk.
..kkkkkkkkkk..
...kkkkkkkk...
..kkkkkkkkkk.k
..kkkkkkkkkkk.
..kk..kk..kk..
""",
    "drage": """\
..h........h..
..hh......hh..
...kkkkkkkk...
..kkkkkkkkkk..
..kkokkkkokk..
..kkkkkkkkkk..
..kkkkkkkkkk..
...kknkknkk...
k...kkkkkk...k
kk.kkkkkkkk.kk
kkkkkkkkkkkkkk
...kk....kk...
""",
}


def piksel(farge):
    # To mellomrom per piksel, slik at rutene blir omtrent kvadratiske
    return Segment("  ", Style(bgcolor=farge))


def lag_bilde(dyr):
    """Lager et Pixels-bilde av dyret. Utseendet avhenger av humøret."""
    humor = dyr.humor()

    kroppsfarge = dyr.farge
    if humor == "syk":
        kroppsfarge = "dark_olive_green3"
    elif humor == "død":
        kroppsfarge = "grey30"

    fargekart = {
        ".": Segment("  "),
        "k": piksel(kroppsfarge),
        "o": piksel("black"),
        "n": piksel("grey23"),
        "r": piksel("red3"),
        "h": piksel("wheat1"),
    }

    # Lukkede øyne når dyret sover, kryss når det er dødt
    if humor == "sover":
        fargekart["o"] = Segment("▁▁", Style(color="black", bgcolor=kroppsfarge))
    elif humor == "død":
        fargekart["o"] = Segment("><", Style(color="black", bgcolor=kroppsfarge))

    # Tunga henger bare ute når dyret er glad
    if humor != "glad":
        fargekart["r"] = piksel(kroppsfarge)

    return Pixels.from_ascii(TEGNINGER[dyr.art], fargekart)


def lag_strek(verdi, farge):
    """Lager en statusstrek, for eksempel [green]███████░░░[/]"""
    return f"[{farge}]{'█' * verdi}[/][grey35]{'░' * (10 - verdi)}[/] {verdi:>2}"


if __name__ == "__main__":
    # Test: vis alle dyrene
    from rich.console import Console
    from kjaeledyr import Hund, Katt, Drage

    console = Console()
    for dyr in [Hund("Fido"), Katt("Pusur"), Drage("Glød")]:
        console.print(dyr)
        console.print(lag_bilde(dyr))
