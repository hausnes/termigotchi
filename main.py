"""
Termigotchi: ta vare på kjæledyrene dine i terminalen.
Kjør spillet med: python main.py

Klassen Spill holder styr på dyrene, myntene, butikken og meldingene.
Klassene for dyr og mat ligger i kjaeledyr.py, og tegningene i grafikk.py.
"""

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from grafikk import lag_bilde, lag_strek
from kjaeledyr import Drage, Hund, Katt, Mat

console = Console()

HUMOR_TEKST = {
    "glad": "[green]😊 Glad[/]",
    "lei seg": "[yellow]😢 Lei seg[/]",
    "syk": "[red]🤒 Syk[/]",
    "sover": "[blue]💤 Sover[/]",
    "død": "[grey50]💀 Død[/]",
}


class Spill:
    def __init__(self):
        self.dyrene = []
        self.mynter = 15
        self.dag = 1
        self.meldinger = ["Velkommen til Termigotchi!"]
        self.butikk = {
            "1": Mat("Tørrfôr", 3, 0, 1),
            "2": Mat("Kjøttbein", 4, 2, 3),
            "3": Mat("Kake", 2, 4, 4),
            "4": Mat("Chili", 1, 1, 3),
        }

    def melding(self, tekst):
        """Legger til en melding som vises nederst på skjermen."""
        self.meldinger.append(tekst)

    def levende_dyr(self):
        return [dyr for dyr in self.dyrene if dyr.er_i_live()]

    # ---------- Tegning av skjermen ----------

    def lag_kort(self, dyr, nummer):
        """Lager et panel med tegning og status for ett dyr."""
        status = Table.grid(padding=(0, 1))
        status.add_row("Sult", lag_strek(dyr.sult, "red"))
        status.add_row("Energi", lag_strek(dyr.energi, "yellow"))
        status.add_row("Glede", lag_strek(dyr.glede, "magenta"))
        status.add_row("Helse", lag_strek(dyr.helse, "green"))
        status.add_row("", "")
        status.add_row("Humør", HUMOR_TEKST[dyr.humor()])

        innhold = Table.grid(padding=(0, 2))
        innhold.add_column(width=28)  # Tegningen er 14 piksler, og hver piksel er 2 tegn bred
        innhold.add_column()
        innhold.add_row(lag_bilde(dyr), status)

        tittel = f"[bold]{nummer}: {dyr.navn}[/] [dim]{dyr.art}, {dyr.alder} dager[/]"
        return Panel(innhold, title=tittel, border_style=dyr.farge, expand=False)

    def vis(self):
        console.clear()
        console.print(
            Panel(
                f"[bold magenta]🐾 TERMIGOTCHI 🐾[/]    Dag {self.dag}    🪙 {self.mynter} mynter",
                expand=False,
            )
        )

        kort = []
        for i, dyr in enumerate(self.dyrene):
            kort.append(self.lag_kort(dyr, i + 1))
        console.print(Columns(kort))

        # Viser bare de fire siste meldingene
        console.print(Panel("\n".join(self.meldinger[-4:]), title="Hendelser", border_style="grey50"))

    # ---------- Input fra brukeren ----------

    def velg_dyr(self):
        """Spør hvilket dyr. Returnerer et levende dyr, eller None ved ugyldig valg."""
        if len(self.levende_dyr()) == 1:
            return self.levende_dyr()[0]  # Bare ett dyr, da trenger vi ikke spørre
        try:
            nummer = int(console.input("Hvilket dyr (nummer)? "))
            if nummer < 1:
                raise IndexError  # Ellers ville 0 gitt det siste dyret i lista
            dyr = self.dyrene[nummer - 1]
        except (ValueError, IndexError):
            self.melding("[red]Ugyldig dyr.[/]")
            return None
        if not dyr.er_i_live():
            self.melding(f"[red]{dyr.navn} lever ikke lenger.[/]")
            return None
        return dyr

    def velg_mat(self):
        for tast, mat in self.butikk.items():
            console.print(f"  {tast}: {mat}")
        valg = console.input("Hvilken mat? ")
        if valg not in self.butikk:
            self.melding("[red]Ugyldig mat.[/]")
            return None
        mat = self.butikk[valg]
        if mat.pris > self.mynter:
            self.melding(f"[red]Du har ikke råd til {mat.navn}.[/]")
            return None
        return mat

    def adopter(self):
        console.print("  1: Hund   2: Katt   3: Drage (koster 15 mynter)")
        art = console.input("Hvilken art? ")
        if art not in ["1", "2", "3"]:
            self.melding("[red]Ugyldig art.[/]")
            return False
        if art == "3" and self.mynter < 15:
            self.melding("[red]Du har ikke råd til en drage ennå.[/]")
            return False

        navn = console.input("Hva skal dyret hete? ").strip()
        if navn == "":
            self.melding("[red]Dyret må ha et navn.[/]")
            return False

        if art == "1":
            self.dyrene.append(Hund(navn))
        elif art == "2":
            self.dyrene.append(Katt(navn))
        else:
            self.mynter -= 15
            self.dyrene.append(Drage(navn))
        self.melding(f"🎉 Velkommen, {navn}!")
        return True

    # ---------- Selve spillet ----------

    def utfor_valg(self, valg):
        """Gjør det spilleren valgte. Returnerer True hvis tiden skal gå."""
        match valg:
            case "1":
                dyr = self.velg_dyr()
                mat = self.velg_mat()
                if dyr is None or mat is None:
                    return False
                self.mynter -= mat.pris
                self.melding(dyr.spis(mat))
            case "2":
                dyr = self.velg_dyr()
                if dyr is None:
                    return False
                self.melding(dyr.leke())
            case "3":
                dyr = self.velg_dyr()
                if dyr is None:
                    return False
                self.melding(dyr.sove())
            case "4":
                dyr = self.velg_dyr()
                if dyr is None:
                    return False
                if self.mynter < 5:
                    self.melding("[red]Medisin koster 5 mynter.[/]")
                    return False
                self.mynter -= 5
                self.melding(dyr.medisin())
            case "5":
                self.mynter += 3
                self.melding("💼 Du jobbet en dag og tjente 3 mynter.")
            case "6":
                return self.adopter()
            case _:
                self.melding("[red]Ugyldig valg.[/]")
                return False
        return True

    def ny_dag(self):
        self.dag += 1
        self.mynter += 1  # Litt lommepenger hver dag
        for dyr in self.levende_dyr():
            hendelse = dyr.tiden_gaar()
            if hendelse is not None:
                self.melding(hendelse)

    def start(self):
        console.clear()
        console.print(Panel("[bold magenta]🐾 TERMIGOTCHI 🐾[/]\nAdopter ditt første kjæledyr!", expand=False))
        while not self.adopter():
            console.print(self.meldinger[-1])

        while len(self.levende_dyr()) > 0:
            self.vis()
            console.print(
                "[bold]1[/] Mate  [bold]2[/] Leke  [bold]3[/] Sove  [bold]4[/] Medisin (5🪙)  "
                "[bold]5[/] Jobbe  [bold]6[/] Adopter  [bold]0[/] Avslutt"
            )
            valg = console.input("[bold]Velg: [/]")
            if valg == "0":
                console.print("Ha det bra! 👋")
                return
            if self.utfor_valg(valg):
                self.ny_dag()

        # Hit kommer vi bare når alle dyrene er døde
        self.vis()
        console.print(Panel(f"[bold]Spillet er over![/] Du klarte deg i {self.dag} dager.", border_style="red"))


if __name__ == "__main__":
    spill = Spill()
    spill.start()
