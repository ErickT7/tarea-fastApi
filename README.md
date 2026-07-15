\# 🚀 API REST de Gestión de Items (Con Persistencia)



Una solución API REST robusta y consistente construida con \*\*Python\*\* y \*\*FastAPI\*\*. El proyecto gestiona un recurso de ítems utilizando almacenamiento persistente relacional.



\## 🛠️ Tecnologías Utilizadas



\*   \*\*Python 3.10+\*\*

\*   \*\*FastAPI\*\*: Framework web moderno de alto rendimiento.

\*   \*\*SQLAlchemy\*\*: ORM para mapeo objeto-relacional.

\*   \*\*SQLite\*\*: Motor de base de datos embebido y portátil (Persistencia real).

\*   \*\*Uvicorn\*\*: Servidor ASGI para la ejecución del entorno.

\*   \*\*Pydantic\*\*: Validación estricta de esquemas.



\---



\## 📋 Características Principales



\*   💾 \*\*Persistencia Relacional Real\*\*: Los datos se guardan físicamente en un archivo `items\_database.db` mediante transacciones SQL estructuradas (fácilmente migorable a PostgreSQL).

\*   📦 \*\*Estructura de Respuesta Consistente\*\*: Formato unificado para éxitos y errores de red.

\*   🚦 \*\*Códigos HTTP Explícitos\*\*: Códigos integrados (200, 201, 400, 401, 404) dentro del cuerpo del JSON.

\*   📑 \*\*Paginación Basada en Base de Datos\*\*: Segmentación de registros mediante sentencias SQL `OFFSET` y `LIMIT`.



\---



\## ⚙️ Instalación y Configuración Local



1\. Accede a la carpeta de tu proyecto:

&#x20;  ```bash

&#x20;  cd C:\\prueba

&#x20;  ```



2\. Activa tu entorno virtual e instala las dependencias:

&#x20;  ```bash

&#x20;  pip install fastapi "uvicorn\[standard]" sqlalchemy

&#x20;  ```



3\. Inicia el servidor de desarrollo:

&#x20;  ```bash

&#x20;  uvicorn main:app --reload

&#x20;  ```

&#x20;  \*Nota: Al levantar el servidor, el ORM creará de forma automática el archivo `items\_database.db` con sus respectivas tablas.\*



