\# Taller 6 — EC2 en una arquitectura escalable



\## Parte 1. Arquitectura inicial



Nuestra arquitectura inicial utiliza una sola instancia EC2 donde ejecutamos Nginx y Flask mediante Docker.



\*\*1. ¿Qué sucede si EC2 falla?\*\*



Si nuestra instancia EC2 deja de funcionar, toda la aplicación deja de estar disponible, porque Nginx y Flask dependen del mismo servidor. Los usuarios no podrían acceder a la API hasta que el servicio se recupere.



\*\*2. ¿Qué sucede si aumenta el tráfico?\*\*



Si muchas personas utilizan la aplicación al mismo tiempo, los recursos de CPU y memoria de EC2 pueden resultar insuficientes. Esto podría provocar respuestas lentas o errores en la aplicación.



\*\*3. ¿Dónde existe un Single Point of Failure?\*\*



El Single Point of Failure (punto único de fallo) está en la instancia EC2, porque todos los componentes principales de nuestra aplicación funcionan dentro de ella. Si la instancia falla, no tenemos otro servidor que pueda atender las solicitudes.



Parte 2. Arquitectura con múltiples instancias



1\. ¿Qué componente distribuye el tráfico?



El Load Balancer recibe las solicitudes de los usuarios y las distribuye entre las tres instancias EC2 disponibles. Esto evita que todo el tráfico llegue a un único servidor.



2\. ¿Dónde se ejecuta cada instancia?



Cada instancia EC2 ejecuta su propia copia de nuestra aplicación Flask. Las instancias funcionan como servidores independientes dentro de AWS y pueden estar ubicadas en diferentes zonas de disponibilidad.



3\. ¿Por qué conviene distribuir instancias entre Availability Zones?



Porque mejora la disponibilidad de nuestra aplicación. Si ocurre una falla en una zona de disponibilidad, las instancias ubicadas en otras zonas pueden continuar atendiendo las solicitudes.



De esta manera reducimos el riesgo de que una sola falla deje toda la aplicación fuera de servicio.



Parte 3. Aplicaciones Stateless



1\. ¿Qué sucede si una petición llega a EC2-1 y la siguiente llega a EC2-2?



El Load Balancer puede enviar las solicitudes a diferentes instancias EC2. Si ambas tienen la misma aplicación y pueden acceder a la información necesaria, las solicitudes deberían funcionar correctamente.



2\. ¿Qué pasa si la sesión está guardada únicamente en la memoria de EC2-1?



Si la siguiente petición llega a EC2-2, esta instancia no tendrá la información de la sesión anterior. Por eso, el usuario podría aparecer como desconectado o perder información de su sesión.



3\. ¿Cómo podemos solucionar este problema?



Podemos guardar las sesiones en un sistema compartido, como Redis, para que todas las instancias puedan consultarlas.



Otra opción es utilizar mecanismos de autenticación sin estado, donde cada solicitud incluye la información necesaria para verificar al usuario.



De esta manera, la aplicación puede atender solicitudes desde diferentes instancias sin depender de la memoria de un solo servidor.



arte 4. Persistencia y almacenamiento compartido



1\. Si EC2-1 y EC2-2 tienen un archivo llamado archivo.txt, ¿son necesariamente el mismo archivo?



No. Aunque los archivos tengan el mismo nombre, cada instancia EC2 tiene su propio almacenamiento. Por eso, los archivos pueden contener información diferente.



Si modificamos el archivo en EC2-1, el archivo de EC2-2 no cambia automáticamente.



2\. ¿Qué problema puede causar esto?



Puede generar inconsistencias en la información. Por ejemplo, si un usuario guarda un archivo en EC2-1 y después su solicitud llega a EC2-2, es posible que la segunda instancia no encuentre ese archivo.



3\. ¿Qué solución proponemos?



Podemos utilizar Amazon EFS, que permite compartir un sistema de archivos entre varias instancias EC2.



