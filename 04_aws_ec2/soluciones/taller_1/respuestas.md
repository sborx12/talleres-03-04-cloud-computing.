Taller 1 — Crear y conectar una instancia EC2



1\. Preguntas de preparación



1\. ¿Qué diferencia existe entre una AMI y un Instance Type?



Una AMI es la imagen que contiene el sistema operativo y la configuración inicial del servidor. En nuestro caso utilizamos Ubuntu 26.04.1 LTS.



El Instance Type define los recursos del servidor, como la CPU y la memoria RAM. Para este taller utilizamos t3.micro, que tiene 2 vCPU y 1 GiB de RAM.



2\. ¿Qué función cumple el Security Group?



El Security Group funciona como un firewall virtual que controla las conexiones permitidas a la instancia. En nuestro caso configuramos el puerto 22 para permitir conexiones SSH desde nuestra dirección IP.



3\. ¿Por qué SSH requiere una autenticación segura?



Porque SSH permite acceder y administrar el servidor de forma remota. Utilizamos una llave privada .pem para autenticarnos y evitar que cualquier persona pueda conectarse sin autorización.



4\. ¿Por qué debemos seleccionar cuidadosamente la región?



Porque la región determina dónde se encuentra físicamente la infraestructura de AWS. También puede influir en la latencia, disponibilidad de servicios y costos. Para este taller seleccionamos N. Virginia (us-east-1).



2\. Tabla de componentes de EC2



Elemento



Valor



¿Para qué sirve?



AMI



Ubuntu 26.04.1 LTS



Proporciona el sistema operativo del servidor.



Instance Type



t3.micro



Define los recursos de CPU y memoria RAM.



Region



us-east-1



Región donde está alojada la instancia.



Availability Zone



us-east-1d



Zona de disponibilidad donde se ejecuta el servidor.



VPC



vpc-0f5d83d785ae37fa2



Red virtual privada de la instancia.



Subnet



subnet-034ec278d2bef549b



Segmento de red donde está ubicada la instancia.



Public IP



52.201.242.196



Permite acceder a la instancia desde Internet.



Private IP



172.31.36.142



Permite comunicación dentro de la red privada.



Security Group



taller1-ssh-sg



Controla las conexiones de entrada y salida.



Key Pair



taller1-aws-key



Permite autenticarnos mediante SSH.



3\. Reto: ¿Qué sucede desde Launch Instance hasta conectarnos por SSH?



Cuando presionamos Launch Instance, AWS comienza a crear un servidor virtual utilizando la configuración que seleccionamos.



Primero, AWS utiliza la AMI de Ubuntu y asigna los recursos correspondientes al tipo de instancia t3.micro. Después, configura el almacenamiento y conecta la instancia a la VPC y Subnet seleccionadas.



También aplica las reglas del Security Group, que en nuestro caso permiten conexiones SSH por el puerto 22 desde nuestra dirección IP.



Cuando la instancia llega al estado Running, podemos identificar su dirección IP pública.



Desde PowerShell utilizamos el comando ssh, indicando la llave privada y la IP pública del servidor. SSH establece una conexión cifrada y verifica nuestra autenticación mediante la llave.



Finalmente, conseguimos acceder a Ubuntu y ejecutar comandos como whoami, hostname, uname -a, df -h, free -h e ip addr.

