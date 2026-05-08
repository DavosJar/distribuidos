#!/usr/bin/env python3
"""
Simulador de Sensores IoT para Flota Logística
===============================================

Publica datos de GPS, temperatura y combustible de tres vehículos
en topics MQTT con estructura jerárquica: flota/{vehiculo_id}/{tipo_sensor}
"""

import json
import time
from datetime import datetime

try:
    # paho-mqtt >= 2.0
    from paho.mqtt.client import Client, CallbackAPIVersion
    MQTT_VERSION = 2
except ImportError:
    # paho-mqtt < 2.0
    from paho.mqtt.client import Client
    MQTT_VERSION = 1

from config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_KEEPALIVE,
    VEHICULOS,
    INTERVALO_PUBLICACION,
)
from sensors import simular_gps, simular_temperatura, simular_combustible


class ClienteMQTT:
    """Gestiona la conexión y publicación de mensajes en MQTT."""

    def __init__(self, broker: str, puerto: int, keepalive: int = 60):
        """
        Inicializa el cliente MQTT.

        Args:
            broker: Dirección del broker MQTT
            puerto: Puerto del broker MQTT
            keepalive: Tiempo de keepalive en segundos
        """
        self.broker = broker
        self.puerto = puerto
        if MQTT_VERSION >= 2:
            self.cliente = Client(CallbackAPIVersion.VERSION1)
        else:
            self.cliente = Client()
        self.cliente.on_connect = self._on_connect
        self.cliente.on_disconnect = self._on_disconnect
        self.conectado = False

    def _on_connect(self, cliente, datos_usuario, flags, codigo_respuesta):
        """Callback ejecutado cuando se conecta al broker."""
        timestamp = self._timestamp()
        if codigo_respuesta == 0:
            print(f"[{timestamp}] ✓ Conectado al broker MQTT")
            self.conectado = True
        else:
            print(f"[{timestamp}] ✗ Error de conexión (rc={codigo_respuesta})")

    def _on_disconnect(self, cliente, datos_usuario, codigo_respuesta):
        """Callback ejecutado cuando se desconecta del broker."""
        timestamp = self._timestamp()
        print(f"[{timestamp}] ✗ Desconectado del broker")
        self.conectado = False

    @staticmethod
    def _timestamp() -> str:
        """Retorna timestamp formateado en ISO."""
        return datetime.now().isoformat()

    def conectar(self):
        """Conecta al broker MQTT."""
        try:
            self.cliente.connect(self.broker, self.puerto, keepalive=MQTT_KEEPALIVE)
            self.cliente.loop_start()
            time.sleep(1)
        except Exception as e:
            print(f"Error al conectar: {e}")
            raise

    def desconectar(self):
        """Desconecta del broker MQTT."""
        self.cliente.loop_stop()
        self.cliente.disconnect()

    def publicar(self, topic: str, datos: dict) -> bool:
        """
        Publica datos en un topic MQTT.

        Args:
            topic: Topic MQTT
            datos: Datos a publicar (será convertido a JSON)

        Returns:
            True si se publicó correctamente
        """
        try:
            from paho.mqtt.client import MQTT_ERR_SUCCESS
            mensaje = json.dumps(datos)
            resultado = self.cliente.publish(topic, mensaje)
            return resultado.rc == MQTT_ERR_SUCCESS
        except Exception as e:
            print(f"Error al publicar en {topic}: {e}")
            return False


def publicar_sensores_vehiculo(cliente: ClienteMQTT, vehiculo_id: str):
    """
    Publica todos los sensores de un vehículo.

    Args:
        cliente: Instancia de ClienteMQTT
        vehiculo_id: ID del vehículo
    """
    timestamp = datetime.now().isoformat()

    # GPS
    datos_gps = {"vehicle_id": vehiculo_id, "timestamp": timestamp}
    datos_gps.update(simular_gps(vehiculo_id))
    cliente.publicar(f"flota/{vehiculo_id}/gps", datos_gps)

    # Temperatura
    datos_temp = {"vehicle_id": vehiculo_id, "timestamp": timestamp}
    datos_temp.update(simular_temperatura(vehiculo_id))
    cliente.publicar(f"flota/{vehiculo_id}/temperatura", datos_temp)

    # Combustible
    datos_fuel = {"vehicle_id": vehiculo_id, "timestamp": timestamp}
    datos_fuel.update(simular_combustible(vehiculo_id))
    cliente.publicar(f"flota/{vehiculo_id}/combustible", datos_fuel)

    print(f"[{timestamp}] ✓ Datos publicados para {vehiculo_id}")


def main():
    """Función principal del simulador."""

    cliente_mqtt = ClienteMQTT(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)

    print("=" * 70)
    print("SIMULADOR DE SENSORES IoT - FLOTA LOGÍSTICA")
    print("=" * 70)
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Vehículos: {', '.join(VEHICULOS)}")
    print(f"Intervalo: {INTERVALO_PUBLICACION}s")
    print("=" * 70)
    print()

    try:
        print("Conectando al broker MQTT...")
        cliente_mqtt.conectar()
        print("Iniciando simulación...\n")

        while True:
            for vehiculo_id in VEHICULOS:
                publicar_sensores_vehiculo(cliente_mqtt, vehiculo_id)

            time.sleep(INTERVALO_PUBLICACION)

    except KeyboardInterrupt:
        print("\n\nDeteniendo simulador...")
        cliente_mqtt.desconectar()
        print("Simulador detenido.")


if __name__ == "__main__":
    main()
