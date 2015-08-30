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
        """
        En caso de la acciond e la derecha...
        """
        if accion == 'Derecha' and robot =='A' or robot =='B' orrobot =='D' or robot =='E':
            if robot=='A':
                return ('B', A, B,C,D,E,F)
             if robot=='B':
                return ('C', A, B,C,D,E,F)
             if robot=='D':
                return ('E', A, B,C,D,E,F)
             if robot=='E':
                return ('F', A, B,C,D,E,F)
        """
        En caso de la accion de la izquierda...
        """
        if accion == 'Izquierda' and robot =='C' or robot =='B' or robot =='F' or robot =='E':
            if robot=='E':
                return ('D', A, B,C,D,E,F)
             if robot=='F':
                return ('E', A, B,C,D,E,F)
             if robot=='B':
                return ('A', A, B,C,D,E,F)
             if robot=='C':
                return ('B', A, B,C,D,E,F)
        """
        En caso de la accion Subir..
        """
        if accion == 'Subir' and robot =='C' or robot =='A':
            if robot=='C':
                return ('F', A, B,C,D,E,F)
             if robot=='A':
                return ('D', A, B,C,D,E,F)
        """
        En caso de la accion Bajar..
        """
        if accion == 'Bajar' and robot =='D' or robot =='F':
            if robot=='D':
                return ('A', A, B,C,D,E,F)
             if robot=='F':
                return ('C', A, B,C,D,E,F)
        """
        En caso de la accion Limpiar
        """
        if accion == 'limpiar':
            if robot =='A':
                return ('A','limpio',B,C,D,E,F)
            if robot =='B':
                return ('B',A,'limpio',C,D,E,F)
            if robot =='C':
                return ('C',A,B,'limpio',D,E,F)
            if robot =='D':
                return ('D',A,B,C,'limpio',E,F)
            if robot =='E':
                return ('E',A,B,C,D,'limpio',F)
            if robot =='F':
                return ('F',A,B,C,D,E,'limpio')
        if accion=='noOp':
            return(robot,A,B,C,D,E,F)


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
               'Derecha' if robot == 'B' or robot == 'A' or robot == 'D' or robot == 'E' else
                'Izquierda' if robot == 'B' or robot == 'C' or robot == 'E' or robot == 'F' else
                'Subir' if robot =='A' or robot =='C' else
                'Bajar' if robot =='D' or robot =='E' else
                'noOp'
                )


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
                'Derecha' if robot == 'B' or robot == 'A' or robot == 'D' or robot == 'E' else
                'Izquierda' if robot == 'B' or robot == 'C' or robot == 'E' or robot == 'F' else
                'Subir' if robot =='A' or robot =='C' else
                'Bajar' if robot =='D' or robot =='E' else
                'noOp'
                )


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
