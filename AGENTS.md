# AGENTS.md — danais-web

Contexto para cualquier persona o agente de IA que trabaje en este repositorio.
Última actualización: 8 de agosto de 2026.

## Qué es esto

Web pública de **Danais Natural Cosmetics** (España). Sitio estático, sin build ni
dependencias: se edita HTML y se publica con GitHub Pages.

- Dominio: `danaisnatural.com` (fichero `CNAME`)
- Repositorio: `marieladanais31-art/danais-web`, rama `main`
- Publicar = `git push`. GitHub Pages republica en 2-3 minutos.
- `.nojekyll` está presente: no se procesa nada con Jekyll.

## Ficheros

| Fichero | Qué es |
|---|---|
| `index.html` | Home completa. HTML, CSS y JS en un solo fichero (~1.600 líneas). |
| `experiencias/index.html` | Landing de Danais Experiences (talleres). |
| `diagnostico.html` | Diagnóstico capilar interactivo. |
| `aviso-legal.html`, `condiciones-uso.html`, `politica-privacidad.html` | Legales. |
| `favicon.ico`, `favicon-16/32.png`, `apple-touch-icon.png`, `icon-192/512.png` | Iconos de marca (monograma D). |
| `assets/` | Imágenes y vídeo. `hero-danais.mp4` es el vídeo del hero. |
| `docs/experiencias-danais-dossier.pdf` | Dossier comercial descargable. |

## Contexto de negocio que condiciona el contenido

**La línea de cosmética de España todavía no se puede vender.** Faltan dos ensayos
en ACATE: estabilidad y compatibilidad. Hasta que estén:

- **No** anunciar los productos como disponibles ni poner fecha de lanzamiento.
- **No** activar carrito ni checkout. Hoy no existe ninguno, y así debe seguir.
- La sección de producto funciona como **lista de espera**, sin cobro.
- Lo que sí se vende y se debe empujar son los **talleres y experiencias**.

Por eso el orden de la home es: Hero → **Experiencias** → Productos → Ingredientes →
Lista de espera → Embajadoras → Historia → Enciclopedia.

**Zona de cobertura de talleres:** Barcelona y provincia de Tarragona (Reus, Salou,
Cambrils, Miami Platja, Hospitalet de l'Infant) y toda la Costa Daurada hasta Vinaròs.

**Tarifas orientativas** (empresas desde 42 €/persona, cumpleaños desde 35 €/persona con
mínimo 8, eventos privados desde 40 €, hoteles desde 450 €/grupo). Siempre acompañadas de
la nota de que el presupuesto final depende de taller, participantes, materiales,
desplazamiento y extras.

**WhatsApp de España en la web:** +34 624 70 27 15.
**WhatsApp de Panamá:** +507 6494-4944 (para la futura `pa.danaisnatural.com`).

## Reglas de contenido que no se pueden romper

1. **Crema solar**: no presentarla nunca como protector solar comercializable ni
   anunciar un SPF concreto. El nombre correcto es "Experiencia de formulación de crema
   solar mineral con color", con enfoque educativo.
2. **Sin claims de eficacia** que no estén respaldados. Ver
   `brands/danais/forbidden-claims.md` en el repo `meta-content-automation`.
3. **Iconos**: el favicon tiene que coincidir con el icono de la app de TikTok. Si se
   cambia uno, hay que cambiar el otro; TikTok rechaza la app si no coinciden.
4. **RGPD**: cualquier formulario nuevo necesita casilla de consentimiento explícita y
   enlace a la política de privacidad, y la finalidad debe reflejarse en esa política.

## Convenciones técnicas

- Todo en un fichero por página: `<style>` en el `<head>`, `<script>` al final del `<body>`.
- Clases en castellano o inglés según el bloque; mantener el estilo del bloque que se toca.
- Variables CSS en `:root`: `--verde`, `--do`, `--crema`, `--oro`, `--teal`.
- Botones: `.btn` más `.btn-gold`, `.btn-teal`, `.btn-outline`, `.btn-dark`, `.btn-wa`, `.btn-white`.
- Las animaciones de entrada usan la clase `.rev` más un IntersectionObserver. Cualquier
  bloque nuevo que deba aparecer con animación necesita `.rev`.
- Rutas de iconos y enlaces internos: **absolutas** (`/favicon.ico`), para que funcionen
  igual desde `/` y desde `/experiencias/`.

## Antes de dar por terminado un cambio

```bash
# anidamiento de etiquetas, ids duplicados y anclas rotas
python3 - <<'PY'
from html.parser import HTMLParser
import re, glob
VOID={'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}
for f in ['index.html','experiencias/index.html','diagnostico.html']:
    html=open(f,encoding='utf-8').read()
    ids=re.findall(r'\sid="([^"]+)"',html)
    dup=[i for i in set(ids) if ids.count(i)>1]
    missing=sorted(a for a in set(re.findall(r'href="#([^"]+)"',html)) if a not in ids and a!='top')
    print(f, 'ids duplicados:', dup or 'ninguno', '| anclas rotas:', missing or 'ninguna')
PY
```

Y revisar en el navegador que el hero, las pestañas de producto y los modales legales
siguen funcionando.

## Pendiente

- [ ] Formulario de reserva de talleres con ciudad, fecha, número de participantes y
      experiencia de interés (hoy la reserva va por WhatsApp).
- [ ] `pa.danaisnatural.com`: versión del diagnóstico capilar filtrada por el catálogo
      disponible en Panamá, con el WhatsApp de Panamá.
- [ ] Galería y testimonios de la experiencia piloto, cuando se haga.
- [ ] Reactivar la línea de producto cuando lleguen los ensayos de ACATE.
