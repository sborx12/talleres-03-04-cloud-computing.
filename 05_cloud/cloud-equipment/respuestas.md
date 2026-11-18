\# Proyecto 05\_cloud — Respuestas de análisis y defensa



\## 1. Preguntas de defensa



\### 1. ¿Por qué utilizar ECR?



Utilizamos Amazon ECR porque permite almacenar y administrar nuestras imágenes Docker en un repositorio privado de AWS. Así podemos construir la aplicación en nuestro computador, publicarla y descargar exactamente la misma imagen en EC2.



\### 2. ¿Por qué no construir la imagen directamente en EC2?



Porque queremos separar el proceso de desarrollo del despliegue. Construimos la imagen localmente, la probamos y después la publicamos en ECR. De esta manera, EC2 solamente necesita descargarla y ejecutarla, sin depender del código fuente ni de herramientas de compilación.



\### 3. ¿Qué diferencia existe entre ECR y S3?



Amazon ECR está diseñado para almacenar imágenes de contenedores Docker. En cambio, Amazon S3 es un servicio de almacenamiento de objetos, como fotografías, documentos y archivos PDF.



En nuestro proyecto, ECR almacena la imagen `equipment-api:3.0`, mientras que S3 almacena los documentos asociados a los equipos.



\### 4. ¿Por qué PostgreSQL y S3 tienen responsabilidades diferentes?



PostgreSQL permite almacenar información estructurada y relacionada mediante tablas, mientras que S3 permite guardar archivos.



Separar estas responsabilidades facilita la organización de los datos y evita almacenar documentos completos dentro de la base de datos.



\### 5. ¿Qué información debería estar en PostgreSQL?



En PostgreSQL almacenamos los empleados, equipos tecnológicos, asignaciones, mantenimientos y metadatos de los documentos.



También guardamos información como el estado de cada equipo, su código interno y el empleado responsable.



\### 6. ¿Qué información debería estar en S3?



En S3 almacenamos archivos como fotografías de equipos, facturas, actas de entrega y documentos PDF.



En nuestro proyecto guardamos `documento\_equipo.pdf` dentro del bucket `equipment-documents-2026-santi`. PostgreSQL almacena la referencia al archivo mediante su clave de S3.



\### 7. ¿Por qué Flask utiliza `db` como hostname?



Porque Flask y PostgreSQL se ejecutan en contenedores diferentes dentro de Docker Compose.



Docker Compose permite comunicarse utilizando los nombres de los servicios. En nuestro caso, `db` identifica al contenedor PostgreSQL.



Si utilizáramos `localhost` desde Flask, estaríamos haciendo referencia al propio contenedor de Flask y no al contenedor de PostgreSQL.



\### 8. ¿Qué pasaría si eliminamos la EC2?



Nuestra aplicación dejaría de estar disponible y perderíamos los contenedores y los datos almacenados únicamente en los recursos locales de esa instancia.



Los documentos guardados en Amazon S3 y las imágenes publicadas en Amazon ECR permanecerían disponibles porque son servicios independientes.



Para proteger PostgreSQL, sería necesario implementar respaldos o trasladar la base de datos a un servicio persistente independiente, como Amazon RDS.



\### 9. ¿Qué componente deberíamos cambiar para soportar varias instancias de Flask?



Deberíamos incorporar un Load Balancer que distribuya las solicitudes entre varias instancias que ejecuten Flask.



También necesitaríamos que las instancias compartieran los datos mediante una base de datos centralizada y que los documentos permanecieran en S3.



\### 10. ¿Cómo evolucionaría esta arquitectura hacia alta disponibilidad?



Podríamos utilizar varias instancias EC2 distribuidas entre diferentes Availability Zones, un Application Load Balancer y un Auto Scaling Group.



También podríamos utilizar Amazon RDS con alta disponibilidad para PostgreSQL y mantener los documentos en S3.



Así reduciríamos la dependencia de una sola instancia EC2.



\---



\## 2. Explicación del despliegue: desde Docker Push hasta Flask



\*\*¿Qué ocurre desde que hacemos `docker push` hasta que el usuario obtiene una respuesta de Flask?\*\*



Primero construimos nuestra imagen Docker en Windows utilizando el código de Flask y el Dockerfile.



