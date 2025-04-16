#!/bin/bash

echo "[*] Esperando a que la base de datos esté disponible..."
sleep 5

echo "[*] Ejecutando migración de base de datos..."
python /app/scripts/init_db.py  # <-- ubicación real en contenedor

echo "[*] Iniciando el bot de Discord..."
python bot.py
