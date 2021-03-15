class Medicamento:
    nombre = ""
    dosis = ""
    tiempo_dosis = 0
    tiempo_actual = 0
    consumidores = []

    def __init__(self, nombre, dosis, tiempo_dosis):
        self.nombre = nombre
        self.dosis = dosis
        self.tiempo_dosis = tiempo_dosis
        self.tiempo_actual = tiempo_dosis

    def agregar_consumidor(self,consumidor):
        consumidores.append(consumidor)
    
    def disminuir_tiempo_dosis(self,segundos):
        tiempo_actual = tiempo_actual - segundos
        if tiempo_actual <= 0:
            tiempo_actual = tiempo_dosis
            