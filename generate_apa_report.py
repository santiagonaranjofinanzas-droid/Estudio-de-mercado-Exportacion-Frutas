"""
Script to generate a concise, crystal-clear, executive APA 7th Edition PDF report
for a prospective Ecuadorian fruit exporter.
- City: Quito, Ecuador
- Style: Concise, clear executive summary, practical, zero jargon, easy to read and act on.
"""

import os
import shutil
from playwright.sync_api import sync_playwright

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Guía Ejecutiva de Exportación de Frutas Tropicales Ecuatorianas</title>
  <style>
    @page {
      size: letter;
      margin: 1in;
    }

    body {
      font-family: 'Times New Roman', Times, serif;
      font-size: 11.5pt;
      line-height: 1.45;
      color: #111111;
      margin: 0;
      padding: 0;
      background-color: #ffffff;
    }

    p {
      margin-top: 0;
      margin-bottom: 0.7em;
      text-align: justify;
      text-indent: 0.5in;
    }

    .no-indent {
      text-indent: 0 !important;
    }

    h1.apa-title {
      font-size: 14pt;
      font-weight: bold;
      text-align: center;
      line-height: 1.4;
      margin-top: 1.8in;
      margin-bottom: 1.5em;
    }

    h1.apa-h1 {
      font-size: 12.5pt;
      font-weight: bold;
      text-align: center;
      margin-top: 1.4em;
      margin-bottom: 0.6em;
      page-break-after: avoid;
    }

    h2.apa-h2 {
      font-size: 11.5pt;
      font-weight: bold;
      text-align: left;
      margin-top: 1.1em;
      margin-bottom: 0.4em;
      page-break-after: avoid;
    }

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
      width: 100%;
    }

    .title-page-meta {
      margin-top: 2.2in;
      font-size: 11.5pt;
      line-height: 1.7;
    }

    .page-break {
      page-break-before: always;
    }

    .abstract-title {
      font-weight: bold;
      text-align: center;
      margin-bottom: 0.8em;
      font-size: 12pt;
    }

    .keywords {
      margin-top: 1.2em;
      text-indent: 0.5in;
    }

    .keywords em {
      font-style: italic;
    }

    /* APA 7 Tables */
    .table-container {
      margin: 1.2em 0;
      page-break-inside: avoid;
    }

    .table-number {
      font-weight: bold;
      font-size: 10.5pt;
      margin-bottom: 2px;
      text-indent: 0;
    }

    .table-title {
      font-style: italic;
      font-size: 10.5pt;
      margin-bottom: 5px;
      text-indent: 0;
    }

    table.apa-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 9.5pt;
      line-height: 1.3;
      margin-bottom: 5px;
      border-top: 2px solid #000000;
      border-bottom: 2px solid #000000;
    }

    table.apa-table th {
      border-bottom: 1px solid #000000;
      padding: 5px 6px;
      font-weight: bold;
      text-align: left;
    }

    table.apa-table td {
      padding: 5px 6px;
      vertical-align: top;
      border-bottom: none;
    }

    .table-note {
      font-size: 8.5pt;
      line-height: 1.25;
      text-indent: 0;
      color: #333333;
    }

    .table-note em {
      font-style: italic;
      font-weight: bold;
    }

    /* Callout Boxes */
    .summary-card {
      border-left: 3px solid #111827;
      background-color: #f9fafb;
      padding: 9px 12px;
      margin: 0.9em 0;
      font-size: 10.5pt;
      line-height: 1.35;
      text-indent: 0;
      page-break-inside: avoid;
    }

    .summary-card strong {
      color: #cd0a33;
    }

    .reference-item {
      padding-left: 0.5in;
      text-indent: -0.5in;
      margin-bottom: 0.7em;
      line-height: 1.35;
      font-size: 10pt;
      text-align: justify;
    }

    ol.apa-list, ul.apa-list {
      margin-top: 0.2em;
      margin-bottom: 0.6em;
      padding-left: 0.4in;
      font-size: 10.5pt;
      line-height: 1.35;
    }

    ol.apa-list li, ul.apa-list li {
      margin-bottom: 0.35em;
      text-align: justify;
    }
  </style>
