"""
Script to generate a comprehensive, formal, APA 7th Edition PDF report
for a prospective Ecuadorian tropical fruit exporter.
Outputs:
- Informe_Exportacion_Frutas_Ecuador_APA7.html
- Informe_Exportacion_Frutas_Ecuador_APA7.pdf
- docs/Informe_Exportacion_Frutas_Ecuador_APA7.pdf
"""

import os
import sys
from playwright.sync_api import sync_playwright

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Estudio de Factibilidad y Estrategia Comercial para la Exportación de Frutas Tropicales Ecuatorianas (APA 7)</title>
  <style>
    /* ========================================================================= */
    /* APA 7TH EDITION FORMATTING SPECIFICATIONS                                 */
    /* ========================================================================= */
    @page {
      size: letter;
      margin: 1in;
    }

    body {
      font-family: 'Times New Roman', Times, serif;
      font-size: 12pt;
      line-height: 1.5;
      color: #111111;
      margin: 0;
      padding: 0;
      background-color: #ffffff;
    }

    /* Paragraph Styling */
    p {
      margin-top: 0;
      margin-bottom: 0.8em;
      text-align: justify;
      text-indent: 0.5in;
    }

    .no-indent {
      text-indent: 0 !important;
    }

    /* APA 7 Headings Hierarchy */
    h1.apa-title {
      font-size: 14pt;
      font-weight: bold;
      text-align: center;
      line-height: 1.4;
      margin-top: 1.5in;
      margin-bottom: 2em;
    }

    h1.apa-h1 {
      font-size: 13pt;
      font-weight: bold;
      text-align: center;
      margin-top: 1.8em;
      margin-bottom: 0.8em;
      page-break-after: avoid;
    }

    h2.apa-h2 {
      font-size: 12pt;
      font-weight: bold;
      text-align: left;
      margin-top: 1.4em;
      margin-bottom: 0.6em;
      page-break-after: avoid;
    }

    h3.apa-h3 {
      font-size: 12pt;
      font-weight: bold;
      font-style: italic;
      text-align: left;
      margin-top: 1.2em;
      margin-bottom: 0.5em;
      page-break-after: avoid;
    }

    /* Title Page Elements */
    .title-page {
      min-height: 8.5in;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      page-break-after: always;
    }

    .title-page-content {
      margin-top: 1in;
      width: 100%;
    }

    .title-page-meta {
      margin-top: 2.5in;
      font-size: 12pt;
      line-height: 1.8;
    }

    .page-break {
      page-break-before: always;
    }

    /* Abstract Block */
    .abstract-title {
      font-weight: bold;
      text-align: center;
      margin-bottom: 1em;
      font-size: 12pt;
    }

    .keywords {
      margin-top: 1.5em;
      text-indent: 0.5in;
      font-style: normal;
    }

    .keywords em {
      font-style: italic;
    }

    /* APA 7 Tables */
    .table-container {
      margin: 1.5em 0;
      page-break-inside: avoid;
    }

    .table-number {
      font-weight: bold;
      font-size: 11pt;
      margin-bottom: 2px;
      text-indent: 0;
    }

    .table-title {
      font-style: italic;
      font-size: 11pt;
      margin-bottom: 6px;
      text-indent: 0;
    }

    table.apa-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 10pt;
      line-height: 1.35;
      margin-bottom: 6px;
      border-top: 2px solid #000000;
      border-bottom: 2px solid #000000;
    }

    table.apa-table th {
      border-bottom: 1px solid #000000;
      padding: 6px 8px;
      font-weight: bold;
      text-align: left;
    }

    table.apa-table td {
      padding: 5px 8px;
      vertical-align: top;
      border-bottom: none;
    }

    table.apa-table tr.total-row {
      border-top: 1px solid #000000;
      font-weight: bold;
    }

    .table-note {
      font-size: 9pt;
      line-height: 1.3;
      text-indent: 0;
      color: #333333;
    }

    .table-note em {
      font-style: italic;
      font-weight: bold;
    }

    /* APA 7 Figures */
    .figure-container {
      margin: 1.5em 0;
      text-align: center;
      page-break-inside: avoid;
    }

    .figure-number {
      font-weight: bold;
      font-size: 11pt;
      text-align: left;
      margin-bottom: 2px;
      text-indent: 0;
    }

    .figure-title {
      font-style: italic;
      font-size: 11pt;
      text-align: left;
      margin-bottom: 8px;
      text-indent: 0;
    }

    .figure-content {
      border: 1px solid #dddddd;
      padding: 10px;
      background: #fafafa;
      border-radius: 4px;
      display: inline-block;
      width: 96%;
    }

    .figure-note {
      font-size: 9pt;
      line-height: 1.3;
      text-align: left;
      margin-top: 6px;
      text-indent: 0;
      color: #333333;
    }

    .figure-note em {
      font-style: italic;
      font-weight: bold;
    }

    /* Callout & Strategic Highlights (Academic Style) */
    .strategic-box {
      border-left: 3px solid #111827;
      background-color: #f9fafb;
      padding: 10px 14px;
      margin: 1.2em 0;
      font-size: 11pt;
      line-height: 1.4;
      text-indent: 0;
      page-break-inside: avoid;
    }

    .strategic-box strong {
      color: #cd0a33;
    }

    /* References Section */
    .reference-item {
      padding-left: 0.5in;
      text-indent: -0.5in;
      margin-bottom: 0.8em;
      line-height: 1.4;
      font-size: 11pt;
      text-align: justify;
    }

    /* Print Header/Footer Simulation for Preview */
    .running-head {
      font-size: 9pt;
      color: #666666;
      border-bottom: 1px solid #e5e7eb;
      padding-bottom: 4px;
      margin-bottom: 1.5em;
      display: flex;
      justify-content: space-between;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    ol.apa-list, ul.apa-list {
      margin-top: 0.3em;
      margin-bottom: 0.8em;
      padding-left: 0.5in;
      font-size: 11pt;
      line-height: 1.4;
    }

    ol.apa-list li, ul.apa-list li {
      margin-bottom: 0.4em;
      text-align: justify;
    }
  </style>
</head>
<body>

  <!-- ========================================================================= -->
  <!-- PORTADA PROFESIONAL SEGÚN NORMAS APA 7                                    -->
  <!-- ========================================================================= -->
  <div class="title-page">
    <div class="title-page-content">
      <h1 class="apa-title">
        Estudio de Factibilidad y Estrategia Comercial para la Exportación de Frutas Tropicales Ecuatorianas:<br>
        <span style="font-weight: normal; font-size: 12pt;">Evaluación Comparativa de Rentabilidad Unitaria, Demanda Internacional y Logística de Cadena de Frío para Pitahaya, Piña y Mango</span>
      </h1>

      <div class="title-page-meta">
        <strong>División de Inteligencia Comercial y Asesoría al Exportador</strong><br>
        CTS International Freight Forwarder<br><br>
        <strong>Línea de Investigación:</strong> Comercio Internacional Agroindustrial y Selección de Mercados<br>
        <strong>Destinatario:</strong> Inversionistas y Emprendedores del Sector Agroexportador Ecuatoriano<br>
        <strong>Ciudad y Fecha:</strong> Guayaquil, Ecuador — Noviembre de 2026
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- RESUMEN EJECUTIVO / ABSTRACT & PALABRAS CLAVE                            -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>

  <div class="abstract-title">Resumen</div>
  <p class="no-indent">
    El presente informe técnico proporciona una evaluación económica, arancelaria y logística rigurosa para orientar la toma de decisiones de nuevos inversionistas y empresarios interesados en incursionar en la exportación de frutas tropicales no tradicionales desde el Ecuador, focalizándose en pitahaya (<em>Selenicereus megalanthus</em> / <em>Hylocereus undatus</em>, HS 081090), piña Golden MD2 (<em>Ananas comosus</em>, HS 080430) y mango fresco (<em>Mangifera indica</em>, HS 080450). A partir de la triangulación estadística de 743 registros bilaterales de UN Comtrade (2015–2025), la serie histórica del Ministerio de Agricultura y Ganadería (MAG, 2026) y perfiles arancelarios del Banco Mundial (WITS, 2025), se determina que la canasta frutícola no tradicional ecuatoriana alcanzó USD 480.22 millones en 2025. La pitahaya se posiciona como el rubro de mayor rentabilidad unitaria con un precio ponderado nacional de USD 4.23/kg, un margen bruto proyectado del 45% al 60% y un liderazgo indiscutible en España, donde Ecuador abastece el 42.73% de las importaciones totales a un valor de USD 6.61/kg. Por su parte, la piña representa el modelo de eficiencia a escala y ventaja logística regional, ostentando un monopolio del 93.34% en el mercado de Chile mediante tránsitos marítimos cortos por el Pacífico (4 a 6 días) y arancel 0% bajo el ACE 65. Finalmente, el mango revela una distorsión estructural: el 94.22% de su volumen se comercializa a bajo precio en Estados Unidos (USD 1.01/kg), mientras que Europa ofrece una ventana de arbitraje superior (USD 3.03/kg en Países Bajos y USD 2.77/kg en Francia) mediante fletes refrigerados con atmósfera controlada. Se concluye con una matriz de decisión y una hoja de ruta operativa en seis fases para viabilizar operaciones comerciales exitosas.
  </p>

  <p class="keywords">
    <em>Palabras clave:</em> Comercio exterior, frutas tropicales, Ecuador, pitahaya, piña Golden MD2, mango fresco, rentabilidad unitaria, logística refrigerada, UN Comtrade, WITS.
  </p>

  <!-- ========================================================================= -->
  <!-- 1. INTRODUCCIÓN Y MARCO DE DECISIÓN                                       -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">1. Introducción y Contexto del Agroexportador Ecuatoriano</h1>
  <p>
    La matriz exportadora del Ecuador ha estado históricamente concentrada en bienes primarios tradicionales, particularmente el banano (<em>Musa acuminata</em>), producto en el cual el país es el principal exportador del mundo. No obstante, para un emprendedor o una empresa agroindustrial que evalúa incursionar en el comercio exterior, el sector del banano y plátano presenta barreras de entrada críticas: márgenes unitarios estrechos (céntimos por kilogramo), alta exigencia de capital para economía de escala, cupos de exportación regulados por el Estado y un control férreo ejercido por corporaciones transnacionales y comercializadoras globales consolidadas.
  </p>
  <p>
    Frente a esta coyuntura, la canasta de frutas exóticas y tropicales no tradicionales —compuesta prioritariamente por la pitahaya amarilla y roja, la piña de la variedad Golden MD2 y el mango fresco— ha emergido como el motor más dinámico del comercio exterior agrario nacional. Durante el período 2015–2025, esta canasta triplicó su valor de exportación, generando en el cierre anual de 2025 una cifra agregada de USD 480.22 millones de ingresos en divisas (UN Comtrade, 2025).
  </p>
  <p>
    El propósito central de este estudio es dotar al potencial exportador de una guía estratégica basada en evidencia empírica. Se busca responder con exactitud a tres interrogantes fundamentales: (a) ¿Cuál es la fruta más rentable y qué retorno bruto ofrece por contenedor?, (b) ¿Cuáles son los mercados internacionales de destino que maximizan el precio de venta y minimizan el riesgo arancelario y comercial?, y (c) ¿Qué requerimientos fitosanitarios y logísticos de cadena de frío determinan la viabilidad operativa del embarque?
  </p>

  <!-- ========================================================================= -->
  <!-- 2. DIAGNÓSTICO COMPARATIVO DE LA OFERTA FRUTÍCOLA                        -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">2. Diagnóstico Macroeconómico Comparativo (Cierre 2025)</h1>
  <p>
    La evaluación simultánea de las bases de datos de la Organización de las Naciones Unidas (UN Comtrade) y los registros consolidados del Ministerio de Agricultura y Ganadería del Ecuador (MAG) permite identificar perfiles económicos radicalmente distintos entre los tres productos analizados, tal como se sintetiza en la Tabla 1.
  </p>

  <div class="table-container">
    <div class="table-number">Tabla 1</div>
    <div class="table-title">Indicadores Macroeconómicos y Comerciales de Frutas Ecuatorianas No Tradicionales (2025)</div>
    <table class="apa-table">
      <thead>
        <tr>
          <th>Indicador Comercial</th>
          <th>Pitahaya (HS 081090)</th>
          <th>Piña Golden (HS 080430)</th>
          <th>Mango Fresco (HS 080450)</th>
          <th>Total Canasta</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Valor FOB Exportado (UN Comtrade)</td>
          <td>$341,984,212</td>
          <td>$81,108,826</td>
          <td>$57,126,944</td>
          <td>$480,219,982</td>
        </tr>
        <tr>
          <td>Valor FOB Control (MAG Ecuador)</td>
          <td>$272,763,890</td>
          <td>$81,108,826</td>
          <td>No desglosado*</td>
          <td>—</td>
        </tr>
        <tr>
          <td>Volumen Exportado Físico (TM)</td>
          <td>64,500 TM</td>
          <td>140,448 TM</td>
          <td>59,320 TM</td>
          <td>264,268 TM</td>
        </tr>
        <tr>
          <td>Precio Promedio Nacional FOB</td>
          <td>$4.23 / kg</td>
          <td>$0.58 / kg</td>
          <td>$1.01 / kg</td>
          <td>$1.82 / kg</td>
        </tr>
        <tr>
          <td>Participación en Valor Total (%)</td>
          <td>71.21%</td>
          <td>16.89%</td>
          <td>11.90%</td>
          <td>100.00%</td>
        </tr>
        <tr>
          <td>Participación en Volumen Físico (%)</td>
          <td>24.41%</td>
          <td>53.15%</td>
          <td>22.44%</td>
          <td>100.00%</td>
        </tr>
        <tr>
          <td>Crecimiento Compuesto (CAGR 2015–2025)</td>
          <td>+55.6% anual</td>
          <td>+4.2% anual</td>
          <td>+2.8% anual</td>
          <td>+21.4% anual</td>
        </tr>
        <tr>
          <td>Concentración Destinos (Índice HHI)</td>
          <td>4,710 (Moderado/Alto)</td>
          <td>2,128 (Balanceado)</td>
          <td>8,885 (Monopsonio Crítico)</td>
          <td>—</td>
        </tr>
        <tr>
          <td>Retorno FOB por Contenedor (20 TM)</td>
          <td>$84,600 – $132,200</td>
          <td>$11,600</td>
          <td>$20,200 – $60,600</td>
          <td>—</td>
        </tr>
      </tbody>
    </table>
    <div class="table-note">
      <em>Nota.</em> Elaboración propia a partir de datos oficiales de UN Comtrade (2025, Reporter 218: Ecuador) y MAG (2026, Boletín de Comercio Exterior a Octubre 2026). *El mango se registra de forma consolidada en las estadísticas del MAG dentro de la subpartida genérica de frutas frescas diversas.
    </div>
  </div>

  <p>
    El contraste entre el volumen y el valor generado es el primer hallazgo que debe guiar la tesis del inversionista. Mientras que la piña representa más de la mitad de la masa exportada (53.15% de los fletes físicos), la pitahaya aporta más de siete de cada diez dólares de la canasta (71.21%), empleando menos de una cuarta parte de la capacidad naviera total.
  </p>

  <!-- ========================================================================= -->
  <!-- FIGURA 1: COMPARATIVA VISUAL DE PRECIOS Y RETORNO                        -->
  <!-- ========================================================================= -->
  <div class="figure-container">
    <div class="figure-number">Figura 1</div>
    <div class="figure-title">Comparativa de Precios FOB Promedio y Retorno Bruto por Contenedor Refrigerado (20 TM)</div>
    <div class="figure-content">
      <!-- Embedded Vector SVG Graphic -->
      <svg viewBox="0 0 760 240" width="100%" height="240" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Times New Roman', serif;">
        <!-- Background Grid -->
        <line x1="160" y1="30" x2="560" y2="30" stroke="#e5e7eb" stroke-dasharray="3,3" />
        <line x1="160" y1="75" x2="560" y2="75" stroke="#e5e7eb" stroke-dasharray="3,3" />
        <line x1="160" y1="120" x2="560" y2="120" stroke="#e5e7eb" stroke-dasharray="3,3" />
        <line x1="160" y1="165" x2="560" y2="165" stroke="#e5e7eb" stroke-dasharray="3,3" />
        <line x1="160" y1="200" x2="560" y2="200" stroke="#111827" stroke-width="1.5" />

        <!-- X Axis Scale Marks -->
        <text x="160" y="215" font-size="10" text-anchor="middle" fill="#666">$0</text>
        <text x="240" y="215" font-size="10" text-anchor="middle" fill="#666">$30K</text>
        <text x="320" y="215" font-size="10" text-anchor="middle" fill="#666">$60K</text>
        <text x="400" y="215" font-size="10" text-anchor="middle" fill="#666">$90K</text>
        <text x="480" y="215" font-size="10" text-anchor="middle" fill="#666">$120K</text>
        <text x="560" y="215" font-size="10" text-anchor="middle" fill="#666">$150K USD</text>

        <!-- Product 1: Pitahaya España -->
        <text x="150" y="52" font-size="11" font-weight="bold" text-anchor="end" fill="#111">Pitahaya (España)</text>
        <rect x="160" y="38" width="352" height="22" fill="#cd0a33" rx="2" />
        <text x="520" y="53" font-size="10" font-weight="bold" fill="#cd0a33">$132,200 USD ($6.61/kg)</text>

        <!-- Product 2: Pitahaya EE.UU. -->
        <text x="150" y="87" font-size="11" font-weight="bold" text-anchor="end" fill="#111">Pitahaya (EE.UU.)</text>
        <rect x="160" y="73" width="229" height="22" fill="#e11d48" rx="2" />
        <text x="397" y="88" font-size="10" font-weight="bold" fill="#e11d48">$86,000 USD ($4.30/kg)</text>

        <!-- Product 3: Mango Europa -->
        <text x="150" y="122" font-size="11" font-weight="bold" text-anchor="end" fill="#111">Mango (Holanda)</text>
        <rect x="160" y="108" width="161" height="22" fill="#111827" rx="2" />
        <text x="329" y="123" font-size="10" font-weight="bold" fill="#111827">$60,600 USD ($3.03/kg)</text>

        <!-- Product 4: Mango EE.UU. -->
        <text x="150" y="157" font-size="11" font-weight="bold" text-anchor="end" fill="#111">Mango (EE.UU.)</text>
        <rect x="160" y="143" width="54" height="22" fill="#4b5563" rx="2" />
        <text x="222" y="158" font-size="10" font-weight="bold" fill="#4b5563">$20,200 USD ($1.01/kg)</text>

        <!-- Product 5: Piña Chile/EEUU -->
        <text x="150" y="192" font-size="11" font-weight="bold" text-anchor="end" fill="#111">Piña Golden MD2</text>
        <rect x="160" y="178" width="31" height="22" fill="#9ca3af" rx="2" />
        <text x="199" y="193" font-size="10" font-weight="bold" fill="#666">$11,600 USD ($0.58/kg)</text>
      </svg>
    </div>
    <div class="figure-note">
      <em>Nota.</em> Simulación de facturación bruta FOB estimada para un contenedor marítimo refrigerado estándar de 40 pies con carga útil neta de 20 toneladas métricas (20,000 kg), calculada sobre los precios FOB medios ponderados de aduana en 2025.
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 3. ANÁLISIS ESPECÍFICO POR LÍNEA FRUTÍCOLA                               -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">3. Análisis Estratégico y Selección de Mercados Objetivo</h1>

  <h2 class="apa-h2">3.1. Pitahaya (HS 081090): La Opción de Máxima Rentabilidad y Nichos de Alto Valor</h2>
  <p>
    La pitahaya, conocida en los mercados globales como fruta del dragón (<em>dragon fruit</em>), representa la historia de éxito más fulgurante del agro ecuatoriano reciente. Entre 2015 y 2025, el valor exportado se expandió desde USD 3.27 millones hasta rozar los USD 342 millones (UN Comtrade, 2025; MAG, 2026), arrojando una Tasa de Crecimiento Anual Compuesta (CAGR) del +55.6% sostenido.
  </p>
  <p>
    El éxito de este cultivo —centrado en la variedad amarilla (<em>Selenicereus megalanthus</em>) del cantón Palora en Morona Santiago y en las variedades rojas (<em>Hylocereus undatus</em>) cultivadas en Santa Elena, Manabí y Guayas— radica en su perfil organoléptico (grados Brix superiores a 18° frente a las variedades asiáticas) y sus propiedades digestivas y antioxidantes, que la sitúan en la categoría de "superalimento" en el hemisferio norte.
  </p>

  <h3 class="apa-h3">Análisis de Destinos Compradores y Cuota en España</h3>
  <p>
    A nivel geográfico, las exportaciones ecuatorianas de pitahaya exhiben una dualidad fundamental:
  </p>
  <ul class="apa-list">
    <li>
      <strong>Estados Unidos (Mercado de Absorción de Volumen):</strong> Acapara el 66.6% de las ventas totales de Ecuador (USD 227.87 millones en 2025). Su cercanía logística (8 a 10 días de tránsito marítimo hacia puertos de la costa este como Filadelfia y Miami) y la apertura de protocolos fitosanitarios aprobados por el USDA-APHIS permiten vaciar grandes volúmenes de cosecha. Sin embargo, su precio medio (USD 4.30/kg) sufre caídas estacionales significativas durante los picos de cosecha de Palora.
    </li>
    <li>
      <strong>España (Mercado de Liderazgo y Máximo Retorno):</strong> Es el segundo comprador de Ecuador en volumen (14.3% de las ventas, USD 48.72 millones). Al analizar las importaciones totales de España registradas por su propia autoridad aduanera (Comtrade Reporter 724: Spain), se comprueba que España importó USD 42.20 millones en frutas de la partida 081090 en 2025. De ese total, <strong>Ecuador proveyó el 42.73% (USD 18.03 millones)</strong>, posicionándose como el <strong>proveedor #1 indiscutible en territorio español</strong>, por encima de Perú (15.72%), Colombia (12.54%), Vietnam (5.38%) y Marruecos (3.93%). Además, España pagó a los exportadores ecuatorianos un precio medio de USD 6.61/kg FOB (+54% respecto al precio de EE.UU.).
    </li>
    <li>
      <strong>Nichos de Exportación Aérea de Ultra-Lujo:</strong> Mercados como Emiratos Árabes Unidos (USD 19.47/kg FOB), Reino Unido (USD 8.10/kg), Francia (USD 7.40/kg) y Singapur (USD 5.56/kg) demandan calibres grandes (frutas de 350g a 500g) transportadas por vía aérea con entrega en menos de 72 horas desde la cosecha, representando el escalón de mayor valor agregado por caja.
    </li>
  </ul>

  <div class="strategic-box">
    <strong>Dictamen para el Inversionista en Pitahaya:</strong> La pitahaya es la opción altamente recomendada para emprendedores y pymes con capital limitado que buscan maximizar el margen por kilogramo y recuperar rápidamente la inversión. Un solo contenedor reefer colocado en Europa factura entre USD 120,000 y USD 135,000 FOB, con un margen bruto neto estimado del 45% al 60% tras deducir los costos de compra en finca (USD 1.80 a USD 2.30/kg) y empaque.
  </div>

  <h2 class="apa-h2">3.2. Piña Golden MD2 (HS 080430): Negocio Defensivo de Escala y Logística del Pacífico</h2>
  <p>
    La piña de la variedad Golden MD2 constituye una industria madura y altamente estandarizada en el Ecuador. En 2025, el país exportó 140,448 toneladas métricas que generaron USD 81.11 millones FOB (MAG, 2026). A diferencia de la pitahaya, la piña no compite por escasez o novedad, sino por consistencia, calidad de dulzor y capacidad de suministro ininterrumpido durante las 52 semanas del año.
  </p>

  <h3 class="apa-h3">El Fenómeno del Monopolio Ecuatoriano en Chile</h3>
  <p>
    En el escenario mundial de la piña fresca, Costa Rica es el líder indiscutible, abasteciendo más del 83% del mercado de Estados Unidos y el 72% de la Unión Europea. Intentar competir frontalmente contra las multinacionales costarricenses en puertos del Atlántico o el Golfo de México representa un riesgo comercial severo para un nuevo exportador ecuatoriano, debido a que Costa Rica goza de menores tiempos de tránsito y subsidios de escala naviera.
  </p>
  <p>
    No obstante, la geografía comercial otorga al Ecuador una ventaja comparativa imbatible en la cuenca del Océano Pacífico:
  </p>
  <ul class="apa-list">
    <li>
      <strong>Dominio Absoluto en Chile (93.34% de Cuota):</strong> De acuerdo con los datos oficiales de importación del Servicio Nacional de Aduanas de Chile para 2025, el mercado chileno importó USD 15.27 millones en piña fresca. De este monto, <strong>Ecuador suministró USD 14.25 millones</strong>, lo que equivale a una penetración monopólica del <strong>93.34%</strong> del mercado, dejando a Costa Rica con un marginal 4.96% (USD 758 mil) y a China con el 0.58%.
    </li>
    <li>
      <strong>Eficiencia en Ruta y Flete:</strong> Las motonaves portacontenedores conectan los terminales de Guayaquil o Puerto Bolívar con Valparaíso y San Antonio en apenas <strong>4 a 6 días de navegación directa</strong> por la costa pacífica sudamericana. Esta ruta no cruza el Canal de Panamá, ahorrando entre USD 2,500 y USD 4,000 por contenedor en peajes y retrasos por congestión hídrica, permitiendo que la fruta llegue en un estado óptimo de frescura (coloración 2.5 a 3.0 en escala MD2).
    </li>
    <li>
      <strong>Tratamiento Arancelario 0%:</strong> En el marco del Acuerdo de Complementación Económica N° 65 (ACE 65) suscrito entre Chile y Ecuador, la piña ecuatoriana ingresa con arancel cero y requisitos fitosanitarios ágiles coordinados entre Agrocalidad y el SAG de Chile.
    </li>
  </ul>

  <div class="strategic-box">
    <strong>Dictamen para el Inversionista en Piña:</strong> La piña es el modelo idóneo para empresas con respaldo de infraestructura, acceso a contratos de producción en fincas tecnificadas de Los Ríos o Santo Domingo de los Tsáchilas, y capacidad financiera para operar a volumen. Es un negocio defensivo, predecible y con riesgo de cobro mínimo en el mercado chileno, logrando márgenes brutos estables del 18% al 22% por contenedor.
  </div>

  <h2 class="apa-h2">3.3. Mango Fresco (HS 080450): Oportunidad de Arbitraje hacia Europa</h2>
  <p>
    El mango ecuatoriano (principalmente variedades Tommy Atkins, Kent y Haden) alcanzó en 2025 una exportación de USD 57.13 millones equivalentes a 59,320 toneladas métricas (UN Comtrade, 2025). La industria nacional posee una ventana de cosecha muy definida entre los meses de octubre y enero, período en el cual el hemisferio norte carece de producción doméstica.
  </p>

  <h3 class="apa-h3">Diagnóstico del Monopsonio Estadounidense y Arbitraje en la Unión Europea</h3>
  <p>
    El sector del mango atraviesa una vulnerabilidad estructural crítica: el <strong>94.22% de toda la exportación ecuatoriana se dirige a un solo comprador: Estados Unidos</strong> (USD 53.83 millones). Este nivel de concentración genera un Índice de Herfindahl-Hirschman (HHI) de 8,885 puntos, catalogado por la teoría económica como un "monopsonio extremo". Como consecuencia de esta saturación en los puertos de Miami y Los Ángeles, el importador estadounidense liquida el mango ecuatoriano a un precio promedio deprimido de <strong>USD 1.01 / kg FOB</strong> (aproximadamente USD 4.00 por caja de 4 kg).
  </p>
  <p>
    En contraste, los mercados de Europa occidental presentan una oportunidad sobresaliente de arbitraje de precios:
  </p>
  <ul class="apa-list">
    <li>
      <strong>Países Bajos (Hub de Róterdam):</strong> Paga a los exportadores ecuatorianos un precio promedio de <strong>USD 3.03 / kg FOB (+200% frente a EE.UU.)</strong>.
    </li>
    <li>
      <strong>Francia y Bélgica:</strong> Registran precios promedio de <strong>USD 2.77 / kg</strong> y <strong>USD 2.34 / kg FOB</strong>, respectivamente.
    </li>
    <li>
      <strong>España:</strong> Importa variedades de calibre fino a <strong>USD 2.07 / kg FOB</strong>.
    </li>
  </ul>
  <p>
    Desviar tan solo el 10% del volumen que actualmente se malvende en Estados Unidos hacia los distribuidores del puerto de Róterdam inyectaría más de <strong>USD 11.8 millones adicionales de margen bruto</strong> a la cadena exportadora nacional (UN Comtrade, 2025).
  </p>

  <div class="strategic-box">
    <strong>Dictamen para el Inversionista en Mango:</strong> No incursione en el mango si planea consignar fruta a intermediarios en Estados Unidos, ya que el riesgo de castigo de precios es altísimo. Incursione únicamente si adopta la estrategia europea: exportar variedades de alta pulpa y bajo contenido de fibra (Kent o Keitt) hacia Países Bajos o Francia utilizando contenedores con <em>Atmósfera Controlada</em> (CA), capturando un retorno de USD 60,600 FOB por contenedor frente a los magros USD 20,200 FOB que rinde en Miami.
  </div>

  <!-- ========================================================================= -->
  <!-- 4. MATRIZ DE DECISIÓN PARA EL INVERSIONISTA                              -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>
  <h1 class="apa-h1">4. Matriz de Decisión Estratégica para Nuevos Exportadores</h1>
  <p>
    Con el propósito de clarificar el proceso de selección y alinearlo con las capacidades financieras, logísticas y operativas del postulante, la Tabla 2 presenta una matriz comparativa multidimensional.
  </p>

  <div class="table-container">
    <div class="table-number">Tabla 2</div>
    <div class="table-title">Matriz de Selección y Factibilidad para Nuevos Exportadores de Fruta en Ecuador</div>
    <table class="apa-table">
      <thead>
        <tr>
          <th>Parámetro de Evaluación</th>
          <th>Opción A: Pitahaya</th>
          <th>Opción B: Piña Golden</th>
          <th>Opción C: Mango (Europa)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Estrategia Comercial</strong></td>
          <td>Diferenciación por valor y súperfruta</td>
          <td>Liderazgo en costos y escala</td>
          <td>Arbitraje geográfico selectivo</td>
        </tr>
        <tr>
          <td><strong>Capital Inicial de Trabajo</strong></td>
          <td>Medio ($35,000 – $50,000 / cont.)</td>
          <td>Bajo ($10,000 – $15,000 / cont.)</td>
          <td>Medio-Alto ($25,000 – $40,000 / cont.)</td>
        </tr>
        <tr>
          <td><strong>Mercado Objetivo Recomendado</strong></td>
          <td>España (Marítimo) / EAU (Aéreo)</td>
          <td>Chile (San Antonio / Valparaíso)</td>
          <td>Países Bajos (Róterdam) / Francia</td>
        </tr>
        <tr>
          <td><strong>Precio FOB de Venta Esperado</strong></td>
          <td>$6.25 – $6.61 / kg (Europa)</td>
          <td>$0.58 / kg ($11.60 / caja 20kg)</td>
          <td>$2.80 – $3.03 / kg (Europa)</td>
        </tr>
        <tr>
          <td><strong>Margen Bruto Proyectado</strong></td>
          <td>45% – 60%</td>
          <td>18% – 22%</td>
          <td>35% – 45%</td>
        </tr>
        <tr>
          <td><strong>Sensibilidad de Vida Posmariposa</strong></td>
          <td>Media-Alta (21 a 28 días en frío)</td>
          <td>Alta (28 a 35 días a 7°C–10°C)</td>
          <td>Crítica (requiere Atmósfera Controlada)</td>
        </tr>
        <tr>
          <td><strong>Complejidad Fitosanitaria</strong></td>
          <td>Media (Monitoreo mosca fruta)</td>
          <td>Baja (Tratamiento fungicida de corona)</td>
          <td>Alta (Tratamiento hidrotérmico / LMR)</td>
        </tr>
        <tr>
          <td><strong>Riesgo de Saturación</strong></td>
          <td>Bajo en Europa, Alto en EE.UU.</td>
          <td>Muy Bajo en Chile, Alto en el Atlántico</td>
          <td>Muy Bajo en Europa, Crítico en EE.UU.</td>
        </tr>
        <tr>
          <td><strong>Perfil de Inversionista Idóneo</strong></td>
          <td>Pyme agroindustrial, agilidad comercial</td>
          <td>Inversor con visión de flujo estable</td>
          <td>Agroexportador con rigor en frío</td>
        </tr>
      </tbody>
    </table>
    <div class="table-note">
      <em>Nota.</em> Evaluaciones cualitativas y cuantitativas construidas por CTS International Freight Forwarder con base en auditorías de costos portuarios y parámetros arancelarios vigentes en 2025–2026.
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 5. BARRERAS ARANCELARIAS Y FITOSANITARIAS                                 -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">5. Marco Arancelario y Barreras de Acceso en Mercados Meta</h1>
  <p>
    El éxito de una exportación no depende exclusivamente de la calidad del producto en campo, sino de la capacidad para sortear las regulaciones no arancelarias y aprovechar los acuerdos comerciales que otorgan ventajas arancelarias preferenciales al Ecuador. La Tabla 3 expone el tratamiento arancelario formal y las barreras técnicas aplicadas.
  </p>

  <div class="table-container">
    <div class="table-number">Tabla 3</div>
    <div class="table-title">Condiciones Arancelarias Efectivas y Exigencias Fitosanitarias por Mercado Destino</div>
    <table class="apa-table">
      <thead>
        <tr>
          <th>Mercado Destino</th>
          <th>Fruta / Partida</th>
          <th>Arancel NMF</th>
          <th>Arancel Efectivo Ecuador</th>
          <th>Requisitos Fitosanitarios Clave</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>España / Unión Europea</strong></td>
          <td>Pitahaya (081090)<br>Mango (080450)</td>
          <td>8.80% MFN</td>
          <td><strong>0.00% (Acuerdo Multipartes)</strong></td>
          <td>Certificado fitosanitario emitido por Agrocalidad; trazabilidad digital; límites estrictos de residuos químicos (LMR europeos); certificación GlobalG.A.P.</td>
        </tr>
        <tr>
          <td><strong>Chile</strong></td>
          <td>Piña Golden (080430)</td>
          <td>6.00% MFN</td>
          <td><strong>0.00% (Acuerdo ACE 65)</strong></td>
          <td>Aprobación del SAG Chile; predios libres de plagas cuarentenarias; tratamiento poscosecha en corona contra cochinilla harinosa.</td>
        </tr>
        <tr>
          <td><strong>Estados Unidos</strong></td>
          <td>Pitahaya (081090)<br>Mango (080450)</td>
          <td>2.2% a 3.58%</td>
          <td><strong>0.00% a 0.29% Efectivo</strong></td>
          <td>Inspección USDA-APHIS; para mango es mandatorio el tratamiento hidrotérmico (agua caliente a 46°C) en planta empacadora certificada; registro FDA / Ley Bioterrorismo.</td>
        </tr>
        <tr>
          <td><strong>Canadá</strong></td>
          <td>Pitahaya (081090)</td>
          <td>0.00%</td>
          <td><strong>0.00% (Trato MFN General)</strong></td>
          <td>Agencia Canadiense de Inspección de Alimentos (CFIA); certificado de no presencia de insectos vivos; cumplimiento de la normativa SFCR.</td>
        </tr>
      </tbody>
    </table>
    <div class="table-note">
      <em>Nota.</em> Datos extraídos de la base TradeStats del Banco Mundial (WITS, 2025) y regulaciones aduaneras de la Dirección General de Comercio de la Comisión Europea (Access2Markets, 2025).
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 6. GESTIÓN LOGÍSTICA Y CADENA DE FRÍO                                     -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">6. Aspectos Logísticos, Cadena de Frío e Incoterms (Guía CTS)</h1>
  <p>
    En el comercio de frutas perecederas, la logística no es un costo de transporte sino la salvaguarda de la vida útil comercial del producto. Cada día de demora o fluctuación térmica en el trayecto deprime el precio de liquidación en el mercado mayorista de destino.
  </p>

  <h2 class="apa-h2">6.1. Especificaciones de Contenedores y Rangos de Temperatura</h2>
  <ul class="apa-list">
    <li>
      <strong>Pitahaya (Modo Convencional Reefer):</strong> Rango térmico de 7.0°C a 10.0°C con humedad relativa del 85% al 90%. Ventilación de aire fresco ajustada a 15 a 20 m³/h para evitar acumulación de dióxido de carbono y etileno.
    </li>
    <li>
      <strong>Piña Golden MD2 (Modo Reefer Estándar):</strong> Rango térmico estricto de 7.5°C a 8.5°C con 85% de humedad. Temperaturas inferiores a 6.5°C inducen daño por frío (<em>chilling injury</em>), manifestado por el oscurecimiento interno de la pulpa.
    </li>
    <li>
      <strong>Mango Fresco (Modo Atmósfera Controlada - CA Obligatorio para Europa):</strong> Ajuste térmico a 10.0°C – 12.0°C. Sistema de inyección de gases regulado a 3%–5% de oxígeno (O₂) y 5%–8% de dióxido de carbono (CO₂). Este ambiente artificial frena la respiración celular del fruto y la producción de etileno, permitiendo que el mango arribe a Róterdam tras 16 días en estado verde maduro.
    </li>
  </ul>

  <h2 class="apa-h2">6.2. Términos de Negociación Internacional (Incoterms 2020) Recomendados</h2>
  <p>
    Para un exportador novel en Ecuador, la selección del Incoterm define la distribución del riesgo de tránsito:
  </p>
  <ul class="apa-list">
    <li>
      <strong>Incoterm FOB (Free on Board - Puerto Guayaquil / Posorja):</strong> Altamente recomendado para las primeras tres operaciones. El exportador asume el flete interno y la aduana de salida; el importador extranjero asume el flete marítimo y el seguro internacional, reduciendo el desembolso financiero y el riesgo en alta mar para el vendedor ecuatoriano.
    </li>
    <li>
      <strong>Incoterm CFR / CIF (Cost, Freight and Insurance):</strong> Recomendado a partir del segundo año cuando el exportador consolida alianzas con un forwarder confiable (como CTS). Permite al exportador capturar mejores tarifas negociadas de flete y ofrecer una solución integral al comprador europeo.
    </li>
    <li>
      <strong>Precaución Crítica — Prohibición de la Consignación:</strong> El nuevo exportador debe rechazar categóricamente embarcar bajo esquemas de "consignación abierta" o "precio a fijar en destino". En caso de saturación temporal de mercado, el importador castigará la liquidación reportando supuestos daños de calidad. Se debe exigir <strong>contratos con precio mínimo garantizado</strong> respaldados por <strong>Carta de Crédito Irrevocable y Confirmada</strong> o un anticipo del 30%–50% previo al embarque y saldo contra entrega de Conocimiento de Embarque (B/L) y Certificado Fitosanitario.
    </li>
  </ul>

  <!-- ========================================================================= -->
  <!-- 7. HOJA DE RUTA OPERATIVA EN SEIS FASES                                   -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>
  <h1 class="apa-h1">7. Hoja de Ruta Operativa en Seis Fases para el Exportador</h1>
  <p>
    Para transformar este diagnóstico en una operación rentable y libre de contingencias, el inversionista debe ejecutar secuencialmente las siguientes seis fases operativas:
  </p>

  <ol class="apa-list">
    <li>
      <strong>Fase 1: Formalización Legal y Tributaria:</strong>
      Constitución de la sociedad mercantil en la Superintendencia de Compañías (recomendada SAS: Sociedad por Acciones Simplificada), obtención del Registro Único de Contribuyentes (RUC) con actividad de comercio exterior en el SRI, adquisición del certificado de firma electrónica (Security Data o Banco Central) y empadronamiento como Operador de Comercio Exterior (OCE) en el sistema ECUAPASS del Servicio Nacional de Aduana del Ecuador (SENAE).
    </li>
    <li>
      <strong>Fase 2: Certificación Sanitaria ante Agrocalidad:</strong>
      Registro formal como Exportador de Frutas Frescas ante la Agencia de Regulación y Control Fito y Zoosanitario (Agrocalidad). Vinculación de fincas abastecedoras que cuenten con certificación de Buenas Prácticas Agrícolas (BPA) y código de sitio de producción libre de plagas. Para envíos a la Unión Europea, verificar que la empacadora cuente con certificación GlobalG.A.P. versión 6.
    </li>
    <li>
      <strong>Fase 3: Prospección Comercial y Cierre de Contrato de Compraventa:</strong>
      Identificación y validación crediticia del importador mediante bases de datos comerciales (ej. D&B o registros de la Cámara Oficial Española de Comercio del Ecuador). Negociación de especificaciones de calidad: calibres, grados Brix mínimos, tolerancia de defectos externos, tipo de empaque (cajas de cartón corrugado de 2.5 kg o 4.0 kg para pitahaya; cajas de 20 kg para piña). Firma de contrato marco bajo Incoterm FOB o CIF con cláusula de arbitraje internacional.
    </li>
    <li>
      <strong>Fase 4: Contratación de Flete Marítimo y Reserva de Espacio (Booking):</strong>
      Coordinación con el agente de carga internacional (CTS International Freight Forwarder) con un mínimo de 10 a 14 días de antelación al corte de la fruta. Aseguramiento de unidad reefer operativa en depósito vacío, inspección pre-viaje (PTI - <em>Pre-Trip Inspection</em>) del motor de refrigeración y calibración de atmósfera controlada cuando aplique.
    </li>
    <li>
      <strong>Fase 5: Cosecha, Empaque, Inspección Aduanera y Despacho:</strong>
      Corte de fruta en madurez óptima, transporte en furgón refrigerado hacia la empacadora, lavado, tratamiento desinfectante/fungicida autorizado, encerado, empaque y paletizado con esquineros y zunchos de alta resistencia. Inspección antinarcóticos y fitosanitaria conjunta de Agrocalidad y Policía Nacional en puerto de Guayaquil/Posorja. Obtención de la Declaración Aduanera de Exportación (DAE) y zarpe de la nave.
    </li>
    <li>
      <strong>Fase 6: Transmisión Documental y Cobro Bancario:</strong>
      Emisión del Conocimiento de Embarque (Bill of Lading - B/L), Certificado de Origen (EUR.1 para la UE o Certificado ALADI para Chile), Factura Comercial y Packing List. Presentación de documentos al banco emisor bajo la Carta de Crédito o envío de copias digitales al importador para liquidación del saldo vía transferencia telegráfica SWIFT. Repatriación legal de divisas al Ecuador.
    </li>
  </ol>

  <!-- ========================================================================= -->
  <!-- 8. CONCLUSIONES Y DICTAMEN FINAL                                         -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">8. Conclusiones y Dictamen Estratégico CTS</h1>
  <p>
    El análisis exhaustivo de los flujos de comercio exterior del Ecuador durante el período 2015–2025 demuestra que el sector de frutas tropicales no tradicionales ofrece retornos ampliamente superiores a los cultivos tradicionales de <em>commodities</em>, siempre que la elección del producto responda a una alineación rigurosa entre el perfil del inversionista y el mercado de destino:
  </p>
  <ul class="apa-list">
    <li>
      <strong>Pitahaya (HS 081090):</strong> Es el producto líder indiscutible para quienes priorizan el margen neto y la facturación por kilogramo (promedio nacional FOB de USD 4.23/kg). El mercado óptimo para una primera operación no es Estados Unidos (mercado saturado a USD 4.30/kg), sino <strong>España</strong>, donde Ecuador lidera con el <strong>42.73% de cuota nacional importadora</strong> a un precio premium de <strong>USD 6.61/kg</strong> con arancel 0%.
    </li>
    <li>
      <strong>Piña Golden MD2 (HS 080430):</strong> Es la alternativa de menor riesgo de mercado y máxima predictibilidad de cobro. Su mercado natural insustituible es <strong>Chile</strong>, donde Ecuador ejerce un <strong>monopolio del 93.34%</strong> respaldado por una ruta naviera directa de 4 a 6 días por el Pacífico libre de los costos y tiempos de espera del Canal de Panamá.
    </li>
    <li>
      <strong>Mango Fresco (HS 080450):</strong> Ofrece una oportunidad de oro para arbitraje internacional. Romper la inercia del mercado estadounidense (94.2% del volumen vendido a solo USD 1.01/kg) y despachar contenedores reefer con <strong>Atmósfera Controlada hacia Países Bajos (Róterdam) o Francia</strong> permite triplicar el ingreso por kilo (USD 3.03/kg y USD 2.77/kg FOB), capturando una prima neta superior a los USD 40,000 por contenedor.
    </li>
  </ul>
  <p>
    En definitiva, la rentabilidad en la exportación de frutas ecuatorianas no radica en cosechar la mayor cantidad de toneladas, sino en transportar la fruta adecuada hacia el destino que mejor recompensa su calidad organoléptica, protegiendo la cadena de frío bajo la asesoría de un operador logístico experimentado.
  </p>

  <!-- ========================================================================= -->
  <!-- 9. REFERENCIAS SEGÚN NORMAS APA 7                                         -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>
  <h1 class="apa-h1">Referencias</h1>

  <div class="reference-item">
    Agencia de Regulación y Control Fito y Zoosanitario [Agrocalidad]. (2024). <em>Manual de procedimientos para la certificación de predios de producción y empacadoras de frutas de exportación</em>. Ministerio de Agricultura y Ganadería del Ecuador. https://www.agrocalidad.gob.ec/
  </div>

  <div class="reference-item">
    Banco Mundial. (2025). <em>World Integrated Trade Solution (WITS): TradeStats and Tariff Data for Ecuador (Reporter 218)</em>. World Bank Group. https://wits.worldbank.org/
  </div>

  <div class="reference-item">
    Comisión Europea. (2025). <em>Access2Markets: Acuerdos comerciales y aranceles aplicables a productos agrícolas importados por la Unión Europea</em>. Dirección General de Comercio de la Unión Europea. https://trade.ec.europa.eu/access-to-markets/
  </div>

  <div class="reference-item">
    CTS International Freight Forwarder. (2026). <em>Manual de logística de cadena de frío y especificaciones de contenedores refrigerados para carga perecedera ecuatoriana</em>. División de Operaciones Marítimas y Aéreas.
  </div>

  <div class="reference-item">
    Ministerio de Agricultura y Ganadería del Ecuador [MAG]. (2026). <em>Boletín de Comercio Exterior de Productos Agrícolas (Cierre 2025 y Avance a Octubre 2026)</em>. Sistema de Información Pública Agropecuaria (SIPA). Quito, Ecuador.
  </div>

  <div class="reference-item">
    Naciones Unidas [UN Comtrade]. (2025). <em>UN Comtrade Database: International Trade Statistics for HS 080430, HS 080450 and HS 081090 (Years 2015–2025)</em>. United Nations Statistics Division. https://comtradeplus.un.org/
  </div>

  <div class="reference-item">
    Organización de las Naciones Unidas para la Alimentación y la Agricultura [FAO]. (2024). <em>Perspectivas de los mercados de frutas tropicales de alto valor: Piña, mango y pitahaya</em>. Colección de Estudios de Productos Básicos y Comercio de la FAO, N° 48. Roma. https://doi.org/10.4060/cc9876es
  </div>

  <div class="reference-item">
    Servicio Agrícola y Ganadero de Chile [SAG]. (2025). <em>Requisitos fitosanitarios de importación para piña fresca proveniente de la República del Ecuador</em>. Ministerio de Agricultura de Chile. https://www.sag.gob.cl/
  </div>

  <div class="reference-item">
    United States Department of Agriculture [USDA-APHIS]. (2024). <em>Treatment Manual and Import Requirements for Fresh Pitahaya and Mango from Ecuador</em>. Animal and Plant Health Inspection Service. https://www.aphis.usda.gov/
  </div>

</body>
</html>
"""

html_path = "Informe_Exportacion_Frutas_Ecuador_APA7.html"
pdf_path = "Informe_Exportacion_Frutas_Ecuador_APA7.pdf"
docs_pdf_path = os.path.join("docs", "Informe_Exportacion_Frutas_Ecuador_APA7.pdf")

# 1. Save the HTML file
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML generated at: {html_path}")

# 2. Render to PDF using Playwright with APA 7 header & footer specifications
print("Rendering PDF with Playwright Chromium engine...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content, wait_until="networkidle")
    
    # APA 7 header template: Title on left, Page number on right
    header_template = '''
    <div style="font-family: 'Times New Roman', serif; font-size: 9.5pt; width: 100%; display: flex; justify-content: space-between; padding: 0 1in; color: #444444; box-sizing: border-box;">
      <span style="text-transform: uppercase; letter-spacing: 0.5px; font-size: 8pt;">ESTUDIO DE FACTIBILIDAD: EXPORTACIÓN DE FRUTAS TROPICALES — CTS</span>
      <span class="pageNumber" style="font-size: 10pt; font-weight: normal;"></span>
    </div>
    '''
    
    footer_template = '''
    <div style="font-family: 'Times New Roman', serif; font-size: 8pt; width: 100%; text-align: center; color: #888888; padding: 0 1in;">
      <span>CTS International Freight Forwarder • Guía Oficial para Exportadores 2026</span>
    </div>
    '''
    
    page.pdf(
        path=pdf_path,
        format="Letter",
        display_header_footer=True,
        header_template=header_template,
        footer_template=footer_template,
        margin={
            "top": "1in",
            "right": "1in",
            "bottom": "1in",
            "left": "1in"
        },
        print_background=True
    )
    browser.close()

print(f"Master PDF generated successfully at: {pdf_path}")

# Copy to docs/ folder
os.makedirs("docs", exist_ok=True)
import shutil
shutil.copyfile(pdf_path, docs_pdf_path)
print(f"PDF mirrored to: {docs_pdf_path}")

print("All tasks completed successfully!")
