Taller 5 — MongoDB con Docker y Docker Compose



Comparación PostgreSQL vs MongoDB



1\. ¿Qué diferencia existe entre tabla y colección?



En PostgreSQL, las tablas almacenan datos organizados en filas y columnas, con una estructura definida. En MongoDB, las colecciones agrupan documentos que pueden tener diferentes campos y estructuras.



2\. ¿Qué diferencia existe entre fila y documento?



Una fila representa un registro dentro de una tabla de PostgreSQL. En MongoDB, un documento almacena información en una estructura similar a JSON y puede contener listas u objetos anidados.



3\. ¿Qué ventaja ofrecen los documentos anidados?



Permiten guardar información relacionada dentro de un mismo documento. Por ejemplo, en nuestro taller guardamos los productos de cada pedido dentro del documento de la orden. Esto facilita consultar toda esa información sin tener que unir varias tablas.



4\. ¿Qué riesgos tiene duplicar datos en documentos?



El principal riesgo es que la información puede quedar desactualizada o inconsistente. Por ejemplo, si guardamos el nombre de un producto en varios pedidos y después cambia, las copias anteriores no se actualizan automáticamente.



5\. ¿Qué tipos de aplicaciones podrían beneficiarse de MongoDB?



MongoDB puede ser útil en aplicaciones que manejan información flexible, como catálogos de productos, comercio electrónico, aplicaciones web y sistemas que almacenan documentos con diferentes estructuras.



6\. ¿Qué modelo resulta más adecuado para el ejercicio universitario y por qué?



Para el ejercicio universitario del Taller 4 considero más adecuado PostgreSQL, porque trabajamos con estudiantes, profesores, cursos e inscripciones que tienen relaciones claras. Las llaves foráneas permiten mantener la integridad de esos datos.



MongoDB también podría utilizarse, pero PostgreSQL facilita representar y controlar las relaciones entre las tablas.

