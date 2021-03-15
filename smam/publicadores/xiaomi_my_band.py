#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------
# Archivo: xiaomi_my_band.py
# Capitulo: 3 Patrón Publica-Subscribe
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
#   Ésta clase define el rol de un publicador, es decir, es un componente que envia mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                       xiaomi_my_band.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Enviar mensajes      |  - Simula información  |
#           |      Publicador       |                         |    sobre algunos signos|
#           |                       |                         |    vitales.            |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +-----------------------------+--------------------------+-----------------------+
#           |         Nombre              |        Parámetros        |        Función        |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Inicializa el      |
#           |       __init__()            |          int: id         |    wearable indicando |
#           |                             |                          |    su identificador.  |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Envía los signos   |
#           |        publish()            |          Ninguno         |    vitales al distri- |
#           |                             |                          |    buidor de mensajes.|
#           +-----------------------------+--------------------------+-----------------------+
#           |   simulate_datetime()       |          Ninguno         |  - Simula valores de  |
#           |                             |                          |    fecha y hora.      |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |          Ninguno         |  - Simula el valor de |
#           |  simulate_x_position()      |                          |    la aceleración en  |
#           |                             |                          |    eje x.             |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula el valor de |
#           |  simulate_y_position()      |          Ninguno         |    la aceleración en  |
#           |                             |                          |    eje y.             |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula el valor de |
#           |  simulate_z_position()      |          Ninguno         |    la aceleración en  |
#           |                             |                          |    eje z.             |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula el valor de |
#           | simulate_body_temperature() |          Ninguno         |    la temperatura     |
#           |                             |                          |    corporal.          |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula los pasos   |
#           |    simulate_step_count()    |          Ninguno         |    dados por un       |
#           |                             |                          |    adulto.            |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula la bateria  |
#           |  simulate_battery_level()   |          Ninguno         |    restante del       |
#           |                             |                          |    wearable.          |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula las horas   |
#           | simulate_hours_of_sleep()   |          Ninguno         |    sueño acumuladas   |
#           |                             |                          |    por un adulto.     |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula las calorias|
#           | simulate_calories_burned()  |          Ninguno         |    consumidas por un  |
#           |                             |                          |    adulto en un día.  |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula el ritmo    |
#           |    simulate_heart_rate()    |          Ninguno         |    cardiaco del cora- |
#           |                             |                          |    zón.               |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |          Ninguno         |  - Simula la presión  |
#           | simulate_blood_preasure()   |                          |    arterial.          |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Agrega el identifi-|
#           |                             |          Ninguno         |    cador de medicamen-|
#           | simulate_drugs()            |                          |    tos de manera      |
#           |                             |                          |    aleatoria.         |
#           +-----------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import pika
import random
import time


class XiaomiMyBand:
    producer = "Xiaomi"
    model = "Xiaomi My Band 2"
    hardware_version = "2.0.3.2.1"
    software_version = "10.2.3.1"
    step_count = 0
    battery_level = 81
    id = 0

    def __init__(self, id):
        self.id = id
        self.medicamentos = self.simulate_drugs()

    def publish(self):
        message = {}
        message['body_temperature'] = self.simulate_body_temperature()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        # Se declara una cola para persistir los mensajes enviados
        channel.queue_declare(queue='body_temperature', durable=True)
        channel.basic_publish(exchange='', routing_key='body_temperature', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión

        time.sleep(1)

        message = {}
        message['heart_rate'] = self.simulate_heart_rate()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        channel.queue_declare(queue='heart_rate', durable=True)
        channel.basic_publish(exchange='', routing_key='heart_rate', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión

        time.sleep(1)
        
        message = {}
        message['blood_preasure'] = self.simulate_blood_preasure()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        channel.queue_declare(queue='blood_preasure', durable=True)
        channel.basic_publish(exchange='', routing_key='blood_preasure', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión

        time.sleep(1)

        message['posicion_x'] = self.simulate_x_position()
        message['posicion_y'] = self.simulate_y_position()
        message['posicion_z'] = self.simulate_z_position()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        channel.queue_declare(queue='posicion', durable=True)
        channel.basic_publish(exchange='', routing_key='posicion', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión

        time.sleep(1)

        message = {}
        message['drugs'] = self.medicamentos
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        # Se declara una cola para persistir los mensajes enviados
        channel.queue_declare(queue='time', durable=True)
        channel.basic_publish(exchange='', routing_key='time', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión        
  
    def simulate_datetime(self):
        return time.strftime("%d:%m:%Y:%H:%M:%S")

    def simulate_x_position(self):
        return random.uniform(0, 1)

    def simulate_y_position(self):
        return random.uniform(0, 1)

    def simulate_z_position(self):
        return random.uniform(0, 1)

    def simulate_body_temperature(self):
        return random.uniform(67, 72)

    def simulate_step_count(self):
        self.step_count += 1
        return self.step_count

    def simulate_battery_level(self):
        self.battery_level -= 1
        return self.battery_level

    def simulate_hours_of_sleep(self):
        hours_sleep = 10 - random.uniform(0, 3)
        return hours_sleep

    def simulate_calories_burned(self):
        return random.randint(1500, 2500)

    def simulate_heart_rate(self):
        return random.randint(60, 150)

    def simulate_blood_preasure(self):
        return random.randint(100, 200)

    def simulate_drugs(self):
        assigned_drugs = random.randint(1,5)
        drugs = []
        for d in range(0,assigned_drugs):
            drug = random.randint(1,6)
            if drug not in drugs:
                drugs.append(drug)
        drugs_str = ' '.join(str(e) for e in drugs)
        return drugs_str                                                     
