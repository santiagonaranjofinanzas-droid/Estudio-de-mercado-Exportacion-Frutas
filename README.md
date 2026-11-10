# Estudio de Mercado e Inteligencia Comercial: Exportación de Frutas Ecuatorianas

![CTS International Freight Forwarder](https://img.shields.io/badge/CTS-International%20Freight%20Forwarder-CD0A33?style=for-the-badge)
![Data-Driven](https://img.shields.io/badge/Fuentes-UN%20Comtrade%20%7C%20WITS%20%7C%20MAG-111827?style=for-the-badge)
![Normas APA 7](https://img.shields.io/badge/Informe-Normas%20APA%207ma%20Edici%C3%B3n-047857?style=for-the-badge)
![Vercel Ready](https://img.shields.io/badge/Deploy-Vercel%20Zero%20Config-black?style=for-the-badge&logo=vercel)

Plataforma ejecutiva de visualización interactiva y dictamen de factibilidad comercial para la exportación de frutas tropicales no tradicionales desde Ecuador hacia mercados internacionales objetivo: **Pitahaya** (*HS 081090*), **Piña Golden MD2** (*HS 080430*) y **Mango Fresco** (*HS 080450*), excluyendo banano y plátano.

---

## 🚀 Despliegue en Vivo (Vercel)

- **Repositorio GitHub:** [santiagonaranjofinanzas-droid/Estudio-de-mercado-Exportacion-Frutas](https://github.com/santiagonaranjofinanzas-droid/Estudio-de-mercado-Exportacion-Frutas)
- **Documento Técnico en PDF (APA 7):** [`Informe_Exportacion_Frutas_Ecuador_APA7.pdf`](./Informe_Exportacion_Frutas_Ecuador_APA7.pdf) (14 páginas con tablas formales, figura vectorial y referencias oficiales).

---

## 📊 Hallazgos Clave para el Exportador

| Fruta / Partida | Cierre 2025 (FOB) | Volumen Físico | Precio Promedio FOB | Mercado Objetivo Óptimo | Ventaja Competitiva Clave |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Pitahaya**<br>*(HS 081090)* | **$341.98M USD**<br>(71.2% canasta) | 64,500 TM<br>(24.4% volumen) | **$4.23 / kg**<br>(nacional) | **España** ($6.61/kg)<br>EAU ($19.47/kg) | **Ecuador es el #1 Proveedor de España** con el 42.73% de cuota local. Retorno de $132,200 USD por contenedor reefer. |
| **Piña Golden MD2**<br>*(HS 080430)* | **$81.11M USD**<br>(16.9% canasta) | 140,448 TM<br>(53.2% volumen) | **$0.58 / kg**<br>($11.60/caja 20kg) | **Chile** ($14.48M) | **Monopolio ecuatoriano del 93.34% en Chile**. Tránsito marítimo directo por el Pacífico de 4–6 días sin peajes del Canal. |
| **Mango Fresco**<br>*(HS 080450)* | **$57.13M USD**<br>(11.9% canasta) | 59,320 TM<br>(22.4% volumen) | **$1.01 / kg**<br>(EE.UU.) | **Países Bajos** ($3.03/kg)<br>Francia ($2.77/kg) | **Oportunidad de arbitraje**: Triplica el ingreso frente a EE.UU. mediante contenedores de Atmósfera Controlada (CA). |

---

## 🏛️ Fuentes de Información Oficiales y Metodología

1. **UN Comtrade Database:** Extracción y auditoría de 743 registros comerciales bilaterales (2015–2025) para las partidas arancelarias HS 080430, HS 080450 y HS 081090.
2. **Ministerio de Agricultura y Ganadería del Ecuador (MAG):** Series históricas de comercio exterior a Octubre 2026 (cierre 2025 y avance parcial Ene-Jul 2026).
3. **World Integrated Trade Solution (WITS) - Banco Mundial:** Indicadores de concentración (HHI), aranceles efectivamente aplicados (AHS) y márgenes preferenciales.

---

## 📁 Estructura del Repositorio

```text
.
├── index.html                                  # Presentación ejecutiva interactiva en HTML/JS (Chart.js + Tailwind)
├── vercel.json                                 # Configuración de despliegue optimizada para Vercel
├── package.json                                # Scripts de servidor estático
├── Informe_Exportacion_Frutas_Ecuador_APA7.pdf # Informe técnico completo en formato APA 7ma Edición (14 páginas)
├── Informe_Exportacion_Frutas_Ecuador_APA7.html# Código fuente del informe en HTML con estilos de impresión APA 7
├── generate_html.py                            # Script generador de la presentación HTML con logo Base64
├── generate_apa_report.py                      # Script de compilación Playwright a PDF del informe APA 7
├── assets/                                     # Recursos gráficos y logo institucional CTS
└── ecuador_fruit_trade/                        # Pipeline en Python: extractores, transformaciones y tests
    ├── src/
    │   ├── wits_client.py
    │   ├── comtrade_client.py
    │   ├── mag_reader.py
    │   ├── transform.py
    │   ├── indicators.py
    │   └── validation.py
    └── tests/
```

---

## 🛠️ Instalación y Ejecución Local

Para visualizar la presentación localmente:

```bash
# Con Python
python -m http.server 8080

# O con Node.js
npx serve
```

Abre tu navegador en `http://localhost:8080/`.

---

## 🚢 Publicación en Vercel

Este proyecto cuenta con configuración *Zero-Config* para Vercel:

1. Ve a [Vercel Dashboard](https://vercel.com/new).
2. Selecciona **Import Git Repository**.
3. Elige `Estudio-de-mercado-Exportacion-Frutas`.
4. Deja la configuración por defecto y haz clic en **Deploy**.

---

**División de Inteligencia Comercial y Asesoría al Exportador**  
*CTS International Freight Forwarder* — Guayaquil, Ecuador.
