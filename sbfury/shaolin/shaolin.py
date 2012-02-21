# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright: Hugo Ruscitti
# Web: www.losersjuegos.com.ar
import pilas
import estados
import personaje

class Shaolin(personaje.Personaje):
    """El protagonista del juego."""

    def __init__(self, enemigos):
        self._cargar_animaciones()
        personaje.Personaje.__init__(self)
        self.hacer(estados.Parado())
        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_una_tecla)
        self.cargar_sonidos()
        self.x = -230
        self.y = -120
        self.actualizar()
        self.enemigos = enemigos

    def actualizar(self):
        personaje.Personaje.actualizar(self)

    def _cargar_animaciones(self):
        cargar = pilas.imagenes.cargar_grilla
        self.animaciones = {
            "parado": cargar("shaolin/parado.png", 4),
            "camina": cargar("shaolin/camina.png", 4),
            "ataca0": cargar("shaolin/ataca0.png", 2),
            "ataca1": cargar("shaolin/ataca1.png", 2),
            "ataca2": cargar("shaolin/ataca0.png", 2),
            "ataca3": cargar("shaolin/ataca1.png", 2),
            "ataca4": cargar("shaolin/ataca4.png", 4),
            "salta": cargar("shaolin/salta.png", 3),
            "levantandose": cargar("shaolin/levantandose.png", 1),
            "ataque_aereo": cargar("shaolin/ataque_aereo.png", 2),
            "es_golpeado": cargar("shaolin/es_golpeado.png", 2),
            "es_golpeado_fuerte": cargar("shaolin/es_golpeado_fuerte.png", 2),
            "en_el_suelo": cargar("shaolin/en_el_suelo.png", 1),
        }

    def cuando_pulsa_una_tecla(self, evento):
        if evento.codigo == pilas.simbolos.a:
            self.comportamiento_actual.pulsa_saltar()
        elif evento.codigo == pilas.simbolos.d:
            self.comportamiento_actual.pulsa_golpear()

    def cargar_sonidos(self):
        self.sonidos = {
            'golpe': pilas.sonidos.cargar("sonidos/golpe.wav"),
            #'musica': pilas.sonidos.cargar("musica/menu.wav"),
        }
        
    def reproducir_sonido(self, nombre):
        self.sonidos[nombre].reproducir()

    def ha_sido_golpeado(self, quien, fuerte=False):
        self.comportamiento_actual.ha_sido_golpeado(quien, fuerte)

    def reducir_energia(self, cantidad):
        "Reduce la energia del shaolin y emite evento avisando a la barra de energia."
        self.energia -= cantidad
        pilas.eventos.se_golpea_a_shaolin.emitir(quien=self)
