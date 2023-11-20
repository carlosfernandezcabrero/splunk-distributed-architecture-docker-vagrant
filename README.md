# Splunk Distributed Architecture

## Requisitos

+ Tener instalado [Vagrant](https://www.vagrantup.com/) ([instrucciones](https://developer.hashicorp.com/vagrant/tutorials/getting-started/getting-started-install?product_intent=vagrant)).
+ Instalar el provider de Docker Compose para Vagrant.

  ``` bash
  vagrant plugin install vagrant-docker-compose
  ```

## Arquitectura por defecto

### Arquitectura general

![Alt text](images/general-archiecture.png)

Las maquinas que se especifican no tienen instalado el software de Splunk, lo que tienen es corriendo un contenedor Docker en modo host con Splunk (salvo los forwarders que tiene un arquitectura mas compleja). Es decir, salvo los forwarders, cada nodo es una maquina virtual creada con Vagrant compuesta por un contenedor Docker donde se ejecuta una instancia de Splunk con la configuración especifica y necesaria para la función que realiza dentro de la arquitectura. En próximas secciones se enseñara como levantar esta arquitectura.

### Arquitectura universal forwarders

![Alt text](images/uf-architecture.png)

### Estructura de los directorios

``` bash
.
├── common              # Archivos comunes
├── images              # Imágenes para el README
├── lb                  # Balanceador de carga
├── splunk-enterprise   # Core
├── universal-forwarder # Forwarders
```

+ common\
  Ficheros comunes utilizados en resto del proyecto.

+ images\
  Imágenes utilizadas para crear e README.

+ lb (192.168.33.4:80)\
  Balanceador de carga para los search heads de producción.

+ splunk-enterprise\
  En este directorio tenemos el Vagrantfile que crea las siguientes piezas de la arquitectura:

  + Master
  + Deployer
  + Deployment Server
  + Indexador de desarrollo
  + Search head de desarrollo
  + Heavy Forwarder
  + Indexadores de producción
  + Search heads de producción

+ universal-forwarder\
  Forwarders

## Uso

### Primera configuración

+ Configurar las rutas de descarga de Splunk. Para ello debemos de renombrar los ficheros `env.example.rb` a `env.rb`.

  + Splunk Enterprise\
  Entre comillas dobles debemos la ruta de descarga del paquete .tgz de la version que queramos utilizar de Splunk Enterprise. Solo debemos añadir la parte de la url a partir de "<https://download.splunk.com/products/splunk/releases/>"

  + Splunk Universal Forwarder\
  Entre comillas dobles debemos la ruta de descarga del paquete .tgz de la version que queramos utilizar de Splunk Universal Forwarder. Solo debemos añadir la parte de la url a partir de "<https://download.splunk.com/products/splunk/releases/>"

### Manejo de las maquinas virtuales o nodos

Para manejar las maquinas virtuales o nodos aprovisionados/as con Vagrant revisar la documentación referida a continuación:

+ Iniciar un entorno: <https://developer.hashicorp.com/vagrant/tutorials/getting-started/getting-started-up>
+ Recrear un entorno: <https://developer.hashicorp.com/vagrant/tutorials/getting-started/getting-started-rebuild>
+ Derribar un entorno: <https://developer.hashicorp.com/vagrant/tutorials/getting-started/getting-started-teardown>

***NOTA: Los comandos de Vagrant siempre se deben realizar en el directorio donde se encuentra el Vagranfile. Dependiendo de que parte queramos manejar deberemos realizar lo sobre una carpeta de la raíz del proyecto u otra. [Ver estructura de directorios](#estructura-de-los-directorios)***

## Personalizar la arquitectura por defecto

### Añadir indexador al cluster de indexadores de producción

Para añadir un indexador al cluster de indexadores de producción debemos modificar el fichero `indexers.txt` que esta presente en la carpeta `files` dentro de la carpeta `common`. Deberemos añadir a este fichero una línea por cada indexador que queramos añadir al cluster. Este línea debe contener exclusivamente la IP del servidor que debe contener el indexador, precedida por `:`.

### Añadir miembro al cluster de search heads de producción

Para añadir un search head al cluster de search heads de producción debemos modificar el fichero `shcluster_members.txt` que esta presente en la carpeta `files` dentro de la carpeta `common`. Deberemos añadir a este fichero una línea por cada search head que queramos añadir al cluster. Este línea debe contener exclusivamente la IP del servidor que debe contener el search head, precedida por `:`.

### Añadir forwarder

Para añadir un forwarder debemos modificar el fichero `forwarders.txt` que esta presente en la carpeta `files` dentro de la carpeta `common`. Deberemos añadir a este fichero una línea por cada forwarder que queramos añadir. Este línea debe contener exclusivamente la IP del servidor que debe contener el forwarder, precedida por `:`.

### Añadir peers al search head de desarrollo

Por defecto el search head de desarrollo solo busca en el indexador de desarrollo. Si queremos añadir los indexadores de producción deberemos seguir los siguientes pasos:

+ Arrancar los indexadores de producción.
+ Acceder al search head de desarrollo.
+ Ir al directorio bin de Splunk.
+ Ejecutar el siguiente comando por cada indexador que queramos añadir como peer al search head de desarrollo:

  ``` bash
  ./splunk add search-server https://<IP-del-indexador>:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234
  ```

También podemos definir lo directamente en la sección `test-sh` del Dockerfile. El comando añadir sigue la misma estructura que el comentado anteriormente. Por ejemplo, si quiero añadir dos indexadores con las IPs `192.168.33.21` y `192.168.33.22`, el comando `CMD` del Dockerfile quedaría de la siguiente forma:

``` Dockerfile
CMD /usr/local/splunk/bin/splunk start --answer-yes --accept-license --no-prompt \
&& /usr/local/splunk/bin/splunk add search-server https://192.168.33.5:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
&& /usr/local/splunk/bin/splunk add search-server https://192.168.33.21:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
&& /usr/local/splunk/bin/splunk add search-server https://192.168.33.22:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
&& tail -f /dev/null
```

## Indexar eventos usando el servidor RabbitMQ de los forwarders

### Diagrama

![Alt text](images/index-events-with-rabbitmq.png)

### Explicación

Para enviar eventos al servidor RabbitMQ de los forwarders tenemos dos opciones:

+ Enviar eventos manualmente a el servidor RabbitMQ. Cuando digo "manualmente" me refiero usando cURL, un script custom, cualquier software, ...

+ Utilizar el script que se proporciona en este repositorio. Este script esta en la carpeta `rabbitmq` dentro de la carpeta `scripts`, dentro de la carpeta `universal-forwarder`. Antes de ejecutar este script debemos cumplir los siguientes requisitos:

  + Tener instalado en Python 3.

  + Instalar las librerías utilizadas. Para instalar las librerías debemos ejecutar `pip install -r requirements.txt`. Podemos instalar estas librerías y usar la version de Python 3 que tengamos instalada de manera global en el ordenador o crear un entorno virtual. La forma recomendad es crear un entorno virtual. Para crear un entorno virtual en Python podemos utilizar **virtualenv** ([Documentación](https://virtualenv.pypa.io/en/latest/index.html)).

  *Nota: Si se utiliza un entorno virtual, antes de lanzar el comando para ejecutar el script, habrá que activarlo.*

  Una vez cumplidos los requisitos para ejecutar el script simplemente debemos invocarlo con el comando `python send.py`. Al lanzar el comando, el script nos pregunta la `exchange` a la que queremos enviar el mensaje y el propio mensaje que queremos enviar. Si le damos enter a cualquiera de las dos pregunta se aplicaran el valor por defecto para la `exchange` (`my_exchange`) y se genera un mensaje con la estructura por defecto con contenido aleatorio.

Para indexar los eventos que enviamos debemos configurar una `Serverclass` con una aplicación que contenga un monitor hacia el archivo con el nombre de la exchange con los mensajes que queramos indexar. Este archivo tiene la extension `.log`. Ademas deberemos añadir a la `Serverclass` los forwarders a los que queramos desplegar la aplicación, es decir, a los clientes de los que queremos indexar datos.

Para definir la `Serverclass` deberemos ir al master node que se encuentra en la maquina con IP `192.168.33.2` y puerto `8000`.

Para enviar datos a producción o desarrollo, ver las dos secciones siguientes.

## Indexación de eventos

### Indexar eventos en producción

Para enviar datos a producción debemos configurar el parámetro `_TCP_ROUTING` con el valor `pr_group` para cada stanza que queramos que envié los datos los indexadores de producción.

### Indexar eventos en desarrollo

Para enviar datos a desarrollo debemos configurar el parámetro `_TCP_ROUTING` con el valor `de_group` o no configurar lo para cada stanza que queramos que envié los datos al indexador de desarrollo. Por defecto los datos se envían al indexador de desarrollo a no ser que se especifique otra cosa.
