import pygame
import sys
import random

pygame.init()
ANCHO, ALTO = 1600, 1200
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("¡Felices 50 Papá!")

try:
    icono = pygame.image.load("icono.png")
    pygame.display.set_icon(icono)
except: pass

ORO, BLANCO = (212, 175, 55), (255, 255, 255)

# Carga de recursos
fondo = pygame.transform.scale(pygame.image.load("sala.png").convert(), (ANCHO, ALTO))
papa = pygame.transform.scale(pygame.image.load("papa pixel.png").convert_alpha(), (160, 260))

cuadros_orig = {
    "esther": pygame.transform.scale(pygame.image.load("Esther pixel.png").convert_alpha(), (300, 220)),
    "jordi": pygame.transform.scale(pygame.image.load("Jordi pixel.png").convert_alpha(), (180, 180)),
    "andrea": pygame.transform.scale(pygame.image.load("Andrea pixel.png").convert_alpha(), (180, 180))
}
cuadros_dibujo = cuadros_orig.copy()
rects = {k: v.get_rect(center=(800 if k=="esther" else (450 if k=="jordi" else 1150), 350)) for k, v in cuadros_orig.items()}

mensajes = {
    "esther": "Feliz cumpleaños amorcito querido, doy gracias a Dios por haber formado una familia contigo. \n\nEres mi cómplice perfecto, sabes que los dos unidos hacemos uno, separados estamos incompletos. \n\nA pesar de las dificultades, siempre nos hemos demostrado confianza y fidelidad. \n\nNo cambies porque estoy muy orgullosa de ti y de nuestra vida juntos. \n\nTe quiero, eres tan necesario como el aire que respiro. \n\nFelices 50 años, sigues estando muy sexy.",
    "jordi": "Papá, feliz 50 aniversario, son un montón ya. \n\nEs increíble todo lo que has hecho a lo largo de estos 50 años, y que aún tengas energía para seguir dando guerra, y sin quedarte calvo ni tener casi canas. \n\nLa verdad es que, aunque ahora no esté tan presente con vosotros, estoy muy contento de teneros. \n\nMuchas felicidades y a seguir.",
    "andrea": "Quién diría que llegaríamos a estar todos juntos, aquí, celebrando un cumpleaños tan importante como el de hoy. \n\n50 años... la vuelta del jamón, ese punto en el que dices 'Ya he vivido mucho' porque se empiezan a acumular los dolores, pero en el que también debes pensar 'Aún me queda la otra mitad por vivir'. \n\nNo sabes lo que me alegro de tenerte. Tu apoyo es como un pilar que me anima a seguir y a lograr metas solo con el objetivo de verte orgulloso y poder seguir viéndote sonreír. \n\nEs cierto que, para ti, 50 puede parecer un número muy grande, pero piensa que yo solo he experimentado 16 años a tu lado; ni la mitad de lo que tú has vivido, pero eso es toda mi vida, y no quiero dejar de disfrutarla contigo. \n\nFeliz 50 cumpleaños, papá. \n\nTe quiero 3.000 toneladas."
}

# Sistema de Confeti
particulas = []
def crear_confeti():
    for _ in range(50):
        particulas.append([random.randint(0, ANCHO), -10, random.randint(1, 3), random.choice([ORO, BLANCO])])

def renderizar_texto_ajustado(superficie, texto, fuente, color):
    global altura_total_texto
    y = 20 + scroll_y
    for parrafo in texto.split('\n'):
        palabras = parrafo.split(' ')
        x = 20
        for palabra in palabras:
            render = fuente.render(palabra, True, color)
            if x + render.get_width() > 960:
                x = 20; y += fuente.get_height() + 5
            superficie.blit(render, (x, y))
            x += render.get_width() + fuente.size(' ')[0]
        y += fuente.get_height() + 5
    altura_total_texto = y - scroll_y

estado = "intro"; mostrar_cuadro = None; scroll_y = 0; musica_activa = True
fade_alpha = 0; fade_surface = pygame.Surface((ANCHO, ALTO)); fade_surface.fill((0, 0, 0))

