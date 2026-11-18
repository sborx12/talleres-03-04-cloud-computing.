

\# Arquitectura del proyecto 05\_cloud



\## Sistema de seguimiento de equipos en AWS



```mermaid

flowchart TD

&#x20;   U\[Usuario] --> I\[Internet]



&#x20;   subgraph AWS\[Amazon Web Services]

&#x20;       subgraph EC2\[Amazon EC2]

&#x20;           N\[Nginx - Puerto 80]

&#x20;           F\[Flask API - Puerto 5000]

&#x20;           P\[(PostgreSQL)]

&#x20;           V\[(Volumen persistente)]

&#x20;           N --> F

&#x20;           F --> P

&#x20;           P --> V

&#x20;       end



&#x20;       S3\[(Amazon S3 - Documentos)]

&#x20;       ECR\[Amazon ECR - Imagen Docker]

&#x20;   end



&#x20;   I --> N

&#x20;   ECR -->|Docker pull| F

&#x20;   F -->|Subir archivos| S3

```



\## Explicación



1\. El usuario accede a la IP pública de EC2.

2\. Nginx recibe las solicitudes HTTP por el puerto 80.

3\. Nginx envía las solicitudes a Flask mediante la red interna de Docker.

4\. Flask consulta y modifica los datos almacenados en PostgreSQL.

5\. PostgreSQL conserva los datos mediante un volumen persistente.

6\. Flask utiliza Amazon S3 para almacenar documentos y fotografías.

7\. La imagen de Flask se construye localmente, se publica en Amazon ECR y se descarga en EC2.

8\. Docker Compose administra los contenedores de Nginx, Flask y PostgreSQL.

```



