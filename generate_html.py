import base64
import os

with open(
    'Demo/CTS_PLATAFORMA_COMERCIAL/frontend/cts_logo_header_clean.png', 'rb'
) as f:
  logo_b64 = base64.b64encode(f.read()).decode('utf-8')

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CTS Trade Intelligence: Rentabilidad y Destinos de Frutas Ecuatorianas</title>
  <meta name="description" content="Informe ejecutivo de inteligencia comercial sobre las frutas más rentables del Ecuador (Pitahaya, Piña, Mango) y sus mercados de destino.">

  <!-- Inter & JetBrains Mono Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Chart.js via CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }},
          colors: {{
            cts: {{
              red: '#CD0A33',       // Rojo corporativo oficial CTS
              redDark: '#A60829',   // Tono oscuro para hover
              redLight: '#FDF2F4',  // Fondo sutil tintado de rojo (al 3-5%)
              black: '#111827',     // Texto principal
              slate: '#4B5563',     // Texto secundario
              muted: '#9CA3AF',     // Muted
              border: '#E5E7EB',    // Borde fino
              canvas: '#F9FAFB',    // Fondo general
              card: '#FFFFFF'       // Superficie de tarjetas
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    @media print {{
      body {{ background: #FFFFFF !important; color: #000000 !important; }}
      .no-print {{ display: none !important; }}
      .slide-page {{ page-break-after: always; min-height: 100vh; display: flex !important; }}
    }}
    .slide-fade {{
      transition: opacity 0.18s ease-in-out, transform 0.18s ease-in-out;
    }}
    .slide-enter {{
      opacity: 0;
      transform: translateY(5px);
    }}
    .slide-show {{
      opacity: 1;
      transform: translateY(0);
    }}
    .chart-box {{
      position: relative;
      width: 100%;
      height: 100%;
      min-height: 250px;
    }}
  </style>
</head>

<body class="bg-cts-canvas text-cts-black font-sans antialiased min-h-screen flex flex-col selection:bg-cts-red selection:text-white">

  <!-- ========================================================================= -->
  <!-- CTS EXECUTIVE HEADER (Clean White with Official Base64 Inlined Logo) -->
  <!-- ========================================================================= -->
  <header class="no-print bg-white border-b border-cts-border sticky top-0 z-50 px-6 lg:px-12 py-2 flex items-center justify-between">
    <div class="flex items-center space-x-4">
      <!-- Inlined High-Res CTS Logo -->
      <a href="javascript:goToSlide(1)" class="flex items-center" title="CTS International Freight Forwarder">
        <img src="data:image/png;base64,{logo_b64}" alt="CTS International Freight Forwarder" class="h-8 md:h-9 w-auto object-contain">
      </a>
      <div class="hidden sm:block h-6 w-[1px] bg-cts-border"></div>
      <div class="hidden sm:block">
        <span class="text-[11px] font-bold tracking-wider uppercase text-cts-black block">Inteligencia Comercial</span>
        <span class="text-[10px] text-cts-slate font-medium">Frutas Ecuatorianas • Cierre 2025 / Avance 2026</span>
      </div>
    </div>

    <!-- Center Navigation Tabs -->
    <div class="flex items-center space-x-1 bg-cts-canvas p-1 rounded-lg border border-cts-border text-xs font-medium">
      <button onclick="goToSlide(1)" id="nav-btn-1" class="px-2.5 py-1 rounded bg-white text-cts-red font-bold shadow-sm transition border-b-2 border-cts-red">01 Tesis</button>
      <button onclick="goToSlide(2)" id="nav-btn-2" class="px-2.5 py-1 rounded text-cts-slate hover:text-cts-black transition">02 Precios y Margen</button>
      <button onclick="goToSlide(3)" id="nav-btn-3" class="px-2.5 py-1 rounded text-cts-slate hover:text-cts-black transition">03 Destinos</button>
      <button onclick="goToSlide(4)" id="nav-btn-4" class="px-2.5 py-1 rounded text-cts-slate hover:text-cts-black transition">04 Pitahaya</button>
      <button onclick="goToSlide(5)" id="nav-btn-5" class="px-2.5 py-1 rounded text-cts-slate hover:text-cts-black transition">05 Piña</button>
      <button onclick="goToSlide(6)" id="nav-btn-6" class="px-2.5 py-1 rounded text-cts-slate hover:text-cts-black transition">06 Mango</button>
      <button onclick="goToSlide(7)" id="nav-btn-7" class="px-2.5 py-1 rounded text-cts-slate hover:text-cts-black transition">07 Cuotas y Estrategia</button>
    </div>

    <!-- Right Navigation Controls -->
    <div class="flex items-center space-x-2">
      <button onclick="prevSlide()" class="p-1.5 rounded-md border border-cts-border text-cts-slate hover:bg-cts-canvas transition" title="Anterior (←)">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      </button>
      <span class="font-mono text-xs font-semibold px-2 text-cts-slate">
        <span id="slide-num-current" class="text-cts-red font-bold">01</span> / <span id="slide-num-total">07</span>
      </span>
      <button onclick="nextSlide()" class="p-1.5 rounded-md border border-cts-border text-cts-slate hover:bg-cts-canvas transition" title="Siguiente (→)">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      </button>
      <button onclick="window.print()" class="hidden md:inline-flex items-center space-x-1.5 text-xs font-semibold px-2.5 py-1.5 rounded-md bg-cts-black text-white hover:bg-cts-red transition">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
        <span>Imprimir</span>
      </button>
      <a href="Informe_Exportacion_Frutas_Ecuador_APA7.pdf" target="_blank" download class="hidden sm:inline-flex items-center space-x-1.5 text-xs font-semibold px-3 py-1.5 rounded-md bg-cts-red text-white hover:bg-cts-red/90 transition shadow-sm" title="Descargar Informe Técnico de Mercado (PDF)">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
        <span>Descargar Informe</span>
      </a>
    </div>
  </header>

  <!-- ========================================================================= -->
  <!-- MAIN SLIDE CANVAS -->
  <!-- ========================================================================= -->
  <main class="flex-1 flex flex-col justify-center items-center p-3 lg:p-6 max-w-7xl w-full mx-auto">
    <div id="slide-canvas" class="slide-fade slide-show w-full bg-white border border-cts-border rounded-xl p-5 lg:p-7 shadow-sm min-h-[580px] flex flex-col justify-between">
      <!-- Dynamic slide rendering via JavaScript -->
    </div>
  </main>

  <!-- ========================================================================= -->
  <!-- SUBTLE CTS FOOTER -->
  <!-- ========================================================================= -->
  <footer class="no-print bg-white border-t border-cts-border px-6 lg:px-12 py-2.5 flex flex-col sm:flex-row items-center justify-between text-xs text-cts-slate">
    <div class="flex items-center space-x-3">
      <span class="w-1.5 h-1.5 rounded-full bg-cts-red"></span>
      <span><strong>CTS International Freight Forwarder</strong> • Plataforma de Inteligencia Comercial</span>
      <span class="hidden md:inline text-cts-muted">|</span>
      <span class="hidden md:inline">Auditoría: UN Comtrade, WITS Banco Mundial, MAG</span>
    </div>
    <div class="flex items-center space-x-2 mt-1 sm:mt-0 font-mono text-[11px] text-cts-muted">
      <span>Navegación: <kbd class="px-1.5 py-0.5 bg-cts-canvas rounded border border-cts-border text-cts-slate">←</kbd> <kbd class="px-1.5 py-0.5 bg-cts-canvas rounded border border-cts-border text-cts-slate">→</kbd></span>
    </div>
  </footer>

  <!-- ========================================================================= -->
  <!-- JAVASCRIPT: DATA ENGINE & INTERACTIVE CHARTS -->
  <!-- ========================================================================= -->
  <script>
    let activeCharts = {{}};

    function destroyCharts() {{
      Object.keys(activeCharts).forEach(key => {{
        if (activeCharts[key]) {{
          activeCharts[key].destroy();
          delete activeCharts[key];
        }}
      }});
    }}

    // DATA FOR SLIDE 2 PRICE MODIFIER BY FRUIT
    const PRICE_DATA_SETS = {{
      all: {{
        title: "Comparativa General de Todas las Frutas",
        avgPrice: "$4.23 (Pitahaya) / $1.01 (Mango) / $0.58 (Piña)",
        bestDest: "EAU ($19.47) • Reino Unido ($8.10) • Francia ($7.40)",
        marginBadge: "Alta Dispersión de Rentabilidad",
        labels: [
          'Pitahaya (Emiratos Árabes)',
          'Pitahaya (Reino Unido)',
          'Pitahaya (Francia)',
          'Pitahaya (España)',
          'Pitahaya (Canadá)',
          'Pitahaya (Estados Unidos)',
          'Mango (Países Bajos)',
          'Mango (España)',
          'Mango (Estados Unidos)',
          'Piña (Chile)',
          'Piña (Estados Unidos)',
          'Piña (Países Bajos)'
        ],
        prices: [19.47, 8.10, 7.40, 6.61, 6.25, 4.30, 3.03, 2.07, 1.01, 0.58, 0.58, 0.52],
        colors: [
          '#CD0A33', '#CD0A33', '#CD0A33', '#CD0A33', '#CD0A33', '#CD0A33',
          '#111827', '#111827', '#9CA3AF',
          '#4B5563', '#4B5563', '#4B5563'
        ]
      }},
      pitahaya: {{
        title: "Pitahaya / Frutas Exóticas (HS 081090)",
        avgPrice: "$4.23 / kg (Ponderado Nacional MAG)",
        bestDest: "Emiratos Árabes: $19.47/kg • Reino Unido: $8.10/kg",
        marginBadge: "Margen Bruto: 45% – 60%",
        labels: [
          'Emiratos Árabes Unidos',
          'Reino Unido',
          'Francia',
          'España (Líder 42.7%)',
          'Canadá',
          'Singapur',
          'Países Bajos',
          'Estados Unidos (#1 Comprador)',
          'Hong Kong',
          'Colombia (Fronterizo)'
        ],
        prices: [19.47, 8.10, 7.40, 6.61, 6.25, 5.56, 4.96, 4.30, 7.42, 0.38],
        colors: [
          '#CD0A33', '#111827', '#111827', '#CD0A33', '#111827', '#4B5563', '#4B5563', '#CD0A33', '#111827', '#9CA3AF'
        ]
      }},
      pina: {{
        title: "Piña Golden MD2 (HS 080430)",
        avgPrice: "$0.58 / kg ($11.60 por caja de 20kg)",
        bestDest: "Rusia ($0.90/kg) • Bélgica ($0.69/kg) • Francia ($0.66/kg)",
        marginBadge: "Margen Bruto: 18% – 22%",
        labels: [
          'Rusia',
          'Bélgica',
          'Francia',
          'España',
          'Argentina',
          'Nueva Zelanda',
          'Uruguay',
          'Chile (Monopolio 93.3%)',
          'Estados Unidos',
          'Países Bajos (Hub)'
        ],
        prices: [0.90, 0.69, 0.66, 0.64, 0.64, 0.62, 0.61, 0.58, 0.58, 0.52],
        colors: [
          '#111827', '#111827', '#111827', '#111827', '#4B5563', '#4B5563', '#4B5563', '#CD0A33', '#CD0A33', '#111827'
        ]
      }},
      mango: {{
        title: "Mango Fresco (HS 080450)",
        avgPrice: "$1.01 en EE.UU. vs. $3.03 en Países Bajos",
        bestDest: "Países Bajos ($3.03/kg) • Francia ($2.77/kg) • España ($2.07/kg)",
        marginBadge: "Arbitraje: +200% Retorno en Europa",
        labels: [
          'Países Bajos (Arbitraje)',
          'Francia',
          'Bélgica',
          'España',
          'Costa Rica',
          'Honduras',
          'Canadá',
          'Guatemala',
          'Estados Unidos (94.2% Volumen)',
          'Colombia (Descarte)'
        ],
        prices: [3.03, 2.77, 2.34, 2.07, 1.86, 1.23, 1.22, 1.11, 1.01, 0.11],
        colors: [
          '#CD0A33', '#CD0A33', '#111827', '#CD0A33', '#4B5563', '#4B5563', '#4B5563', '#4B5563', '#9CA3AF', '#CBD5E1'
        ]
      }}
    }};

    function updatePriceChart(fruitKey) {{
      const dataSet = PRICE_DATA_SETS[fruitKey] || PRICE_DATA_SETS['all'];
      
      // Update UI Labels
      document.getElementById('s2-metric-title').innerText = dataSet.title;
      document.getElementById('s2-metric-avg').innerText = dataSet.avgPrice;
      document.getElementById('s2-metric-best').innerText = dataSet.bestDest;
      document.getElementById('s2-metric-badge').innerText = dataSet.marginBadge;

      const ctx = document.getElementById('chart-s2-prices');
      if (!ctx) return;

      if (activeCharts['s2']) {{
        activeCharts['s2'].destroy();
      }}

      activeCharts['s2'] = new Chart(ctx, {{
        type: 'bar',
        indexAxis: 'y',
        data: {{
          labels: dataSet.labels,
          datasets: [{{
            label: 'Precio FOB (USD / kg)',
            data: dataSet.prices,
            backgroundColor: dataSet.colors,
            borderRadius: 3
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{ callbacks: {{ label: (c) => ` $${{c.raw.toFixed(2)}} USD / kg` }} }}
          }},
          scales: {{
            x: {{ grid: {{ color: 'rgba(0,0,0,0.04)' }}, title: {{ display: true, text: 'USD por Kilogramo FOB', font: {{ size: 10 }} }} }},
            y: {{ ticks: {{ font: {{ size: 10, family: 'Inter' }} }} }}
          }}
        }}
      }});
    }}

    const SLIDES = [
      // -----------------------------------------------------------------------
      // SLIDE 1: PORTADA EJECUTIVA CTS
      // -----------------------------------------------------------------------
      {{
        id: 1,
        render: () => `
          <div class="space-y-6">
            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-cts-border pb-5">
              <div class="space-y-1">
                <div class="flex items-center space-x-2">
                  <span class="text-xs font-mono font-bold tracking-widest uppercase text-cts-red">CTS Presentación Gerencial</span>
                  <span class="text-xs text-cts-muted font-mono">• Comercio Exterior</span>
                </div>
                <h1 class="text-2xl lg:text-4xl font-extrabold text-cts-black tracking-tight">
                  Exportaciones de Frutas Ecuatorianas:<br>
                  <span class="text-cts-slate">Rentabilidad Unitaria y Mercados de Destino</span>
                </h1>
              </div>

              <!-- Top Macro Badge -->
              <div class="bg-cts-canvas border border-cts-border p-3.5 rounded-lg text-right font-mono text-xs">
                <div class="text-cts-slate">Canasta Frutal No Tradicional 2025</div>
                <div class="text-2xl font-black text-cts-black">$480.22M USD</div>
                <div class="text-[11px] text-cts-red font-semibold">Pitahaya • Piña • Mango</div>
              </div>
            </div>

            <!-- Visual Chart 1: Volume vs Value -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
              <div class="lg:col-span-2 chart-box" style="height: 280px;">
                <div class="flex justify-between items-center mb-1 text-xs">
                  <span class="font-bold text-cts-black uppercase tracking-wide">Valor Exportado vs. Tonelaje Físico (2025)</span>
                  <span class="font-mono text-[10px] text-cts-slate">Barras: Millones USD | Puntos: Miles TM</span>
                </div>
                <canvas id="chart-s1-macro"></canvas>
              </div>

              <!-- 3 Pillar Summaries -->
              <div class="space-y-3 font-sans text-xs">
                <div class="p-3.5 rounded-lg border border-cts-border bg-white border-l-4 border-l-cts-red shadow-sm">
                  <div class="flex justify-between items-center">
                    <strong class="text-cts-black text-sm">Pitahaya: La Más Rentable</strong>
                    <span class="font-mono text-xs font-bold text-cts-red">$4.23/kg</span>
                  </div>
                  <p class="text-[11px] text-cts-slate mt-1">
                    Aporta el <strong>71% del valor total</strong> con solo el 24% del volumen físico. Precio líder en nichos de hasta $19.47/kg.
                  </p>
                </div>

                <div class="p-3.5 rounded-lg border border-cts-border bg-white border-l-4 border-l-cts-black shadow-sm">
                  <div class="flex justify-between items-center">
                    <strong class="text-cts-black text-sm">Piña: Motor de Volumen</strong>
                    <span class="font-mono text-xs font-bold text-cts-black">140,448 TM</span>
                  </div>
                  <p class="text-[11px] text-cts-slate mt-1">
                    Representa el <strong>53% del tonelaje total</strong>. Negocio defensivo de escala y monopolio del 93.3% en Chile.
                  </p>
                </div>

                <div class="p-3.5 rounded-lg border border-cts-border bg-white border-l-4 border-l-cts-muted shadow-sm">
                  <div class="flex justify-between items-center">
                    <strong class="text-cts-black text-sm">Mango: Arbitraje hacia Europa</strong>
                    <span class="font-mono text-xs font-bold text-cts-red">3x Retorno</span>
                  </div>
                  <p class="text-[11px] text-cts-slate mt-1">
                    Holanda paga <strong>$3.03/kg</strong> frente a solo $1.01/kg en EE.UU., ofreciendo una vía para desconcentrar el 94% de ventas.
                  </p>
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between text-xs font-mono text-cts-muted pt-3 border-t border-cts-border">
              <span>UN Comtrade Oficial (Reporter 218) • MAG Octubre 2026 • Banco Mundial WITS</span>
              <span class="text-cts-red font-semibold">Usa las flechas para avanzar →</span>
            </div>
          </div>
        `,
        init: () => {{
          const ctx = document.getElementById('chart-s1-macro');
          if (!ctx) return;
          activeCharts['s1'] = new Chart(ctx, {{
            type: 'bar',
            data: {{
              labels: ['Pitahaya (Exóticas)', 'Piña Golden MD2', 'Mango Fresco'],
              datasets: [
                {{
                  label: 'Valor Exportado (Millones USD)',
                  data: [341.98, 81.11, 57.13],
                  backgroundColor: ['#CD0A33', '#111827', '#4B5563'],
                  borderRadius: 3,
                  yAxisID: 'y'
                }},
                {{
                  label: 'Volumen (Miles TM)',
                  data: [64.50, 140.45, 59.32],
                  backgroundColor: '#E5E7EB',
                  borderColor: '#9CA3AF',
                  borderWidth: 1,
                  borderRadius: 3,
                  yAxisID: 'y1'
                }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 11, family: 'Inter' }} }} }},
                tooltip: {{
                  callbacks: {{
                    label: (c) => c.datasetIndex === 0 ? ` Valor FOB: $${{c.raw.toFixed(1)}}M USD` : ` Volumen: ${{c.raw.toFixed(1)}}K Toneladas`
                  }}
                }}
              }},
              scales: {{
                y: {{ type: 'linear', position: 'left', grid: {{ color: 'rgba(0,0,0,0.04)' }}, title: {{ display: true, text: 'Millones USD', font: {{ size: 10 }} }} }},
                y1: {{ type: 'linear', position: 'right', grid: {{ display: false }}, title: {{ display: true, text: 'Miles TM', font: {{ size: 10 }} }} }},
                x: {{ ticks: {{ font: {{ weight: '600', size: 11 }} }} }}
              }}
            }}
          }});
        }}
      }},

      // -----------------------------------------------------------------------
      // SLIDE 2: PRECIOS Y MARGEN CON SELECTOR DE LISTA POR FRUTA
      // -----------------------------------------------------------------------
      {{
        id: 2,
        render: () => `
          <div class="space-y-5">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3 border-b border-cts-border pb-3">
              <div>
                <span class="text-xs font-mono font-bold uppercase text-cts-red">Pregunta 1 • Rentabilidad por Kilogramo</span>
                <h2 class="text-2xl font-bold text-cts-black tracking-tight">Precios FOB (USD / kg) y Márgenes por Mercado</h2>
              </div>
              
              <!-- FRUIT DROPDOWN SELECTOR REQUESTED BY USER -->
              <div class="flex items-center space-x-2">
                <label for="fruit-price-select" class="text-xs font-bold text-cts-slate uppercase font-mono">Seleccionar Fruta:</label>
                <select id="fruit-price-select" onchange="updatePriceChart(this.value)" class="bg-white border-2 border-cts-red text-cts-black rounded-lg px-3 py-1.5 text-xs font-bold focus:outline-none focus:ring-1 focus:ring-cts-red cursor-pointer shadow-sm">
                  <option value="all" selected>Todas las Frutas (Comparativa General)</option>
                  <option value="pitahaya">Pitahaya (HS 081090) — Mayor Rentabilidad</option>
                  <option value="pina">Piña Golden MD2 (HS 080430) — Escala</option>
                  <option value="mango">Mango Fresco (HS 080450) — Arbitraje</option>
                </select>
              </div>
            </div>

            <!-- Dynamic Summary Badges updated by Selector -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
              <div class="p-3 bg-white border border-cts-border rounded-lg border-l-4 border-l-cts-red shadow-sm">
                <span class="text-cts-slate text-[10px] uppercase font-bold">Vista Actual:</span>
                <div id="s2-metric-title" class="text-xs font-bold text-cts-black mt-0.5 truncate">Comparativa General de Todas las Frutas</div>
                <div id="s2-metric-badge" class="text-[11px] font-bold text-cts-red mt-1">Alta Dispersión de Rentabilidad</div>
              </div>

              <div class="p-3 bg-white border border-cts-border rounded-lg border-l-4 border-l-cts-black shadow-sm">
                <span class="text-cts-slate text-[10px] uppercase font-bold">Precio Promedio de Retorno:</span>
                <div id="s2-metric-avg" class="text-xs font-bold text-cts-black mt-0.5">$4.23 (Pitahaya) / $1.01 (Mango) / $0.58 (Piña)</div>
                <div class="text-[11px] text-cts-slate mt-1">Valores FOB Oficiales 2025</div>
              </div>

              <div class="p-3 bg-white border border-cts-border rounded-lg border-l-4 border-l-cts-muted shadow-sm">
                <span class="text-cts-slate text-[10px] uppercase font-bold">Mejores Mercados Pagadores:</span>
                <div id="s2-metric-best" class="text-xs font-bold text-cts-black mt-0.5 truncate">EAU ($19.47) • Reino Unido ($8.10) • Francia ($7.40)</div>
                <div class="text-[11px] text-emerald-700 font-bold mt-1">Europa paga hasta 3x vs EE.UU.</div>
              </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
              <!-- Visual Chart: Modified in real-time by dropdown selector -->
              <div class="lg:col-span-2 chart-box" style="height: 310px;">
                <canvas id="chart-s2-prices"></canvas>
              </div>

              <!-- Static/Dynamic Key Analytical Insights -->
              <div class="space-y-3 text-xs">
                <div class="p-3 bg-cts-canvas rounded border border-cts-border text-xs text-cts-slate leading-relaxed">
                  <strong class="text-cts-black block mb-1">Impacto de Rentabilidad por Contenedor (20 TM):</strong>
                  <ul class="space-y-1.5 font-mono text-[11px]">
                    <li class="flex justify-between border-b border-cts-border/50 pb-1"><span>Pitahaya a España:</span><strong class="text-cts-red">$132,200 USD</strong></li>
                    <li class="flex justify-between border-b border-cts-border/50 pb-1"><span>Mango a Países Bajos:</span><strong class="text-cts-black">$60,600 USD</strong></li>
                    <li class="flex justify-between border-b border-cts-border/50 pb-1"><span>Mango a EE.UU.:</span><strong class="text-cts-slate">$20,200 USD</strong></li>
                    <li class="flex justify-between"><span>Piña Golden a Chile/EE.UU.:</span><strong class="text-cts-slate">$11,600 USD</strong></li>
                  </ul>
                </div>

                <div class="p-3 bg-cts-redLight rounded border border-cts-red/20 text-xs text-cts-black">
                  <strong class="text-cts-red font-bold">Diagnóstico:</strong> Selecciona una fruta en el selector superior para analizar la curva detallada de precios por país comprador.
                </div>
              </div>
            </div>
          </div>
        `,
        init: () => {{
          updatePriceChart('all');
        }}
      }},

      // -----------------------------------------------------------------------
      // SLIDE 3: DESTINOS DE EXPORTACIÓN (STACKED BARS)
      // -----------------------------------------------------------------------
      {{
        id: 3,
        render: () => `
          <div class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-cts-border pb-3">
              <div>
                <span class="text-xs font-mono font-bold uppercase text-cts-red">Pregunta 2 • Concentración Geográfica</span>
                <h2 class="text-2xl font-bold text-cts-black tracking-tight">¿A qué Países Exportamos Mayoritariamente?</h2>
              </div>
              <span class="text-xs font-mono text-cts-slate">Cierre 2025 • FOB Millones USD</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
              <div class="lg:col-span-2 chart-box" style="height: 310px;">
                <div class="flex justify-between items-center mb-1">
                  <span class="text-xs font-bold text-cts-black uppercase tracking-wide">Top 7 Mercados y Mezcla Exportadora</span>
                  <span class="text-[10px] font-mono text-cts-slate">Rojo: Pitahaya | Negro: Mango | Gris: Piña</span>
                </div>
                <canvas id="chart-s3-destinations"></canvas>
              </div>

              <div class="space-y-3 text-xs">
                <div class="p-3.5 bg-white rounded-lg border border-cts-border border-l-4 border-l-cts-red shadow-sm">
                  <span class="font-bold text-cts-black block text-sm">Estados Unidos: 64.1%</span>
                  <p class="text-cts-slate mt-1">$307.9M USD. Principal comprador de las tres frutas, pero con márgenes unitarios menores que Europa.</p>
                </div>

                <div class="p-3.5 bg-white rounded-lg border border-cts-border border-l-4 border-l-cts-black shadow-sm">
                  <span class="font-bold text-cts-black block text-sm">Unión Europea: 20.4%</span>
                  <p class="text-cts-slate mt-1">España ($53.7M) y Holanda ($34.5M) absorben exóticas y piña con <strong>arancel 0%</strong> y los precios más altos.</p>
                </div>

                <div class="p-3.5 bg-white rounded-lg border border-cts-border border-l-4 border-l-cts-muted shadow-sm">
                  <span class="font-bold text-cts-black block text-sm">Chile: 3.0% (Monopolio)</span>
                  <p class="text-cts-slate mt-1">$14.5M USD en piña fresca. Ecuador suministra el <strong>93.3%</strong> del mercado chileno sin cruzar el Canal.</p>
                </div>
              </div>
            </div>
          </div>
        `,
        init: () => {{
          const ctx = document.getElementById('chart-s3-destinations');
          if (!ctx) return;
          activeCharts['s3'] = new Chart(ctx, {{
            type: 'bar',
            data: {{
              labels: ['Estados Unidos', 'España', 'Países Bajos', 'Canadá', 'Chile', 'Argentina', 'Hong Kong'],
              datasets: [
                {{ label: 'Pitahaya / Exóticas', data: [227.87, 48.72, 13.34, 17.40, 0.0, 0.0, 6.60], backgroundColor: '#CD0A33', borderRadius: 2 }},
                {{ label: 'Mango Fresco', data: [53.83, 0.33, 0.48, 1.21, 0.0, 0.0, 0.0], backgroundColor: '#111827', borderRadius: 2 }},
                {{ label: 'Piña Golden', data: [26.27, 4.66, 20.66, 0.0, 14.48, 6.31, 0.0], backgroundColor: '#9CA3AF', borderRadius: 2 }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 11, family: 'Inter' }} }} }},
                tooltip: {{ callbacks: {{ label: (c) => ` ${{c.dataset.label}}: $${{c.raw.toFixed(2)}}M USD` }} }}
              }},
              scales: {{
                x: {{ stacked: true, grid: {{ display: false }} }},
                y: {{ stacked: true, grid: {{ color: 'rgba(0,0,0,0.04)' }}, title: {{ display: true, text: 'Millones USD', font: {{ size: 10 }} }} }}
              }}
            }}
          }});
        }}
      }},

      // -----------------------------------------------------------------------
      // SLIDE 4: PITAHAYA VISUAL FOCUS (CURVA Y DONUT)
      // -----------------------------------------------------------------------
      {{
        id: 4,
        render: () => `
          <div class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-cts-border pb-3">
              <div>
                <span class="text-xs font-mono font-bold uppercase text-cts-red">Fruta Estrella • HS 081090</span>
                <h2 class="text-2xl font-bold text-cts-black tracking-tight">Pitahaya: Crecimiento Exponencial (+55% CAGR) y Rentabilidad en Destinos Clave</h2>
              </div>
              <span class="text-xs font-mono text-cts-slate">Crecimiento 2015–2025: +55.6% Anual</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div class="chart-box" style="height: 290px;">
                <div class="flex justify-between items-center mb-1">
                  <span class="text-xs font-bold text-cts-black uppercase">Evolución Histórica de Ventas (2015–2025)</span>
                  <span class="text-[10px] font-mono text-cts-slate">MAG / Comtrade</span>
                </div>
                <canvas id="chart-s4-history"></canvas>
              </div>

              <div class="chart-box" style="height: 290px;">
                <div class="flex justify-between items-center mb-1">
                  <span class="text-xs font-bold text-cts-black uppercase">Destinos de Exportación de Ecuador (2025)</span>
                  <span class="text-[10px] font-mono text-cts-red font-bold">EE.UU. #1 Volumen | España #1 Cuota</span>
                </div>
                <canvas id="chart-s4-destinations"></canvas>
              </div>
            </div>

            <!-- Clarifying Dual-Perspective Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
              <div class="p-2.5 bg-cts-canvas rounded border border-cts-border text-cts-slate">
                <span class="text-[10px] uppercase font-bold text-cts-black block">Volumen País (MAG 2025):</span>
                <span class="font-bold text-cts-black text-xs">$272.76M USD</span> (64,500 TM)
                <div class="text-[10px] text-cts-slate mt-0.5">Avance Ene-Jul 2026: $136.77M</div>
              </div>

              <div class="p-2.5 bg-white rounded border border-cts-border border-l-4 border-l-cts-red text-cts-slate">
                <span class="text-[10px] uppercase font-bold text-cts-red block">1° Destino en Volumen (EE.UU.):</span>
                <span class="font-bold text-cts-black text-xs">66.6% de ventas</span> ($227.9M USD)
                <div class="text-[10px] text-cts-slate mt-0.5">Precio FOB: $4.30 / kg</div>
              </div>

              <div class="p-2.5 bg-white rounded border border-cts-border border-l-4 border-l-cts-black text-cts-slate">
                <span class="text-[10px] uppercase font-bold text-cts-black block">2° Destino y Líder en España:</span>
                <span class="font-bold text-cts-red text-xs">42.7% Cuota en España (#1 Proveedor)</span>
                <div class="text-[10px] text-cts-slate mt-0.5">14.3% de ventas ($48.7M) a $6.61/kg</div>
              </div>
            </div>
          </div>
        `,
        init: () => {{
          const ctx1 = document.getElementById('chart-s4-history');
          if (ctx1) {{
            activeCharts['s4_h'] = new Chart(ctx1, {{
              type: 'line',
              data: {{
                labels: ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'],
                datasets: [{{
                  label: 'FOB Millones USD (MAG)',
                  data: [3.27, 6.95, 12.88, 32.00, 44.05, 66.43, 91.17, 99.36, 171.74, 207.04, 272.76],
                  borderColor: '#CD0A33',
                  backgroundColor: 'rgba(205, 10, 51, 0.05)',
                  borderWidth: 2.5,
                  pointBackgroundColor: '#CD0A33',
                  pointRadius: 3,
                  fill: true,
                  tension: 0.25
                }}]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ display: false }},
                  tooltip: {{ callbacks: {{ label: (c) => ` $${{c.raw.toFixed(2)}}M USD` }} }}
                }},
                scales: {{
                  y: {{ grid: {{ color: 'rgba(0,0,0,0.04)' }}, title: {{ display: true, text: 'Millones USD', font: {{ size: 10 }} }} }},
                  x: {{ grid: {{ display: false }} }}
                }}
              }}
            }});
          }}

          const ctx2 = document.getElementById('chart-s4-destinations');
          if (ctx2) {{
            activeCharts['s4_d'] = new Chart(ctx2, {{
              type: 'doughnut',
              data: {{
                labels: ['Estados Unidos', 'España', 'Canadá', 'Países Bajos', 'Francia', 'Hong Kong', 'Otros'],
                datasets: [{{
                  data: [66.6, 14.3, 5.1, 3.9, 3.1, 1.9, 5.1],
                  backgroundColor: ['#CD0A33', '#111827', '#4B5563', '#6B7280', '#9CA3AF', '#CBD5E1', '#E5E7EB'],
                  borderWidth: 1.5,
                  borderColor: '#FFFFFF'
                }}]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ position: 'right', labels: {{ boxWidth: 10, font: {{ size: 10, family: 'Inter' }} }} }},
                  tooltip: {{ callbacks: {{ label: (c) => ` ${{c.label}}: ${{c.raw}}%` }} }}
                }},
                cutout: '65%'
              }}
            }});
          }}
        }}
      }},

      // -----------------------------------------------------------------------
      // SLIDE 5: PINEAPPLE VISUAL FOCUS (CHILE MONOPOLY)
      // -----------------------------------------------------------------------
      {{
        id: 5,
        render: () => `
          <div class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-cts-border pb-3">
              <div>
                <span class="text-xs font-mono font-bold uppercase text-cts-red">Volumen y Escala • HS 080430</span>
                <h2 class="text-2xl font-bold text-cts-black tracking-tight">Piña Golden MD2: Monopolio en Chile y Cartera Global</h2>
              </div>
              <span class="text-xs font-mono text-cts-slate">Cierre 2025: $81.11M USD (140,448 TM)</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div class="chart-box" style="height: 290px;">
                <div class="text-xs font-bold text-cts-black uppercase mb-1">Participación en las Importaciones de Chile (2025)</div>
                <canvas id="chart-s5-chile"></canvas>
              </div>

              <div class="chart-box" style="height: 290px;">
                <div class="text-xs font-bold text-cts-black uppercase mb-1">Destinos de la Piña Ecuatoriana (HHI: 2,128 Balanceado)</div>
                <canvas id="chart-s5-destinations"></canvas>
              </div>
            </div>

            <div class="p-3 bg-cts-canvas rounded border border-cts-border text-xs font-mono flex flex-col sm:flex-row justify-between items-center text-cts-slate">
              <span><strong>Tránsito a Chile:</strong> 4 a 6 días directos por el Pacífico</span>
              <span><strong>Flete sin Canal:</strong> Gran ventaja en costo reefer</span>
              <span class="text-cts-black font-bold">Avance 2026: $58.79M (72% de 2025 en 7 meses)</span>
            </div>
          </div>
        `,
        init: () => {{
          const ctx1 = document.getElementById('chart-s5-chile');
          if (ctx1) {{
            activeCharts['s5_c'] = new Chart(ctx1, {{
              type: 'doughnut',
              data: {{
                labels: ['Ecuador ($14.25M CIF)', 'Costa Rica ($0.76M CIF)', 'Otros ($0.26M)'],
                datasets: [{{
                  data: [93.34, 4.96, 1.70],
                  backgroundColor: ['#CD0A33', '#111827', '#E5E7EB'],
                  borderWidth: 1.5,
                  borderColor: '#FFFFFF'
                }}]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 10, family: 'Inter' }} }} }},
                  tooltip: {{ callbacks: {{ label: (c) => ` ${{c.label}}: ${{c.raw}}%` }} }}
                }},
                cutout: '65%'
              }}
            }});
          }}

          const ctx2 = document.getElementById('chart-s5-destinations');
          if (ctx2) {{
            activeCharts['s5_d'] = new Chart(ctx2, {{
              type: 'bar',
              data: {{
                labels: ['EE.UU.', 'Países Bajos', 'Chile', 'Argentina', 'España', 'Nueva Zelanda', 'Bélgica'],
                datasets: [{{
                  label: 'FOB Millones USD',
                  data: [26.27, 20.66, 14.48, 6.31, 4.66, 1.83, 1.55],
                  backgroundColor: '#111827',
                  borderRadius: 3
                }}]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ display: false }},
                  tooltip: {{ callbacks: {{ label: (c) => ` $${{c.raw.toFixed(2)}}M USD` }} }}
                }},
                scales: {{
                  y: {{ grid: {{ color: 'rgba(0,0,0,0.04)' }}, title: {{ display: true, text: 'Millones USD', font: {{ size: 10 }} }} }},
                  x: {{ ticks: {{ font: {{ size: 10 }} }} }}
                }}
              }}
            }});
          }}
        }}
      }},

      // -----------------------------------------------------------------------
      // SLIDE 6: MANGO VISUAL FOCUS (PRECIOS Y ARBITRAJE)
      // -----------------------------------------------------------------------
      {{
        id: 6,
        render: () => `
          <div class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-cts-border pb-3">
              <div>
                <span class="text-xs font-mono font-bold uppercase text-cts-red">Oportunidad de Arbitraje • HS 080450</span>
                <h2 class="text-2xl font-bold text-cts-black tracking-tight">Mango: Concentración en EE.UU. vs. Valor en Europa</h2>
              </div>
              <span class="text-xs font-mono text-cts-slate">94.2% vendido en EE.UU. a $1.01/kg</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div class="chart-box" style="height: 290px;">
                <div class="text-xs font-bold text-cts-black uppercase mb-1">Precio FOB Obtenido por Kilo según Mercado de Destino</div>
                <canvas id="chart-s6-prices"></canvas>
              </div>

              <div class="chart-box" style="height: 290px;">
                <div class="text-xs font-bold text-cts-black uppercase mb-1">Dependencia de Comprador (HHI: 8,885 Puntos - Crítico)</div>
                <canvas id="chart-s6-concentration"></canvas>
              </div>
            </div>

            <div class="p-3 bg-cts-redLight rounded border border-cts-red/20 text-xs text-cts-black flex justify-between items-center font-mono">
              <span><strong>Ganancia por Arbitraje:</strong> Desviar 10% de la cosecha a Países Bajos generaría <strong>+$11.8M USD</strong> adicionales en margen.</span>
              <span class="font-bold text-cts-red">Arancel UE: 0.0%</span>
            </div>
          </div>
        `,
        init: () => {{
          const ctx1 = document.getElementById('chart-s6-prices');
          if (ctx1) {{
            activeCharts['s6_p'] = new Chart(ctx1, {{
              type: 'bar',
              data: {{
                labels: ['Países Bajos', 'Francia', 'Bélgica', 'España', 'Costa Rica', 'Canadá', 'Estados Unidos'],
                datasets: [{{
                  label: 'Precio FOB (USD / kg)',
                  data: [3.03, 2.77, 2.34, 2.07, 1.86, 1.22, 1.01],
                  backgroundColor: ['#CD0A33', '#CD0A33', '#111827', '#111827', '#4B5563', '#6B7280', '#9CA3AF'],
                  borderRadius: 3
                }}]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ display: false }},
                  tooltip: {{ callbacks: {{ label: (c) => ` Precio FOB: $${{c.raw.toFixed(2)}} / kg` }} }}
                }},
                scales: {{
                  y: {{ grid: {{ color: 'rgba(0,0,0,0.04)' }}, title: {{ display: true, text: 'USD por Kilogramo', font: {{ size: 10 }} }} }}
                }}
              }}
            }});
          }}

          const ctx2 = document.getElementById('chart-s6-concentration');
          if (ctx2) {{
            activeCharts['s6_c'] = new Chart(ctx2, {{
              type: 'doughnut',
              data: {{
                labels: ['Estados Unidos ($53.83M)', 'Canadá ($1.21M)', 'Países Bajos ($0.48M)', 'Otros 14 Países ($1.61M)'],
                datasets: [{{
                  data: [94.22, 2.11, 0.85, 2.82],
                  backgroundColor: ['#CD0A33', '#111827', '#4B5563', '#E5E7EB'],
                  borderWidth: 1.5,
                  borderColor: '#FFFFFF'
                }}]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 10, family: 'Inter' }} }} }},
                  tooltip: {{ callbacks: {{ label: (c) => ` ${{c.label}}: ${{c.raw}}%` }} }}
                }},
                cutout: '65%'
              }}
            }});
          }}
        }}
      }},

      // -----------------------------------------------------------------------
      // SLIDE 7: CUOTAS Y HOJA DE RUTA ESTRATÉGICA CTS
      // -----------------------------------------------------------------------
      {{
        id: 7,
        render: () => `
          <div class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-cts-border pb-3">
              <div>
                <span class="text-xs font-mono font-bold uppercase text-cts-red">Benchmarking y Hoja de Ruta</span>
                <h2 class="text-2xl font-bold text-cts-black tracking-tight">Cuota de Mercado de Ecuador y Plan de Acción Comercial</h2>
              </div>
              <span class="text-xs font-mono text-cts-slate">Penetración en Destinos Clave (%)</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div class="chart-box" style="height: 290px;">
                <div class="text-xs font-bold text-cts-black uppercase mb-1">Participación de Ecuador en las Importaciones del Mercado Destino (%)</div>
                <canvas id="chart-s7-shares"></canvas>
              </div>

              <div class="space-y-2.5 font-sans text-xs">
                <div class="p-3 bg-white rounded border border-cts-border border-l-4 border-l-cts-red shadow-sm">
                  <div class="flex justify-between items-center">
                    <strong class="text-cts-black">1. España (Pitahaya Directa)</strong>
                    <span class="font-mono text-cts-red font-bold">42.7% Cuota (#1 Proveedor)</span>
                  </div>
                  <p class="text-cts-slate mt-0.5">Ecuador suministra el 42.7% de toda la pitahaya importada por España. Oportunidad de consolidar contratos directos cobrando $6.61/kg sin intermediarios.</p>
                </div>

                <div class="p-3 bg-white rounded border border-cts-border border-l-4 border-l-cts-black shadow-sm">
                  <div class="flex justify-between items-center">
                    <strong class="text-cts-black">2. Países Bajos (Arbitraje de Mango)</strong>
                    <span class="font-mono text-cts-black font-bold">$3.03/kg</span>
                  </div>
                  <p class="text-cts-slate mt-0.5">Capturar fletes refrigerados de atmósfera controlada para triplicar el ingreso por kilo frente al mercado de Miami.</p>
                </div>

                <div class="p-3 bg-white rounded border border-cts-border border-l-4 border-l-cts-muted shadow-sm">
                  <div class="flex justify-between items-center">
                    <strong class="text-cts-black">3. Chile (Blindaje de Piña)</strong>
                    <span class="font-mono text-cts-black font-bold">93.3% Cuota</span>
                  </div>
                  <p class="text-cts-slate mt-0.5">Asegurar espacios de bodega en navieras del Pacífico e introducir pitahaya y mango libres de arancel (ACE 65).</p>
                </div>

                <div class="p-3 bg-white rounded border border-cts-border border-l-4 border-l-cts-red shadow-sm">
                  <div class="flex justify-between items-center">
                    <strong class="text-cts-black">4. Canadá (Exóticas Premium)</strong>
                    <span class="font-mono text-cts-red font-bold">$6.25/kg</span>
                  </div>
                  <p class="text-cts-slate mt-0.5">Mercado multicultural en expansión para pitahaya con protocolos fitosanitarios transparentes.</p>
                </div>
              </div>
            </div>

            <div class="p-3.5 bg-cts-black text-white rounded-lg flex flex-col sm:flex-row justify-between items-center text-xs font-mono">
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full bg-cts-red"></span>
                <span><strong>Conclusión:</strong> Pitahaya maximiza margen; Piña sostiene volumen; Mango a Europa ofrece la mayor ganancia inmediata.</span>
              </div>
              <button onclick="goToSlide(1)" class="mt-2 sm:mt-0 px-3 py-1 bg-white text-cts-black font-bold rounded hover:bg-cts-red hover:text-white transition">
                Volver al Inicio
              </button>
            </div>
          </div>
        `,
        init: () => {{
          const ctx = document.getElementById('chart-s7-shares');
          if (!ctx) return;
          activeCharts['s7_s'] = new Chart(ctx, {{
            type: 'bar',
            data: {{
              labels: [
                'Chile (Piña Fresca)',
                'España (Pitahaya / Exóticas)',
                'EE.UU. (Pitahaya / Exóticas)',
                'Canadá (Pitahaya / Exóticas)',
                'EE.UU. (Mango Fresco)',
                'Países Bajos (Pitahaya)',
                'Países Bajos (Piña Fresca)',
                'EE.UU. (Piña Fresca)',
                'Países Bajos (Mango Fresco)'
              ],
              datasets: [{{
                label: 'Cuota de Mercado de Ecuador (%)',
                data: [93.34, 42.73, 21.62, 7.82, 7.51, 4.63, 3.85, 3.05, 0.81],
                backgroundColor: [
                  '#CD0A33', '#CD0A33', '#111827', '#111827', '#4B5563',
                  '#6B7280', '#9CA3AF', '#CBD5E1', '#E5E7EB'
                ],
                borderRadius: 3
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ display: false }},
                tooltip: {{ callbacks: {{ label: (c) => ` Cuota de Ecuador: ${{c.raw}}%` }} }}
              }},
              scales: {{
                y: {{ grid: {{ color: 'rgba(0,0,0,0.04)' }}, title: {{ display: true, text: 'Participación (%)', font: {{ size: 10 }} }} }},
                x: {{ ticks: {{ font: {{ size: 9, family: 'Inter' }}, maxRotation: 40, minRotation: 40 }} }}
              }}
            }}
          }});
        }}
      }}
    ];

    let currentSlide = 1;
    const totalSlides = SLIDES.length;

    function renderSlide(slideId) {{
      if (slideId < 1 || slideId > totalSlides) return;
      currentSlide = slideId;

      destroyCharts();

      const canvas = document.getElementById('slide-canvas');
      canvas.classList.remove('slide-show');
      canvas.classList.add('slide-enter');

      setTimeout(() => {{
        const slide = SLIDES[currentSlide - 1];
        canvas.innerHTML = slide.render();
        canvas.classList.remove('slide-enter');
        canvas.classList.add('slide-show');

        document.getElementById('slide-num-current').innerText = String(currentSlide).padStart(2, '0');
        document.getElementById('slide-num-total').innerText = String(totalSlides).padStart(2, '0');

        for (let i = 1; i <= totalSlides; i++) {{
          const btn = document.getElementById(`nav-btn-${{i}}`);
          if (btn) {{
            if (i === currentSlide) {{
              btn.className = "px-2.5 py-1 rounded bg-white text-cts-red font-bold shadow-sm transition border-b-2 border-cts-red";
            }} else {{
              btn.className = "px-2.5 py-1 rounded text-cts-slate hover:text-cts-black transition";
            }}
          }}
        }}

        if (slide.init) {{
          slide.init();
        }}
      }}, 70);
    }}

    function nextSlide() {{
      if (currentSlide < totalSlides) {{
        renderSlide(currentSlide + 1);
      }}
    }}

    function prevSlide() {{
      if (currentSlide > 1) {{
        renderSlide(currentSlide - 1);
      }}
    }}

    function goToSlide(id) {{
      renderSlide(id);
    }}

    window.addEventListener('keydown', (e) => {{
      if (['SELECT', 'INPUT', 'TEXTAREA'].includes(e.target?.tagName)) {{
        return;
      }}
      if (e.key === 'ArrowRight' || e.key === ' ') {{
        if (e.key === ' ') e.preventDefault();
        nextSlide();
      }} else if (e.key === 'ArrowLeft') {{
        prevSlide();
      }}
    }});

    window.addEventListener('DOMContentLoaded', () => {{
      renderSlide(1);
    }});
  </script>
</body>
</html>
"""

with open('presentacion_frutas_ecuador/index.html', 'w', encoding='utf-8') as f:
  f.write(html_content)

print(
    'Successfully generated presentacion_frutas_ecuador/index.html with'
    ' Base64 logo and interactive Slide 2 fruit selector!'
)
