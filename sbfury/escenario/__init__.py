# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright: Hugo Ruscitti
# Web: www.losersjuegos.com.ar

import pilas
import enemigos

class Escenario:
    """Controla la apariencia del escenario y el desplazamiengo de cámara.

    El escenario se va moviendo a medida que el protagonista avanza, y
    en determinados puntos del escenario construye nuevo enemigos.
    """

    def __init__(self, escena_juego):
        self.bloqueada = False
        fondos = [
                    ("nivel1/layer_3.png", -320, 240, 500),
                    ("nivel1/layer_2.png", -320, 240, 450),
                    ("nivel1/layer_1.png", -320, 240, 440),
                    ("nivel1/layer_0.png", -320,  19, 430),
                 ]
        self.capas = []

        for imagen, x, y, z in fondos:
            capa = pilas.actores.Actor(imagen)
            capa.centro = ("izquierda", "arriba")
            capa.x = x
            capa.y = y
            capa.z = z

            self.capas.append(capa)

        self.escena_juego = escena_juego
        self.shaolin = escena_juego.shaolin
        self.cargar_temporizador()
        self._crear_capas()

        self.enemigos = [
            (0, CrearEnemigo(enemigos.Red, 110 - 500, -200)),
            (0, PausaHastaEliminarEnemigos()),
            (500, CrearEnemigo(enemigos.Red, 500 - 500, -150)),
            (500, CrearEnemigo(enemigos.Red, 500 + 500, -100)),
            (500, CrearEnemigo(enemigos.Red, 500 + 500, -200)),
            (800, CrearEnemigo(enemigos.Red, 800 + 500, -200)),
            (800, CrearEnemigo(enemigos.Red, 880, -200)),
        ]

    def cargar_temporizador(self):
        pilas.mundo.tareas.siempre(0.1, self.mover_camara)

    def mover_camara(self):
        if not self._esta_bloqueada():
            camara = pilas.mundo.camara

            if camara.x + 100 < self.shaolin.x:
                camara.x = [self.shaolin.x - 100], 0.1

            self._procesar_creacion_de_enemigos(camara.x)

    def _procesar_creacion_de_enemigos(self, camara_x):
        a_eliminar = []

        for x_creacion, item in self.enemigos:
            if camara_x >= x_creacion:
                item.ejecutar(self)
                a_eliminar.append((x_creacion, item))

        if a_eliminar:
            for x in a_eliminar:
                self.enemigos.remove(x)

    def _esta_bloqueada(self):
        """Retorna True si la camara tiene que permanecer estática."""
        if self.bloqueada:
            if self.escena_juego.cantidad_de_enemigos == 0:
                self.bloqueada = False

        return self.bloqueada

    def _crear_capas(self):
        fondo = pilas.fondos.Desplazamiento()
        fondo.agregar(self.capas[0], (1793)/(5300.0 + 640))
        fondo.agregar(self.capas[1], 0.5567)
        fondo.agregar(self.capas[2], 1)
        fondo.agregar(self.capas[3], 1)

    def bloquear_camara(self):
        self.bloqueada = True


class Item:
    """Representa un elemento del escenario que se tiene que construir."""

    def ejecutar(self):
        raise Exception("Metodo no implementado")

class CrearEnemigo(Item):
    """Representa al creación de un enemigo."""

    def __init__(self, clase_enemigo, x, y):
        self.clase_enemigo = clase_enemigo
        self.x = x
        self.y = y

    def ejecutar(self, escenario):
        escenario.escena_juego.crear_enemigo(self.clase_enemigo, self.x, self.y)

class PausaHastaEliminarEnemigos(Item):
    """Realiza una bloqueo del desplazamiento de camara en el escenario.

    Este bloqueo de desplazamiento queda activo hasta que se logren
    eliminar a todos los enemigos que existan en la pantalla."""

    def ejecutar(self, escenario):
        print "bloqueando la escena."
        escenario.bloquear_camara()
