#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: procesador_de_medicamento.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Equipo 3
# Version: 2.0.1 Marzo 2021
# Descripción:
#
#   Esta clase define el rol de un suscriptor, es decir, es un componente que recibe mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                     procesador_de_presion.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se suscribe a los   |
#           |                       |                         |    eventos generados   |
#           |                       |  - Identificar cuando   |    por el wearable     |
#           |     Procesador de     |    a un adulto mayor    |    Xiaomi My Band.     |
#           |        Medicamento    |    le toca tomar un     |                        |
#           |                       |       medicamento.      |  - Define el valor ex- |
#           |                       |                         |    tremo de la presión |
#           |                       |                         |    arterial en 110.    |
#           |                       |                         |  - Notifica al monitor |
#           |                       |                         |    cuando un valor ex- |
#           |                       |                         |    tremo es detectado. |
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
#           |                        |  - method: propio de     |    valores extremos de|
#           |                        |     Rabbit.              |    la presión         |
#           |       callback()       |  - properties: propio de |    arterial.          |
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

    medicamentos = []
    break_val = 3

    def __init__(self,medicamentos):
        self.medicamentos = medicamentos
        self.break_val = 3
    
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
        self.break_val = self.break_val - 1
        print(json_message['datetime'])

        #print(json_message['medicamentos'])

        #if self.break_val == 0:
         #   monitor = Monitor()
          #  monitor.print_medicine_notification(json_message['datetime'], json_message['id'],medicamentos[2].dosis, 
           # 'medicamento', json_message['model'])
            #self.break_val = 3

        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def string_to_json(self, string):
        print("MENSAJE:" + str(string))
        message = {}
        string = string.decode('utf-8')
        string = string.replace('{', '')
        string = string.replace('}', '')
        values = string.split(', ')
        for x in values:
            v = x.split(': ')
            message[v[0].replace('\'', '')] = v[1].replace('\'', '')
        return message

    def __reducir_tiempo(self,segundos):
        pass


if __name__ == '__main__':
    # Inicialización de medicamentos.
    medicamentos = []
    medicamentos.append(Medicamento('Paracetamol','500mg',8))
    medicamentos.append(Medicamento('Ibuprofeno','200mg',12))
    medicamentos.append(Medicamento('Insulina','100mg',12))
    medicamentos.append(Medicamento('Furosemida','300mg',8))
    medicamentos.append(Medicamento('Piroxicam','100mg',24))
    medicamentos.append(Medicamento('Tolbutamida','200mg',24))

    p_medicamento = ProcesadorMedicamento(medicamentos)
    p_medicamento.consume()