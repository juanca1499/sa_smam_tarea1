#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: Medicamento.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): 
#   Alejandro Carrillo Villegas 
#   César Gabriel Díaz Curiel
#   Juan Carlos García Murillo
#   Josué Guillermo González Pinedo
#   José Germán González Rodarte
# Version: 2.0.2 Marzo 2021
# Descripción:
#
#   Esta clase define las caracteristicas de un medicamento.
#
#   Las características de ésta clase son las siguientes:
#
#                                          Medicamento.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |                  |
#           |                       |                         |                        |
#           |                       |  - Almacenar            |                        |
#           |      Medicamento      |    datos de un          |                        |
#           |                       |    medicamento.         |                        |
#           |                       |                         |    Define en que       |
#           |                       |                         |    momento se le       |
#           |                       |                         |    suministra un       |
#           |                       |                         |    medicamento         |
#           |                       |                         |    a un adulto mayor.  |
#           +-----------------------+-------------------------+------------------------+
#
#-------------------------------------------------------------------------

class Medicamento:
    nombre = ""
    dosis = ""
    tiempo_dosis = 0

    def __init__(self, nombre, dosis, tiempo_dosis):
        self.nombre = nombre
        self.dosis = dosis
        self.tiempo_dosis = tiempo_dosis
            