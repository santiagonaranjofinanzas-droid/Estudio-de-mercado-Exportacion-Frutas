# Inteligencia Comercial de Frutas Ecuatorianas (WITS, UN Comtrade, MAG)

Sistema reproducible de extracción, validación estadística, análisis de concentración y benchmarking internacional para la inteligencia comercial de frutas ecuatorianas: **Pitahaya**, **Piña** y **Mango** (excluido banano y plátano).

---

## 1. Arquitectura del Proyecto

```text
ecuador_fruit_trade/
├── config/
│   └── products.yaml            # Configuración de partidas HS6, subpartidas, fuentes y benchmarks
├── data/
│   ├── raw/                     # Respuestas crudas originales de APIs (JSON/XML) y archivo MAG
│   │   ├── comtrade/            # Respuestas completas de UN Comtrade API preview
│   │   ├── wits/                # Respuestas XML SDMX de World Bank WITS API
│   │   ├── partnerAreas.json    # Diccionario de referencia geográfica de UN Comtrade
│   │   └── mag_comercioexterior_2026octubre.xlsx
│   ├── processed/               # Datasets normalizados en CSV y Parquet
│   │   ├── exportaciones_historicas.csv / .parquet
│   │   ├── destinos_frutas_2025.csv / .parquet
│   │   ├── demanda_competidores.csv / .parquet
│   │   ├── indicadores_economicos.csv / .parquet
│   │   └── auditoria_conciliacion.csv / .parquet
│   └── outputs/                 # Entregables finales ejecutivos
│       ├── comercio_frutas_ecuador.xlsx  # Libro maestro Excel multi-pestaña formateado
│       ├── resumen_mercados.md           # Informe analítico comercial exhaustivo
│       └── charts/                       # 7 Gráficos en PNG de alta resolución (300 DPI)
│           ├── 1_evolucion_historica_frutas.png
│           ├── 2_top10_destinos_por_fruta.png
│           ├── 3_participacion_principales_compradores.png
│           ├── 4_crecimiento_demanda_internacional.png
│           ├── 5_principales_competidores_por_mercado.png
│           ├── 6_comparacion_precios_unitarios.png
│           └── 7_concentracion_mercados_hhi.png
├── src/
│   ├── __init__.py
│   ├── wits_client.py           # Cliente robusto para API REST SDMX V2.1 de WITS (World Bank)
│   ├── comtrade_client.py       # Cliente para UN Comtrade con control de rate limit y backoff
│   ├── mag_reader.py            # Parser y estandarizador de unidades para la base de control MAG
│   ├── transform.py             # Motor de consolidación, rankings y estructuración de datos
│   ├── indicators.py            # Fórmulas económicas (HHI, CR3, CAGR, cuotas, precios FOB/kg)
│   └── validation.py            # Auditoría estadística y conciliación frente a controles MAG
├── tests/
│   └── test_pipeline.py         # Suite de pruebas unitarias y de integración con PyTest
├── requirements.txt             # Dependencias estrictas del proyecto
├── .env.example                 # Plantilla de variables de entorno (credenciales opcionales)
├── main.py                      # Orquestador del pipeline completo de un solo comando
└── README.md                    # Documentación técnica y manual de reproducción
```

---

## 2. Requisitos Previos e Instalación

1. **Python 3.10 o superior** (probado en Python 3.12).
2. Instalar las dependencias requeridas:

```bash
pip install -r ecuador_fruit_trade/requirements.txt
```

---

## 3. Instrucciones de Ejecución

Para ejecutar el pipeline completo de extracción, validación, cálculo de indicadores y generación de todos los entregables (Excel, CSV, Parquet, Gráficos e Informe):

```bash
python ecuador_fruit_trade/main.py
```

Para ejecutar las pruebas automatizadas de integridad y validación matemática:

```bash
python -m pytest ecuador_fruit_trade/tests/test_pipeline.py -v
```

---

## 4. Fuentes de Información y Metodología de Conciliación

