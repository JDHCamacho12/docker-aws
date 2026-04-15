# Proyecto Airflow con Celery y RabbitMQ en Docker

Apache Airflow con `CeleryExecutor`, RabbitMQ como broker de mensajes y PostgreSQL externo como base de datos de metadatos.

## Arquitectura

- 1 nodo master: `scheduler`, `api-server`, RabbitMQ y Flower.
- Nodos worker: workers de Celery.
- PostgreSQL externo: RDS o instancia administrada fuera de Docker.

## Estructura

```text
docker-aws/
|-- .env
|-- .env.example
|-- README.md
|-- airflow/
|   |-- dags/
|   |-- logs/
|   `-- plugins/
|-- master/
|   |-- .env
|   `-- docker-compose.yml
`-- worker/
    |-- .env
    `-- docker-compose.yml
```

## Requisitos previos

- Docker y Docker Compose en cada nodo.
- PostgreSQL externo accesible desde master y workers.
- Clave SSH para `git-sync` si vas a sincronizar DAGs desde Git.
- Conectividad de red entre workers y el master por el puerto `5672`.

## Configuracion inicial

### 1. Preparar variables

```bash
cp .env.example .env
cp .env master/.env
cp .env worker/.env
```

Completa estos valores:

- `FERNET_KEY`
- `API_SERVER_SECRET_KEY`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `RABBITMQ_DEFAULT_USER`
- `RABBITMQ_DEFAULT_PASS`
- `RABBITMQ_DEFAULT_VHOST`
- `MASTER_PRIVATE_IP`
- `GIT_SYNC_REPO`
- `GIT_SYNC_BRANCH`
- `GIT_SSH_KEY_PATH`

Nota: `master/.env` y `worker/.env` deben tener los mismos valores que `.env`, porque Docker Compose usa el archivo `.env` local de cada carpeta al interpolar variables.

### 2. Inicializar el master

```bash
cd master
docker compose up airflow-init
docker compose up -d
```

`airflow-init` ahora:

- usa la base de datos externa
- ejecuta `airflow db migrate`
- crea el usuario administrador
- falla visiblemente si algo sale mal

### 3. Levantar workers

```bash
cd worker
docker compose up -d
```

Si quieres activar `git-sync`, levantalo con:

```bash
docker compose --profile git-sync up -d
```

## Servicios

### Master

- RabbitMQ: `5672`
- RabbitMQ Management: `15672`
- Airflow API/UI: `127.0.0.1:8081`
- Flower: `127.0.0.1:5555`

### Worker

- Airflow Celery Worker
- `git-sync`

## Acceso

- Airflow UI: `http://localhost:8081`
- Flower: `http://localhost:5555`
- RabbitMQ Management: `http://localhost:15672`

Si expones estos puertos a la red privada de AWS, cambia la publicacion en `master/docker-compose.yml`.

## Notas importantes

- El proyecto ya no levanta PostgreSQL local en el master.
- La creacion del usuario de Airflow depende de `FabAuthManager`.
- Se agrega `_PIP_ADDITIONAL_REQUIREMENTS=apache-airflow-providers-fab` para asegurar el provider de autenticacion en Airflow 3.
- `git-sync` queda como servicio opcional mediante el profile `git-sync`.
