
#!/bin/bash
set -e

# Instalar Docker
apt-get update
apt-get install -y docker.io

# Iniciar Docker automaticamente
systemctl enable --now docker

# Descargar y ejecutar un contenedor Nginx
docker run -d \
  --name web-automatizada \
  --restart unless-stopped \
  -p 80:80 \
  nginx:alpine
