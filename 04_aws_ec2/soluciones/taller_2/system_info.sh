
#!/bin/bash

echo "Hostname: $(hostname)"
echo "Usuario: $(whoami)"
echo "Fecha: $(date)"

echo "Uptime:"
uptime

echo "Disco:"
df -h /

echo "Memoria:"
free -h

echo "-------------------------"
echo "Informacion de la ruta:"
echo "-------------------------"

if [ -n "$1" ] && [ -e "$1" ]; then
    echo "Ruta: $1"
    df -h "$1"
else
    echo "Debes ingresar una ruta valida."
fi

