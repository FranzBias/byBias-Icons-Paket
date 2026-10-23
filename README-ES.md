# byBias-Icons-Packet 📦

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Author](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20by%20Francesco-blueviolet)
![GitHub stars](https://img.shields.io/github/stars/FranzBias/byBias-Icons-Paket?style=flat) ![GitHub issues](https://img.shields.io/github/issues/FranzBias/byBias-Icons-Paket) [![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=HUF5MYDG465RY)

![Icono de byBias-Icons-Packet](icons-packet.svg)

<p align="center">
  <img src="screenshots/01-dashboard.png" width="45%" alt="byBias-Icons-Packet: dashboard">
  <img src="screenshots/02-main-flow.png" width="45%" alt="byBias-Icons-Packet: main flow actions">
</p>

**Una aplicación GTK unificada para gestionar una colección personal de iconos en Linux Mint / Cinnamon.**

🇬🇧 [README-EN.md](README-EN.md) · 🇮🇹 [README-IT.md](README-IT.md) · 🇩🇪 [README-DE.md](README-DE.md) · 🇪🇸 [README-ES.md](README-ES.md) · 🇫🇷 [README-FR.md](README-FR.md) · 🇳🇱 [README-NL.md](README-NL.md) · 🇷🇺 [README-RU.md](README-RU.md) · 🇸🇦 [README-AR.md](README-AR.md) · 🇨🇳 [README-ZH.md](README-ZH.md) · 🇯🇵 [README-JA.md](README-JA.md)

---

## 💛 Un momento de sinceridad

> Desde hace unos meses estoy atravesando una etapa difícil: pocos
> encargos, y los pocos que hay pagan poco. Si esto no cambia pronto,
> tendré que buscar trabajo en otro sitio — no hay nada de malo en ello,
> pero preferiría con mucho seguir construyendo proyectos como este.
>
> Si **byBias-Icons-Packet** te resulta útil y quieres apoyarlo, una
> donación —aunque sea de un solo euro— marca la diferencia si somos
> muchos los que la hacemos. Y si no puedes donar, **contarlo** a otros
> ayuda igualmente muchísimo. Gracias de corazón, en cualquier caso, por
> haber llegado hasta aquí leyendo. 🙏

---

**byBias-Icons-Packet** reúne todo el conjunto de herramientas de iconos
byBias en una sola aplicación GTK3, pensada para gestionar *tu propia*
colección: extraer, limpiar, nombrar de forma coherente y convertirla en un
tema. Está en camino un tema de iconos libre (GPL-3) creado con la
aplicación. La ventana principal es un panel: cada
acción es una tarjeta visible, y al pulsarla se abre su panel en la misma
ventana — sin rebuscar en menús, sin memorizar comandos.

## Acciones

El **Flujo principal** cubre el trabajo cotidiano de crear y mantener un
tema de iconos, de principio a fin:

- **Extraer iconos** — extrae los iconos de archivos `.ico`, `.exe`,
  `.dll`, `.icl` (incluso renombrados para parecer otra cosa),
  reconstruyendo PNG limpios con la transparencia preservada. Útil cuando
  un paquete de iconos descargado es en realidad un ejecutable de
  Windows disfrazado.
- **Crear / actualizar tema** — copia una carpeta de origen en un
  auténtico tema de iconos: limpia nombres de archivos y carpetas
  (espacios/guiones bajos → guion, acentos eliminados), genera un
  `index.theme` correcto y reconstruye la caché, y puede activar el tema
  en todo el sistema con un clic.
- **Aplicar icono** — un selector organizado según *tus propias*
  categorías (no las genéricas del sistema) te permite explorar la
  colección visualmente y aplicar cualquier icono a una carpeta.
- **Iconos simbólicos** — convierte un PNG a color en un icono SVG
  monocromo de 16×16 "simbólico", del tipo usado en paneles y menús que
  cambian de color automáticamente para adaptarse a temas claros u
  oscuros.
- **Caza de gigantes** — busca colisiones de nombre entre tus iconos y
  los del sistema; una colisión es la causa clásica de iconos que de
  repente aparecen enormes, o como triángulos de imagen rota.
- **Prefijar todo** — la opción segura y sin supervisión: añade el
  prefijo `bybias-` a todos los iconos del tema para que ninguno pueda
  sustituir jamás por accidente a un icono del sistema.
- **Reemplazar iconos del sistema** — elige una casilla del sistema
  (papelera llena/vacía, carpeta genérica, carpeta de inicio, y más) y
  una imagen tuya: se instala con el nombre estándar exacto, así que
  ocupa el lugar de ese icono en todo el escritorio.
- **Clic derecho en Nemo** — *Cambiar icono…* abre tu colección y aplica el icono a la carpeta o al archivo seleccionado; *Pegar icono* usa la imagen del portapapeles. Las instala `install.sh` (pulsa F5 en Nemo para ver el icono nuevo).

Más allá del flujo principal, el panel agrupa herramientas más
especializadas en cuatro secciones, cada una pensada para un tipo
concreto de quebradero de cabeza:

**Mantenimiento** — mantener ordenada una gran colección con el tiempo.
- *Buscar duplicados* compara los iconos por el contenido real de la
  imagen (un hash de los píxeles), no por el nombre del archivo, así que
  detecta el mismo icono guardado dos veces con nombres distintos.
- *Hoja de contacto* representa toda la colección como un único mosaico
  PNG etiquetado — una forma genuinamente útil de *ver* lo que tienes en
  lugar de ir haciendo clic carpeta por carpeta.
- *Buscar similares* toma un icono de referencia y ordena el resto de la
  colección según cuán cercano esté su color dominante, útil para
  construir un subconjunto visualmente coherente.

**Producción** — dar forma a los iconos para su uso real.
- *Normalizar tamaños* toma un PNG de origen sobredimensionado y genera
  el conjunto completo de tamaños estándar (de 16 a 256 px), redimensionado
  correctamente en lugar de dejar que el sistema lo escale mal sobre la
  marcha.
- *Recolorear / invertir* aplica un tinte elegido a iconos monocromos, o
  invierte claro y oscuro, para que un conjunto simbólico pueda adaptarse
  al tema opuesto.
- *Recortar y centrar* elimina márgenes transparentes irregulares y
  recentra el icono con un relleno uniforme — la solución para un
  conjunto mixto que se ve ligeramente "descolocado" sin motivo aparente.

**Distribución** — compartir lo que has construido.
- *Exportar paquete* comprime el tema junto con un `LICENSE` y un
  `README` generados automáticamente, listo para publicar.
- *Generar showcase* construye una imagen promocional a partir de una
  selección de iconos, del tipo que querrías en una página de descarga.

**Seguridad y comodidad** — la red de seguridad.
- *Copia de seguridad / restaurar* toma una instantánea con fecha y hora
  del tema antes de un cambio arriesgado, con una forma de volver atrás
  en un clic si algo sale mal.
- *Diagnóstico* pasa todo el tema por una lista de comprobación
  diagnóstica (herencia, nombres con acentos, colisiones, validez de la
  caché) y señala los problemas *antes* de que se conviertan en iconos
  gigantes o triángulos de imagen rota.

Un menú en la esquina superior izquierda de la ventana (☰) da acceso
rápido a **Acerca de** (incluyendo el enlace a GitHub), un **selector de
idioma** que cubre los 10 idiomas de este README, y un interruptor de
**tema claro/oscuro** para la propia aplicación.

## Requisitos

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils
```

En el primer arranque, si falta alguna dependencia, byBias-Icons-Packet
la detecta, enumera exactamente lo que hace falta, pide tu consentimiento
explícito y la instala mediante la autenticación gráfica del propio
sistema (pkexec) o sudo — así que también puedes simplemente lanzarla y
dejar que se configure sola. Tu contraseña siempre la gestiona el
sistema, nunca la aplicación.

## Ejecutar

```bash
python3 icons-packet
```

**Estructura** — `icons_packet_core.py` contiene toda la lógica (sin
GTK, comprobable de forma independiente); `icons_packet_gui.py` es el
panel GTK3; `icons-packet` es el lanzador, que también se encarga
de la comprobación de dependencias descrita arriba.

**Convención de nombres** — los nombres de archivos y carpetas usan
únicamente guiones (`-`), nunca espacios ni guiones bajos; la aplicación
convierte ambos automáticamente cada vez que toca un tema.

## 🌱 Errar es humano

Este proyecto se construyó rápido, por una sola persona, en su tiempo
libre — así que es del todo posible que aún tenga algunas asperezas: un
error, un comportamiento extraño, una cadena mal traducida, una frase
imprecisa en este mismo README. Si detectas algo, por favor
abre un issue — los informes de errores, las correcciones
de idioma y las imprecisiones en general son todos genuinamente
bienvenidos. Lo mismo vale para las **solicitudes de funciones**: si hay
algo que te gustaría que la aplicación hiciera, o hiciera de otra manera,
dilo sin problema. Las sugerencias determinan hacia dónde va este
proyecto a partir de ahora.

---

*Hecho con ❤️ por FranzBias — [github.com/FranzBias/byBias-Icons-Paket](https://github.com/FranzBias/byBias-Icons-Paket)*
