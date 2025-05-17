# Asistente para Agente Comercial

Herramienta de dictado en tiempo real con sugerencias inteligentes para agentes comerciales durante conversaciones con clientes.

## Características

- Dictado de voz en tiempo real
- Transcripción de texto en vivo
- Sugerencias inteligentes basadas en el contenido de la conversación usando GPT-4.1
- Interfaz web simple y responsive

## Requisitos

- Docker y Docker Compose
- Conexión a Internet
- Navegador moderno (Chrome, Edge o Safari recomendados)
- Clave API de OpenAI

## Configuración

1. Clonar este repositorio
2. Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
# OpenAI API Configuration
OPENAI_API_KEY=tu_clave_api_de_openai_aqui

# Flask Configuration
FLASK_APP=src/main.py
FLASK_ENV=development
FLASK_DEBUG=1
```

3. Reemplazar `tu_clave_api_de_openai_aqui` con tu clave API real de OpenAI

## Iniciar la aplicación

```bash
# Construir e iniciar los contenedores
docker-compose up -d

# Ver logs de la aplicación
docker-compose logs -f
```

La aplicación estará disponible en: http://localhost:8501

## Uso

1. Abre la aplicación en tu navegador
2. Haz clic en "Iniciar dictado"
3. Comienza a hablar y verás la transcripción en tiempo real
4. Las sugerencias aparecerán automáticamente basadas en el contenido de la conversación
5. Haz clic en "Detener" cuando desees finalizar la grabación

## Estructura del proyecto

```
Sandetel-RAG-Solution/
├── src/                      # Código fuente
│   ├── static/               # Archivos estáticos (CSS, JS)
│   │   ├── css/
│   │   └── js/
│   ├── templates/            # Plantillas HTML
│   ├── services/             # Servicios (OpenAI, etc.)
│   └── main.py               # Punto de entrada principal
├── Dockerfile                # Configuración de Docker
├── docker-compose.yml        # Configuración de Docker Compose
├── requirements.txt          # Dependencias de Python
└── .env                      # Variables de entorno (no incluido en el repo)
``` 