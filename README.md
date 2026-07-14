## 🐳 Arquitectura Contenerizada (Docker & Docker Compose)

Para garantizar la portabilidad absoluta el ecosistema completo del monitor climático está orquestado con **Docker Compose**. 
Esto permite levantar la API, el Worker y la base de datos en memoria en segundos con redes aisladas.

### Componentes del Sistema:
1. **api-service (FastAPI):** Expone los endpoints HTTP. Recibe las ráfagas de los sensores y encola los datos en Redis en microsegundos.
2. **redis-service (Redis):** Actúa como buffer de mensajería (Message Queue) de alta velocidad en memoria RAM.
3. **worker-service (Python Worker):** Proceso en segundo plano que consume de forma asíncrona la cola de Redis y persiste los datos ordenadamente en la base de datos SQLite (`clima_agro.db`).

### 🚀 Cómo ejecutar el proyecto en producción:

Asegúrese de tener Docker y Docker Desktop instalados y corriendo, luego ejecute:

```bash
docker-compose up --build