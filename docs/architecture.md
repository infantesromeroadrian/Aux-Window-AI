# Arquitectura de Sandetel RAG Solution

## Visión General

Sandetel RAG Solution es una aplicación web que proporciona asistencia a agentes de atención al cliente mediante el análisis de conversaciones y la generación de sugerencias utilizando modelos de lenguaje de OpenAI. La aplicación sigue una arquitectura modular basada en principios de programación orientada a objetos y patrón MVC adaptado.

## Diagrama de Arquitectura

```
+----------------------------------------+
|                Cliente                  |
|     (Navegador web / Interfaz UI)       |
+------------------+---------------------+
                  |
                  | HTTP
                  v
+------------------+---------------------+
|             Controllers                 |
|   +-------------+    +-------------+   |
|   |ViewController|    |APIController|   |
|   +-------------+    +-------------+   |
+------------------+---------------------+
                  |
                  v
+------------------+---------------------+
|              Services                   |
|   +----------------+  +--------------+ |
|   |AssistantService|  |OpenAIService | |
|   +----------------+  +--------------+ |
+------------------+---------------------+
                  |
                  v
+------------------+---------------------+
|              Models                     |
| +-------------+ +------------+ +------+|
| |AssistantModel| |SentimentModel| |HistoryModel||
| +-------------+ +------------+ +------+|
+------------------+---------------------+
                  |
                  v
+------------------+---------------------+
|             Data Storage                |
|  (Archivos JSON / Vector Store)         |
+----------------------------------------+
```

## Componentes Principales

### 1. Controladores (Controllers)

Los controladores manejan las solicitudes HTTP y actúan como intermediarios entre la vista y los servicios.

- **ViewController**: Gestiona las rutas relacionadas con la interfaz de usuario.
- **APIController**: Gestiona los endpoints de la API REST.

### 2. Servicios (Services)

Los servicios contienen la lógica de negocio y coordinan las operaciones entre diferentes componentes.

- **AssistantService**: Coordina las operaciones del asistente, integrando el análisis de sentimiento, generación de sugerencias y almacenamiento.
- **OpenAIService**: Gestiona la comunicación con la API de OpenAI.

### 3. Modelos (Models)

Los modelos encapsulan la lógica específica del dominio y las estructuras de datos.

- **AssistantModel**: Encapsula la lógica para generar sugerencias.
- **SentimentModel**: Maneja el análisis de sentimiento de textos.
- **HistoryModel**: Gestiona el almacenamiento y recuperación del historial de conversaciones.

### 4. Utilidades (Utils)

Componentes auxiliares que proporcionan funcionalidades comunes.

- **CacheManager**: Gestiona el caché de respuestas para mejorar el rendimiento.

## Flujo de Datos

1. El cliente envía una solicitud HTTP al servidor.
2. El controlador correspondiente recibe la solicitud y la valida.
3. El controlador llama al servicio apropiado para procesar la solicitud.
4. El servicio utiliza los modelos necesarios para realizar operaciones específicas del dominio.
5. Los modelos interactúan con el almacenamiento de datos si es necesario.
6. El resultado se devuelve al servicio, luego al controlador, y finalmente al cliente.

## Características Clave de la Arquitectura

- **Separación de Responsabilidades**: Cada componente tiene una responsabilidad única y bien definida.
- **Encapsulamiento**: La implementación interna de cada componente está oculta detrás de interfaces claras.
- **Modularidad**: Los componentes son independientes y pueden evolucionar por separado.
- **Extensibilidad**: Es fácil añadir nuevos componentes o modificar los existentes sin afectar a otros.
- **Testabilidad**: Los componentes pueden probarse de forma aislada.

## Escalabilidad y Consideraciones Futuras

- **Integración de RAG Completo**: Implementar recuperación aumentada utilizando la base de vectores ya existente.
- **Escalado Horizontal**: Posibilidad de dividir componentes en microservicios.
- **Autenticación y Autorización**: Añadir gestión de usuarios y permisos.
- **Análisis en Tiempo Real**: Mejorar la respuesta en tiempo real mediante WebSockets.
- **Multimodalidad**: Expandir para manejar otros tipos de entradas más allá del texto. 