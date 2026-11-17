\# Taller 5 — Automatización de EC2 con User Data



\## 1. Objetivo



En este taller aprendimos a automatizar la configuración inicial de una instancia EC2 mediante User Data, utilizando scripts Bash para instalar servicios y preparar un servidor automáticamente.



\## 2. Configuración manual de Nginx



Primero utilizamos una instancia EC2 existente para instalar Nginx manualmente.



Ejecutamos los comandos:



```bash

sudo apt update

sudo apt install -y nginx

sudo systemctl status nginx

```



Comprobamos que Nginx estaba funcionando mediante el estado `active (running)` y accedimos a la página predeterminada desde el navegador.



\## 3. Configuración automática con User Data



Creamos el archivo `user\_data.sh` para automatizar la instalación de Nginx.



Al iniciar una nueva instancia EC2, AWS ejecutó el script de User Data, que realizó las siguientes tareas:



\- Actualizar la lista de paquetes.

\- Instalar Nginx.

\- Habilitar e iniciar el servicio.

\- Crear una página HTML personalizada.



Finalmente, verificamos desde el navegador el mensaje \*\*Servidor provisionado automáticamente\*\*.



\## 4. Comparación entre instalación manual y User Data



| Enfoque | Configuración manual | User Data |

|---|---|---|

| Repetibilidad | Debemos repetir los comandos en cada servidor. | Podemos utilizar el mismo script en varias instancias. |

| Tiempo | Requiere intervención del administrador. | La configuración se realiza automáticamente durante el inicio. |

| Errores humanos | Mayor posibilidad de omitir pasos o escribir comandos incorrectos. | Reduce los errores al ejecutar instrucciones previamente definidas. |

| Documentación | Los comandos deben registrarse por separado. | El script documenta los pasos de instalación. |

| Automatización | Baja, porque requiere ejecutar los comandos manualmente. | Alta, porque no requiere intervención durante el provisionamiento. |



\## 5. Reto: Automatizar Docker



Creamos el archivo `user\_data\_docker.sh` para instalar Docker y ejecutar automáticamente un contenedor Nginx.



El script realizó las siguientes tareas:



1\. Actualizó los paquetes de Ubuntu.

2\. Instaló Docker.

3\. Habilitó e inició el servicio Docker.

4\. Descargó la imagen `nginx:alpine`.

5\. Ejecutó un contenedor publicando el puerto 80.



Comprobamos que el proceso funcionó al acceder a la IP pública de la instancia y visualizar la página \*\*Welcome to nginx!\*\*.



\## 6. ¿Qué tareas convendría automatizar en una arquitectura real?



En una arquitectura real sería conveniente automatizar la instalación de programas, la configuración de servicios, el despliegue de aplicaciones y la creación de archivos de configuración.



También podríamos automatizar la instalación de Docker, la ejecución de contenedores, la configuración de registros y algunas verificaciones del estado del servidor.



Esto permitiría preparar nuevas instancias de manera más rápida y consistente, especialmente cuando necesitamos desplegar varios servidores con una configuración similar.



Para configuraciones más complejas también sería importante utilizar herramientas de infraestructura como código y administrar las credenciales mediante servicios seguros.



&#x20;

