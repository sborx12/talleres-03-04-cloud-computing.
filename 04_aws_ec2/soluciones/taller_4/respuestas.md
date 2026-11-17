\# Taller 4 — Seguridad de red en EC2



\## 1. Auditoría de puertos



Ejecuté el comando `sudo ss -tulpn` para identificar los puertos que estaban escuchando en nuestra instancia EC2.



Encontré que SSH utiliza el puerto 22 y que Docker publica Nginx mediante el puerto 80. También identificamos algunos servicios internos del sistema.



No encontré el puerto 5000 publicado directamente en EC2 ni un servicio PostgreSQL escuchando en el puerto 5432.



\## 2. Tabla de análisis de puertos



| Puerto | Servicio | ¿Necesita ser público? | ¿Por qué? |

|---|---|---|---|

| 22 | SSH | No para todo Internet | Se necesita para administrar EC2, pero debe limitarse a una IP autorizada. |

| 80 | HTTP / Nginx | Sí, si la aplicación es pública | Permite que los usuarios accedan a la API mediante Nginx. En este laboratorio está restringido a nuestra IP. |

| 5000 | Flask | No | Flask puede comunicarse internamente con Nginx mediante Docker. |

| 5432 | PostgreSQL | No | La base de datos debe aceptar conexiones únicamente desde los servicios autorizados. |



\## 3. Configuración actual del Security Group



Revisé las reglas de entrada de nuestra instancia y encontramos lo siguiente:



| Servicio | Puerto | Protocolo | Origen |

|---|---|---|---|

| HTTP | 80 | TCP | 181.54.0.241/32 |

| SSH | 22 | TCP | 181.54.0.241/32 |



La configuración permite conexiones únicamente desde la dirección IP indicada.



No existen reglas de entrada para los puertos 5000 y 5432.



\## 4. Principio de mínimo privilegio



El principio de mínimo privilegio consiste en permitir solamente los accesos necesarios para el funcionamiento de un sistema.



Para la aplicación, SSH debe estar disponible únicamente desde una IP autorizada y Nginx debe ser el encargado de recibir las solicitudes HTTP.



Flask se comunica internamente con Nginx mediante la red de Docker, mientras que PostgreSQL, si se utilizara, debería permanecer protegido dentro de una red privada.



De esta manera se reducen los servicios expuestos y los posibles riesgos de seguridad.



\## 5. Preguntas de análisis



\*\*1. ¿Qué riesgo existe al abrir SSH al mundo?\*\*



Si permitimos SSH desde cualquier dirección IP, personas no autorizadas podrían intentar acceder al servidor. Esto aumenta el riesgo de ataques automatizados y de intentos de autenticación.



Por eso es mejor limitar el acceso a las direcciones IP que realmente necesitan administrar la instancia.



\*\*2. ¿Qué diferencia existe entre Security Group y firewall dentro del sistema operativo?\*\*



El Security Group es un firewall virtual de AWS que controla el tráfico permitido hacia y desde la instancia.



Un firewall del sistema operativo, como UFW en Ubuntu, funciona dentro del servidor y permite establecer reglas adicionales de seguridad.



Los dos pueden trabajar juntos para proteger la instancia.



\*\*3. ¿Por qué no debemos exponer PostgreSQL públicamente si no es necesario?\*\*



Porque una base de datos puede almacenar información importante. Si exponemos el puerto 5432 a Internet, aumentamos la posibilidad de intentos de acceso no autorizado y explotación de vulnerabilidades.



Es más seguro permitir conexiones solamente desde las aplicaciones o servidores que necesitan utilizar la base de datos.



\*\*4. ¿Por qué Nginx puede ser el único punto público de entrada?\*\*



Porque Nginx funciona como proxy inverso y recibe las solicitudes de los usuarios.



Después envía esas solicitudes a Flask mediante la red interna de Docker.



Así no necesitamos publicar directamente el puerto 5000 y podemos centralizar el acceso HTTP en Nginx.



\## 6. Reto: Propuesta de Security Group seguro



Para nuestra API Flask detrás de Nginx proponemos las siguientes reglas:



| Regla | Puerto | Protocolo | Origen | Justificación |

|---|---|---|---|---|

| SSH | 22 | TCP | IP autorizada /32 | Permite administrar EC2 de manera restringida. |

| HTTP | 80 | TCP | IP autorizada /32 durante el laboratorio | Permite probar Nginx sin abrir el acceso a todo Internet. |

| HTTPS | 443 | TCP | 0.0.0.0/0 en un despliegue público con TLS configurado | Permite que los usuarios accedan mediante conexiones cifradas. |

| Flask | 5000 | TCP | Sin regla pública | La API se comunica internamente con Nginx. |

| PostgreSQL | 5432 | TCP | Sin regla pública | Evita exponer la base de datos a Internet. |



Esta propuesta mantiene el acceso administrativo restringido y reduce los puertos expuestos.



En un entorno de producción sería recomendable utilizar HTTPS, configurar un certificado TLS y limitar las conexiones según las necesidades reales de la aplicación.



&#x20;

