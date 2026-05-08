"""
Funciones de simulación de sensores IoT para vehículos.
"""

import random
from config import (
    COORDENADAS_BASE,
    GPS_RANGO_LATITUD,
    GPS_RANGO_LONGITUD,
    GPS_RANGO_VELOCIDAD,
    TEMPERATURA_RANGO,
    COMBUSTIBLE_RANGO,
)


def simular_gps(vehiculo_id: str) -> dict:
    """
    Simula datos de GPS para un vehículo.

    Args:
        vehiculo_id: Identificador del vehículo

    Returns:
        Dict con latitud, longitud y velocidad
    """
    base_lat = COORDENADAS_BASE["lat"]
    base_lng = COORDENADAS_BASE["lng"]

    latitud = base_lat + random.uniform(*GPS_RANGO_LATITUD)
    longitud = base_lng + random.uniform(*GPS_RANGO_LONGITUD)
    velocidad = random.uniform(*GPS_RANGO_VELOCIDAD)

    return {
        "lat": round(latitud, 6),
        "lng": round(longitud, 6),
        "speed": round(velocidad, 1),
    }


def simular_temperatura(vehiculo_id: str) -> dict:
    """
    Simula datos de temperatura del compartimento de carga.

    Args:
        vehiculo_id: Identificador del vehículo

    Returns:
        Dict con temperatura y unidad
    """
    temperatura = random.uniform(*TEMPERATURA_RANGO)

    return {"temperature": round(temperatura, 1), "unit": "celsius"}


def simular_combustible(vehiculo_id: str) -> dict:
    """
    Simula el nivel de combustible del vehículo.

    Args:
        vehiculo_id: Identificador del vehículo

    Returns:
        Dict con nivel de combustible y unidad
    """
    combustible = random.uniform(*COMBUSTIBLE_RANGO)

    return {"fuel_level": round(combustible, 1), "unit": "percent"}
