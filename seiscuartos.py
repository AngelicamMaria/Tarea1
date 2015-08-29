#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doscuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""

__author__ = 'juliowaissman'
"""
Modificado para 6 cuartos en 2 pisos.
"""

import entornos
from random import choice


class DosCuartos(entornos.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como
                (robot, A, B) // refiniendo (robot, A,B,C,D,E,F)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"
    //Refiniendo: puede tener valor desde A a F y cada uno puede ser limio p sucio

    Las acciones válidas en el entorno son
            "irA", "irB", "limpiar" y "noOp".
            //refiniendo para 6 cuartos:
            //Derecha, Izquierda, arriba, abajo, limpiar, noOp
            // La accion de derecha no es valido en los cuartos de hasta la izquierda.
            //La acion de la izquierda no es valido en los cuartos de hasta la izquierda.
            //La acion de subir y bajar, solamente es valido en los cuartos de las esquinas.
            //Los cuartos estan de estas dos maneras:
            |D|E|F|
            |A|B|C|

    Los sensores es una tupla
                (robot, limpio?)
    con la ubicación del robot y el estado de limieza

    """

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B,C,D,E,F = estado

        if accion == 'Derecha' and robot =='A':





        """
        return (('A', A, B) if accion == 'irA' else
                ('B', A, B) if accion == 'irB' else
                (robot, A, B) if accion == 'noOp' else
                ('A', 'limpio', B) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio'))
        """
    def sensores(self, estado):
        robot, A, B = estado
        return robot, A if robot == 'A' else B

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1


class AgenteAleatorio(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos.Agente):
    """
    Un agente reactivo simple

    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')


class AgenteReactivoModeloDosCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio','sucio', 'sucio','sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2,'C': 3, 'D': 4,'E':5, 'F': 6}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B ,C, D, E, F= self.modelo[1], self.modelo[2], self.modelo[1], self.modelo[2], self.modelo[1], self.modelo[2]
        return ('noOp' if A == B ==C == D ==E == F == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'Derecha' if robot == 'B' or robot == 'A' robot == 'D' or robot == 'E' else
                'Izquierda' if robot == 'B' or robot == 'C' robot == 'E' or robot == 'F' else
                'Subir' if robot =='A' or robot =='C' else
                'Bajar' if robot =='D' or robot =='E')


def test():
    """
    Prueba del entorno y los agentes

    """
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(DosCuartos(),
                       AgenteAleatorio(['Derecha', 'Izquierda', 'limpiar','Subir','Bajar','noOp']),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoDoscuartos(),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

if __name__ == '__main__':
    test()
