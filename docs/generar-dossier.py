#!/usr/bin/env python3
"""
Genera el dossier comercial de Experiencias Danais.

El anterior eran seis imagenes de pagina completa: todo el material grafico era
generado por IA, no habia una sola linea de texto seleccionable y pesaba 3,3 MB.
Para un dossier que se manda por correo a empresas y hoteles eso es lo peor de
los tres mundos: parece falso, no se puede copiar ni buscar, y llena el buzon.

Este se construye con las fotos reales del obrador y del producto, con texto de
verdad, y con los datos actuales: 2 h 30 min de taller, 39 EUR por persona en
privados y presupuesto en empresas y hoteles.
"""

import os
import fitz

BASE = '/Users/marielaandrade/Documents/GitHub/danais-web'
FOTOS = f'{BASE}/assets/experiencias'
SALIDA = f'{BASE}/docs/experiencias-danais-dossier.pdf'

A4 = fitz.paper_rect('a4')          # 595 x 842 pt
W, H = A4.width, A4.height
M = 52                              # margen

# Paleta de la marca, tomada de las variables CSS del sitio.
VERDE = (0.055, 0.322, 0.290)       # #0e5249 aprox, el teal de Danais
VERDE_OSC = (0.043, 0.196, 0.157)
ORO = (0.784, 0.643, 0.365)         # #C8A45D
CREMA = (0.980, 0.976, 0.969)       # #FAF9F7
TEXTO = (0.176, 0.192, 0.188)
GRIS = (0.443, 0.451, 0.435)

TITULO = 'didot'
CUERPO = 'georgia'
FUENTES = {
    TITULO: '/System/Library/Fonts/Supplemental/Didot.ttc',
    CUERPO: '/System/Library/Fonts/Supplemental/Georgia.ttf',
}

doc = fitz.open()


def nueva(fondo=CREMA):
    p = doc.new_page(width=W, height=H)
    p.draw_rect(A4, color=None, fill=fondo)
    for n, f in FUENTES.items():
        p.insert_font(fontname=n, fontfile=f)
    return p


def texto(p, x, y, txt, size=10.5, fuente=CUERPO, color=TEXTO, ancho=None, leading=1.5):
    """Escribe respetando el ancho disponible. Devuelve la y final."""
    if ancho is None:
        ancho = W - 2 * M
    caja = fitz.Rect(x, y - size, x + ancho, y + size * leading * 60)
    rc = p.insert_textbox(caja, txt, fontname=fuente, fontsize=size,
                          color=color, lineheight=leading, align=0)
    # insert_textbox devuelve el espacio sobrante; se calcula la altura usada.
    usado = (caja.height - rc) if rc >= 0 else caja.height
    return y + usado - size


def filete(p, y, x0=M, x1=None, color=ORO, grosor=0.8):
    p.draw_line(fitz.Point(x0, y), fitz.Point(x1 or (W - M), y),
                color=color, width=grosor)


def pie(p, n):
    filete(p, H - 46, color=(0.85, 0.83, 0.79), grosor=0.5)
    p.insert_text((M, H - 32), 'Danais Natural Cosmetics · www.danaisnatural.com',
                  fontname=CUERPO, fontsize=7.5, color=GRIS)
    p.insert_text((W - M - 18, H - 32), f'{n:02d}', fontname=CUERPO,
                  fontsize=7.5, color=GRIS)


def foto(p, nombre, rect):
    """Inserta la foto llenando el rectangulo sin deformarla.

    keep_proportion deja bandas cuando la relacion no coincide, asi que se
    recorta antes con PIL para que la imagen ocupe el hueco entero.
    """
    ruta = f'{FOTOS}/{nombre}'
    if not os.path.exists(ruta):
        return
    from PIL import Image, ImageOps
    import io
    im = Image.open(ruta).convert('RGB')
    objetivo = (int(rect.width * 3), int(rect.height * 3))   # 3x para 216 ppp
    im = ImageOps.fit(im, objetivo, Image.LANCZOS, centering=(0.5, 0.5))
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=82, optimize=True)
    p.insert_image(rect, stream=buf.getvalue())


