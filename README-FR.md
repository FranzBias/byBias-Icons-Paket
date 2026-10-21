# byBias-Icons-Packet 📦

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Author](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20by%20Francesco-blueviolet)
![GitHub stars](https://img.shields.io/github/stars/FranzBias/byBias-Icons-Paket?style=flat) ![GitHub issues](https://img.shields.io/github/issues/FranzBias/byBias-Icons-Paket) [![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=HUF5MYDG465RY)

![Icône de byBias-Icons-Packet](icons-packet.svg)

**Une application GTK unifiée pour gérer une collection personnelle d'icônes sur Linux Mint / Cinnamon — livrée avec une collection prête à l'emploi de près de 30 000 icônes (140 Mo).**

🇬🇧 [README-EN.md](README-EN.md) · 🇮🇹 [README-IT.md](README-IT.md) · 🇩🇪 [README-DE.md](README-DE.md) · 🇪🇸 [README-ES.md](README-ES.md) · 🇫🇷 [README-FR.md](README-FR.md) · 🇳🇱 [README-NL.md](README-NL.md) · 🇷🇺 [README-RU.md](README-RU.md) · 🇸🇦 [README-AR.md](README-AR.md) · 🇨🇳 [README-ZH.md](README-ZH.md) · 🇯🇵 [README-JA.md](README-JA.md)

---

## 💛 Un moment de sincérité

> Depuis quelques mois, je traverse une période difficile : trop peu de
> missions, et celles qu'il y a paient trop peu. Si les choses ne
> changent pas bientôt, je devrai chercher du travail ailleurs — rien de
> mal à cela, mais je préférerais de loin continuer à construire des
> projets comme celui-ci.
>
> Si **byBias-Icons-Packet** t'est utile et que tu souhaites le
> soutenir, un don — même d'un seul euro — fait une vraie différence si
> assez de monde s'y met. Et si tu ne peux pas faire de don, **en parler**
> autour de toi aide tout autant. Merci sincèrement d'être arrivé·e
> jusqu'ici. 🙏

---

**byBias-Icons-Packet** réunit toute la boîte à outils d'icônes byBias
dans une seule application GTK3, et est livrée avec la collection pour
laquelle elle a été conçue : un ensemble sélectionné, nettoyé et nommé de
façon cohérente de **près de 30 000 icônes (140 Mo)**, prêt à intégrer
directement dans un thème. La fenêtre principale est un tableau de bord :
chaque action est une carte visible, et un clic ouvre son panneau dans la
même fenêtre — pas besoin de fouiller dans des menus ni de mémoriser des
commandes.

## Actions

Le **Flux principal** couvre le travail quotidien de création et
d'entretien d'un thème d'icônes, du début à la fin :

- **Extraire les icônes** — extrait les icônes de fichiers `.ico`,
  `.exe`, `.dll`, `.icl` (même renommés pour ressembler à autre chose),
  en reconstruisant des PNG propres avec la transparence préservée.
  Pratique quand un pack d'icônes téléchargé est en réalité un
  exécutable Windows déguisé.
- **Créer / mettre à jour un thème** — copie un dossier source dans un
  véritable thème d'icônes : nettoie les noms de fichiers et de
  dossiers (espaces/underscores → tiret, accents retirés), génère un
  `index.theme` correct et reconstruit le cache, et peut activer le
  thème sur tout le système en un clic.
- **Appliquer une icône** — un sélecteur organisé selon *tes propres*
  catégories (pas les catégories génériques du système) te permet de
  parcourir la collection visuellement et d'appliquer n'importe quelle
  icône à un dossier.
- **Icônes symboliques** — transforme un PNG en couleur en une icône SVG
  monochrome 16×16 « symbolique », du type utilisé dans les panneaux et
  menus qui se recolorent automatiquement selon le thème clair ou
  sombre.
- **Chasse aux géants** — recherche les collisions de noms entre tes
  icônes et les icônes système ; une collision est la cause classique
  d'icônes qui apparaissent soudainement géantes, ou sous forme de
  triangles d'image cassée.
- **Tout préfixer** — l'option sûre et sans surveillance : ajoute un
  préfixe `bybias-` à toutes les icônes du thème afin qu'aucune ne
  puisse jamais remplacer accidentellement une icône système.
- **Remplacer les icônes système** — choisis un emplacement système
  (corbeille pleine/vide, dossier générique, dossier personnel, et
  plus) et une de tes images : elle est installée sous le nom standard
  exact, et prend donc la place de cette icône partout où elle apparaît
  sur le bureau.

Au-delà du flux principal, le tableau de bord regroupe des outils plus
spécialisés en quatre sections, chacune pensée pour un type de casse-tête
particulier :

**Maintenance** — garder une grande collection en ordre dans la durée.
- *Détecter les doublons* compare les icônes par le contenu réel de
  l'image (un hachage des pixels), pas par le nom du fichier, et détecte
  ainsi la même icône enregistrée deux fois sous des noms différents.
- *Planche contact* affiche toute la collection sous la forme d'une
  unique mosaïque PNG légendée — un moyen vraiment utile de réellement
  *voir* ce que l'on possède plutôt que de cliquer dossier par dossier.
- *Trouver des similaires* prend une icône de référence et classe le
  reste de la collection selon la proximité de leur couleur dominante,
  utile pour constituer un sous-ensemble visuellement cohérent.

**Production** — façonner les icônes pour un usage réel.
- *Normaliser les tailles* prend un PNG source surdimensionné et génère
  le jeu complet de tailles standard (de 16 à 256 px), correctement
  redimensionné plutôt que laissé au système qui l'adapterait mal à la
  volée.
- *Recolorer / inverser* applique une teinte choisie aux icônes
  monochromes, ou inverse le clair et le sombre, afin qu'un jeu
  symbolique puisse être adapté au thème opposé.
- *Rogner et centrer* supprime les marges transparentes irrégulières et
  recentre l'icône avec un remplissage cohérent — la solution pour un
  jeu hétérogène qui paraît légèrement « de travers » sans raison
  évidente.

**Distribution** — partager ce que tu as construit.
- *Exporter le paquet* compresse le thème avec un `LICENSE` et un
  `README` générés automatiquement, prêt à être publié.
- *Générer une vitrine* construit une image promotionnelle à partir
  d'une sélection d'icônes, du genre que l'on voudrait sur une page de
  téléchargement.

**Sécurité et confort** — le filet de sécurité.
- *Sauvegarde / restauration* prend un instantané horodaté du thème
  avant une modification risquée, avec un retour en arrière possible en
  un clic si quelque chose tourne mal.
- *Diagnostic* fait passer tout le thème par une checklist de diagnostic
  (héritage, noms accentués, collisions, validité du cache) et signale
  les problèmes *avant* qu'ils ne deviennent des icônes géantes ou des
  triangles d'image cassée.

Un menu en haut à gauche de la fenêtre (☰) donne un accès rapide à **À
propos** (avec le lien GitHub), à un **sélecteur de langue** couvrant les
10 langues de ce README, et à un interrupteur **thème clair/sombre** pour
l'application elle-même.

## Prérequis

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```

Au premier lancement, si une dépendance manque, byBias-Icons-Packet le
détecte, liste exactement ce qu'il faut, demande ton consentement
explicite, et l'installe via l'authentification graphique du système
lui-même (pkexec) ou sudo — tu peux donc aussi simplement la lancer et la
laisser s'installer toute seule. Ton mot de passe est toujours géré par
le système, jamais par l'application.

## Lancer

```bash
python3 icons-packet
```

**Structure** — `icons_packet_core.py` contient toute la logique (sans
GTK, testable indépendamment) ; `icons_packet_gui.py` est le tableau de
bord GTK3 ; `icons-packet` est le lanceur, qui gère aussi la
vérification des dépendances décrite ci-dessus.

**Convention de nommage** — les noms de fichiers et de dossiers
n'utilisent que des tirets (`-`), jamais d'espaces ni d'underscores ;
l'application convertit les deux automatiquement dès qu'elle touche un
thème.

## 🌱 L'erreur est humaine

Ce projet a été construit rapidement, par une seule personne, sur son
temps libre — il est donc tout à fait possible qu'il ait encore quelques
aspérités : un bug, un comportement étrange, une chaîne mal traduite, une
phrase imprécise dans ce README même. Si tu remarques quoi que ce soit,
merci d'ouvrir une issue — les rapports de bugs, les
corrections de langue et les imprécisions en général sont tous
sincèrement les bienvenus. Il en va de même pour les **demandes de
fonctionnalités** : s'il y a quelque chose que tu aimerais que
l'application fasse, ou fasse différemment, dis-le. Les suggestions
déterminent la suite de ce projet.

---

*Fait avec ❤️ par FranzBias — [github.com/FranzBias/byBias-Icons-Paket](https://github.com/FranzBias/byBias-Icons-Paket)*
