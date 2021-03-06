from datetime import datetime, timedelta
from enum import Enum, unique
from time import sleep
from math import pi

@unique
class TipoZombie(Enum):
    ''' Clase usada para especificar el tipo de Zombie '''
    ZOMBIEBAILARIN = 1
    ZOMBIEPULTA    = 2
    ZOMBIEINSTEIN  = 3
    ZOMBIEACUATICO = 4
    ZOMBIEVOLADOR  = 5

class Zombie:

    NORMAL   =  5
    ENFADADO = 10
    AGRESIVO = 20

    TIEMPO_DE_VIDA = timedelta(minutes=5)

    def __init__(self, nombre:str, tipo:TipoZombie, factor_supervicencia:int = 1):
        if not isinstance(tipo, TipoZombie):
            raise Exception('-E- Tipo de Zombie inválido')
        self._nombre = nombre
        self._tipo = tipo
        self._ultimo_alimento = datetime.now()
        self._cerebros_devorados = 0
        self._factor_supervivencia = factor_supervicencia
        self._timestamp = datetime.now()

    def __str__(self) -> str:
        return self.info()

    @property
    def tiempo_sin_alimento(self) -> timedelta:
        ''' Regresa el tiempo transcurrido desde la última vez que nuestro zombie comió '''
        return datetime.now() - self._ultimo_alimento

    def info(self) -> str:
        ''' Retorna los detalles de nuestro Zombie incluyendo cuanto tiempo ha pasado desde su último cerebro.'''
        return f'''
        Zombi
        --------------------
        Nombre:         {self._nombre}
        Tipo:           {self._tipo.name}
        Último cerebro: {self.tiempo_sin_alimento}
        '''

    def comer(self) -> None:
        ''' Reinicia el tiempo que ha pasado sin alimento nuestro zombie '''
        self._ultimo_alimento = datetime.now()
        self._cerebros_devorados += 1

    @property
    def estado_de_animo(self) -> str:
        ''' Regresa el estado de ánimo de nuestro zombie basado en el tiempo que ha pasado sin comer '''
        if self.tiempo_sin_alimento > timedelta(seconds=self.AGRESIVO):
            return 'agresivo'
        elif self.tiempo_sin_alimento > timedelta(seconds=self.ENFADADO):
            return 'enfadado'
        elif self.tiempo_sin_alimento > timedelta(seconds=self.NORMAL):
            return 'normal'
        else:
            return 'contento'
    
    @property
    def peligrosidad(self) -> str:
        ''' Regresa el nivel de peligrosidad del zombie en tres niveles alta, media o baja '''
        tipo_agresivo = self._tipo == TipoZombie.ZOMBIEINSTEIN or self._tipo == TipoZombie.ZOMBIEPULTA
        con_buen_animo = self.estado_de_animo == 'contento' or self.estado_de_animo == 'normal'
        if not tipo_agresivo and con_buen_animo and self._cerebros_devorados >= 1:
            return 'baja'
        elif not tipo_agresivo and not con_buen_animo and self._cerebros_devorados >= 1:
            return 'media'
        else:
            return 'alta'
    
    @property
    def tiempo_de_vida_total(self) -> timedelta:
        ''' Regresa el tiempo que el zombie tiene antes de desaparecer. Si se come un cerebro, entonces se suman 2 minutos'''
        return Zombie.TIEMPO_DE_VIDA * self._factor_supervivencia + \
                timedelta(minutes=2) * self._cerebros_devorados
    
    @property
    def tiempo_de_vida_restante(self) -> timedelta:
        ''' Regresa el tiempo que le resta al zombie basado en el tiempo de vida total '''
        return self.tiempo_de_vida_total - (datetime.now() - self._timestamp)

    # SPLIT TEMPORARY VARIABLE
    # Extraemos las variables y sus expresiones a métodos separados
    def ir(self, lugar:str, tiempo_del_recorrido:timedelta) -> str:
        '''
        Regresa un mensaje con los detalles del recorrido.
        indica si el zombie debería de ir a tal lugar basado en
        el tiempo de vida que le queda
        '''
        if self.tiempo_de_vida_restante >= tiempo_del_recorrido:
            return f'Adelante, puede ir al {lugar}', True
        else:
            return f'No se recomienda ir al {lugar}. Desaparecerá antes', False
    
    def buscar_cerebros(self, radio: int) -> str:
        ''' Regresa los detalles asociados a la búsqueda de cerebros. El
            radio está en kilómetros'''
        perimetro = 2 * pi * radio
        area = pi * pow(radio, 2)
        return f'''Detalles de la búsqueda
        perímetro: {perimetro} km
        radio    : {area} km
        '''

class ZombieBailarin(Zombie):
    def __init__(self, nombre:str):
        super().__init__(nombre, TipoZombie.ZOMBIEBAILARIN, 1.5)

if __name__ == "__main__":
    # Creamos al zombie
    zombie_bailarin = ZombieBailarin('Zombie bailarín 1')

    # Esperamos un poco antes de preguntar por sus detalles
    print('-I- Buscando cerebros...')
    print(f'-I- {zombie_bailarin.buscar_cerebros(10)}')
    sleep(4)
    print('-I- Encontramos uno, a comer...')
    zombie_bailarin.comer()
    print('-I- Buscando cerebros...')
    print(f'-I- {zombie_bailarin.buscar_cerebros(2)}')
    sleep(3)

    # Veamos si puede llegar al refugio para zombies. Primero vemos el tiempo
    # de vida total que le queda
    print(f'-I- Tiempo de vida total: {zombie_bailarin.tiempo_de_vida_total}')
    print(f'-I- Tiempo de vida restante: {zombie_bailarin.tiempo_de_vida_restante}')

    # Llamamos al método ir... veamos que nos dice
    msg, puede_ir = zombie_bailarin.ir('refugio para zombies', timedelta(minutes=250))
    if puede_ir:
        print(f'-I- {msg}')
    else:
        print(f'-W- {msg}')