De esta manera, las instancias pueden acceder a los mismos archivos sin depender de copias locales independientes.



También podríamos utilizar Amazon S3 para almacenar archivos como imágenes o documentos, y una base de datos administrada como Amazon RDS para guardar información estructurada.



Esto permite separar los datos de los servidores y facilita la escalabilidad de nuestra aplicación.



Parte 5. Auto Scaling



1\. ¿Qué problema resuelve Auto Scaling?



Auto Scaling permite ajustar automáticamente la cantidad de instancias EC2 según la demanda de nuestra aplicación.



Si aumenta el tráfico, puede iniciar nuevas instancias para distribuir la carga. Si el tráfico disminuye, puede reducir la cantidad de servidores para evitar utilizar recursos innecesarios.



2\. ¿Qué diferencia existe entre escalar verticalmente y horizontalmente?



La escalabilidad vertical consiste en aumentar los recursos de una misma instancia, por ejemplo, cambiar de una EC2 con poca memoria RAM a otra más potente.



La escalabilidad horizontal consiste en agregar más instancias EC2 para que trabajen juntas y compartan las solicitudes de los usuarios.



3\. ¿Qué métrica podríamos utilizar como señal de escalamiento?



Podríamos utilizar el porcentaje de uso de CPU de las instancias.



Por ejemplo, como propuesta para nuestro laboratorio, si el uso promedio de CPU supera el 70 % durante varios minutos, Auto Scaling podría aumentar la cantidad de instancias.



También podríamos utilizar la cantidad de solicitudes que recibe la aplicación.



Estos valores son ejemplos de configuración y deberían ajustarse según el comportamiento real del sistema.



4\. ¿Por qué es útil combinar Auto Scaling con un Load Balancer?



Porque Auto Scaling administra la cantidad de instancias disponibles, mientras que el Load Balancer distribuye las solicitudes entre las instancias saludables.



De esta manera, nuestra aplicación puede responder mejor a los cambios de tráfico y mantener una mayor disponibilidad.



Parte 6. Propuesta de arquitectura escalable



Nuestra propuesta consiste en utilizar un Application Load Balancer para distribuir las solicitudes entre tres instancias EC2 que ejecutan la misma aplicación Flask mediante Docker.



Las instancias pueden estar distribuidas entre diferentes Availability Zones para mejorar la disponibilidad.



También utilizamos una base de datos compartida mediante Amazon RDS para evitar que cada servidor almacene información independiente.



1\. ¿Qué elementos deberían ser públicos?



El Application Load Balancer debería ser el punto público de entrada mediante HTTP y HTTPS. Las instancias EC2 y la base de datos no necesitan estar expuestas directamente a Internet.



2\. ¿Qué elementos deberían ser privados?



Las instancias EC2 que ejecutan Flask y la base de datos Amazon RDS deberían ubicarse en subredes privadas. El acceso a la aplicación se realizaría mediante el Load Balancer.



3\. ¿Qué elementos deberían ser escalables?



Principalmente las instancias EC2 que ejecutan Flask. Utilizaríamos EC2 Auto Scaling para aumentar o disminuir su cantidad según la demanda.



4\. ¿Qué elementos deberían ser persistentes?



La información de la aplicación debería guardarse en servicios como Amazon RDS. Para archivos compartidos podríamos utilizar Amazon EFS o Amazon S3, dependiendo de las necesidades.



5\. ¿Qué elementos deberían ser monitoreados?



Deberíamos monitorear el uso de CPU, memoria y almacenamiento de las instancias EC2, además de los tiempos de respuesta, errores y solicitudes del Load Balancer.



También sería importante supervisar la base de datos y las instancias que Auto Scaling inicia o elimina.



Podríamos utilizar Amazon CloudWatch para recopilar métricas, consultar registros y configurar alarmas.



6\. ¿Cómo mejora esta arquitectura nuestra aplicación?



Esta arquitectura mejora la disponibilidad porque no depende de una sola instancia EC2.



