Taller 2 — Administración de Linux en EC2



1\. Exploración del servidor



En este taller utilizamos una instancia EC2 de AWS con Ubuntu para practicar la administración remota de Linux mediante SSH.



Ejecutamos los siguientes comandos:



Comando



Función



pwd



Muestra la ubicación actual dentro del servidor.



ls -lah



Lista los archivos y directorios con sus detalles.



uptime



Muestra el tiempo de funcionamiento del servidor.



df -h



Permite consultar el espacio utilizado y disponible en disco.



free -h



Muestra la cantidad de memoria RAM utilizada y disponible.



ps aux



Muestra los procesos que están ejecutándose.



Estos comandos permiten conocer el estado general de los recursos de la instancia.



2\. Estructura de archivos



Creamos el directorio ec2-lab con tres subdirectorios:



scripts: para guardar scripts de automatización.



logs: para almacenar registros.



data: para almacenar archivos de información.



También creamos el archivo identificacion.txt con el contenido EC2 laboratorio.



3\. Análisis de procesos



Utilizamos ps aux | head y ps aux | grep ssh para consultar procesos del sistema.



Tres procesos que pueden encontrarse en Ubuntu son:



Proceso



Función



systemd



Administra el inicio del sistema y sus servicios.



sshd



Gestiona las conexiones SSH remotas.



cron



Ejecuta tareas programadas automáticamente.



Cada proceso tiene un identificador llamado PID. También podemos consultar qué usuario lo ejecuta y cuántos recursos de CPU y memoria consume.



Nota: estos son ejemplos habituales; deben verificarse contra los procesos observados en la instancia.



4\. Logs y servicios



Utilizamos sudo journalctl -n 30 para consultar los últimos 30 registros del sistema.



También ejecutamos sudo systemctl status ssh para comprobar el estado del servicio SSH.



Estas herramientas permiten revisar el funcionamiento de los servicios e identificar posibles problemas.



5\. Script Bash



Creamos el archivo system\_info.sh para consultar automáticamente:



Nombre del servidor.



Usuario conectado.



Fecha del sistema.



Tiempo de actividad.



Uso del disco.



Memoria RAM.



Le asignamos permisos de ejecución mediante chmod +x y lo ejecutamos desde la terminal de Ubuntu.



6\. Reto final



Modificamos el script para recibir una ruta como argumento.



Por ejemplo:



./scripts/system\_info.sh /var/log



Utilizamos $1 para obtener el argumento y df -h "$1" para mostrar información del sistema de archivos que contiene esa ruta.



También agregamos una validación para comprobar que se haya ingresado una ruta existente.

