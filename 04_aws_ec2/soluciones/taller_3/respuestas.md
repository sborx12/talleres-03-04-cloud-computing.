\# Taller 3 — Docker en EC2 y despliegue de una aplicación



\## 1. Objetivo



En este taller desplegamos una API Flask dentro de una instancia EC2 de AWS utilizando Docker, Docker Compose y Nginx.



El objetivo fue publicar una aplicación en Internet y comprender cómo se comunican los diferentes componentes.



\## 2. Instalación de Docker



Instalamos Docker Engine y Docker Compose en una instancia EC2 con Ubuntu.



Verificamos la instalación mediante los comandos:



```bash

sudo docker --version

sudo docker compose version

sudo docker run hello-world

```



El contenedor `hello-world` confirmó que Docker estaba funcionando.



\## 3. API Flask



Creamos una aplicación Flask con dos rutas principales:



\- `/`: devuelve un mensaje y datos del entorno.

\- `/health`: devuelve `{"status": "ok"}`.



Utilizamos un `Dockerfile` basado en Python 3.12 para construir la imagen `ec2-flask-api`.



Después ejecutamos la aplicación dentro de un contenedor Docker.



\## 4. Publicación de la aplicación



Inicialmente publicamos Flask mediante el puerto 5000 de EC2.



Configuramos el Security Group para permitir temporalmente las conexiones desde nuestra dirección IP.



Posteriormente incorporamos Nginx como proxy inverso para que los usuarios pudieran acceder a la aplicación por el puerto 80.



\## 5. Docker Compose y Nginx



Utilizamos Docker Compose para administrar dos servicios:



\- \*\*Flask:\*\* ejecuta nuestra aplicación en el puerto interno 5000.

\- \*\*Nginx:\*\* recibe las solicitudes HTTP por el puerto 80 y las envía a Flask.



De esta manera, no es necesario exponer directamente el puerto 5000 a Internet.



\## 6. Explicación del flujo de comunicación



\*\*Internet → Security Group → EC2 → Docker → Nginx → Flask\*\*



Cuando un usuario ingresa la dirección IP pública de EC2 en su navegador, la solicitud llega primero al Security Group de AWS.



Si la conexión está permitida, llega a la instancia EC2 por el puerto 80.



Docker dirige la conexión al contenedor de Nginx, que funciona como proxy inverso.



Nginx reenvía la solicitud al servicio Flask utilizando la red interna de Docker y el puerto 5000.



Finalmente, Flask procesa la solicitud y devuelve una respuesta JSON, que regresa al navegador a través de Nginx.



\## 7. Reto: hostname y hora actual



Modificamos nuestra API para mostrar el hostname del contenedor, el hostname de EC2 y la hora actual.



\*\*¿Cuál es la diferencia entre EC2 y un contenedor Docker?\*\*



EC2 es una máquina virtual que dispone de recursos como CPU, memoria, almacenamiento y un sistema operativo propio.



Un contenedor Docker es un entorno aislado que ejecuta una aplicación dentro del sistema operativo del servidor.



El contenedor comparte el kernel del sistema anfitrión, mientras que EC2 funciona como un servidor virtual independiente.



Por eso, el hostname de EC2 identifica al servidor virtual y el hostname del contenedor identifica el entorno donde se ejecuta Flask.



&#x20;

