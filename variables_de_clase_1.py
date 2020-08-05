class Gato:
    # Recibimos la instancia como primer argumento
    # Podemos nombrar al argumento diferente pero por convención usamos self
    def __init__(self, nombre, edad, peso, color):
        # Definimos VARIABLES DE INSTANCIA
        self.nombre = nombre
        self.edad = edad
        self.peso = peso
        self.color = color
    
    # El argumento self se pasa de manera automática
    def detalles(self):
        return '{} es un gato de {} años color {} que pesa {} kilos.'.format(
            self.nombre,
            self.edad,
            self.color,
            self.peso
        )
    
    def vacunar(self):
        return 'suministramos {} litros contra la rinotraqueitis'.format(
            # Multiplicamos el peso por un valor fijo
            # ¿Qué pasaría si necesitamos cambiar el valor más adelante?
            self.peso * 0.003
        )

tom = Gato('Tom', 3, 7, 'café')
print(tom.vacunar())
