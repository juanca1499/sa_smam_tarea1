#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: monitor.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Perla Velasco & Yonathan Mtz.
# Edición: 
#   Alejandro Carrillo Villegas 
#   César Gabriel Díaz Curiel
#   Juan Carlos García Murillo
#   Josué Guillermo González Pinedo
#   José Germán González Rodarte
# Version: 2.0.2 Marzo 2021
# Descripción:
#
#   Ésta clase define el rol del monitor, es decir, muestra datos, alertas y advertencias sobre los signos vitales de los adultos mayores.
#
#   Las características de ésta clase son las siguientes:
#
#                                            monitor.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |        Monitor        |  - Mostrar datos a los  |         Ninguna        |
#           |                       |    usuarios finales.    |                        |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |  print_notification()  |  - datetime: fecha en que|  - Imprime el mensa-  |
#           |                        |     se envió el mensaje. |    je recibido.       |
#           |                        |  - id: identificador del |                       |
#           |                        |     dispositivo que      |                       |
#           |                        |     envió el mensaje.    |                       |
#           |                        |  - value: valor extremo  |                       |
#           |                        |     que se desea notifi- |                       |
#           |                        |     car.                 |                       |
#           |                        |  - name_param: signo vi- |                       |
#           |                        |     tal que se desea     |                       |
#           |                        |     notificar            |                       |
#           +------------------------+--------------------------+-----------------------+
#           |  print_position()      |  - datetime: fecha en que|  - Imprime el mensa-  |
#           |                        |     se envió el mensaje. |    je recibido.       |
#           |                        |  - id: identificador del |                       |
#           |                        |     dispositivo que      |                       |
#           |                        |     envió el mensaje.    |                       |
#           |                        |  - positions: arreglo que|                       |
#           |                        |    contiene los valores  |                       |
#           |                        |    de los 3 valores.     |                       |
#           |                        |  - model: modelo de la   |                       |
#           |                        |    banda                 |                       |
#           +------------------------+--------------------------+-----------------------+
#           |  print_medicine_       |  - datetime: fecha en que|  - Imprime el mensa-  |
#           |  notification()        |     se envió el mensaje. |    je recibido.       |
#           |                        |  - id: identificador del |                       |
#           |                        |     dispositivo que      |                       |
#           |                        |     envió el mensaje.    |                       |
#           |                        |  - value: dosis del me-  |                       |
#           |                        |    dicamento que toca    |                       |
#           |                        |    suministrar.          |                       |
#           |                        |  - name_param: Medica-   |                       |
#           |                        |    mento que toca        |                       |
#           |                        |    suministrar.          |                       |
#           |                        |  - model: modelo de la   |                       |
#           |                        |    banda                 |                       |
#           +------------------------+--------------------------+-----------------------+
#           |   format_datetime()    |  - datetime: fecha que se|  - Formatea la fecha  |
#           |                        |     formateará.          |    en que se recibió  |
#           |                        |                          |    el mensaje.        |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------


class Monitor:

    def print_notification(self, datetime, id, value, name_param, model):
        print("  ---------------------------------------------------")
        print("    ADVERTENCIA")
        print("  ---------------------------------------------------")
        print("    Se ha detectado un incremento de " + str(name_param) + " (" + str(value) + ")" + " a las " + str(self.format_datetime(datetime)) + " en el adulto mayor que utiliza el dispositivo " + str(model) + ":" + str(id))
        print("")
        print("")

    def print_position(self, datetime, id, positions, model):
        print("  ---------------------------------------------------")
        print("    AVISO POSICIÓN")
        print("  ---------------------------------------------------")
        print("El adulto mayor que utiliza el dispositivo " + str(model) + ":" + str(id) + " tiene las siguientes coordenadas:")
        print("x = " + positions[0])
        print("y = " + positions[1])
        print("z = " + positions[2])
        print("")
        print("")
    
    def print_medicine_notification(self, datetime, id, value, name_param, model):
        print("  ---------------------------------------------------")
        print("    AVISO MEDICAMENTO " + str(datetime))
        print("  ---------------------------------------------------")
        print("Le toca su dosis de " + str(name_param) + " (" + str(value) + ")" + " al adulto mayor que utiliza el dispositivo " + str(model) + ":" + str(id))
        print("")
        print("")
        
    def format_datetime(self, datetime):
        values_datetime = datetime.split(':')
        f_datetime = values_datetime[3] + ":" + values_datetime[4] + " del " + \
            values_datetime[0] + "/" + \
            values_datetime[1] + "/" + values_datetime[2]
        return f_datetime