Después etiquetamos la imagen y ejecutamos `docker push` para publicarla en nuestro repositorio privado de Amazon ECR.



En EC2 utilizamos el IAM Role `LabInstanceProfile` para autenticarnos en ECR y descargar la imagen mediante Docker.



Docker Compose utiliza esa imagen para iniciar el contenedor Flask junto con PostgreSQL y Nginx.



Cuando un usuario ingresa a la dirección pública de nuestra instancia, la solicitud pasa por el Security Group y llega a Nginx mediante el puerto 80.



Nginx reenvía la solicitud al contenedor Flask por el puerto interno 5000.



Flask procesa la solicitud y, si es necesario, consulta PostgreSQL o utiliza Amazon S3.



Finalmente, Flask devuelve una respuesta que Nginx envía al navegador del usuario.



\---



\## 3. Reto: Nuevas versiones de la API



Durante el desarrollo publicamos tres versiones principales:



| Versión | Funcionalidad |

|---|---|

| 1.0 | API Flask inicial con `/health` y `/equipos`. |

| 2.0 | Consulta de equipos mediante PostgreSQL. |

| 3.0 | Gestión de empleados, equipos, asignaciones, mantenimientos, historial y documentos S3. |



Para actualizar la aplicación modificamos la versión de la imagen en Docker Compose y descargamos la nueva versión desde ECR.



No reconstruimos la imagen de Flask dentro de EC2.



\## 4. Reto: Health Check



\*\*¿Qué diferencia existe entre que un contenedor esté running y que la aplicación esté saludable?\*\*



`Running` significa que el proceso principal del contenedor sigue ejecutándose. Sin embargo, esto no garantiza que la aplicación responda correctamente.



`Healthy` significa que Docker ejecutó satisfactoriamente la comprobación configurada para el contenedor.



En nuestro proyecto agregamos un Health Check que consulta `/health` en Flask. Después comprobamos que `equipment-api` aparecía en estado `Up (healthy)`.



Esta verificación confirma que el endpoint responde, aunque no garantiza por sí sola que todas las dependencias de la aplicación funcionen correctamente.



\## 5. Reto: Persistencia de PostgreSQL



\*\*¿Qué persiste cuando eliminamos un contenedor?\*\*



Los datos almacenados en un volumen Docker pueden conservarse aunque eliminemos y volvamos a crear el contenedor.



En nuestro proyecto configuramos un volumen llamado `postgres\_data` para almacenar la información de PostgreSQL.



Realizamos una prueba recreando el contenedor de la base de datos y comprobamos que los equipos Lenovo y HP seguían registrados.



Esto demuestra que los datos no dependen únicamente del sistema de archivos temporal del contenedor.



Sin embargo, un volumen local no sustituye una copia de seguridad externa.



\## 6. Reto: Escalabilidad conceptual



\*\*1. ¿Qué componente puede escalar horizontalmente?\*\*



La API Flask puede escalar horizontalmente ejecutando varias copias en diferentes instancias o contenedores.



\*\*2. ¿Qué componentes deben ser compartidos?\*\*



Las instancias deben acceder a una base de datos común y al almacenamiento de documentos en S3.



\*\*3. ¿Por qué los archivos no deberían permanecer en el disco local de cada EC2?\*\*



Porque cada instancia tiene su propio almacenamiento. Si guardamos un archivo en una instancia y otra recibe la siguiente solicitud, puede que no encuentre ese archivo.



Además, si eliminamos la instancia, podemos perder los archivos almacenados únicamente allí.



Utilizar S3 permite separar los documentos de las instancias que ejecutan la aplicación.



\---



\## 7. Seguridad



Durante el proyecto aplicamos varias medidas:



\- Utilizamos un repositorio privado en ECR.

\- Mantuvimos privado el bucket de Amazon S3.

\- Restringimos el acceso SSH a nuestra IP autorizada.

\- No publicamos PostgreSQL mediante el puerto 5432.

\- Utilizamos Nginx como punto de entrada hacia Flask.

\- Guardamos la contraseña de PostgreSQL fuera del código fuente.

\- Utilizamos un IAM Role para acceder a los servicios AWS desde EC2.



Para un entorno de producción también sería necesario configurar HTTPS, autenticación de usuarios, controles de autorización, gestión centralizada de secretos y respaldos periódicos.



&#x20;