def encabezado(p, eyebrow, titulo, cursiva=None):
    y = M + 14
    p.insert_text((M, y), eyebrow.upper(), fontname=CUERPO, fontsize=8,
                  color=ORO, render_mode=0)
    y += 34
    p.insert_text((M, y), titulo, fontname=TITULO, fontsize=30, color=VERDE)
    if cursiva:
        y += 34
        p.insert_text((M, y), cursiva, fontname=TITULO, fontsize=30, color=VERDE_OSC)
    filete(p, y + 16, x1=M + 90)
    return y + 44


# ─────────────────────────────────────────────── 1. PORTADA
p = nueva(CREMA)
for n, f in FUENTES.items():
    p.insert_font(fontname=n, fontfile=f)
foto(p, 'hero-experiencias.jpg', fitz.Rect(0, 0, W, 400))
p.draw_rect(fitz.Rect(0, 330, W, 430), color=None,
            fill=CREMA, fill_opacity=0.0)
# Banda de degradado simulada con rectangulos de opacidad creciente.
for i in range(24):
    o = i / 24 * 0.95
    p.draw_rect(fitz.Rect(0, 400 - (24 - i) * 5, W, 400 - (23 - i) * 5),
                color=None, fill=CREMA, fill_opacity=o)

# Logo de la marca sobre la banda crema.
logo = f'{BASE}/assets/danais-logo-sin-fondo.png'
if os.path.exists(logo):
    from PIL import Image as _Im
    _l = _Im.open(logo)
    _bb = _l.getchannel('A').getbbox() if _l.mode == 'RGBA' else None
    if _bb:
        _l = _l.crop(_bb)
    _w = 150
    _h = _w * _l.size[1] / _l.size[0]
    import io as _io
    _b = _io.BytesIO()
    _fondo = _Im.new('RGB', _l.size, (250, 249, 247))
    _fondo.paste(_l, (0, 0), _l if _l.mode == 'RGBA' else None)
    _fondo.save(_b, 'PNG')
    p.insert_image(fitz.Rect(M, 452, M + _w, 452 + _h), stream=_b.getvalue())

y = 528
p.insert_text((M, y), 'EXPERIENCIAS DANAIS', fontname=CUERPO, fontsize=9, color=ORO)
y += 46
p.insert_text((M, y), 'Talleres de', fontname=TITULO, fontsize=38, color=VERDE)
y += 42
p.insert_text((M, y), 'cosmética natural', fontname=TITULO, fontsize=38, color=VERDE)
y += 26
filete(p, y, x1=M + 120)
y += 34
texto(p, M, y, 'Para cumpleaños, empresas, hoteles, asociaciones y grupos privados. '
               'Dos horas y media con las manos en la masa, en la Costa Daurada.',
      size=12, ancho=380, leading=1.6)

y = H - 118
filete(p, y - 34, color=(0.85, 0.83, 0.79), grosor=0.5)
p.insert_text((M, y), 'www.danaisnatural.com', fontname=CUERPO, fontsize=10.5, color=VERDE)
p.insert_text((M, y + 18), 'WhatsApp +34 624 70 27 15', fontname=CUERPO, fontsize=10.5, color=TEXTO)
p.insert_text((M, y + 36), 'Mont-roig del Camp · Tarragona', fontname=CUERPO, fontsize=9, color=GRIS)

# ─────────────────────────────────────────────── 2. QUE ES
p = nueva()
y = encabezado(p, 'Qué es', 'Un taller, no', 'una demostración')
y = texto(p, M, y, 'Nadie mira mientras otro trabaja. Cada participante elige su fórmula, la '
                   'elabora con sus manos y se lleva puesto lo que ha hecho.', size=12.5, ancho=440)
y += 26
y = texto(p, M, y, 'Trabajamos con plantas del Mediterráneo —olivo, romero, lavanda, caléndula— y '
                   'explicamos qué hace cada ingrediente y por qué. Sin nombres impronunciables '
                   'y sin prometer lo que un cosmético no puede cumplir.', ancho=440)
y += 34
foto(p, 'como-se-vive.jpg', fitz.Rect(M, y, W - M, y + 250))
y += 274

