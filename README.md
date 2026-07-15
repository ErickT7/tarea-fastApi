# 🚀 API REST de Gestión de Items

Una solución API REST empresarial, robusta y consistente construida con **Python** y **FastAPI**. El proyecto gestiona un recurso de ítems utilizando almacenamiento persistente relacional, validaciones estrictas, paginación avanzada, suite de pruebas unitarias y empaquetado en contenedores Docker.

## 🛠️ Tecnologías Utilizadas

*   **Python 3.10+**
*   **FastAPI**: Framework web moderno de alto rendimiento.
*   **SQLAlchemy**: ORM para el mapeo objeto-relacional.
*   **SQLite**: Motor de base de datos embebido para persistencia relacional real.
*   **Pytest & HTTPX**: Suite para pruebas unitarias y de integración.
*   **Docker**: Dockerización completa para despliegues portátiles.

---

## 📋 Características Principales

*   💾 **Persistencia Relacional**: Los datos se guardan físicamente en un archivo `items_database.db` mediante transacciones SQL estructuradas (fácilmente intercambiable por PostgreSQL o MySQL).
*   📦 **Estructura de Respuesta Consistente**: Formato unificado de respuestas JSON (`codigo`, `estado`, `mensaje`, `datos`) tanto para respuestas exitosas como para excepciones del sistema.
*   🚦 **Códigos HTTP Explícitos**: Control nativo de códigos de estado (200, 201, 400, 401, 404) devueltos en las cabeceras y en el cuerpo del JSON.
*   📑 **Paginación en Base de Datos**: Segmentación de registros mediante parámetros query (`?pag=1&limit=10`) ejecutados con sentencias SQL `OFFSET` y `LIMIT`.
*   🛡️ **Seguridad Básica**: Simulación de protección de rutas (401 Unauthorized) mediante cabeceras Bearer Token.

---

## ⚙️ Instrucciones de Ejecución Local (Sin Docker)

Sigue estos pasos en tu terminal (`CMD` o PowerShell) para levantar el entorno de desarrollo:

### 1. Activar el Entorno Virtual e Instalar Dependencias
```cmd
:: Acceder a la carpeta del proyecto
cd C:\prueba

:: Instalar todos los paquetes requeridos
pip install fastapi "uvicorn[standard]" sqlalchemy pytest httpx
```

### 2. Iniciar el Servidor de Desarrollo
```bash
uvicorn main:app --reload
```
*Nota: Al levantar el servidor, el ORM creará de forma automática el archivo `items_database.db` con sus respectivas tablas.* El proyecto estará disponible en: `http://127.0.0.1:8000`

### 3. Ejecutar la Suite de Tests Unitarios
Para comprobar la integridad de los endpoints y las validaciones de seguridad (201, 400 y 401), abre otra ventana de terminal en la carpeta raíz y ejecuta:
```bash
pytest
```

---

## 🐳 Instrucciones de Ejecución con Docker

Si tienes Docker instalado y deseas levantar la aplicación de forma aislada y contenerizada, ejecuta los siguientes comandos en la raíz del proyecto:

### 1. Construir la Imagen de Docker
```bash
docker build -t api-items .
```

### 2. Levantar el Contenedor
```bash
docker run -d -p 8000:8000 --name contenedor-api api-items
```
La API se ejecutará de forma aislada y expondrá el puerto `8000` directamente en tu navegador: `http://localhost:8000`

---

## 🔌 Documentación Interactiva (Swagger UI)

Con el servidor corriendo (ya sea local o en Docker), puedes interactuar directamente con los endpoints desde las interfaces gráficas autogeneradas:
*   **Swagger UI (Recomendado)**: `http://127.0.0`
*   **ReDoc**: `http://127.0.0`

### Formato Estándar de las Respuestas JSON

**Éxito al crear un recurso (POST 201):**
```json
{
  "codigo": 201,
  "estado": "exito",
  "mensaje": "Recurso guardado en base de datos correctamente",
  "datos": {
    "id": 1,
    "title": "Escribir pruebas",
    "description": "Implementar pytest",
    "priority": "alta",
    "completed": false
  }
}
```

**Error por datos faltantes (Bad Request 400):**
```json
{
  "codigo": 400,
  "estado": "error",
  "mensaje": "Datos de entrada inválidos",
  "datos": [ ... detalles de los campos faltantes ... ]
}
```