Además, permite distribuir las solicitudes entre varios servidores, aumentar la capacidad cuando sea necesario y mantener los datos separados de las instancias que ejecutan la aplicación.



Parte 7. Reto final — Journey to Cloud (J2C)



¿Cómo evolucionaría nuestro laboratorio hacia una arquitectura escalable?



1\. Docker local



Inicialmente desarrollamos y ejecutamos nuestra aplicación mediante Docker en nuestro computador. Esto nos permitió probar Flask y Nginx sin necesitar infraestructura en la nube.



2\. Docker en EC2



Después trasladamos nuestra aplicación a una instancia EC2 de AWS. Utilizamos Docker para ejecutar los contenedores y Nginx para publicar la API en Internet.



Esto permitió que nuestra aplicación pudiera utilizarse desde otros computadores, sin depender de que nuestro equipo personal estuviera encendido.



3\. Múltiples instancias EC2



El siguiente paso sería ejecutar la misma aplicación en varias instancias EC2. De esta manera tendríamos diferentes servidores capaces de responder a las solicitudes.



Esto ayudaría a disminuir la dependencia de un solo servidor.



4\. Load Balancer



Incorporaríamos un Load Balancer para distribuir las solicitudes entre las instancias disponibles.



Así podríamos aprovechar mejor los recursos y evitar que todo el tráfico llegara a una sola EC2.



5\. Auto Scaling



Finalmente, utilizaríamos Auto Scaling para aumentar o reducir automáticamente la cantidad de instancias según el tráfico.



Esto permitiría adaptar la capacidad de nuestra aplicación a la demanda sin tener que crear manualmente cada servidor.



¿Cómo se relaciona esta evolución con Journey to Cloud (J2C)?



Journey to Cloud representa el proceso de pasar de una solución local a una arquitectura que aprovecha los servicios de computación en la nube.



En nuestro laboratorio comenzamos ejecutando Docker localmente y después utilizamos AWS EC2 para desplegar nuestra aplicación.



Posteriormente diseñamos una arquitectura con múltiples instancias, Load Balancer y Auto Scaling.



Esta evolución demuestra cómo una aplicación puede pasar de un entorno sencillo de desarrollo a una infraestructura con mayor escalabilidad y disponibilidad.



Parte 8. Comparación de arquitecturas



Característica



Una instancia EC2



Múltiples instancias EC2



Disponibilidad



Depende de un servidor.



Puede continuar funcionando si falla una instancia.



Escalabilidad



Limitada por los recursos de una EC2.



Permite agregar más instancias.



Distribución del tráfico



Todas las solicitudes llegan al mismo servidor.



Un Load Balancer distribuye las solicitudes.



Tolerancia a fallos



Existe un punto único de fallo.



Puede reducirse utilizando varias Availability Zones.



Administración



Más sencilla.



Requiere administrar más componentes.



Costos



Generalmente menores para aplicaciones pequeñas.



Pueden aumentar por utilizar más recursos.



Parte 9. Evolución hacia servicios administrados



Como siguiente etapa podríamos utilizar Amazon ECS para administrar nuestros contenedores, Amazon RDS para gestionar la base de datos y Amazon CloudWatch para monitorear la aplicación.



También podríamos incorporar servicios como AWS Fargate para ejecutar contenedores sin administrar directamente las instancias EC2.



Estos servicios permitirían reducir algunas tareas de administración de infraestructura y concentrarnos más en el desarrollo de nuestra aplicación.



Conclusión



En este taller comprendimos las limitaciones de utilizar una sola instancia EC2 y aprendimos cómo diseñar una arquitectura más escalable.



Analizamos la utilidad del Load Balancer, Auto Scaling, las aplicaciones stateless y el almacenamiento compartido.



Finalmente, relacionamos estos conceptos con Journey to Cloud, entendiendo cómo podemos evolucionar desde una aplicación Docker local hasta una arquitectura distribuida en AWS.