p.insert_text((M, y), 'IDEAL PARA', fontname=CUERPO, fontsize=8, color=ORO)
y += 22
col = [
    ('Cumpleaños y celebraciones', 'Una actividad que se recuerda más que una comida.'),
    ('Empresas y team building', 'Trabajo en equipo real, con un resultado que cada persona se lleva.'),
    ('Hoteles y turismo', 'Actividad de temporada con identidad local para vuestros huéspedes.'),
    ('Asociaciones y grupos', 'Formato flexible, adaptable a la edad y al perfil del grupo.'),
]
for t, d in col:
    p.insert_text((M, y), t, fontname=TITULO, fontsize=12, color=VERDE)
    y = texto(p, M, y + 15, d, size=9.5, color=GRIS, ancho=440) + 18
pie(p, 2)

# ─────────────────────────────────────────────── 3. LOS TALLERES
p = nueva()
y = encabezado(p, 'Catálogo', 'Los talleres')
talleres = [
    ('Cuidado del cabello rizado',
     'Identifica tu tipo de rizo y elabora los productos clave de tu rutina: gel definidor, '
     'crema de peinar y técnica de aplicación sin frizz.'),
    ('Cosmética capilar natural',
     'Champú y acondicionador sólidos a medida, mascarillas e ingredientes botánicos.'),
    ('Maceraciones botánicas',
     'Infusionar plantas en aceites y crear bases naturales con identidad propia.'),
    ('Ungüentos y bálsamos',
     'Formular cuidados sencillos y útiles, de los que se usan a diario.'),
    ('Aromaterapia',
     'Aromas, mezclas y combinaciones para una experiencia relajante y creativa.'),
    ('Sales de baño',
     'Ideal para celebraciones y detalles personalizados.'),
    ('Mascarillas',
     'Arcillas, plantas, aceites y texturas para una preparación a medida.'),
]
for i, (t, d) in enumerate(talleres, 1):
    p.insert_text((M, y), f'{i:02d}', fontname=TITULO, fontsize=13, color=ORO)
    p.insert_text((M + 30, y), t, fontname=TITULO, fontsize=13.5, color=VERDE)
    y = texto(p, M + 30, y + 17, d, size=9.8, color=GRIS, ancho=420) + 22
y += 6
foto(p, 'cosmetica-capilar.jpg', fitz.Rect(M, y, W - M, y + 190))
pie(p, 3)

# ─────────────────────────────────────────────── 4. COMO FUNCIONA
p = nueva()
y = encabezado(p, 'Cómo funciona', 'Lo que incluye')
bloques = [
    ('Duración', '2 h 30 min de taller, montaje y recogida aparte.'),
    ('Grupo', 'Desde 8 participantes. Adaptamos el formato al tamaño y al perfil.'),
    ('Incluido', 'Dinamización guiada, ingredientes, materiales, utensilios y envases. '
                 'Cada participante se lleva su creación terminada.'),
    ('Dónde', 'Vamos a vuestro espacio —oficina, hotel, casa, sala— o lo organizamos '
              'en un espacio preparado para la actividad.'),
    ('Zona', 'Barcelona y provincia de Tarragona: Reus, Salou, Cambrils, Miami Platja, '
             'Hospitalet de l\'Infant y toda la Costa Daurada hasta Vinaròs. '
             'Fuera de esa zona, consúltanos.'),
]
for t, d in bloques:
    p.insert_text((M, y), t.upper(), fontname=CUERPO, fontsize=8, color=ORO)
    y = texto(p, M, y + 18, d, size=11, ancho=440) + 24
y += 10
foto(p, 'experiencias-cuadrada.jpg', fitz.Rect(M, y, M + 240, y + 240))
foto(p, 'formatos.jpg', fitz.Rect(M + 252, y, W - M, y + 240))
pie(p, 4)