while True:
    pos_raton = pygame.mouse.get_pos()
    sobre_cuadro = any(rects[n].collidepoint(pos_raton) for n in cuadros_orig) if (estado == "salon" and not mostrar_cuadro) else False
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if sobre_cuadro else pygame.SYSTEM_CURSOR_ARROW)

    for e in pygame.event.get():
        if e.type == pygame.QUIT: 
            pygame.mixer.music.fadeout(1000); pygame.quit(); sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_m:
                musica_activa = not musica_activa
                if not musica_activa: pygame.mixer.music.pause()
                else: pygame.mixer.music.unpause()
            elif e.key == pygame.K_ESCAPE:
                if estado == "salon": estado = "final"; fade_alpha = 255
                elif estado == "final": estado = "salon"; fade_alpha = 255
        
        elif e.type == pygame.MOUSEWHEEL and mostrar_cuadro:
            scroll_y = max(min(0, 400 - altura_total_texto), min(0, scroll_y + e.y * 40))
        elif e.type == pygame.MOUSEBUTTONDOWN and estado == "intro":
            estado = "salon"; pygame.mixer.music.load("cumple.mp3"); pygame.mixer.music.set_volume(0.2); pygame.mixer.music.play(-1); fade_alpha = 255
        elif e.type == pygame.MOUSEBUTTONDOWN and estado == "salon":
            if not mostrar_cuadro:
                for n, r in rects.items():
                    if r.collidepoint(e.pos): mostrar_cuadro = n; scroll_y = 0; fade_alpha = 150; crear_confeti()
            elif mostrar_cuadro and (1270 <= e.pos[0] <= 1300 and 360 <= e.pos[1] <= 390):
                mostrar_cuadro = None; fade_alpha = 150

    if estado == "salon" and not mostrar_cuadro:
        for n in cuadros_orig:
            if rects[n].collidepoint(pos_raton):
                nuevo_tam = (int(cuadros_orig[n].get_width()*1.1), int(cuadros_orig[n].get_height()*1.1))
                cuadros_dibujo[n] = pygame.transform.scale(cuadros_orig[n], nuevo_tam)
            else: cuadros_dibujo[n] = cuadros_orig[n]

    if fade_alpha > 0: fade_alpha -= 5
    
    pantalla.fill((0, 0, 0))
    if estado == "intro":
        for i in range(ALTO):
            c = int(30 * (1 - i/ALTO))
            pygame.draw.line(pantalla, (c, c, c), (0, i), (ANCHO, i))
        pygame.draw.rect(pantalla, ORO, (50, 50, ANCHO-100, ALTO-100), 5)
        t1 = pygame.font.SysFont("Verdana", 75, bold=True).render("¡FELIZ 50 CUMPLEAÑOS PAPÁ!", True, ORO)
        pantalla.blit(t1, (ANCHO//2 - t1.get_width()//2, 400))
        t2 = pygame.font.SysFont("Verdana", 30, italic=True).render("Haz clic para entrar • Pulsa 'M' para silenciar", True, BLANCO)
        pantalla.blit(t2, (ANCHO//2 - t2.get_width()//2, 700))
    elif estado == "salon":
        pantalla.blit(fondo, (0,0))
        pantalla.blit(papa, (580, 540))
        for n in cuadros_dibujo:
            r_dibujo = cuadros_dibujo[n].get_rect(center=rects[n].center)
            pantalla.blit(cuadros_dibujo[n], r_dibujo)
        
        # Confeti
        for p in particulas[:]:
            p[1] += p[2]
            pygame.draw.circle(pantalla, p[3], (p[0], p[1]), 5)
            if p[1] > ALTO: particulas.remove(p)

        if mostrar_cuadro:
            caja = pygame.Surface((1000, 500), pygame.SRCALPHA); caja.fill((0, 0, 0, 220))
            renderizar_texto_ajustado(caja, mensajes[mostrar_cuadro], pygame.font.SysFont("Verdana", 28), BLANCO)
            pantalla.blit(caja, (300, 350))
            pygame.draw.rect(pantalla, (200, 0, 0), (1270, 360, 30, 30))
            pantalla.blit(pygame.font.SysFont("Verdana", 25, bold=True).render("X", True, BLANCO), (1278, 363))
    elif estado == "final":
        t = pygame.font.SysFont("Verdana", 80, bold=True).render("¡Disfruta mucho de tu día, Papá!", True, ORO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, ALTO//2))
        t_sub = pygame.font.SysFont("Verdana", 30, italic=True).render("(Pulsa ESC para volver al salón)", True, BLANCO)
        pantalla.blit(t_sub, (ANCHO//2 - t_sub.get_width()//2, ALTO//2 + 100))
    
    if fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        pantalla.blit(fade_surface, (0,0))
    pygame.display.flip()