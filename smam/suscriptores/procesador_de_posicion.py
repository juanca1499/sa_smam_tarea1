#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: procesador_de_posicion.py
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
#   Esta clase define el rol de un suscriptor, es decir, es un componente que recibe mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                   procesador_de_posicion.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se suscribe a los   |
#           |                       |                         |    eventos generados   |
#           |                       |  - Procesar valores     |    por el wearable     |
#           |     Procesador de     |    de posición en       |    Xiaomi My Band.     |
#           |     posición          |    tres ejes.           |  - Indica valores de   |
#           |                       |                         |    la posición en la   |
#           |                       |                         |    que se encuentra    |
#           |                       |                         |    el individuo.       |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Recibe los valores |
#           |       consume()        |          Ninguno         |    de tres ejes       |
#           |                        |                          |    desde el distribui-|
#           |                        |                          |    dor de mensajes.   |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - ch: propio de Rabbit. |  - Procesa los valores|
#           |                        |  - method: propio de     |    de tres ejes       |
#           |                        |     Rabbit.              |    referentes a la    |
#           |       callback()       |  - properties: propio de |    posición.          |
#           |                        |     Rabbit.              |                       |
#           |                        |  - body: mensaje recibi- |                       |
#           |                        |     do.                  |                       |
#           +------------------------+--------------------------+-----------------------+
#           |    string_to_json()    |  - string: texto a con-  |  - Convierte un string|
#           |                        |     vertir en JSON.      |    en un objeto JSON. |
#           +------------------------+--------------------------+-----------------------+
#
#
#           Nota: "propio de Rabbit" implica que se utilizan de manera interna para realizar
#            de manera correcta la recepcion de datos, para éste ejemplo no shubo necesidad
#            de utilizarlos y para evitar la sobrecarga de información se han omitido sus
#            detalles. Para más información acerca del funcionamiento interno de RabbitMQ
#            puedes visitar: https://www.rabbitmq.com/
#
#-------------------------------------------------------------------------
import pika
import sys
sys.path.append('../')
from monitor import Monitor
import time


class ProcesadorPosicion:

    def consume(self):
        try:
            # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los valores de los tres ejes referentes a la posicion
            channel = connection.channel()
            # Se declara una cola para leer los mensajes enviados por el
            # Publicador
            channel.queue_declare(queue='posicion', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_message_callback=self.callback, queue='posicion')
            channel.start_consuming()  # Se realiza la suscripción en el Distribuidor de Mensajes
        except (KeyboardInterrupt, SystemExit):
            channel.close()  # Se cierra la conexión
            sys.exit("Conexión finalizada...")
            time.sleep(1)
            sys.exit("Programa terminado...")

    def callback(self, ch, method, properties, body):
        json_message = self.string_to_json(body)
        posiciones = [json_message['posicion_x'],json_message['posicion_y'],json_message['posicion_z']] 
        monitor = Monitor()
        monitor.print_position(json_message['datetime'], json_message['id'], posiciones, json_message['model'])
        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def string_to_json(self, string):
        message = {}
        string = string.decode('utf-8')
        string = string.replace('{', '')
        string = string.replace('}', '')
        values = string.split(', ')
        for x in values:
            v = x.split(': ')
            message[v[0].replace('\'', '')] = v[1].replace('\'', '')
        return message

if __name__ == '__main__':
    p_posicion = ProcesadorPosicion()
    p_posicion.consume()
