Taller 2 — Reverse Proxy con Nginx



Diferencia entre Reverse Proxy y Load Balancing



Un Reverse Proxy recibe las solicitudes del cliente y las envía al servicio correspondiente. En el taller, Nginx dirige /api/users/ al servicio de usuarios y /api/products/ al servicio de productos.



El Load Balancing permite distribuir las solicitudes entre varias instancias de un mismo servicio. En este caso, Nginx distribuye las peticiones entre users1 y users2 utilizando Round Robin.



La diferencia principal es que un Reverse Proxy funciona como intermediario entre el cliente y los servidores, mientras que un Load Balancer reparte el tráfico entre varios servidores.



Resultados del experimento



Primero se configura Nginx para dirigir las solicitudes a dos servicios diferentes: usuarios y productos. Comprobamos que cada ruta respondía correctamente.



Después creamos dos instancias del servicio de usuarios. Al realizar 12 solicitudes, observamos que 6 fueron atendidas por users1 y 6 por users2.



Finalmente, agregamos el servicio de pedidos con dos instancias: orders1 y orders2. Al realizar otras 12 solicitudes, cada instancia respondió 6 veces.