</head>
<body>

  <!-- ========================================================================= -->
  <!-- PORTADA PROFESIONAL APA 7                                                 -->
  <!-- ========================================================================= -->
  <div class="title-page">
    <div class="title-page-content">
      <h1 class="apa-title">
        Guía Práctica y Resumen de Oportunidades para la Exportación de Frutas Tropicales Ecuatorianas:<br>
        <span style="font-weight: normal; font-size: 12pt;">Análisis de Rentabilidad, Mercados Clave y Recomendaciones para el Nuevo Exportador (Pitahaya, Piña y Mango)</span>
      </h1>

      <div class="title-page-meta">
        <strong>División de Inteligencia Comercial y Asesoría al Exportador</strong><br>
        CTS International Freight Forwarder<br><br>
        <strong>Dirigido a:</strong> Nuevos Exportadores e Inversionistas Agropecuarios<br>
        <strong>Ciudad y Fecha:</strong> Quito, Ecuador — Noviembre de 2026
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- RESUMEN EJECUTIVO (DIRECTO Y CLARO)                                      -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>

  <div class="abstract-title">Resumen Ejecutivo</div>
  <p class="no-indent">
    Este informe ofrece una guía directa, sin tecnicismos innecesarios, para cualquier persona o empresa en Ecuador que desee exportar fruta fresca no tradicional y necesite saber con certeza: ¿qué fruta conviene exportar?, ¿cuánto se gana por contenedor? y ¿a qué país es más seguro y rentable vender? A partir de datos oficiales de comercio exterior (UN Comtrade, 2025; MAG, 2026), se analizan tres productos principales: pitahaya, piña y mango (excluyendo el banano, dominado por grandes corporaciones). La conclusión principal es clara: <strong>(a) La pitahaya</strong> es la fruta de mayor ganancia por kilo ($4.23/kg promedio) y su mejor mercado es <strong>España</strong>, donde Ecuador lidera las ventas con un precio de $6.61/kg; <strong>(b) La piña Golden</strong> es ideal para quien busca un negocio seguro y estable de gran volumen hacia <strong>Chile</strong> (93.3% del mercado es ecuatoriano y el viaje en barco toma solo 4 a 6 días); y <strong>(c) El mango</strong> representa una gran oportunidad si se vende a <strong>Europa</strong> ($3.03/kg en Holanda), evitando saturar el mercado de Estados Unidos donde pagan muy poco ($1.01/kg).
  </p>

  <p class="keywords">
    <em>Palabras clave:</em> Exportación de frutas, Ecuador, pitahaya, piña golden, mango, precios por contenedor, mercados de destino, guía práctica para exportar.
  </p>

  <!-- ========================================================================= -->
  <!-- 1. COMPARATIVA RÁPIDA: ¿CUÁNTO SE GANA POR FRUTA?                         -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">1. Comparativa Rápida: Rentabilidad y Retorno por Contenedor</h1>
  <p>
    Para un exportador, lo más importante no es solo cuánto volumen produce el campo, sino cuánto dinero neto le deja cada contenedor refrigerado (de aproximadamente 20 toneladas métricas o 20,000 kg). La Tabla 1 resume de manera sencilla los números reales obtenidos en aduanas durante el año 2025.
  </p>

  <div class="table-container">
    <div class="table-number">Tabla 1</div>
    <div class="table-title">Resumen Comercial de las Tres Frutas Ecuatorianas (Cierre 2025)</div>
    <table class="apa-table">
      <thead>
        <tr>
          <th>Fruta Analizada</th>
          <th>Precio de Venta Promedio</th>
          <th>Facturación por Contenedor (20 TM)</th>
          <th>Margen Bruto Estimado</th>
          <th>Mercado Recomendado</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Pitahaya</strong> (HS 081090)</td>
          <td>$4.23 / kg nacional ($6.61 en España)</td>
          <td><strong>$86,000 a $132,200 USD</strong></td>
          <td><strong>45% a 60%</strong> (Alta ganancia)</td>
          <td><strong>España</strong> (Líder en ventas) y EE.UU.</td>
        </tr>
        <tr>
          <td><strong>Piña Golden</strong> (HS 080430)</td>
          <td>$0.58 / kg ($11.60 por caja de 20 kg)</td>
          <td><strong>$11,600 USD</strong></td>
          <td><strong>18% a 22%</strong> (Flujo estable)</td>
          <td><strong>Chile</strong> (Monopolio de Ecuador)</td>
        </tr>
        <tr>
          <td><strong>Mango Fresco</strong> (HS 080450)</td>
          <td>$1.01 / kg en EE.UU. vs. $3.03 en Europa</td>
          <td><strong>$20,200 en EE.UU. vs. $60,600 en Holanda</strong></td>
          <td><strong>35% a 45%</strong> (Vendiendo en Europa)</td>
          <td><strong>Países Bajos y Francia</strong></td>
        </tr>
      </tbody>
    </table>
    <div class="table-note">
      <em>Nota.</em> Datos oficiales recopilados de UN Comtrade (2025) y del Ministerio de Agricultura y Ganadería del Ecuador (MAG, 2026). Valores expresados en dólares de los Estados Unidos (USD) en condición FOB (fruta puesta en puerto de salida en Ecuador).
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 2. ANÁLISIS SENCILLO DE CADA FRUTA                                       -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">2. ¿Qué Mercado Conviene Elegir para Cada Fruta?</h1>

  <h2 class="apa-h2">2.1. Pitahaya: La Opción Más Rentable</h2>
  <p>
    La pitahaya es actualmente la "fruta estrella" de Ecuador. En 2025 se exportaron más de <strong>$341 millones de dólares</strong> (UN Comtrade, 2025). Sus características clave para el exportador son:
  </p>
  <ul class="apa-list">
    <li><strong>España es nuestro mejor comprador:</strong> Aunque a Estados Unidos le vendemos mayor cantidad de cajas (66.6% de nuestras ventas), España es donde mejor pagan. De toda la pitahaya que compra España al mundo, <strong>el 42.7% se la compra a Ecuador</strong>, siendo nosotros su proveedor número uno.</li>
    <li><strong>Excelente precio:</strong> España paga en promedio <strong>$6.61 por kilo</strong>, mientras que en Estados Unidos pagan $4.30 por kilo. Además, en Europa la pitahaya ecuatoriana entra con <strong>arancel del 0%</strong>.</li>
    <li><strong>Ventas en avión (mercados VIP):</strong> Para clientes de lujo en Emiratos Árabes o Reino Unido, la fruta se envía por vía aérea y llega a pagarse entre <strong>$8.00 y $19.47 por kilo</strong>.</li>
  </ul>

  <div class="summary-card">
    <strong>Consejo para el Exportador:</strong> Si tienes un capital mediano y buscas el mayor beneficio por cada dólar invertido, la pitahaya hacia España o Europa es la opción ganadora. Con solo uno o dos contenedores al mes se logra una facturación muy atractiva.
  </div>

  <h2 class="apa-h2">2.2. Piña Golden: El Negocio Más Seguro y Cercano</h2>
  <p>
    La piña no deja una ganancia gigante por kilo ($0.58/kg), pero es un producto muy seguro y constante que se vende todo el año. En 2025 Ecuador exportó más de 140,000 toneladas (MAG, 2026).
  </p>
  <ul class="apa-list">
    <li><strong>Dominio total en Chile:</strong> De cada 100 piñas que compra Chile del extranjero, <strong>93 piñas son de Ecuador</strong> (93.3% del mercado). Nuestro principal competidor mundial (Costa Rica) apenas tiene el 5% de Chile.</li>
    <li><strong>Viaje rápido en barco:</strong> El barco desde Ecuador a Chile tarda solo <strong>4 a 6 días</strong> de navegación directa por el Pacífico. No pasa por el Canal de Panamá, lo que ahorra miles de dólares en peajes y garantiza que la fruta llegue fresca y amarilla.</li>
    <li><strong>Cero impuestos:</strong> Gracias a los acuerdos comerciales con Chile (ACE 65), la piña ecuatoriana entra sin pagar aranceles.</li>
  </ul>

  <div class="summary-card">
    <strong>Consejo para el Exportador:</strong> La piña es ideal para quien ya tiene acceso a fincas grandes o empaques tecnificados en Los Ríos o Santo Domingo y busca un negocio de bajo riesgo, con pagos rápidos y clientes fieles en Chile.
  </div>

  <h2 class="apa-h2">2.3. Mango: El Secreto del Arbitraje en Europa</h2>
  <p>
    En el mango existe hoy un grave error que la mayoría de exportadores comete: <strong>el 94.2% de todo el mango ecuatoriano se envía a Estados Unidos</strong>. Al llegar todo el producto junto a Miami en los mismos meses, el precio se desploma a apenas <strong>$1.01 por kilo</strong> ($4 dólares por caja de 4 kilos).
  </p>
  <ul class="apa-list">
    <li><strong>La oportunidad en Europa:</strong> Países Bajos (puerto de Róterdam) paga <strong>$3.03 por kilo</strong> y Francia paga <strong>$2.77 por kilo</strong> (tres veces más que en EE.UU.).</li>
    <li><strong>El requisito técnico:</strong> Como el barco a Europa tarda de 14 a 16 días, el mango debe viajar en un contenedor con <strong>Atmósfera Controlada</strong> (un sistema que regula el oxígeno y frena la maduración para que la fruta llegue verde y firme).</li>
  </ul>

  <div class="summary-card">
    <strong>Consejo para el Exportador:</strong> No envíes mango a consignación a Estados Unidos porque corres el riesgo de perder dinero. El negocio rentable está en firmar contratos de venta firme hacia Holanda o Francia con fruta de buena variedad (Kent o Keitt).
  </div>

  <!-- ========================================================================= -->
  <!-- 3. MATRIZ DE DECISIÓN: ¿CUÁL TE CONVIENE SEGÚN TU PERFIL?                -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>
  <h1 class="apa-h1">3. Matriz de Decisión: ¿Qué Fruta Elegir Según Tu Capital?</h1>
  <p>
    Para saber cuál es la mejor fruta para tu proyecto particular, revisa la Tabla 2 según el dinero disponible y la experiencia con la que cuentes.
  </p>

  <div class="table-container">
    <div class="table-number">Tabla 2</div>
    <div class="table-title">Guía de Decisión según el Perfil del Emprendedor o Inversionista</div>
    <table class="apa-table">
      <thead>
        <tr>
          <th>Criterio de Decisión</th>
          <th>Pitahaya (España / Europa)</th>
          <th>Piña Golden (Chile)</th>
          <th>Mango (Europa)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Dinero necesario por contenedor</strong></td>
          <td>Medio ($35,000 a $45,000 USD)</td>
          <td>Bajo ($10,000 a $15,000 USD)</td>
          <td>Medio ($25,000 a $35,000 USD)</td>
        </tr>
        <tr>
          <td><strong>Tipo de ganancia esperada</strong></td>
          <td>Muy alta por kilo (45% – 60%)</td>
          <td>Moderada pero fija (18% – 22%)</td>
          <td>Alta si va a Europa (35% – 45%)</td>
        </tr>
        <tr>
          <td><strong>Días de viaje en barco</strong></td>
          <td>14 a 16 días (hacia Algeciras/Valencia)</td>
          <td>4 a 6 días (Valparaíso/San Antonio)</td>
          <td>14 a 16 días (Róterdam)</td>
        </tr>
        <tr>
          <td><strong>Riesgo de que no te paguen</strong></td>
          <td>Bajo si usas Carta de Crédito</td>
          <td>Muy bajo (mercado consolidado)</td>
          <td>Medio (exige contrato cerrado)</td>
        </tr>
        <tr>
          <td><strong>Perfil recomendado</strong></td>
          <td>Emprendedor que busca alta rentabilidad</td>
          <td>Empresario de volumen y estabilidad</td>
          <td>Productor con buen manejo de frío</td>
        </tr>
      </tbody>
    </table>
    <div class="table-note">
      <em>Nota.</em> Estimaciones elaboradas por la División de Asesoría al Exportador de CTS International Freight Forwarder con base en costos de flete, empaque y compra de fruta en finca para 2025–2026.
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 4. PASO A PASO PARA EMPEZAR A EXPORTAR                                    -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">4. Hoja de Ruta: Los 6 Pasos para Realizar Tu Primera Exportación</h1>
  <p>
    Para que tu primera exportación sea exitosa y evites errores costosos, sigue estos seis pasos en orden:
  </p>

  <ol class="apa-list">
    <li>
      <strong>Paso 1: Formalizar la empresa:</strong> Crear una compañía (la más rápida y recomendada es una SAS: Sociedad por Acciones Simplificada), sacar el RUC con actividad de exportación en el SRI y registrarte en el sistema aduanero ECUAPASS con tu firma electrónica.
    </li>
    <li>
      <strong>Paso 2: Registrarte en Agrocalidad:</strong> Registrarse como exportador de fruta fresca en Agrocalidad y asegurarte de que la finca donde compres la fruta tenga registro de Buenas Prácticas Agrícolas (BPA) y esté libre de plagas. Para Europa te pedirán certificación GlobalG.A.P.
    </li>
    <li>
      <strong>Paso 3: Cerrar la venta con el comprador extranjero:</strong> Acordar el precio por caja y la forma de pago. <em>Regla de oro:</em> Nunca envíes fruta "a consignación" (donde te dicen que te pagarán según cómo se venda allá). Pide siempre un <strong>anticipo (30% a 50%)</strong> o una <strong>Carta de Crédito bancaria</strong> que garantice tu dinero antes de que el barco zarpe.
    </li>
    <li>
      <strong>Paso 4: Coordinar la logística y el frío con tu forwarder:</strong> Contactar con anticipación a tu operador logístico (CTS Freight Forwarder) para reservar el contenedor refrigerado en el barco y definir la temperatura exacta (ej. 8°C para pitahaya, 8°C para piña y atmósfera controlada para mango).
    </li>
    <li>
      <strong>Paso 5: Empaque, inspección y subida al barco:</strong> Cosechar en el punto justo de madurez, empacar en cajas de cartón limpias y paletizar. En el puerto de salida (Guayaquil o Posorja), Agrocalidad y la Policía Antinarcóticos inspeccionan la carga y se genera la Declaración Aduanera (DAE).
    </li>
    <li>
      <strong>Paso 6: Envío de documentos y cobro:</strong> Una vez que el barco zarpa, la naviera entrega el conocimiento de embarque (Bill of Lading o B/L). Envías copias de la factura, certificado de origen y fitosanitario al cliente y tu banco recibe la transferencia internacional de tu pago.
    </li>
  </ol>

  <!-- ========================================================================= -->
  <!-- 5. CONCLUSIÓN Y DICTAMEN FINAL                                            -->
  <!-- ========================================================================= -->
  <h1 class="apa-h1">5. Conclusión y Recomendación Final</h1>
  <p>
    Exportar fruta desde Ecuador es un negocio sumamente rentable si se elige el destino correcto y se cuida la cadena de frío. Para quien va a iniciar hoy:
  </p>
  <ul class="apa-list">
    <li><strong>La mejor recomendación general:</strong> Iniciar con <strong>Pitahaya hacia España</strong>. Tienes arancel 0%, eres parte del país líder del mercado, el producto se vende con excelente margen ($132,000 USD por contenedor) y la fruta tolera perfectamente los 15 días de viaje marítimo.</li>
    <li><strong>Si buscas bajo riesgo y rapidez:</strong> Exportar <strong>Piña Golden hacia Chile</strong>. El cobro es casi inmediato por la cercanía (5 días de viaje) y no tienes competidores que puedan igualar el flete de Ecuador.</li>
  </ul>

  <!-- ========================================================================= -->
  <!-- REFERENCIAS APA 7                                                         -->
  <!-- ========================================================================= -->
  <div class="page-break"></div>
  <h1 class="apa-h1">Referencias</h1>

  <div class="reference-item">
    Agrocalidad. (2024). <em>Guía de requisitos fitosanitarios para la exportación de frutas frescas</em>. Agencia de Regulación y Control Fito y Zoosanitario del Ecuador. https://www.agrocalidad.gob.ec/
  </div>

  <div class="reference-item">
    Banco Mundial. (2025). <em>Base de datos arancelarios WITS para exportaciones de Ecuador</em>. World Integrated Trade Solution. https://wits.worldbank.org/
  </div>

  <div class="reference-item">
    Comisión Europea. (2025). <em>Acuerdo Comercial Multipartes entre la Unión Europea y Ecuador: Aranceles y normativas de importación agrícola</em>. Dirección General de Comercio. https://trade.ec.europa.eu/
  </div>

  <div class="reference-item">
    CTS International Freight Forwarder. (2026). <em>Manual práctico de fletes marítimos refrigerados y tiempos de tránsito para perecederos</em>. Quito, Ecuador.
  </div>

  <div class="reference-item">
    Ministerio de Agricultura y Ganadería del Ecuador [MAG]. (2026). <em>Boletín estadístico de comercio exterior agrario (Cierre 2025 a Octubre 2026)</em>. SIPA. Quito, Ecuador.
  </div>

  <div class="reference-item">
    Naciones Unidas [UN Comtrade]. (2025). <em>Estadísticas oficiales de comercio internacional para pitahaya (081090), piña (080430) y mango (080450)</em>. División de Estadísticas de la ONU. https://comtradeplus.un.org/
  </div>

  <div class="reference-item">
    Servicio Agrícola y Ganadero de Chile [SAG]. (2025). <em>Protocolo fitosanitario de importación para piña ecuatoriana bajo el Acuerdo ACE 65</em>. Santiago de Chile. https://www.sag.gob.cl/
  </div>

