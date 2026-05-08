#!/bin/bash
# Script para ejecutar el simulador de sensores

cd "$(dirname "$0")"

# Activar venv
source venv/bin/activate

# Ejecutar el simulador
python sensor_simulador.py