| Fuente | Ámbito y Cobertura | Rol en el Proyecto |
| :--- | :--- | :--- |
| **UN Comtrade API** | Estadísticas bilaterales por país socio y partida arancelaria HS a 6 dígitos (`080430`, `080450`, `081090`). | Identificación de los TOP destinos de exportación de Ecuador, demanda de importación de los mercados compradores y cuotas de países competidores. |
| **WITS (Banco Mundial)** | Indicadores SDMX de comercio agregado y aranceles efectivamente aplicados (AHS) vs nación más favorecida (MFN). | Evaluación de barreras arancelarias de acceso a los mercados objetivo para el sector de vegetales y frutas frescas (`06-15_Vegetable`). |
| **Ministerio de Agricultura (MAG)** | Hoja `MAG_CE_2026Octubre` de la base nacional de comercio exterior del Ecuador (2010 a 2026 parcial). | Control de conciliación para las exportaciones totales ecuatorianas y obtención de series de pitahaya pura nacional (`0810904000`). |

### Conciliación Estadística 2025:
- **Piña (HS 080430):** Conciliación 100% exacta entre UN Comtrade y MAG (**USD 81,108,645.51** / 140,448 TM).
- **Pitahaya (HS 081090 vs MAG):** UN Comtrade registra USD 341.98M bajo la partida agregada `081090` (Otras frutas frescas). El MAG registra la pitahaya pura aislada por **USD 272.76M** (representa el **79.76%** del total de la partida; el 20.24% restante corresponde a maracuyá, uvilla, granadilla y frutos exóticos).
- **Mango (HS 080450):** UN Comtrade registra **USD 57.13M** bajo la partida `080450` (Guayaba, Mango y Mangostán). En Ecuador más del 95% es mango fresco según gremios productores; el MAG no lo publica como partida desagregada independiente.

---

## 5. Principales Hallazgos Comerciales

1. **Pitahaya (HS 081090):**
   - Fruta con el mayor dinamismo histórico (CAGR 2015–2025 de **55.6% anual**).
   - Precio unitario FOB de exportación elevado: **USD 4.30/kg** en EE.UU., **USD 6.61/kg** en España, **USD 7.40/kg** en Francia y **USD 19.47/kg** en EAU.
   - En **España**, Ecuador es el **líder de mercado con el 42.7% de cuota de importación**, superando a competidores como Perú (15.7%), Colombia (12.5%) y Vietnam (5.4%).

2. **Piña (HS 080430):**
   - Cartera de destinos balanceada con índice de concentración moderado (HHI de 2,128 puntos).
   - Mercado principal: Estados Unidos (32.4%), Países Bajos (25.5%) y Chile (17.9%).
   - En **Chile**, Ecuador tiene un **monopolio de facto con el 93.3% del mercado**, aprovechando fletes marítimos directos por el Pacífico de corto tiempo de tránsito.

3. **Mango (HS 080450):**
   - **Riesgo crítico de concentración:** El **94.2% del valor exportado se destina a EE.UU.** (HHI de 8,885 puntos).
   - Fuerte oportunidad de diversificación en Europa: Países Bajos y España pagan precios de **USD 2.07 a USD 3.03/kg**, mientras que el mercado estadounidense paga en promedio **USD 1.01/kg**.

---

## 6. Selección de Mercados Potenciales para Operaciones Comerciales

1. **España (Pitahaya y Frutas Exóticas):** Líder indiscutible con cuota consolidada (42.7%), arancel 0% UE y alta apreciación de valor.
2. **Países Bajos (Mango y Piña):** Hub europeo con importaciones masivas (USD 392M en mango) y baja penetración ecuatoriana actual (<1%), con precios que triplican los de EE.UU.
3. **Chile (Piña Fresca):** Liderazgo consolidado (93.3% de participación), sin paso por el Canal de Panamá ni barreras arancelarias (ACE 65).
4. **Canadá (Pitahaya y Mango):** Mercado de alto poder adquisitivo con USD 327M en importaciones conjuntas y protocolos fitosanitarios estables.
