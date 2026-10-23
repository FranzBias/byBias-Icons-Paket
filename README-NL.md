# byBias-Icons-Packet 📦

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Author](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20by%20Francesco-blueviolet)
![GitHub stars](https://img.shields.io/github/stars/FranzBias/byBias-Icons-Paket?style=flat) ![GitHub issues](https://img.shields.io/github/issues/FranzBias/byBias-Icons-Paket) [![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=HUF5MYDG465RY)

![byBias-Icons-Packet icoon](icons-packet.svg)

<p align="center">
  <img src="screenshots/01-dashboard.png" width="45%" alt="byBias-Icons-Packet: dashboard">
  <img src="screenshots/02-main-flow.png" width="45%" alt="byBias-Icons-Packet: main flow actions">
</p>

**Een uniforme GTK-app voor het beheren van een persoonlijke iconencollectie op Linux Mint / Cinnamon.**

🇬🇧 [README-EN.md](README-EN.md) · 🇮🇹 [README-IT.md](README-IT.md) · 🇩🇪 [README-DE.md](README-DE.md) · 🇪🇸 [README-ES.md](README-ES.md) · 🇫🇷 [README-FR.md](README-FR.md) · 🇳🇱 [README-NL.md](README-NL.md) · 🇷🇺 [README-RU.md](README-RU.md) · 🇸🇦 [README-AR.md](README-AR.md) · 🇨🇳 [README-ZH.md](README-ZH.md) · 🇯🇵 [README-JA.md](README-JA.md)

---

## 💛 Een eerlijk moment

> Al een paar maanden zit ik in een moeilijke periode: te weinig
> opdrachten, en de weinige die er zijn betalen te weinig. Als dit niet
> snel verandert, moet ik elders werk gaan zoeken — daar is niets mis
> mee, maar ik zou veel liever projecten zoals dit blijven bouwen.
>
> Als **byBias-Icons-Packet** nuttig voor je is en je het wilt
> ondersteunen: een donatie — al is het maar één euro — maakt echt
> verschil als genoeg mensen meedoen. En als je niet kunt doneren, helpt
> het net zo goed om het **door te vertellen**. Hartelijk dank, hoe dan
> ook, dat je tot hier hebt gelezen. 🙏

---

**byBias-Icons-Packet** bundelt de volledige byBias-iconenset in één
GTK3-app, gemaakt om *je eigen* iconencollectie te beheren: extraheren,
opschonen, consistent benoemen en er een thema van maken. Een vrij
icoonthema (GPL-3), gemaakt met de app, is onderweg. Het
hoofdvenster is een dashboard: elke actie is een zichtbare kaart, en een
klik opent het bijbehorende paneel in hetzelfde venster — geen menu's
doorzoeken, geen commando's onthouden.

## Acties

De **Hoofdstroom** dekt het dagelijkse werk van het opbouwen en
onderhouden van een icoonthema, van begin tot eind:

- **Iconen extraheren** — haalt iconen uit `.ico`-, `.exe`-, `.dll`-,
  `.icl`-bestanden (ook hernoemde), en bouwt schone PNG's met behouden
  transparantie. Handig wanneer een gedownload iconenpakket eigenlijk
  een vermomd Windows-programma is.
- **Thema maken / bijwerken** — kopieert een bronmap naar een echt
  icoonthema: ruimt bestands- en mapnamen op (spaties/underscores →
  koppelteken, accenten verwijderd), genereert een correcte
  `index.theme` en herbouwt de cache, en kan het thema met één klik
  systeembreed activeren.
- **Icoon toepassen** — een kiezer, georganiseerd volgens *jouw eigen*
  categorieën (niet de generieke systeemcategorieën), laat je de
  collectie visueel doorbladeren en elk icoon op een map toepassen.
- **Symbolische iconen** — verandert een kleuren-PNG in een monochroom
  16×16 "symbolisch" SVG-icoon, van het type dat in panelen en menu's
  wordt gebruikt en automatisch van kleur verandert bij een licht of
  donker thema.
- **Jacht op de reuzen** — zoekt naar naamconflicten tussen jouw iconen
  en systeemiconen; een conflict is de klassieke oorzaak van iconen die
  plotseling reusachtig verschijnen, of als kapotte-afbeelding-
  driehoeken.
- **Alles voorvoegen** — de veilige, onbewaakte optie: voegt een
  `bybias-`-voorvoegsel toe aan elk icoon in het thema, zodat geen enkel
  icoon ooit per ongeluk een systeempictogram kan vervangen.
- **Systeemiconen vervangen** — kies een systeemslot (prullenbak vol/
  leeg, generieke map, thuismap, en meer) en een van je eigen
  afbeeldingen: deze wordt geïnstalleerd onder de exacte
  standaardnaam, en neemt zo overal op het bureaublad de plek van dat
  icoon over.
- **Rechtsklik in Nemo** — *Pictogram wijzigen…* opent je collectie en past het pictogram toe op de gekozen map of het gekozen bestand; *Pictogram plakken* gebruikt de afbeelding op het klembord. Geïnstalleerd door `install.sh` (druk op F5 in Nemo om het nieuwe pictogram te zien).

Naast de hoofdstroom bundelt het dashboard meer gespecialiseerde
hulpmiddelen in vier secties, elk gericht op een specifiek soort
hoofdpijn:

**Onderhoud** — een grote collectie op orde houden in de loop van de
tijd.
- *Duplicaten vinden* vergelijkt iconen op basis van de werkelijke
  afbeeldingsinhoud (een hash van de pixels), niet op bestandsnaam, en
  vindt zo hetzelfde icoon dat tweemaal onder verschillende namen is
  opgeslagen.
- *Contactblad* geeft de hele collectie weer als één enkel gelabeld
  PNG-mozaïek — een echt nuttige manier om daadwerkelijk te *zien* wat
  je hebt, in plaats van map voor map te klikken.
- *Vergelijkbare vinden* neemt één referentie-icoon en rangschikt de
  rest van de collectie op hoe dicht hun dominante kleur bij elkaar
  ligt, nuttig voor het samenstellen van een visueel samenhangende
  subset.

**Productie** — iconen vormgeven voor daadwerkelijk gebruik.
- *Formaten normaliseren* neemt één te grote bron-PNG en genereert de
  volledige standaardset (16 tot 256 px), correct verkleind in plaats
  van door het systeem slecht on-the-fly geschaald.
- *Herkleuren / omkeren* past een gekozen tint toe op monochrome
  iconen, of keert licht en donker om, zodat een symbolische set kan
  worden aangepast aan het tegengestelde thema.
- *Bijsnijden en centreren* verwijdert ongelijke transparante marges en
  centreert het icoon opnieuw met consistente opvulling — de oplossing
  voor een gemengde set die zonder duidelijke reden een beetje "scheef"
  oogt.

**Distributie** — delen wat je hebt gebouwd.
- *Pakket exporteren* zipt het thema samen met een automatisch
  gegenereerde `LICENSE` en `README`, klaar om te publiceren.
- *Showcase genereren* bouwt een promotieafbeelding uit een selectie
  iconen, van het soort dat je op een downloadpagina zou willen.

**Veiligheid en gemak** — het vangnet.
- *Back-up / herstellen* maakt een momentopname met tijdstempel van het
  thema vóór een riskante wijziging, met een manier om met één klik
  terug te gaan als er iets misgaat.
- *Gezondheidscontrole* laat het hele thema door een diagnostische
  checklist lopen (overerving, geaccentueerde namen, conflicten,
  cachegeldigheid) en signaleert problemen *voordat* ze reuzenpictogrammen
  of kapotte-afbeelding-driehoeken worden.

Een menu linksboven in het venster (☰) geeft snelle toegang tot **Over**
(inclusief de GitHub-link), een **taalkiezer** die alle 10 talen van dit
README omvat, en een **licht/donker thema**-schakelaar voor de app zelf.

## Vereisten

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```

Ontbreekt bij de eerste start een afhankelijkheid, dan detecteert
byBias-Icons-Packet dit, somt precies op wat nodig is, vraagt om je
uitdrukkelijke toestemming, en installeert het via de grafische
authenticatie van het systeem zelf (pkexec) of sudo — je kunt de app dus
ook gewoon starten en zichzelf laten installeren. Je wachtwoord wordt
altijd door het systeem beheerd, nooit door de app.

## Uitvoeren

```bash
python3 icons-packet
```

**Structuur** — `icons_packet_core.py` bevat alle logica (zonder GTK,
onafhankelijk testbaar); `icons_packet_gui.py` is het GTK3-dashboard;
`icons-packet` is de launcher, die ook de hierboven beschreven
afhankelijkheidscontrole afhandelt.

**Naamgevingsconventie** — bestands- en mapnamen gebruiken uitsluitend
koppeltekens (`-`), nooit spaties of underscores; de app zet beide
automatisch om zodra ze een thema aanraakt.

## 🌱 Fouten maken is menselijk

Dit project is snel gebouwd, door één persoon, in de vrije tijd — het is
dus heel goed mogelijk dat het nog wat ruwe randjes heeft: een bug, een
vreemd gedrag, een verkeerd vertaalde tekst, een onnauwkeurige zin in dit
README zelf. Zie je iets, open dan gerust een
issue — bugmeldingen, taalcorrecties en algemene
onnauwkeurigheden zijn allemaal oprecht welkom. Hetzelfde geldt voor
**functiewensen**: is er iets dat je zou willen dat de app deed, of
anders deed, zeg het gerust. Suggesties bepalen waar dit project
vervolgens naartoe gaat.

---

*Gemaakt met ❤️ door FranzBias — [github.com/FranzBias/byBias-Icons-Paket](https://github.com/FranzBias/byBias-Icons-Paket)*
