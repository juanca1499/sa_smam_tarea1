#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: procesador_de_medicamento.py
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
#                                     procesador_de_medicamento.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se suscribe a los   |
#           |                       |                         |    eventos generados   |
#           |                       |  - Identificar cuando   |    por el wearable     |
#           |     Procesador de     |    a un adulto mayor    |    Xiaomi My Band.     |
#           |      Medicamento      |    le toca tomar un     |                        |
#           |                       |       medicamento.      |    Define en que       |
#           |                       |                         |    momento se le       |
#           |                       |                         |    suministra un       |
#           |                       |                         |    medicamento         |
#           |                       |                         |    a un adulto mayor.  |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Recibe los signos  |
#           |       consume()        |          Ninguno         |    vitales vitales    |
#           |                        |                          |    desde el distribui-|
#           |                        |                          |    dor de mensajes.   |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - ch: propio de Rabbit. |  - Procesa y detecta  |
#           |                        |  - method: propio de     |    en que momento     |
#           |                        |     Rabbit.              |    se le suministra   |
#           |       callback()       |  - properties: propio de |    medicamento.       |
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
from catalogos.medicamento import Medicamento

class ProcesadorMedicamento:

    drugs = []
    array_bands = []
    array_time = []

    def __init__(self,drugs):
        self.drugs = drugs
    
    def consume(self):
        try:
            # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los signos vitales
            channel = connection.channel()
            # Se declara una cola para leer los mensajes enviados por el
            # Publicador
            channel.queue_declare(queue='time', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_message_callback=self.callback, queue='time')
            channel.start_consuming()  # Se realiza la suscripción en el Distribuidor de Mensajes
        except (KeyboardInterrupt, SystemExit):
            channel.close()  # Se cierra la conexión
            sys.exit("Conexión finalizada...")
            time.sleep(1)
            sys.exit("Programa terminado...")

    def callback(self, ch, method, properties, body):
        json_message = self.string_to_json(body)
        
        # Lista de medicamentos del paciente actual
        meds = list(map(int, json_message['drugs'].split()))
        
        #Si la banda no ha emitido ninguna alerta se agreaga
        if json_message['id'] not in array_bands:
            array_bands.append(json_message['id'])
            array_time.append(-1)
        #Si la banda no ha emitido los mensajes correspondientes a dicha hora
        if int(json_message['datetime'].split(':')[-2])!=array_time[array_bands.index(json_message['id'])]:
            # Se recorren los id's de los medicamentos que el paciente tiene asignados.
            for m in meds:
                # Se identifica cuales medicamentos le tocan al paciente de acuerdo 
                # al MINUTO actual (por practicidad).  
                if int(json_message['datetime'].split(':')[-2]) % drugs[m-1].tiempo_dosis == 0:
                    monitor = Monitor()
                    monitor.print_medicine_notification(json_message['datetime'],json_message['id'],drugs[m-1].dosis,drugs[m-1].nombre,json_message['model'])
            #Agrega en el arreglo array_time que se emitieron los mensajes correspondientes a esa hora        
            array_time[array_bands.index(json_message['id'])]= int(json_message['datetime'].split(':')[-2])

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
    # Inicialización de medicamentos.
    drugs = []
    drugs.append(Medicamento('Paracetamol','500mg',2))
    drugs.append(Medicamento('Ibuprofeno','200mg',3))
    drugs.append(Medicamento('Insulina','100mg',2))
    drugs.append(Medicamento('Furosemida','300mg',5))
    drugs.append(Medicamento('Piroxicam','100mg',3))
    drugs.append(Medicamento('Tolbutamida','200mg',2))
    array_bands = []
    array_time = []

    p_medicamento = ProcesadorMedicamento(drugs)
    p_medicamento.consume()