# ─────────────────────────────────────────────── 5. TARIFAS
p = nueva()
y = encabezado(p, 'Tarifas', 'Cuánto cuesta')
tarifas = [
    ('Cumpleaños, despedidas y eventos privados', 'desde 39 € / persona',
     'Mínimo 8 participantes · 2 h 30 min de taller'),
    ('Empresas y team building', 'presupuesto a medida',
     'En vuestras oficinas o en un espacio preparado'),
    ('Hoteles y turismo', 'presupuesto a medida',
     'Según grupo, temporada y montaje'),
]
for t, precio, nota in tarifas:
    p.draw_rect(fitz.Rect(M, y - 14, W - M, y + 52), color=(0.88, 0.86, 0.82),
                fill=(1, 1, 1), width=0.6)
    p.insert_text((M + 16, y + 6), t, fontname=TITULO, fontsize=12.5, color=VERDE)
    p.insert_text((M + 16, y + 24), nota, fontname=CUERPO, fontsize=8.5, color=GRIS)
    p.insert_text((W - M - 150, y + 6), precio, fontname=TITULO, fontsize=12.5, color=VERDE_OSC)
    y += 76
y += 4
y = texto(p, M, y, 'Precios orientativos. El presupuesto final depende del taller elegido, el '
                   'número de participantes, los materiales, el desplazamiento y los extras.',
          size=9, color=GRIS, ancho=440)
y += 34
foto(p, 'otras-experiencias.jpg', fitz.Rect(M, y, W - M, y + 250))
pie(p, 5)

# ─────────────────────────────────────────────── 6. RESERVAR
p = nueva(fondo=VERDE_OSC)
for n, f in FUENTES.items():
    p.insert_font(fontname=n, fontfile=f)
y = M + 30
p.insert_text((M, y), 'RESERVAR', fontname=CUERPO, fontsize=9, color=ORO)
y += 46
p.insert_text((M, y), 'Cuéntanos', fontname=TITULO, fontsize=36, color=(1, 1, 1))
y += 40
p.insert_text((M, y), 'qué quieres crear', fontname=TITULO, fontsize=36, color=ORO)
y += 30
filete(p, y, x1=M + 110, color=ORO)
y += 44

texto(p, M, y, 'Con estos cinco datos te enviamos una propuesta con precio, sin compromiso:',
      size=11.5, color=(0.93, 0.93, 0.90), ancho=430)
y += 44
for d in ['Tipo de evento', 'Número aproximado de personas', 'Ciudad o localidad',
          'Fecha o periodo deseado', 'Taller que te interesa']:
    p.insert_text((M + 4, y), '·', fontname=CUERPO, fontsize=12, color=ORO)
    p.insert_text((M + 20, y), d, fontname=CUERPO, fontsize=11, color=(0.93, 0.93, 0.90))
    y += 24

y += 26
filete(p, y, color=(0.35, 0.45, 0.40), grosor=0.6)
y += 34
p.insert_text((M, y), 'WhatsApp', fontname=CUERPO, fontsize=8, color=ORO)
p.insert_text((M, y + 20), '+34 624 70 27 15', fontname=TITULO, fontsize=17, color=(1, 1, 1))
y += 56
p.insert_text((M, y), 'Formulario', fontname=CUERPO, fontsize=8, color=ORO)
p.insert_text((M, y + 20), 'danaisnatural.com/experiencias', fontname=TITULO,
              fontsize=17, color=(1, 1, 1))
y += 56
p.insert_text((M, y), 'Correo', fontname=CUERPO, fontsize=8, color=ORO)
p.insert_text((M, y + 20), 'marieladanais31@gmail.com', fontname=TITULO,
              fontsize=15, color=(1, 1, 1))

foto(p, 'experiencias-cuadrada.jpg', fitz.Rect(0, H - 190, W, H - 74))
p.insert_text((M, H - 44), 'Danais Natural Cosmetics · Mont-roig del Camp, Tarragona',
              fontname=CUERPO, fontsize=8, color=(0.62, 0.68, 0.64))

doc.set_metadata({
    'title': 'Experiencias Danais · Talleres de cosmética natural',
    'author': 'Danais Natural Cosmetics',
    'subject': 'Dossier comercial de talleres de cosmética natural para grupos, '
               'empresas y hoteles en Tarragona y Barcelona',
    'keywords': 'talleres cosmética natural, experiencias botánicas, team building, '
                'cumpleaños, hoteles, Tarragona, Costa Daurada, cabello rizado',
})
doc.save(SALIDA, deflate=True, garbage=4)
print(f'dossier: {doc.page_count} paginas, {os.path.getsize(SALIDA)//1024} KB')