</body>
</html>
"""

html_path = "Informe_Exportacion_Frutas_Ecuador.html"
pdf_path = "Informe_Exportacion_Frutas_Ecuador.pdf"
docs_pdf_path = os.path.join("docs", "Informe_Exportacion_Frutas_Ecuador.pdf")
dist_html_path = os.path.join("presentacion_frutas_ecuador", "Informe_Exportacion_Frutas_Ecuador.html")
dist_pdf_path = os.path.join("presentacion_frutas_ecuador", "Informe_Exportacion_Frutas_Ecuador.pdf")

# 1. Guardar archivo HTML fuente
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
shutil.copyfile(html_path, dist_html_path)

# 2. Renderizar con Playwright Chromium en PDF (Estilo APA 7 claro y conciso)
print("Generando PDF conciso y claro en Playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content, wait_until="networkidle")

    header_template = '''
    <div style="font-family: 'Times New Roman', serif; font-size: 9pt; width: 100%; display: flex; justify-content: space-between; padding: 0 1in; color: #444444; box-sizing: border-box;">
      <span style="text-transform: uppercase; letter-spacing: 0.5px; font-size: 8pt;">GUÍA PRÁCTICA: EXPORTACIÓN DE FRUTAS — QUITO, ECUADOR</span>
      <span class="pageNumber" style="font-size: 9.5pt; font-weight: normal;"></span>
    </div>
    '''

    footer_template = '''
    <div style="font-family: 'Times New Roman', serif; font-size: 8pt; width: 100%; text-align: center; color: #777777; padding: 0 1in;">
      <span>CTS International Freight Forwarder • Guía Ejecutiva de Exportación</span>
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

# 3. Copiar a docs/ y a presentacion_frutas_ecuador/
os.makedirs("docs", exist_ok=True)
shutil.copyfile(pdf_path, docs_pdf_path)
shutil.copyfile(pdf_path, dist_pdf_path)

print(f"PDF generado exitosamente en: {pdf_path}")
print("Actualizaciones listas para sincronizar con GitHub y Vercel.")
