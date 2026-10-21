# byBias-Icons-Packet 📦
![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Author](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20by%20Francesco-blueviolet)

![byBias-Icons-Packet icon](icons-packet.svg)

<p align="center">
  <img src="screenshots/01-dashboard.png" width="45%" alt="byBias-Icons-Packet: dashboard">
  <img src="screenshots/02-main-flow.png" width="45%" alt="byBias-Icons-Packet: main flow actions">
</p>

---
**A unified GTK app for managing a personal icon collection on Linux Mint / Cinnamon.**

🇬🇧 [English](#english) · 🇮🇹 [Italiano](#italiano) · 🇩🇪 [Deutsch](#deutsch) · 🇪🇸 [Español](#español) · 🇫🇷 [Français](#français) · 🇳🇱 [Nederlands](#nederlands) · 🇷🇺 [Русский](#русский) · 🇸🇦 [العربية](#العربية) · 🇨🇳 [中文](#中文) · 🇯🇵 [日本語](#日本語)

---
## English

**byBias-Icons-Packet** gathers the whole byBias icon toolkit into a single GTK3 app. The
main window is a dashboard: every action is a visible card, and clicking one
opens its panel in the same window.

**Actions**
- **Extract icons** — pull icons out of `.ico`, `.exe`, `.dll`, `.icl` files (even renamed), rebuilding PNGs with transparency.
- **Create / update theme** — copy a source folder into a theme, clean up names (spaces/underscores → hyphen, accents removed), generate `index.theme` and cache, activate.
- **Apply icon** — pick an icon from your collection, organised in *your* categories, and apply it to a folder.
- **Symbolic icons** — generate monochrome 16×16 SVG symbolic icons from PNGs.
- **Hunt the giants** — find and defuse name collisions with system icons (the cause of giant / missing-icon triangles).
- **Prefix everything** — add the `bybias-` prefix to all icons: zero automatic substitutions.
- **Replace system icons** — pick a system slot (full/empty trash, folders, home, etc.) and one of your images: it's installed under the standard name, so it replaces the system icon everywhere it appears.

The dashboard also groups extra tools into four selectable sections:

*Maintenance* — **find duplicates** (identical icons by content, not name), **contact sheet** (a PNG mosaic of the whole collection), **find similar** (icons close by dominant colour).

*Production* — **normalize sizes** (from one big PNG to the full 16→256 set), **recolor / invert** (apply a tint or swap light↔dark), **trim & center** (uniform padding, centered icon).

*Distribution* — **export package** (a zip with `index.theme`, LICENSE and README), **make showcase** (a promo image of the theme).

*Safety & convenience* — **backup / restore** (snapshots with a "go back" option), **health-check** (diagnoses the theme against the FAQ checklist before problems become triangles).

A menu at the top-left of the window (☰) gives quick access to **About**, the **website link**, and a **light/dark theme** switch for the app itself.

**Requirements**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```
On first run, if any dependency is missing, byBias-Icons-Packet detects it, lists what's needed, asks for your consent, and installs it via the system's graphical authentication (pkexec) or sudo — so you can also just launch it and let it set itself up. Your password is handled by the system, never by the app.

**Run**
```bash
python3 icons-packet
```
**Structure** — `icons_packet_core.py` holds all logic (GTK-free, testable);
`icons_packet_gui.py` is the GTK3 dashboard; `icons-packet` is the launcher.

**Naming convention** — file and folder names use hyphens only (`-`), never
spaces or underscores; the app converts both automatically.

---

## Italiano

**byBias-Icons-Packet** riunisce l'intera suite di strumenti byBias per le icone in una sola app GTK3. La finestra principale è una dashboard: ogni azione è un riquadro visibile, e cliccandone uno si apre il suo pannello nella stessa finestra.

**Azioni**
- **Estrai icone** — estrae le icone da file `.ico`, `.exe`, `.dll`, `.icl` (anche rinominati), ricostruendo PNG con trasparenza.
- **Crea / aggiorna tema** — copia una cartella sorgente in un tema, bonifica i nomi (spazi/underscore → trattino, via gli accenti), genera `index.theme` e cache, attiva.
- **Applica icona** — scegli un'icona dalla collezione, organizzata nelle *tue* categorie, e applicala a una cartella.
- **Icone simboliche** — genera icone simboliche SVG 16×16 monocromatiche dai PNG.
- **Caccia ai giganti** — trova e disinnesca le collisioni di nome con le icone di sistema (causa di icone giganti / triangoli).
- **Prefissa tutto** — aggiunge il prefisso `bybias-` a tutte le icone: zero sostituzioni automatiche.
- **Sostituisci icone di sistema** — scegli una casella di sistema (cestino pieno/vuoto, cartelle, home, ecc.) e una tua immagine: viene installata col nome standard, così sostituisce l'icona di sistema ovunque compaia.

La dashboard raggruppa inoltre strumenti extra in quattro sezioni selezionabili:

*Manutenzione* — **rileva duplicati** (icone identiche per contenuto, non per nome), **contact sheet** (mosaico PNG dell'intera collezione), **trova simili** (icone vicine per colore dominante).

*Produzione* — **normalizza taglie** (da un PNG grande al set completo 16→256), **ricolora / inverti** (applica una tinta o inverti chiaro↔scuro), **rifila e centra** (padding uniforme, icona centrata).

*Distribuzione* — **esporta pacchetto** (zip con `index.theme`, LICENSE e README), **genera showcase** (immagine promozionale del tema).

*Sicurezza & comodità* — **backup / ripristino** (snapshot con "torna a prima"), **health-check** (diagnostica il tema secondo la checklist della FAQ, prima che i problemi diventino triangoli).

Un menu in alto a sinistra (☰) dà accesso rapido a **Informazioni**, al **link del sito** e a un interruttore **tema chiaro/scuro** per l'app stessa.

**Requisiti**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```
Al primo avvio, se manca qualche dipendenza, byBias-Icons-Packet la rileva, elenca cosa serve, chiede il tuo consenso e la installa tramite l'autenticazione grafica di sistema (pkexec) o sudo — quindi puoi anche solo lanciarlo e
lasciare che si configuri da solo. La password la gestisce il sistema, mai l'app.

**Avvio**
```bash
python3 icons-packet
```
**Struttura** — `icons_packet_core.py` contiene tutta la logica (senza GTK,
testabile); `icons_packet_gui.py` è la dashboard GTK3; `icons-packet` è il
launcher.

**Convenzione dei nomi** — i nomi di file e cartelle usano solo trattini
(`-`), mai spazi né underscore; l'app converte entrambi automaticamente.

---

## Deutsch

**byBias-Icons-Packet** vereint das gesamte byBias-Icon-Toolkit in einer einzigen GTK3-App. Das Hauptfenster ist ein Dashboard: Jede Aktion ist eine sichtbare
Kachel; ein Klick öffnet das zugehörige Panel im selben Fenster.

**Aktionen**
- **Icons extrahieren** — Icons aus `.ico`-, `.exe`-, `.dll`-, `.icl`-Dateien holen (auch umbenannt), als PNG mit Transparenz.
- **Thema erstellen / aktualisieren** — Quellordner in ein Thema kopieren, Namen bereinigen (Leerzeichen/Unterstriche → Bindestrich, Akzente entfernt), `index.theme` und Cache erzeugen, aktivieren.
- **Icon anwenden** — ein Icon aus der Sammlung in *deinen* Kategorien wählen und auf einen Ordner anwenden.
- **Symbolische Icons** — monochrome 16×16-SVG-Icons aus PNGs erzeugen.
- **Jagd auf die Riesen** — Namenskollisionen mit System-Icons finden und entschärfen (Ursache riesiger / fehlender Icons).
- **Alles mit Präfix** — allen Icons das Präfix `bybias-` geben: keine automatischen Ersetzungen.

**Voraussetzungen**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```

**Starten**
```bash
python3 icons-packet
```

---

## Español

Icons-Packet reúne todo el conjunto de herramientas de iconos byBias en una sola aplicación GTK3. La ventana principal es un panel: cada acción es una tarjeta visible y, al pulsarla, se abre su panel en la misma ventana.

**Acciones**
- **Extraer iconos** — extrae iconos de archivos `.ico`, `.exe`, `.dll`, `.icl` (incluso renombrados), reconstruyendo PNG con transparencia.
- **Crear / actualizar tema** — copia una carpeta de origen en un tema, limpia los nombres (espacios/guiones bajos → guion, sin acentos), genera `index.theme` y caché, activa.
- **Aplicar icono** — elige un icono de la colección, organizada en *tus* categorías, y aplícalo a una carpeta.
- **Iconos simbólicos** — genera iconos simbólicos SVG 16×16 monocromos a partir de PNG.
- **Caza de gigantes** — encuentra y desactiva las colisiones de nombres con iconos del sistema.
- **Prefijar todo** — añade el prefijo `bybias-` a todos los iconos: cero sustituciones automáticas.

**Requisitos**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```

**Ejecutar**
```bash
python3 icons-packet
```

---

## Français

**byBias-Icons-Packet** réunit toute la boîte à outils d'icônes byBias dans une seule application GTK3. La fenêtre principale est un tableau de bord : chaque action est une carte visible, et un clic ouvre son panneau dans la même fenêtre.

**Actions**
- **Extraire les icônes** — extrait les icônes des fichiers `.ico`, `.exe`, `.dll`, `.icl` (même renommés), en reconstruisant des PNG avec transparence.
- **Créer / mettre à jour un thème** — copie un dossier source dans un thème, nettoie les noms (espaces/underscores → tiret, accents retirés), génère `index.theme` et le cache, active.
- **Appliquer une icône** — choisis une icône dans la collection, organisée selon *tes* catégories, et applique-la à un dossier.
- **Icônes symboliques** — génère des icônes symboliques SVG 16×16 monochromes à partir de PNG.
- **Chasse aux géants** — trouve et neutralise les collisions de noms avec les icônes système.
- **Tout préfixer** — ajoute le préfixe `bybias-` à toutes les icônes : zéro substitution automatique.

**Prérequis**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```
**Lancer**
```bash
python3 icons-packet
```
---

## Nederlands

**byBias-Icons-Packet** bundelt de volledige byBias-iconenset in één GTK3-app. Het hoofdvenster is een dashboard: elke actie is een zichtbare kaart, en een klik opent het bijbehorende paneel in hetzelfde venster.

**Acties**
- **Iconen extraheren** — haal iconen uit `.ico`-, `.exe`-, `.dll`-, `.icl`-bestanden (ook hernoemd), als PNG met transparantie.
- **Thema maken / bijwerken** — kopieer een bronmap naar een thema, ruim namen op (spaties/underscores → koppelteken, accenten weg), genereer `index.theme` en cache, activeer.
- **Icoon toepassen** — kies een icoon uit de collectie, geordend in *jouw* categorieën, en pas het toe op een map.
- **Symbolische iconen** — genereer monochrome 16×16 SVG-iconen uit PNG's.
- **Jacht op de reuzen** — vind en ontmantel naamconflicten met systeemiconen.
- **Alles voorvoegen** — geef alle iconen het voorvoegsel `bybias-`: geen automatische vervangingen.

**Vereisten**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```
**Uitvoeren**
```bash
python3 icons-packet
```
---

## Русский

**byBias-Icons-Packet** объединяет весь набор инструментов byBias для значков в одном приложении GTK3. Главное окно — это панель: каждое действие представлено видимой карточкой, и по нажатию открывается его панель в том же окне.

**Действия**
- **Извлечь значки** — извлекает значки из файлов `.ico`, `.exe`, `.dll`, `.icl` (даже переименованных), восстанавливая PNG с прозрачностью.
- **Создать / обновить тему** — копирует исходную папку в тему, очищает имена (пробелы/подчёркивания → дефис, без акцентов), создаёт `index.theme` и кэш, активирует.
- **Применить значок** — выберите значок из коллекции, организованной по *вашим* категориям, и примените его к папке.
- **Символические значки** — создаёт монохромные значки SVG 16×16 из PNG.
- **Охота на гигантов** — находит и обезвреживает конфликты имён со системными значками.
- **Префикс для всего** — добавляет префикс `bybias-` ко всем значкам: никаких автоматических замен.

**Требования**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```

**Запуск**
```bash
python3 icons-packet
```

---

## العربية

يجمع **byBias-Icons-Packet** مجموعة أدوات أيقونات byBias بالكامل في تطبيق GTK3 واحد.
النافذة الرئيسية لوحة تحكم: كل إجراء بطاقة مرئية، والنقر عليها يفتح لوحته في النافذة نفسها.

**الإجراءات**
- **استخراج الأيقونات** — استخراج الأيقونات من ملفات `.ico` و`.exe` و`.dll` و`.icl` (حتى المعاد تسميتها)، وإعادة بناء صور PNG بالشفافية.
- **إنشاء / تحديث سمة** — نسخ مجلد مصدر إلى سمة، وتنظيف الأسماء (مسافات/شرطات سفلية ← شرطة، وإزالة التشكيل)، وإنشاء `index.theme` والذاكرة المؤقتة، والتفعيل.
- **تطبيق أيقونة** — اختر أيقونة من المجموعة، المنظّمة وفق فئاتك، وطبّقها على مجلد.
- **أيقونات رمزية** — إنشاء أيقونات رمزية SVG أحادية اللون بحجم 16×16 من ملفات PNG.
- **مطاردة العمالقة** — العثور على تعارضات الأسماء مع أيقونات النظام وإبطالها.
- **بادئة للكل** — إضافة البادئة `bybias-` إلى كل الأيقونات: لا استبدالات تلقائية.

**المتطلبات**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```
**التشغيل**
```bash
python3 icons-packet
```
---

## 中文

**byBias-Icons-Packet** 将整套 byBias 图标工具集整合到一个 GTK3 应用中。主窗口是一个仪表盘：每个操作都是一张可见的卡片，点击后会在同一窗口中打开其面板。

**功能**
- **提取图标** — 从 `.ico`、`.exe`、`.dll`、`.icl` 文件（即使已重命名）中提取图标，重建带透明度的 PNG。
- **创建 / 更新主题** — 将源文件夹复制到主题，清理名称（空格/下划线 → 连字符，去除重音），生成 `index.theme` 和缓存，并激活。
- **应用图标** — 从按*你的*分类整理的图标集中选择图标，应用到某个文件夹。
- **符号图标** — 从 PNG 生成单色 16×16 SVG 符号图标。
- **猎巨人** — 查找并化解与系统图标的命名冲突。
- **全部加前缀** — 为所有图标添加 `bybias-` 前缀：不做任何自动替换。

**依赖**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```
**运行**
```bash
python3 icons-packet
```
---

## 日本語

**byBias-Icons-Packet** は byBias のアイコンツール一式を単一の GTK3 アプリにまとめたものです。 メインウィンドウはダッシュボードで、各アクションが見えるカードになっており、 クリックすると同じウィンドウ内にそのパネルが開きます。

**機能**
- **アイコン抽出** — `.ico`・`.exe`・`.dll`・`.icl` ファイル（名前変更済みでも）からアイコンを抽出し、透過付き PNG を再構築します。
- **テーマの作成 / 更新** — ソースフォルダをテーマにコピーし、名前を整理（スペース/アンダースコア → ハイフン、アクセント除去）、`index.theme` とキャッシュを生成し、有効化します。
- **アイコンの適用** — *あなたの*カテゴリーで整理されたコレクションからアイコンを選び、フォルダに適用します。
- **シンボリックアイコン** — PNG から単色 16×16 の SVG シンボリックアイコンを生成します。
- **巨人狩り** — システムアイコンとの名前衝突を見つけて無効化します。
- **すべてにプレフィックス** — すべてのアイコンに `bybias-` を付与：自動置換なし。

**必要環境**
```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```
**実行**
```bash
python3 icons-packet
```
---
