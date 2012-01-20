# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright: Hugo Ruscitti
# Web: www.losersjuegos.com.ar
import pilas

class Escenario:

    def __init__(self, shaolin):
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

        #pilas.mundo.camara.x = [1000], 20

        self.shaolin = shaolin
        self.cargar_temporizador()
        self.crear_capas()

    def cargar_temporizador(self):
        pilas.mundo.tareas.siempre(0.1, self.mover_camara)

    def mover_camara(self):
        camara = pilas.mundo.camara
        if camara.x + 100 < self.shaolin.x:
            camara.x = [self.shaolin.x - 100], 0.1


    def crear_capas(self):
        fondo = pilas.fondos.Desplazamiento()
        fondo.agregar(self.capas[0], (1793)/(5300.0 + 640))
        fondo.agregar(self.capas[1], 0.5567)
        fondo.agregar(self.capas[2], 1)
        fondo.agregar(self.capas[3], 1)


