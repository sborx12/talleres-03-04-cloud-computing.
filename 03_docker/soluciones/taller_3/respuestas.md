\# Taller 3 — Tres APIs Flask Balanceadas con PostgreSQL



\## Preguntas de análisis



\*\*1. ¿Dónde se encuentra el estado del negocio?\*\*



El estado del negocio se encuentra en PostgreSQL, porque allí se almacenan los productos, sus nombres y precios. Las tres instancias Flask consultan la misma base de datos.



\*\*2. ¿Por qué las APIs pueden ser stateless?\*\*



Porque las API no necesitan guardar los productos en su propia memoria. Cada vez que reciben una solicitud consultan PostgreSQL, por eso todas pueden acceder a la misma información.



\*\*3. ¿Qué ocurre si una API reinicia?\*\*



La instancia se detiene temporalmente, pero los productos no se pierden porque están guardados en PostgreSQL. Cuando vuelve a funcionar puede consultar los mismos datos.



\*\*4. ¿Qué ocurre si PostgreSQL reinicia?\*\*



Durante el reinicio las API pueden presentar errores al intentar consultar la base de datos. Cuando PostgreSQL vuelve a estar disponible pueden continuar funcionando. Los datos se conservan gracias al volumen de Docker.



\*\*5. ¿Dónde existen puntos únicos de falla?\*\*



Principalmente en Nginx y PostgreSQL, porque solo tenemos una instancia de cada uno. Si Nginx falla, los usuarios no pueden acceder mediante el puerto 8080. Si PostgreSQL falla, las API no pueden consultar los productos.



\*\*6. ¿El balanceamiento de API soluciona el escalamiento de la base de datos?\*\*



No. El balanceamiento distribuye las solicitudes entre las tres API, pero todas siguen utilizando la misma base de datos. Si PostgreSQL recibe demasiadas consultas, puede convertirse en un cuello de botella.



\*\*7. ¿Qué mecanismos podrían añadirse en una arquitectura de producción?\*\*



Se podrían implementar varias instancias de Nginx, replicación de PostgreSQL, copias de seguridad, monitoreo, health checks y escalamiento automático para mejorar la disponibilidad y el rendimiento.



 
