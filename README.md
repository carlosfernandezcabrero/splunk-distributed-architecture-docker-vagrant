# Splunk Distributed Architecture

## Diseño arquitectura

### Arquitectura general

![Alt text](images/general-archiecture.png)

### Arquitectura universal forwarders

![Alt text](images/uf-architecture.png)

## Uso

### Añadir indexador al cluster de indexadores de producción

Para añadir un indexador al cluster de indexadores de producción debemos modificar el fichero `indexers.txt` que esta presente en la carpeta `files` dentro de la carpeta `common`. Deberemos añadir a este fichero una línea por cada indexador que queramos añadir al cluster. Este línea debe contener exclusivamente la IP del servidor que debe contener el indexador, precedida por `:`.

### Añadir miembro al cluster de search heads de producción

### Indexar eventos con usando el servidor RabbitMQ de los forwarders

### Enviar eventos a producción

### Enviar eventos a desarrollo
