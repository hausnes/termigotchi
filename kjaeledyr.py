"""
Klassene i Termigotchi: Mat, Kjaeledyr og de tre dyreartene Hund, Katt og Drage.

Metodene returnerer en melding (tekst) i stedet for å printe den.
Da kan hovedprogrammet bestemme hvor og når meldingen skal vises.
"""

import random


def begrens(verdi):
    """Passer på at en verdi alltid er mellom 0 og 10."""
    return max(0, min(10, verdi))


class Mat:
    def __init__(self, navn, metthet, glede, pris):
        self.navn = navn
        self.metthet = metthet  # Hvor mye sulten går ned
        self.glede = glede      # Hvor mye gleden går opp
        self.pris = pris        # Hvor mange mynter maten koster

    def __str__(self):
        return f"{self.navn} ({self.pris} mynter)"


class Kjaeledyr:
    def __init__(self, navn, art, farge):
        self.navn = navn
        self.art = art          # Brukes til å finne riktig tegning i grafikk.py
        self.farge = farge      # Fargen på kroppen i tegningen
        self.sult = 3
        self.energi = 7
        self.glede = 7
        self.helse = 10
        self.alder = 0
        self.sover = False

    def __str__(self):
        return f"{self.navn} ({self.art}, {self.alder} dager)"

    def er_i_live(self):
        return self.helse > 0

    def humor(self):
        """Returnerer hvordan dyret har det. Brukes til å velge tegning og tekst."""
        if not self.er_i_live():
            return "død"
        if self.sover:
            return "sover"
        if self.helse <= 4:
            return "syk"
        if self.sult >= 8 or self.glede <= 3:
            return "lei seg"
        return "glad"

    def spis(self, mat):
        self.sover = False  # Dyret våkner hvis det får mat
        self.sult = begrens(self.sult - mat.metthet)
        self.glede = begrens(self.glede + mat.glede)
        return f"{self.navn} spiste {mat.navn}. Nam!"

    def leke(self):
        if self.sover:
            return f"{self.navn} sover. La dyret sove ut først!"
        if self.energi < 2:
            return f"{self.navn} er for trøtt til å leke."
        self.glede = begrens(self.glede + 3)
        self.energi = begrens(self.energi - 2)
        self.sult = begrens(self.sult + 1)
        return f"Du lekte med {self.navn}."

    def sove(self):
        self.sover = True
        self.energi = begrens(self.energi + 2)
        return f"{self.navn} legger seg til å sove. Zzz ..."

    def medisin(self):
        self.helse = begrens(self.helse + 4)
        self.glede = begrens(self.glede - 1)  # Ingen liker medisin
        return f"{self.navn} fikk medisin og føler seg bedre."

    def tiden_gaar(self):
        """Kjøres én gang hver runde. Returnerer en melding, eller None."""
        self.alder += 1
        self.sult = begrens(self.sult + 1)
        # randint(0, 1) gjør at gleden bare går ned omtrent annenhver dag
        self.glede = begrens(self.glede - random.randint(0, 1))

        if self.sover:
            # Et sovende dyr får energi, og våkner når det er uthvilt
            self.energi = begrens(self.energi + 2)
            if self.energi == 10:
                self.sover = False
                return f"☀️  {self.navn} våknet uthvilt!"
        else:
            self.energi = begrens(self.energi - random.randint(0, 1))

        # Dyret mister helse hvis det ikke blir tatt vare på
        if self.sult >= 9 or self.energi == 0 or self.glede == 0:
            self.helse = begrens(self.helse - 2)
            if not self.er_i_live():
                return f"💀 {self.navn} klarte seg ikke ..."
            return f"⚠️  {self.navn} har det ikke bra og mister helse!"
        return None


class Hund(Kjaeledyr):
    def __init__(self, navn):
        super().__init__(navn, "hund", "dark_orange3")

    def leke(self):
        # Hunder elsker å leke: mer glede, men de blir fortere sultne
        melding = super().leke()
        if melding.startswith("Du lekte"):  # Bare hvis leken faktisk skjedde
            self.glede = begrens(self.glede + 1)
            self.sult = begrens(self.sult + 1)
        return melding


class Katt(Kjaeledyr):
    def __init__(self, navn):
        super().__init__(navn, "katt", "grey62")

    def leke(self):
        # Katter gjør som de vil. Av og til gidder de ikke å leke.
        if not self.sover and random.randint(1, 3) == 1:
            return f"{self.navn} ser på deg og går sin vei. Typisk katt."
        return super().leke()

    def sove(self):
        # Katter er eksperter på å sove
        melding = super().sove()
        self.energi = begrens(self.energi + 2)
        return melding


class Drage(Kjaeledyr):
    def __init__(self, navn):
        super().__init__(navn, "drage", "green3")
        self.ild = 0  # Nytt attributt som bare drager har

    def spis(self, mat):
        # Drager blir ekstra glade av sterk mat, og får ild i magen
        melding = super().spis(mat)
        if mat.navn == "Chili":
            self.ild = self.ild + 1
            self.glede = begrens(self.glede + 2)
            melding = melding + f" 🔥 {self.navn} spruter ild!"
        return melding

    def __str__(self):
        return f"{super().__str__()}, ild: {self.ild}"


if __name__ == "__main__":
    # Enkel test av klassene. Kjøres bare når du starter denne fila direkte.
    test = Drage("Test")
    print(test)
    print(test.spis(Mat("Chili", 1, 1, 3)))
    print(test.leke())
    print(test.tiden_gaar())
    print(test, test.humor())
