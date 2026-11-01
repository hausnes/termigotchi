# termigotchi
Ta vare på din Tamagotchi i terminalen.

Spillet bygger videre på [time2_med_oop.py](time2_med_oop.py). Du adopterer kjæledyr, gir dem mat, leker med dem og legger dem til å sove. Hver handling tar én dag, og dyrene blir sultnere og triste av seg selv. Mat og medisin koster mynter, så noen ganger må du jobbe. Spillet er over når ingen av dyrene lever lenger.

## Kjøre spillet

```
pip install rich-pixels
python main.py
```

Gjør terminalvinduet stort, slik at dyrene får plass ved siden av hverandre.

## Filer

| Fil | Hva den inneholder |
| --- | --- |
| [main.py](main.py) | Klassen `Spill` med meny og hovedløkke. Det er denne fila du kjører. |
| [kjaeledyr.py](kjaeledyr.py) | Klassene `Mat`, `Kjaeledyr`, `Hund`, `Katt` og `Drage` |
| [grafikk.py](grafikk.py) | Pikseltegningene av dyrene, laget med `Pixels.from_ascii()` fra rich-pixels |
| [time2_med_oop.py](time2_med_oop.py) | Den opprinnelige, enkle versjonen fra timen |

Kjører du `python kjaeledyr.py` eller `python grafikk.py`, får du en liten test av klassene og tegningene.

## Klassediagram

```
┌──────────────────────┐        ┌──────────────────────┐
│        Spill         │        │         Mat          │
├──────────────────────┤        ├──────────────────────┤
│ dyrene    (liste)    │        │ navn                 │
│ butikk    (dict)     │        │ metthet              │
│ mynter               │        │ glede                │
│ dag                  │        │ pris                 │
│ meldinger (liste)    │        ├──────────────────────┤
├──────────────────────┤        │ __str__()            │
│ vis()                │        └──────────────────────┘
│ velg_dyr()           │
│ velg_mat()           │        ┌──────────────────────┐
│ adopter()            │        │      Kjaeledyr       │
│ utfor_valg(valg)     │        ├──────────────────────┤
│ ny_dag()             │        │ navn, art, farge     │
│ start()              │        │ sult, energi, glede  │
└──────────────────────┘        │ helse, alder, sover  │
                                ├──────────────────────┤
                                │ er_i_live()          │
                                │ humor()              │
                                │ spis(mat)            │
                                │ leke()               │
                                │ sove()               │
                                │ medisin()            │
                                │ tiden_gaar()         │
                                └──────────────────────┘
                                   ▲        ▲        ▲
                    ┌──────────────┘        │        └──────────────┐
          ┌─────────┴────────┐  ┌───────────┴──────┐  ┌─────────────┴────┐
          │       Hund       │  │       Katt       │  │      Drage       │
          ├──────────────────┤  ├──────────────────┤  ├──────────────────┤
          │                  │  │                  │  │ ild              │
          ├──────────────────┤  ├──────────────────┤  ├──────────────────┤
          │ leke()           │  │ leke()           │  │ spis(mat)        │
          │                  │  │ sove()           │  │ __str__()        │
          └──────────────────┘  └──────────────────┘  └──────────────────┘
```

`Spill` har en liste med `Kjaeledyr`-objekter og en dictionary med `Mat`-objekter. Når du mater et dyr, sendes et `Mat`-objekt inn i `spis(mat)`.

## Ideer til utvidelser

- Lag en ny dyreart, med egen tegning i `grafikk.py`.
- Gi dyrene et eget favorittmat-attributt.
- Lagre spillet til en JSON-fil, slik at du kan fortsette senere.
- La tilfeldige hendelser skje i `ny_dag()`, for eksempel at du finner mynter.
