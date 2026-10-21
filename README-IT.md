# byBias-Icons-Packet 📦

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Author](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20by%20Francesco-blueviolet)
![GitHub stars](https://img.shields.io/github/stars/FranzBias/byBias-Icons-Paket?style=flat) ![GitHub issues](https://img.shields.io/github/issues/FranzBias/byBias-Icons-Paket) [![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=HUF5MYDG465RY)

![Icona di byBias-Icons-Packet](icons-packet.svg)

**Un'app GTK unificata per gestire una collezione personale di icone su Linux Mint / Cinnamon — con inclusa una collezione pronta all'uso di quasi 30.000 icone (140 MB).**

🇬🇧 [README-EN.md](README-EN.md) · 🇮🇹 [README-IT.md](README-IT.md) · 🇩🇪 [README-DE.md](README-DE.md) · 🇪🇸 [README-ES.md](README-ES.md) · 🇫🇷 [README-FR.md](README-FR.md) · 🇳🇱 [README-NL.md](README-NL.md) · 🇷🇺 [README-RU.md](README-RU.md) · 🇸🇦 [README-AR.md](README-AR.md) · 🇨🇳 [README-ZH.md](README-ZH.md) · 🇯🇵 [README-JA.md](README-JA.md)

---

## 💛 Un momento di sincerità

> Da qualche mese sto attraversando un periodo difficile: pochi incarichi,
> e quei pochi poco remunerativi. Se non cambia qualcosa nei prossimi
> mesi, dovrò cercare lavoro altrove — nulla di male, ma preferirei
> continuare a costruire progetti - come questo.
>
> Se **byBias-Icons-Packet** ti è utile e vuoi sostenerlo, una donazione —
> anche di un solo euro — fa la differenza se in tanti la fanno. E se non
> puoi donare, **parlarne** ad altri aiuta comunque moltissimo. Grazie di
> cuore, in ogni caso, per essere arrivato/a fin qui a leggere. 🙏

---

**byBias-Icons-Packet** riunisce l'intera suite di strumenti byBias per le
icone in una sola app GTK3, e viene distribuita insieme alla collezione
per cui è nata: un set curato, ripulito e rinominato in modo coerente di
**quasi 30.000 icone (140 MB)**, pronto da inserire direttamente in un
tema. La finestra principale è una dashboard: ogni azione è un riquadro
visibile, e cliccandone uno si apre il suo pannello nella stessa finestra
— niente menu da scavare, niente comandi da memorizzare.

## Azioni

Il **Flusso principale** copre il lavoro quotidiano di costruzione e
manutenzione di un tema di icone, dall'inizio alla fine:

- **Estrai icone** — estrae le icone da file `.ico`, `.exe`, `.dll`,
  `.icl` (anche rinominati per sembrare altro), ricostruendo PNG puliti
  con la trasparenza preservata. Utile quando un pacchetto di icone
  scaricato è in realtà un eseguibile Windows travestito.
- **Crea / aggiorna tema** — copia una cartella sorgente in un vero tema
  di icone: bonifica nomi di file e cartelle (spazi/underscore →
  trattino, accenti rimossi), genera un `index.theme` corretto e
  rigenera la cache, e può attivare il tema su tutto il sistema in un
  clic.
- **Applica icona** — un selettore organizzato nelle *tue* categorie (non
  quelle generiche di sistema) permette di sfogliare la collezione
  visivamente e applicare qualsiasi icona a una cartella.
- **Icone simboliche** — trasforma un PNG a colori in un'icona SVG
  monocromatica 16×16 "simbolica", il tipo usato in pannelli e menu che
  si ricolora automaticamente per adattarsi ai temi chiari o scuri.
- **Caccia ai giganti** — cerca collisioni di nome tra le tue icone e
  quelle di sistema; una collisione è la causa classica di icone che
  compaiono improvvisamente enormi, o come triangoli di immagine rotta.
- **Prefissa tutto** — l'opzione sicura e a mani libere: aggiunge un
  prefisso `bybias-` a ogni icona del tema così nessuna può mai
  sostituire per sbaglio un'icona di sistema.
- **Sostituisci icone di sistema** — scegli una casella di sistema
  (cestino pieno/vuoto, cartella generica, cartella home, e altre) e una
  tua immagine: viene installata col nome standard esatto, così prende
  il posto di quell'icona ovunque compaia sul desktop.

Oltre al flusso principale, la dashboard raggruppa strumenti più
specializzati in quattro sezioni, ognuna pensata per un tipo specifico di
grattacapo:

**Manutenzione** — tenere in ordine una grande collezione nel tempo.
- *Rileva duplicati* confronta le icone per contenuto reale dell'immagine
  (un hash dei pixel), non per nome del file, quindi individua la stessa
  icona salvata due volte con nomi diversi.
- *Contact sheet* rende l'intera collezione come un unico mosaico PNG
  etichettato — un modo davvero utile per *vedere* cosa si ha invece di
  cliccare tra le cartelle una a una.
- *Trova simili* prende un'icona di riferimento e ordina il resto della
  collezione per quanto il loro colore dominante sia vicino, utile per
  costruire un sottoinsieme visivamente coerente.

**Produzione** — dare forma alle icone per l'uso reale.
- *Normalizza taglie* prende un PNG sorgente sovradimensionato e genera
  l'intero set standard (da 16 a 256 px), ridimensionato correttamente
  invece di lasciare che sia il sistema a scalarlo male al volo.
- *Ricolora / inverti* applica una tinta scelta a icone monocromatiche, o
  inverte chiaro e scuro, così un set simbolico può essere adattato al
  tema opposto.
- *Rifila e centra* rimuove margini trasparenti irregolari e ricentra
  l'icona con un padding coerente — la cura per un set misto che sembra
  leggermente "storto" senza un motivo evidente.

**Distribuzione** — condividere quello che hai costruito.
- *Esporta pacchetto* comprime il tema insieme a un `LICENSE` e un
  `README` generati automaticamente, pronto per la pubblicazione.
- *Genera showcase* costruisce un'immagine promozionale a partire da una
  selezione di icone, il tipo che vorresti su una pagina di download.

**Sicurezza & comodità** — la rete di salvataggio.
- *Backup / ripristino* crea uno snapshot con data e ora del tema prima
  di una modifica rischiosa, con un modo per tornare indietro in un clic
  se qualcosa va storto.
- *Health-check* fa passare l'intero tema attraverso una checklist
  diagnostica (ereditarietà, nomi con accenti, collisioni, validità della
  cache) e segnala i problemi *prima* che diventino icone giganti o
  triangoli di immagine rotta.

Un menu in alto a sinistra (☰) dà accesso rapido a **Informazioni**
(incluso il link a GitHub), a un **selettore di lingua** che copre tutte e
10 le lingue di questo README, e a un interruttore **tema chiaro/scuro**
per l'app stessa.

## Requisiti

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```

Al primo avvio, se manca qualche dipendenza, byBias-Icons-Packet la
rileva, elenca esattamente cosa serve, chiede il tuo consenso esplicito e
la installa tramite l'autenticazione grafica di sistema (pkexec) o sudo —
quindi puoi anche solo lanciarlo e lasciare che si configuri da solo. La
password la gestisce sempre il sistema, mai l'app.

## Avvio

```bash
python3 icons-packet
```

**Struttura** — `icons_packet_core.py` contiene tutta la logica (senza
GTK, testabile in modo indipendente); `icons_packet_gui.py` è la
dashboard GTK3; `icons-packet` è il launcher, che gestisce anche
il controllo delle dipendenze descritto sopra.

**Convenzione dei nomi** — i nomi di file e cartelle usano solo trattini
(`-`), mai spazi né underscore; l'app converte entrambi automaticamente
ogni volta che tocca un tema.

## 🌱 Sbagliare è umano

Questo progetto è stato costruito in fretta, da una sola persona, nel
tempo libero — quindi è del tutto possibile che abbia ancora qualche
spigolo: un bug, un comportamento strano, una stringa tradotta male, una
frase imprecisa in questo stesso README. Se noti qualcosa, per favore
apri una issue — segnalazioni di bug, correzioni di
lingua e imprecisioni in generale sono tutte davvero benvenute. Lo stesso
vale per le **richieste di funzionalità**: se c'è qualcosa che vorresti
l'app facesse, o facesse diversamente, dillo pure. I suggerimenti
determinano dove va questo progetto da qui in avanti.

---

*Fatto con ❤️ da FranzBias — [github.com/FranzBias/byBias-Icons-Paket](https://github.com/FranzBias/byBias-Icons-Paket)*
