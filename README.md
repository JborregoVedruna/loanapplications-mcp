# Loan Applications MCP Server (GestorPrestamos)

Este proyecto es un servidor que implementa el **Model Context Protocol (MCP)** para la gestión automatizada de solicitudes de préstamos. Actúa como un orquestador que conecta una interfaz de IA con servicios externos de gestión de préstamos y consulta de impagos (ASNEF).

## ✨ Características Principales

- 🤖 **FastMCP Implementation**: Servidor ligero basado en el framework FastMCP para una integración fluida con LLMs.
- 🛠️ **Herramientas de Decisión**: Proporciona herramientas (tools) para login, consulta de solicitudes pendientes, verificación de impagos por DNI y resolución de trámites.
- 🔌 **Integración Plug-and-Play**: Conexión directa con la API de Loans Manager (Spring Boot) y la API de Debts (Flask).
- 🔐 **Gestión de Sesión**: Manejo automatizado de tokens JWT de manager para operaciones administrativas.
- ⚙️ **Configuración Dinámica**: Uso de variables de entorno para una fácil adaptación a diferentes entornos de desarrollo y producción.

## 🚀 Instrucciones para Ejecutar el Proyecto

### Requisitos Previos

- Python 3.10 o superior.
- Acceso a las APIs externas (Loans Manager y Debts).

### Ejecución Local

1.  **Clonar el repositorio** y situarse en la raíz del proyecto.
2.  **Crear y activar entorno virtual**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Instalar dependencias**:
    ```powershell
    pip install "mcp[cli]" requests python-dotenv
    ```
4.  **Configurar variables de entorno**:
    Crea un archivo `.env` basado en la siguiente configuración (ver sección Variables de Entorno).
5.  **Ejecutar el servidor**:
    ```powershell
    python main.py
    ```

### ⚙️ Variables de Entorno (.env)

El proyecto requiere las siguientes variables configuradas en el archivo `.env`:

- `LOANSMANAGER_API`: URL base de la API de gestión de préstamos.
- `DEBTS_API`: URL base de la API de consultas de impagos.
- `PENDINGLOANAPPLICATION_ENDPOINT`: Endpoint para solicitudes pendientes.
- `LOGIN_ENDPOINT`: Endpoint para autenticación.
- `DEBTS_BY_DNI_ENDPOINT`: Endpoint para consulta por DNI.
- `MANAGER_USER` / `MANAGER_PASS`: Credenciales de administrador.

---

## 🏗️ Arquitectura y Decisiones Técnicas

El servidor MCP ha sido diseñado para servir de puente inteligente entre el modelo de lenguaje y la lógica de negocio técnica:

### 1. Protocolo MCP (Model Context Protocol)

Se utiliza el estándar MCP para exponer funciones internas como herramientas que una IA puede invocar de forma autónoma. Esto permite que el asistente no solo "lea" información, sino que ejecute acciones correctivas (como rechazar préstamos de morosos).

### 2. Capa de Adaptación de APIs

El servidor encapsula la complejidad de las peticiones HTTP y la gestión de headers (incluyendo tokens de autorización) dentro de funciones de Python decoradas con `@mcp.tool()`.

### 3. Automatización de Flujos de Trabajo

Aunque gran parte de la lógica reside en las APIs externas, el servidor MCP permite automatizar flujos complejos, como el escaneo masivo de DNI en listas de morosidad para tomar decisiones en bloque sobre solicitudes de préstamo pendientes.

### 4. Seguridad y Autenticación

- **Bearer Authentication**: El servidor gestiona la obtención del `access_token` mediante una herramienta de login, permitiendo que las llamadas subsiguientes estén autorizadas.
- **Environment Driven**: No hay credenciales "hardcoded"; todo se gestiona mediante variables de entorno protegidas.

---

## 📈 Mejoras y Extensiones Futuras

Para enriquecer las capacidades de este conector, se proponen las siguientes evoluciones:

### Técnicas

- **Persistencia de Sesión**: Implementar un sistema de refresco de tokens automático para evitar sesiones caducadas durante tareas largas.
- **Dockerización**: Crear un `Dockerfile` para desplegar el servidor MCP como un contenedor independiente en infraestructuras de orquestación.
- **Logging Estructurado**: Integrar con sistemas como Loki o ELK para monitorizar las interacciones entre la IA y las APIs de backend.

### Funcionales

- **Herramienta de Aprobación**: Añadir el flujo completo para aprobar préstamos que cumplan con todos los criterios.
- **Notificaciones**: Integrar herramientas para que la IA pueda enviar notificaciones inmediatas tras una resolución.
- **Soporte Multi-idioma**: Adaptar las descripciones de las herramientas para soportar consultas en múltiples idiomas.
