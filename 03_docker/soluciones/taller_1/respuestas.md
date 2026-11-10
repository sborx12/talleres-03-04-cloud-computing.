Preguntas 



1\. ¿Por qué el cliente solamente conoce localhost:8080?



Porque Nginx funciona como punto de entrada. El cliente envía las solicitudes al puerto 8080 y Nginx las redirige internamente a las instancias de Flask.



2\. ¿Qué función cumple upstream?



Permite definir un grupo de servidores a los que Nginx puede enviar las solicitudes.



3\. ¿Qué estrategia utiliza Nginx por defecto en este escenario?



Utiliza Round Robin, que distribuye las solicitudes de forma rotativa entre los servidores disponibles.



4\. ¿Qué ocurre al detener api2?



Nginx sigue distribuyendo las solicitudes entre api1 y api3. En la prueba, ambas instancias respondieron seis solicitudes y no se presentaron errores.



5\. ¿Qué componente podría convertirse en un punto único de falla?



Nginx, porque todas las solicitudes pasan por él. Si deja de funcionar, los usuarios no podrían acceder a las API mediante el punto de entrada configurado.



6\. ¿Por qué este diseño representa escalamiento horizontal?



Porque ejecutamos varias instancias de una misma aplicación para distribuir las solicitudes, en lugar de aumentar los recursos de una sola instancia.



7\. ¿Qué tendría que cambiar para tener cinco instancias?



Agregar dos servicios adicionales, api4 y api5, en docker-compose.yml y registrarlos dentro del bloque upstream de Nginx.

