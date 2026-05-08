"""
Configuración centralizada para el simulador de sensores IoT.
"""

# ============================================================================
# CONFIGURACIÓN MQTT
# ============================================================================

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# ============================================================================
# VEHÍCULOS
# ============================================================================

VEHICULOS = ["VH-001", "VH-002", "VH-003"]
INTERVALO_PUBLICACION = 5  # segundos

# ============================================================================
# COORDENADAS BASE (Quito, Ecuador)
# ============================================================================

COORDENADAS_BASE = {
    "lat": -2.1709,
    "lng": -79.9224
}

# ============================================================================
# RANGOS DE SIMULACIÓN
# ============================================================================

# GPS
GPS_RANGO_LATITUD = (-0.01, 0.01)
GPS_RANGO_LONGITUD = (-0.01, 0.01)
GPS_RANGO_VELOCIDAD = (20, 80)

# Temperatura (en Celsius)
TEMPERATURA_RANGO = (-5, 8)

# Combustible (porcentaje)
COMBUSTIBLE_RANGO = (10, 100)
