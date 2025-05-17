# Informe Técnico: Sistema RAG Vectorstores con Asistencia en Tiempo Real por Voz

## Índice

- [Control documental](#control-documental)
- [Glosario de términos](#glosario-de-términos)
- [Documentación de referencia](#documentación-de-referencia)
- [INTRODUCCIÓN](#introducción)
  - [Alcance](#alcance)
  - [Objetivos](#objetivos)
- [DESCRIPCIÓN DEL ENTORNO TECNOLÓGICO](#descripción-del-entorno-tecnológico)
  - [Elementos de la Infraestructura](#elementos-de-la-infraestructura)
- [VALORACIÓN TÉCNICA](#valoración-técnica)
  - [REQ1.1 – Agent Assistant para Sandetel IA proporcionada por Alisys (IA onpremise)](#req11--agent-assistant-para-sandetel-ia-proporcionada-por-alisys-ia-onpremise)
  - [REQ1.2 – Agent Assistant para Sandetel IA proporcionada por Alisys (API IA)](#req12--agent-assistant-para-sandetel-ia-proporcionada-por-alisys-api-ia)
  - [REQ2 – Agent Assistant para Sandetel IA externa a Alisys](#req2--agent-assistant-para-sandetel-ia-externa-a-alisys)
- [VALORACIÓN](#valoración)
- [ANEXOS](#anexos)

## Control documental

### Control de cambios

| Versión | Fecha      | Anotaciones / Cambios | Autor | Cargo              |
|---------|------------|----------------------|-------|---------------------|
| 1.0     | 24-2-2025  | Versión inicial del documento | 313   | Ingeniero de Cliente |

## Glosario de términos

| Término | Definición |
|---------|------------|
| RAG     | Retrieval Augmented Generation, técnica que combina recuperación de información con generación de texto mediante LLMs |
| LLM     | Large Language Model, modelo de lenguaje de gran escala capaz de entender y generar texto |
| Embedding | Representación vectorial de texto que captura su significado semántico |
| Vectorstore | Base de datos optimizada para almacenar y consultar vectores (embeddings) |
| FAISS   | Biblioteca de Facebook AI para búsqueda de similitud eficiente entre vectores |
| ChromaDB | Base de datos vectorial moderna con capacidades avanzadas de metadatos |

## Documentación de referencia

| Descripción |
|-------------|
| [Documentación de FastAPI](https://fastapi.tiangolo.com/) |
| [FAISS: Biblioteca de búsqueda de similitud](https://github.com/facebookresearch/faiss) |
| [Sentence Transformers](https://www.sbert.net/) |
| [ChromaDB Documentation](https://docs.trychroma.com/) |

## INTRODUCCIÓN

### Alcance

El alcance de este documento consiste en detallar las tareas necesarias para implantar un asistente virtual para los agentes de Sandetel que permita ir recomendando en tiempo real al agente soluciones a las dudas que vayan planteando los ciudadanos.

El sistema propuesto utiliza tecnología RAG (Retrieval Augmented Generation) junto con transcripción de voz en tiempo real para proporcionar asistencia contextual durante las llamadas de soporte. La herramienta analiza automáticamente las conversaciones, identifica necesidades del cliente y proporciona respuestas semánticamente relevantes utilizando modelos de lenguaje avanzados (LLM).

### Objetivos

El objetivo de este documento consiste en valorar el coste en horas de desarrollo y materiales necesarios para poder implantar la solución descrita en el alcance.

Se presentan diferentes alternativas de implementación con sus correspondientes requisitos técnicos y estimaciones de recursos, contemplando opciones de despliegue tanto con modelos locales (on-premise) como mediante APIs externas.

## DESCRIPCIÓN DEL ENTORNO TECNOLÓGICO

### Elementos de la Infraestructura

[Se deben exponer los servidores y máquinas en los que se realizará algún tipo de modificación. Exponer las máquinas de DESARROLLO, que es en las que realmente se trabajará]

| Sistema | IP | Comentarios |
|---------|----|---------------------------------|
| XXX     | XXX| Entorno de Integración          |
| XXX     | XXX| Entorno de Producción           |

## VALORACIÓN TÉCNICA

Se describirán a continuación los requisitos desde un punto de vista técnico. Se debe exponer la solución técnica que se va a adoptar, utilizando todas las herramientas necesarias y suficientes para una clara definición.

En la descripción de cada requisito será necesario que participen todos los departamentos que pudieran estar implicados en la viabilidad (de acuerdo a como se estructuren estos requisitos en el análisis funcional).

### REQ1.1 – Agent Assistant para Sandetel IA proporcionada por Alisys (IA onpremise)

#### TÍTULO

Agent Assistant para Sandetel IA proporcionada por Alisys (IA onpremise)

#### DESCRIPCIÓN TEXTUAL DE LA SOLUCIÓN

El sistema propuesto ofrece asistencia en tiempo real a los agentes de call center de Sandetel mediante una solución onpremise que integra reconocimiento de voz y modelos LLM alojados localmente. La arquitectura implementa un sistema RAG (Retrieval Augmented Generation) que extrae información relevante de una base de conocimiento vectorizada para proporcionar respuestas precisas y contextuales.

La solución permite:
- Transcripción de llamadas en tiempo real mediante Whisper ejecutado localmente
- Búsqueda semántica en la base de conocimiento vectorizada
- Generación de respuestas mediante modelos LLM locales
- Interfaz para el agente con recomendaciones en tiempo real

#### DIAGRAMAS NECESARIOS

**Arquitectura del Sistema de Asistencia por Voz**

```
┌───────────────────────────────────────────────────────────┐
│                Sistema RAG con Asistencia                │
│                 en Tiempo Real por Voz                   │
└───────────────┬──────────────────────────────┬───────────┘
                │                              │
   ┌────────────▼───────────┐       ┌──────────▼───────────┐
   │  Frontend Call Center  │       │   Interfaz Web RAG   │
   │ (Interfaz del agente)  │       │   (Búsqueda Manual)  │
   └────────────┬───────────┘       └───────────┬──────────┘
                │                               │
                │ (Websocket streaming)         │ (REST API)
                │                               │
 ┌──────────────▼───────────────────────────────▼─────────────┐
 │                 API Gateway (FastAPI + WS)                 │
 └───────────────┬─────────────────────────────────┬──────────┘
                 │                                 │
                 ▼                                 ▼
 ┌─────────────────────────┐      ┌───────────────────────────┐
 │ Transcripción en Tiempo │      │    Procesamiento RAG      │
 │ Real (Whisper/OpenAI)   │      │    Vectorstores + LLM     │
 └───────────────┬─────────┘      └───────────┬───────────────┘
                 │                            │
                 └─────────────┬──────────────┘
                               │
                 ┌─────────────▼─────────────┐
                 │  Base de conocimiento     │
                 │    (FAISS / ChromaDB)     │
                 └───────────────────────────┘
```

#### ANÁLISIS POR ÁREAS

##### INGENIERÍA CCC



##### ARQUITECTURA



##### SISTEMAS



##### CIBERSEGURIDAD



##### BI



##### DISEÑO



##### TT



##### Ingeniería IA

###### 1. Modelos LLM para Asistencia

El sistema soporta múltiples modelos LLM para la generación de respuestas (interno):

1. **Mistral-7B** (local):
   - Características: Modelo liviano de alto rendimiento
   - Requerimientos: GPU con mínimo 16GB VRAM
   - Ventajas: Operación completamente local, sin latencia de API

ó

2. **DeepSeek Coder R1** (local/API):
   - Características: Especializado en respuestas técnicas
   - Requerimientos: GPU con 24GB+ VRAM para local
   - Ventajas: Alto rendimiento en contenido técnico

###### 2. Motor de Transcripción

Para la conversión de voz a texto en tiempo real:

1. **Whisper** (local): 
   - Variantes: tiny, base, medium, large
   - Requerimientos: GPU con 4-8GB VRAM mínimo
   - Precisión/Velocidad: Ajustable según la variante del modelo
   - Nota: Se puede usar con API (whisper v2) o en local (está liberado, no necesitaría licencia)

###### 3. Infraestructura Propuesta

Para cumplir con la volumetría esperada, recomendamos una arquitectura altamente escalable:

- **Cloud Provider**: Se debe optar por implementarlo en cloud privada Alisys (no AWS o Azure)
- **Computación GPU dedicada**: Para transcripción en tiempo real y embeddings
  - Nota: En principio vale con la H100 porque daría para 700 agentes en paralelo de un LLama
- **Contenedores Docker** y orquestación mediante Kubernetes con HPA (Horizontal Pod Autoscaling)
- **Autoescalado** según demanda en horario pico (8:00-12:00 y 15:00-18:00)
- **Gestión centralizada de logs** y monitoreo continuo (Prometheus/Grafana)
- **Redis** para caché de sesiones y resultados frecuentes
- **Arquitectura multi-zona** para alta disponibilidad (mínimo 2 zonas)

###### 4. Presupuesto Computacional

En base a los requisitos de volumetría y rendimiento esperados, se presenta el siguiente presupuesto computacional estimado para la infraestructura necesaria.

**4.1 Dimensionamiento de Recursos**

*4.1.1 Entorno de Producción*

| Componente | Especificaciones | Cantidad | Propósito |
|------------|------------------|----------|-----------|
| **Servidores de Aplicación** | (8 vCPU, 16 GB RAM) | 4 | Servir API REST y WebSockets para la interfaz web y conexiones de agentes |
| **Servidores para Transcripción** | (4 vCPU, 16 GB RAM, 1 GPU NVIDIA T4) | 2 | Ejecutar modelos Whisper para transcripción de voz en tiempo real (Para correr en local sí se necesita GPU/CPU) |
| **Servidores de Inference LLM** | (8 vCPU, 32 GB RAM, 1 GPU NVIDIA A10G) | 2 | Ejecutar modelos LLM (Mistral o similar) para generación de respuestas (Para el caso onpremise es necesaria GPU) |
| **Servidores de Base de Datos** | (8 vCPU, 32 GB RAM) | 2 | Almacenamiento vectorial con ChromaDB, gestión de metadatos y caché |
| **Balanceador de Carga** | Application Load Balancer | 1 | Distribución de tráfico y gestión de sesiones persistentes para WebSockets |
| **Almacenamiento** | (1000 IOPS) | 500 GB | Almacenamiento persistente para índices vectoriales, logs y configuraciones |
| **CDN** | Distribución global | 1 | Distribución eficiente de assets estáticos para la interfaz de usuario |
| **Redis** | (2 vCPU, 8GB RAM) | 2 | Caché de resultados frecuentes y gestión de sesiones |

*4.1.2 Entorno de Desarrollo/Pruebas*

| Componente | Especificaciones | Cantidad | Propósito |
|------------|------------------|----------|-----------|
| **Servidor Todo-en-Uno** | (8 vCPU, 32 GB RAM, 1 GPU) | 1 | Entorno integrado para desarrollo y pruebas con todos los componentes |
| **Almacenamiento** | 100 GB SSD | 1 | Datos de prueba, configuraciones y logs de desarrollo |

**4.2 Costos Estimados Mensuales (USD)**

*4.2.1 Infraestructura de Producción*

Nota: Los siguientes precios son para implementación en nube pública (AWS/Azure). En la solución onpremise en cloud privada Alisys no aplican estos precios.

| Componente | Costo Unitario | Cantidad | Costo Total |
|------------|----------------|----------|-------------|
| **Servidores de Aplicación** | $340/mes | 4 | $1,360 |
| **Servidores para Transcripción** | $526/mes | 2 | $1,052 |
| **Servidores de Inference LLM** | $798/mes | 2 | $1,596 |
| **Servidores de Base de Datos** | $308/mes | 2 | $616 |
| **Balanceador de Carga** | $25/mes + $0.008/GB | 1 | ~$125 |
| **Almacenamiento EBS** | $0.08/GB/mes | 500 GB | $40 |
| **CDN** | $0.085/GB (primeros 10TB) | Estimado | ~$200 |
| **Redis** | $100/mes | 2 | $200 |
| **Transferencia de Datos** | Varios | - | ~$250 |
| **Servicios Adicionales** (Monitoreo, Backup) | - | - | ~$200 |
| **Total Estimado** | | | **$5,639/mes** |

*4.2.2 Infraestructura de Desarrollo/Pruebas*

Nota: Estos son precios en nube pública. Para implementación en cloud privada Alisys deberán consultarse con el equipo de plataforma.

| Componente | Costo Unitario | Cantidad | Costo Total |
|------------|----------------|----------|-------------|
| **Servidor Todo-en-Uno** | $693/mes | 1 | $693 |
| **Almacenamiento** | $0.08/GB/mes | 100 GB | $8 |
| **Total Estimado** | | | **$701/mes** |

**4.3 Consideraciones Adicionales**

- **Escalabilidad**: Los costos pueden variar según el uso real y las necesidades de escalado.
- **Reservas de Instancias**: Se recomienda contratar instancias reservadas para obtener hasta un 40% de descuento en los costos de cómputo.
- **Optimización de Costos**:
  - Implementar políticas de autoescalado para reducir recursos en horas de baja demanda
  - Utilizar Spot Instances para cargas de trabajo tolerantes a interrupciones
  - Monitorizar y ajustar continuamente el dimensionamiento según uso real
  - Optimizar el almacenamiento con políticas de retención de datos
- **Servicios Gestionados**: Se podría considerar servicios como SageMaker para reducir la complejidad operativa de los modelos de ML, aunque esto incrementaría los costos.
- **Alta Disponibilidad**: Los costos incluyen redundancia para alta disponibilidad. Si se pudiera tolerar cierto riesgo, se podría reducir en un 20-25%.

**4.4 Especificaciones Detalladas de Máquinas Virtuales (VMs)**

La siguiente información detalla las especificaciones técnicas de las máquinas virtuales recomendadas para la implementación del sistema:

*4.4.1 VMs para Producción*

| Tipo de VM | vCPUs | RAM | Almacenamiento | GPU | Sistema Operativo | Software Base | Cantidad |
|------------|-------|-----|----------------|-----|-------------------|---------------|----------|
| **VM Aplicación** | 8 | 16 GB | 100 GB SSD | No | Ubuntu Server 22.04 LTS | Docker, Python 3.10 | 4 |
| **VM Transcripción** | 4 | 16 GB | 100 GB SSD | NVIDIA T4 | Ubuntu Server 22.04 LTS | Docker, CUDA 12.1 | 2 |
| **VM LLM** | 8 | 32 GB | 150 GB SSD | NVIDIA A10G | Ubuntu Server 22.04 LTS | Docker, CUDA 12.1 | 2 |
| **VM Base de Datos** | 8 | 32 GB | 250 GB SSD (datos) + 50 GB SSD (SO) | No | Ubuntu Server 22.04 LTS | Docker, PostgreSQL 15 | 2 |
| **VM Redis** | 2 | 8 GB | 50 GB SSD | No | Ubuntu Server 22.04 LTS | Redis 7.x | 2 |

*4.4.2 Almacenamiento Centralizado*

| Componente | Tipo | Capacidad | IOPS | Throughput | Propósito |
|------------|------|-----------|------|------------|-----------|
| **Vector Store** | Block Storage SSD | 750 GB | 3000 IOPS | 250 MiB/s | Almacenamiento de vectores e índices FAISS/ChromaDB |
| **Datos Compartidos** | Network File System | 500 GB | 1000 IOPS | 100 MiB/s | Documentos de conocimiento, logs, configuraciones |
| **Backup** | Object Storage | 2 TB | N/A | N/A | Copias de seguridad diarias y semanales |

*4.4.3 VM para Desarrollo/Pruebas*

| Tipo de VM | vCPUs | RAM | Almacenamiento | GPU | Sistema Operativo | Software Base |
|------------|-------|-----|----------------|-----|-------------------|---------------|
| **VM Desarrollo** | 8 | 32 GB | 200 GB SSD | NVIDIA T4 | Ubuntu Server 22.04 LTS | Docker, CUDA 12.1, Python 3.10 |

*4.4.4 Requisitos de Red*

| Componente | Ancho de Banda | Latencia Máxima | Consideraciones |
|------------|----------------|-----------------|-----------------|
| **Red Interna** | 10 Gbps | <1 ms | Comunicación entre componentes |
| **Conexión a APIs** | 1 Gbps | <50 ms | Para conexiones a APIs externas |
| **Conexión Clientes** | 1 Gbps | <100 ms | Para conexiones de agentes |

Esta configuración de VMs está diseñada para soportar hasta 100 agentes simultáneos con capacidad de escalar horizontalmente según las necesidades.

**4.5 Plan de Implementación Progresiva**

Se recomienda una estrategia de implementación en fases:

1. **Fase Piloto** (2 meses): → 320 horas
   - 25% de la infraestructura estimada (25 agentes)
   - Objetivos: validar arquitectura, medir rendimiento, ajustar modelos

2. **Fase de Escalado** (1 mes): → 160 horas
   - 50% de la infraestructura estimada (50 agentes)
   - Objetivos: optimizar rendimiento, ajustar puntos de autoescalado

3. **Fase de Producción Completa**: → 240 horas
   - 100% de la infraestructura estimada (100+ agentes)
   - Objetivos: servicio completo, monitoreo de métricas de negocio

4. **Optimización Continua**: → 80 horas trimestrales
   - Ajuste basado en métricas reales de uso
   - Potencial reducción de costos del 15-20% mediante optimización de recursos
   - Revisión trimestral de utilización y ROI

### REQ1.2 – Agent Assistant para Sandetel IA proporcionada por Alisys (API IA)

#### TÍTULO

Agent Assistant para Sandetel IA proporcionada por Alisys (API IA)

#### DESCRIPCIÓN TEXTUAL DE LA SOLUCIÓN

Esta variante del sistema Agent Assistant se implementa utilizando APIs externas para los componentes de IA, manteniendo la arquitectura general pero eliminando la necesidad de infraestructura GPU local para los modelos LLM y de transcripción. La solución utiliza APIs de OpenAI (o proveedores similares) para procesamiento de lenguaje natural y transcripción, mientras mantiene el componente de vectorstore y la lógica de negocio en la infraestructura de Alisys.

#### DIAGRAMAS NECESARIOS

La arquitectura es similar a la de la solución on-premise, con la diferencia de que los componentes de IA se sustituyen por llamadas a APIs externas:

```
┌───────────────────────────────────────────────────────────┐
│                Sistema RAG con Asistencia                │
│               en Tiempo Real por Voz (API)               │
└───────────────┬──────────────────────────────┬───────────┘
                │                              │
   ┌────────────▼───────────┐       ┌──────────▼───────────┐
   │  Frontend Call Center  │       │   Interfaz Web RAG   │
   │ (Interfaz del agente)  │       │   (Búsqueda Manual)  │
   └────────────┬───────────┘       └───────────┬──────────┘
                │                               │
                │ (Websocket streaming)         │ (REST API)
                │                               │
 ┌──────────────▼───────────────────────────────▼─────────────┐
 │                 API Gateway (FastAPI + WS)                 │
 └───────────────┬─────────────────────────────────┬──────────┘
                 │                                 │
                 ▼                                 ▼
 ┌─────────────────────────┐      ┌───────────────────────────┐
 │    API Transcripción    │      │    Procesamiento RAG      │
 │   (OpenAI Whisper API)  │      │  Vectorstores + API LLM   │
 └───────────────┬─────────┘      └───────────┬───────────────┘
                 │                            │
                 └─────────────┬──────────────┘
                               │
                 ┌─────────────▼─────────────┐
                 │  Base de conocimiento     │
                 │    (FAISS / ChromaDB)     │
                 └───────────────────────────┘
```

#### ANÁLISIS POR ÁREAS

##### INGENIERÍA CCC



##### ARQUITECTURA



##### SISTEMAS



##### CIBERSEGURIDAD



##### BI



##### Ingeniería IA

###### 1. Modelos LLM para Asistencia (API externa)

El sistema soporta múltiples modelos LLM para la generación de respuestas (externo):

1. **GPT-4** (API):
   - Características: Modelo de última generación
   - Requerimientos: Conexión a API de OpenAI, clave API
   - Ventajas: Máxima calidad de respuestas

###### 2. Motor de Transcripción (API externa)

Para la conversión de voz a texto en tiempo real:

1. **OpenAI Whisper API**:
   - Ventajas: Sin requerimientos de hardware local
   - Desventajas: Dependencia de conexión a internet, costes por uso

###### 3. Infraestructura Propuesta

Para cumplir con la volumetría esperada, recomendamos una arquitectura altamente escalable:

- **Cloud Provider**: Se debe optar por implementarlo en cloud privada Alisys (no AWS o Azure)
- **Computación GPU dedicada**: Si usamos la API de ChatGPT y API Whisper no hay necesidad de implementar una GPU dedicada
- **Contenedores Docker** y orquestación mediante Kubernetes con HPA (Horizontal Pod Autoscaling)
- **Autoescalado** según demanda en horario pico (8:00-12:00 y 15:00-18:00)
- **Gestión centralizada de logs** y monitoreo continuo (Prometheus/Grafana)
- **Redis** para caché de sesiones y resultados frecuentes
- **Arquitectura multi-zona** para alta disponibilidad (mínimo 2 zonas)

###### 4. Presupuesto Computacional

En base a los requisitos de volumetría y rendimiento esperados, se presenta el siguiente presupuesto computacional estimado para la infraestructura necesaria.

**4.1 Dimensionamiento de Recursos**

*4.1.1 Entorno de Producción*

| Componente | Especificaciones | Cantidad | Propósito |
|------------|------------------|----------|-----------|
| **Servidores de Aplicación** | (8 vCPU, 16 GB RAM) | 4 | Servir API REST y WebSockets para la interfaz web y conexiones de agentes |
| **Servidores para Transcripción** | (4 vCPU, 16 GB RAM) | 2 | Integración con Whisper API (no hace falta GPU) |
| **Servidores de Inference LLM** | (8 vCPU, 32 GB RAM) | 2 | Integración con API de ChatGPT (no hace falta GPU local) |
| **Servidores de Base de Datos** | (8 vCPU, 32 GB RAM) | 2 | Almacenamiento vectorial con ChromaDB, gestión de metadatos y caché |
| **Balanceador de Carga** | Application Load Balancer | 1 | Distribución de tráfico y gestión de sesiones persistentes para WebSockets |
| **Almacenamiento** | (1000 IOPS) | 500 GB | Almacenamiento persistente para índices vectoriales, logs y configuraciones |
| **CDN** | Distribución global | 1 | Distribución eficiente de assets estáticos para la interfaz de usuario |
| **Redis** | (2 vCPU, 8GB RAM) | 2 | Caché de resultados frecuentes y gestión de sesiones |

*4.1.2 Entorno de Desarrollo/Pruebas*

| Componente | Especificaciones | Cantidad | Propósito |
|------------|------------------|----------|-----------|
| **Servidor Todo-en-Uno** | (8 vCPU, 32 GB RAM, 1 GPU) | 1 | Entorno integrado para desarrollo y pruebas con todos los componentes |
| **Almacenamiento** | 100 GB SSD | 1 | Datos de prueba, configuraciones y logs de desarrollo |

**4.2 Costos Estimados Mensuales (USD)**

*4.2.1 Infraestructura de Producción*

Nota: Los siguientes precios son para implementación en nube pública (AWS/Azure). Para implementación en cloud privada Alisys, consultar con el equipo de plataforma.

| Componente | Costo Unitario | Cantidad | Costo Total |
|------------|----------------|----------|-------------|
| **Servidores de Aplicación** | $340/mes | 4 | $1,360 |
| **Servidores para Transcripción** | $526/mes | 2 | $1,052 |
| **Servidores de Inference LLM** | $798/mes | 2 | $1,596 |
| **Servidores de Base de Datos** | $308/mes | 2 | $616 |
| **Balanceador de Carga** | $25/mes + $0.008/GB | 1 | ~$125 |
| **Almacenamiento EBS** | $0.08/GB/mes | 500 GB | $40 |
| **CDN** | $0.085/GB (primeros 10TB) | Estimado | ~$200 |
| **Redis** | $100/mes | 2 | $200 |
| **Transferencia de Datos** | Varios | - | ~$250 |
| **Servicios Adicionales** (Monitoreo, Backup) | - | - | ~$200 |
| **Total Estimado** | | | **$5,639/mes** |

*4.2.2 Infraestructura de Desarrollo/Pruebas*

Nota: Estos son precios en nube pública. Para implementación en cloud privada Alisys deberán consultarse con el equipo de plataforma.

| Componente | Costo Unitario | Cantidad | Costo Total |
|------------|----------------|----------|-------------|
| **Servidor Todo-en-Uno** | $693/mes | 1 | $693 |
| **Almacenamiento** | $0.08/GB/mes | 100 GB | $8 |
| **Total Estimado** | | | **$701/mes** |

*4.2.3 Costos Estimados de APIs (OpenAI)*

Basado en el volumen de llamadas proporcionado (1500 llamadas diarias, 5 minutos promedio, 150,000 minutos mensuales):

| Servicio | Cálculo | Costo Mensual Estimado |
|----------|---------|------------------------|
| **Whisper API** | 150,000 minutos × $0.006/minuto | $900 |
| **GPT-4 API (Entrada)** | 1500 llamadas × 20 días × 5 consultas/llamada × 1000 tokens/consulta × $0.03/1K tokens | $4,500 |
| **GPT-4 API (Salida)** | 1500 llamadas × 20 días × 5 consultas/llamada × 400 tokens/consulta × $0.06/1K tokens | $3,600 |
| **Total Estimado APIs** | | **$9,000/mes** |

**Notas sobre la estimación:**
- Se asume que cada llamada de 5 minutos genera aproximadamente 5 consultas al sistema RAG durante la conversación
- Cada consulta al sistema RAG implica alrededor de 1000 tokens de entrada (transcripción + contexto)
- Cada respuesta del modelo GPT-4 genera aproximadamente 400 tokens
- Los precios son basados en las tarifas actuales de OpenAI ($0.006/min para Whisper, $0.03/1K tokens entrada y $0.06/1K tokens salida para GPT-4)
- Se pueden lograr optimizaciones mediante cacheo de respuestas frecuentes y uso selectivo de la API

Estos costos de API deben agregarse a la infraestructura base estimada anteriormente para obtener el costo total del proyecto en la modalidad de API externa.

**4.3 Consideraciones Adicionales**

- **Escalabilidad**: Los costos pueden variar según el uso real y las necesidades de escalado.
- **Reservas de Instancias**: Se recomienda contratar instancias reservadas para obtener hasta un 40% de descuento en los costos de cómputo.
- **Optimización de Costos**:
  - Implementar políticas de autoescalado para reducir recursos en horas de baja demanda
  - Utilizar Spot Instances para cargas de trabajo tolerantes a interrupciones
  - Monitorizar y ajustar continuamente el dimensionamiento según uso real
  - Optimizar el almacenamiento con políticas de retención de datos
- **Servicios Gestionados**: Se podría considerar servicios como SageMaker para reducir la complejidad operativa de los modelos de ML, aunque esto incrementaría los costos.
- **Alta Disponibilidad**: Los costos incluyen redundancia para alta disponibilidad. Si se pudiera tolerar cierto riesgo, se podría reducir en un 20-25%.

**4.4 Especificaciones Detalladas de Máquinas Virtuales (VMs)**

La siguiente información detalla las especificaciones técnicas de las máquinas virtuales recomendadas para la implementación del sistema API:

*4.4.1 VMs para Producción*

| Tipo de VM | vCPUs | RAM | Almacenamiento | GPU | Sistema Operativo | Software Base | Cantidad |
|------------|-------|-----|----------------|-----|-------------------|---------------|----------|
| **VM Aplicación** | 8 | 16 GB | 100 GB SSD | No | Ubuntu Server 22.04 LTS | Docker, Python 3.10 | 4 |
| **VM Transcripción** | 4 | 16 GB | 80 GB SSD | No | Ubuntu Server 22.04 LTS | Docker | 2 |
| **VM LLM** | 8 | 32 GB | 100 GB SSD | No | Ubuntu Server 22.04 LTS | Docker | 2 |
| **VM Base de Datos** | 8 | 32 GB | 250 GB SSD (datos) + 50 GB SSD (SO) | No | Ubuntu Server 22.04 LTS | Docker, PostgreSQL 15 | 2 |
| **VM Redis** | 2 | 8 GB | 50 GB SSD | No | Ubuntu Server 22.04 LTS | Redis 7.x | 2 |

*4.4.2 Almacenamiento Centralizado*

| Componente | Tipo | Capacidad | IOPS | Throughput | Propósito |
|------------|------|-----------|------|------------|-----------|
| **Vector Store** | Block Storage SSD | 750 GB | 3000 IOPS | 250 MiB/s | Almacenamiento de vectores e índices FAISS/ChromaDB |
| **Datos Compartidos** | Network File System | 500 GB | 1000 IOPS | 100 MiB/s | Documentos de conocimiento, logs, configuraciones |
| **Backup** | Object Storage | 2 TB | N/A | N/A | Copias de seguridad diarias y semanales |

*4.4.3 VM para Desarrollo/Pruebas*

| Tipo de VM | vCPUs | RAM | Almacenamiento | GPU | Sistema Operativo | Software Base |
|------------|-------|-----|----------------|-----|-------------------|---------------|
| **VM Desarrollo** | 8 | 32 GB | 200 GB SSD | No | Ubuntu Server 22.04 LTS | Docker, Python 3.10 |

*4.4.4 Requisitos de Red*

| Componente | Ancho de Banda | Latencia Máxima | Consideraciones |
|------------|----------------|-----------------|-----------------|
| **Red Interna** | 10 Gbps | <1 ms | Comunicación entre componentes |
| **Conexión a APIs** | 1 Gbps | <50 ms | Para conexiones a APIs externas (crítico) |
| **Conexión Clientes** | 1 Gbps | <100 ms | Para conexiones de agentes |

**Nota sobre almacenamiento**: A diferencia de la versión on-premise, esta configuración no requiere GPUs locales pero necesita un ancho de banda confiable para las APIs externas. El almacenamiento centralizado se ha mantenido con las mismas especificaciones para garantizar el rendimiento del vector store.

**4.5 Plan de Implementación Progresiva**

Se recomienda una estrategia de implementación en fases:

1. **Fase Piloto** (2 meses): → 320 horas
   - 25% de la infraestructura estimada (25 agentes)
   - Objetivos: validar arquitectura, medir rendimiento, ajustar modelos

2. **Fase de Escalado** (1 mes): → 160 horas
   - 50% de la infraestructura estimada (50 agentes)
   - Objetivos: optimizar rendimiento, ajustar puntos de autoescalado

3. **Fase de Producción Completa**: → 240 horas
   - 100% de la infraestructura estimada (100+ agentes)
   - Objetivos: servicio completo, monitoreo de métricas de negocio

4. **Optimización Continua**: → 80 horas trimestrales
   - Ajuste basado en métricas reales de uso
   - Potencial reducción de costos del 15-20% mediante optimización de recursos
   - Revisión trimestral de utilización y ROI

### REQ2 – Agent Assistant para Sandetel IA externa a Alisys

#### TÍTULO

Agent Assistant para Sandetel IA externa

#### DESCRIPCIÓN TEXTUAL DE LA SOLUCIÓN



#### DIAGRAMAS NECESARIOS



#### ANÁLISIS POR ÁREAS

##### INGENIERÍA CCC



##### ARQUITECTURA



##### SISTEMAS



##### CIBERSEGURIDAD



##### BI



##### Ingeniería IA



## VALORACIÓN

A continuación, se expone la valoración final, en horas, que conlleva el cumplimiento de todos los requisitos y trabajos expuestos en los puntos anteriores.

| ID REQUISITO | EQUIPO | HORAS |
|-------------|--------|-------|
| REQ1.1 | Ingeniería CCC | |
| | Sistemas | |
| | TT | |
| | Ingeniería IA | |
| | Plataforma | |
| REQ1.2 | Ingeniería CCC | |
| | Sistemas | |
| | TT | |
| | Ingeniería IA | |
| | Plataforma | |
| REQ2 | Ingeniería CCC | |
| | Sistemas | |
| SUBTOTAL | | |
| QA | | |
| Puesta en Producción | | |
| Documentación | | |
| DDP | | |
| TOTAL | | |

## ANEXOS

[Aportar toda la información que se considere relevante para apoyar la valoración técnica:
- Información de conexión a interfaces externas
- Diagramas que aumenten el detalle de la propuesta
- … …] 