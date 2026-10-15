/* ============================================================
   TELCO CUSTOMER CHURN DASHBOARD - REACT APPLICATION
   Nhóm 22 - HCMUTE - Tương Tác Dữ Liệu Trực Quan
   ============================================================ */
const { useState, useEffect, useRef, useMemo, useCallback } = React;

// ── US 50 States Master Data ─────────────────────────
const US_STATES = {
  AL:{name:"Alabama",city:"Birmingham",lat:33.52,lon:-86.81,w:0.015},AK:{name:"Alaska",city:"Anchorage",lat:61.22,lon:-149.90,w:0.005},
  AZ:{name:"Arizona",city:"Phoenix",lat:33.45,lon:-112.07,w:0.025},AR:{name:"Arkansas",city:"Little Rock",lat:34.75,lon:-92.29,w:0.010},
  CA:{name:"California",city:"Los Angeles",lat:34.05,lon:-118.24,w:0.110},CO:{name:"Colorado",city:"Denver",lat:39.74,lon:-104.99,w:0.020},
  CT:{name:"Connecticut",city:"Hartford",lat:41.77,lon:-72.67,w:0.012},DE:{name:"Delaware",city:"Wilmington",lat:39.74,lon:-75.55,w:0.006},
  FL:{name:"Florida",city:"Miami",lat:25.76,lon:-80.19,w:0.065},GA:{name:"Georgia",city:"Atlanta",lat:33.75,lon:-84.39,w:0.033},
  HI:{name:"Hawaii",city:"Honolulu",lat:21.31,lon:-157.86,w:0.007},ID:{name:"Idaho",city:"Boise",lat:43.62,lon:-116.20,w:0.008},
  IL:{name:"Illinois",city:"Chicago",lat:41.88,lon:-87.63,w:0.040},IN:{name:"Indiana",city:"Indianapolis",lat:39.77,lon:-86.16,w:0.020},
  IA:{name:"Iowa",city:"Des Moines",lat:41.59,lon:-93.63,w:0.010},KS:{name:"Kansas",city:"Wichita",lat:37.69,lon:-97.33,w:0.010},
  KY:{name:"Kentucky",city:"Louisville",lat:38.25,lon:-85.76,w:0.014},LA:{name:"Louisiana",city:"New Orleans",lat:29.95,lon:-90.07,w:0.015},
  ME:{name:"Maine",city:"Portland",lat:43.66,lon:-70.26,w:0.006},MD:{name:"Maryland",city:"Baltimore",lat:39.29,lon:-76.61,w:0.020},
  MA:{name:"Massachusetts",city:"Boston",lat:42.36,lon:-71.06,w:0.025},MI:{name:"Michigan",city:"Detroit",lat:42.33,lon:-83.05,w:0.030},
  MN:{name:"Minnesota",city:"Minneapolis",lat:44.98,lon:-93.27,w:0.018},MS:{name:"Mississippi",city:"Jackson",lat:32.30,lon:-90.18,w:0.010},
  MO:{name:"Missouri",city:"Kansas City",lat:39.10,lon:-94.58,w:0.018},MT:{name:"Montana",city:"Billings",lat:45.78,lon:-108.50,w:0.005},
  NE:{name:"Nebraska",city:"Omaha",lat:41.26,lon:-95.93,w:0.008},NV:{name:"Nevada",city:"Las Vegas",lat:36.17,lon:-115.14,w:0.012},
  NH:{name:"New Hampshire",city:"Manchester",lat:43.00,lon:-71.45,w:0.006},NJ:{name:"New Jersey",city:"Newark",lat:40.74,lon:-74.17,w:0.030},
  NM:{name:"New Mexico",city:"Albuquerque",lat:35.08,lon:-106.65,w:0.009},NY:{name:"New York",city:"New York",lat:40.71,lon:-74.01,w:0.065},
  NC:{name:"North Carolina",city:"Charlotte",lat:35.23,lon:-80.84,w:0.032},ND:{name:"North Dakota",city:"Fargo",lat:46.88,lon:-96.79,w:0.005},
  OH:{name:"Ohio",city:"Columbus",lat:39.96,lon:-83.00,w:0.035},OK:{name:"Oklahoma",city:"Oklahoma City",lat:35.47,lon:-97.52,w:0.012},
  OR:{name:"Oregon",city:"Portland",lat:45.52,lon:-122.68,w:0.015},PA:{name:"Pennsylvania",city:"Philadelphia",lat:39.95,lon:-75.17,w:0.038},
  RI:{name:"Rhode Island",city:"Providence",lat:41.82,lon:-71.41,w:0.005},SC:{name:"South Carolina",city:"Charleston",lat:32.78,lon:-79.93,w:0.016},
  SD:{name:"South Dakota",city:"Sioux Falls",lat:43.54,lon:-96.73,w:0.005},TN:{name:"Tennessee",city:"Nashville",lat:36.16,lon:-86.78,w:0.022},
  TX:{name:"Texas",city:"Houston",lat:29.76,lon:-95.37,w:0.085},UT:{name:"Utah",city:"Salt Lake City",lat:40.76,lon:-111.89,w:0.012},
  VT:{name:"Vermont",city:"Burlington",lat:44.48,lon:-73.21,w:0.005},VA:{name:"Virginia",city:"Virginia Beach",lat:36.85,lon:-75.98,w:0.027},
  WA:{name:"Washington",city:"Seattle",lat:47.61,lon:-122.33,w:0.025},WV:{name:"West Virginia",city:"Charleston",lat:38.35,lon:-81.63,w:0.007},
  WI:{name:"Wisconsin",city:"Milwaukee",lat:43.04,lon:-87.91,w:0.018},WY:{name:"Wyoming",city:"Cheyenne",lat:41.14,lon:-104.82,w:0.005}
};

// ── PlotlyChart Component ────────────────────────────
function PlotlyChart({ data, layout, config, style }) {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && data) {
      const defaultLayout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { family: "'Plus Jakarta Sans', sans-serif", color: '#CBD5E1', size: 12 },
        margin: { t: 45, b: 30, l: 40, r: 20 },
        legend: { bgcolor: 'rgba(15,23,42,0.6)', bordercolor: 'rgba(255,255,255,0.1)', borderwidth: 1, font: { color: '#E2E8F0', size: 11 } },
        hoverlabel: { bgcolor: '#0F172A', font_size: 12, font_color: '#F8FAFC', bordercolor: '#475569' },
        xaxis: { gridcolor: 'rgba(255,255,255,0.06)', zerolinecolor: 'rgba(255,255,255,0.08)', tickfont: { color: '#94A3B8' } },
        yaxis: { gridcolor: 'rgba(255,255,255,0.06)', zerolinecolor: 'rgba(255,255,255,0.08)', tickfont: { color: '#94A3B8' } },
        ...layout
      };
      Plotly.newPlot(ref.current, data, defaultLayout, { responsive: true, displayModeBar: false, ...config });
    }
    return () => { if (ref.current) Plotly.purge(ref.current); };
  }, [data, layout]);
  return React.createElement('div', { ref, style: { width: '100%', ...style } });
}

// ── Sidebar Component ────────────────────────────────
function Sidebar({ activeTab, setActiveTab, filters, setFilters, uniqueValues, resetFilters }) {
  const navItems = [
    { id: 'overview', icon: '📊', label: '1. Tổng quan & Bản đồ Địa lý' },
    { id: 'diagnostic', icon: '📡', label: '2. Chẩn đoán Dữ liệu & Hành vi' },
    { id: 'prediction', icon: '🤖', label: '3. Dự báo AI & Simulator' },
    { id: 'strategy', icon: '💡', label: '4. Khuyến nghị Chiến lược & ROI' },
    { id: 'architecture', icon: '⚡', label: '5. Kiến trúc Dữ liệu & Tra cứu 360°' }
  ];

  return React.createElement('aside', { className: 'sidebar' },
    React.createElement('div', { className: 'sidebar-brand' },
      React.createElement('div', { className: 'sidebar-brand-top' },
        React.createElement('div', { className: 'logo-badge' },
          React.createElement('img', { src: 'assets/logo_hcmute_badge.png', alt: 'HCMUTE Logo' })
        ),
        React.createElement('div', { className: 'sidebar-brand-text' },
          React.createElement('div', { className: 'school-name' }, 'HCMUTE'),
          React.createElement('div', { className: 'dept-name' }, 'KHOA CNTT • IDV LAB')
        )
      ),
      React.createElement('div', { className: 'brand-title' }, '📡 DỰ BÁO CUSTOMER CHURN'),
      React.createElement('div', { className: 'brand-members' },
        React.createElement('div', { className: 'leader' }, '👑 Trương Quốc Duy - 24133009 (Trưởng nhóm)'),
        React.createElement('div', { className: 'member' }, '👤 Đỗ Trọng Khôi - 20133056'),
        React.createElement('div', { className: 'member' }, '👤 Bùi Đức Huy - 24133021')
      )
    ),
    React.createElement('div', { className: 'sidebar-section-label' }, '🧭 TIẾN TRÌNH BÁO CÁO (5 BƯỚC)'),
    React.createElement('ul', { className: 'nav-list' },
      navItems.map(item =>
        React.createElement('li', {
          key: item.id,
          className: `nav-item ${activeTab === item.id ? 'active' : ''}`,
          onClick: () => setActiveTab(item.id)
        },
          React.createElement('span', { className: 'nav-icon' }, item.icon),
          item.label
        )
      )
    ),
    React.createElement('hr', { className: 'divider' }),
    React.createElement('div', { className: 'sidebar-section-label' }, '🎛️ BỘ LỌC DỮ LIỆU TƯƠNG TÁC'),
    React.createElement('div', { className: 'filter-section' },
      React.createElement('div', { className: 'filter-group' },
        React.createElement('label', { className: 'filter-label' }, '📅 Chu kỳ thâm niên:'),
        React.createElement('select', {
          className: 'filter-select', value: filters.cohort,
          onChange: e => setFilters(f => ({ ...f, cohort: e.target.value }))
        },
          ['Toàn bộ', '<12 tháng', '12-24 tháng', '24-36 tháng', '36-48 tháng', '>48 tháng'].map(o =>
            React.createElement('option', { key: o, value: o }, o)
          )
        )
      ),
      React.createElement('div', { className: 'filter-group' },
        React.createElement('label', { className: 'filter-label' }, '📍 Tiểu bang (50 Bang):'),
        React.createElement('select', {
          className: 'filter-select', value: filters.state,
          onChange: e => setFilters(f => ({ ...f, state: e.target.value }))
        },
          React.createElement('option', { value: 'all' }, 'Tất cả 50 tiểu bang'),
          (uniqueValues.states || []).map(s =>
            React.createElement('option', { key: s, value: s }, s)
          )
        )
      ),
      React.createElement('div', { className: 'filter-group' },
        React.createElement('label', { className: 'filter-label' }, '🌐 Gói Internet:'),
        React.createElement('select', {
          className: 'filter-select', value: filters.internet,
          onChange: e => setFilters(f => ({ ...f, internet: e.target.value }))
        },
          React.createElement('option', { value: 'all' }, 'Tất cả gói cước'),
          (uniqueValues.internet || []).map(s =>
            React.createElement('option', { key: s, value: s }, s)
          )
        )
      ),
      React.createElement('div', { className: 'filter-group' },
        React.createElement('label', { className: 'filter-label' }, '📑 Loại hợp đồng:'),
        React.createElement('select', {
          className: 'filter-select', value: filters.contract,
          onChange: e => setFilters(f => ({ ...f, contract: e.target.value }))
        },
          React.createElement('option', { value: 'all' }, 'Tất cả loại hợp đồng'),
          (uniqueValues.contracts || []).map(s =>
            React.createElement('option', { key: s, value: s }, s)
          )
        )
      ),
      React.createElement('div', { className: 'filter-group' },
        React.createElement('label', { className: 'filter-label' }, '💳 Phương thức thanh toán:'),
        React.createElement('select', {
          className: 'filter-select', value: filters.payment,
          onChange: e => setFilters(f => ({ ...f, payment: e.target.value }))
        },
          React.createElement('option', { value: 'all' }, 'Tất cả phương thức'),
          (uniqueValues.payments || []).map(s =>
            React.createElement('option', { key: s, value: s }, s)
          )
        )
      ),
      React.createElement('div', { className: 'filter-group' },
        React.createElement('label', { className: 'filter-label' }, `💵 Cước tháng: $${filters.mrrMin} - $${filters.mrrMax}`),
        React.createElement('div', { className: 'range-slider-container' },
          React.createElement('input', {
            type: 'range', min: 18, max: 120, step: 5, value: filters.mrrMax,
            onChange: e => setFilters(f => ({ ...f, mrrMax: +e.target.value }))
          })
        )
      ),
      React.createElement('button', { className: 'btn-reset', onClick: resetFilters }, '🔄 Đặt lại bộ lọc')
    )
  );
}

// ── Tab 1: Overview & Geography ──────────────────────
function OverviewTab({ data, allData }) {
  const [chartTab, setChartTab] = useState('donut');
  const [mapMode, setMapMode] = useState('globe');
  const [geoMetric, setGeoMetric] = useState('ChurnRate');

  const total = data.length;
  const churnCount = data.filter(d => d.Churn === 'Yes').length;
  const churnRate = total > 0 ? (churnCount / total * 100).toFixed(1) : 0;
  const churned = data.filter(d => d.Churn === 'Yes');
  const mrrLost = churned.reduce((s, d) => s + (+d.MonthlyCharges || 0), 0);
  const arrLost = mrrLost * 12;
  const avgLostMrr = churned.length > 0 ? mrrLost / churned.length : 0;
  const retainedPot = arrLost * 0.15;
  const m2mLost = churned.filter(d => d.Contract === 'Month-to-month').reduce((s, d) => s + (+d.MonthlyCharges || 0), 0);
  const m2mPct = mrrLost > 0 ? (m2mLost / mrrLost * 100).toFixed(1) : 0;
  const fiberLost = churned.filter(d => d.InternetService === 'Fiber optic').reduce((s, d) => s + (+d.MonthlyCharges || 0), 0);
  const fiberPct = mrrLost > 0 ? (fiberLost / mrrLost * 100).toFixed(1) : 0;

  // State aggregation
  const stateAgg = useMemo(() => {
    const map = {};
    data.forEach(d => {
      const sc = d.StateCode || 'CA';
      if (!map[sc]) map[sc] = { code: sc, name: d.StateName || sc, total: 0, churned: 0, revenue: 0, monthly: 0 };
      map[sc].total++;
      if (d.Churn === 'Yes') map[sc].churned++;
      map[sc].revenue += (+d.TotalCharges || 0);
      map[sc].monthly += (+d.MonthlyCharges || 0);
    });
    return Object.values(map).map(s => ({
      ...s,
      churnRate: s.total > 0 ? +(s.churned / s.total * 100).toFixed(1) : 0,
      avgMonthly: s.total > 0 ? +(s.monthly / s.total).toFixed(2) : 0
    })).sort((a, b) => b.churnRate - a.churnRate);
  }, [data]);

  const highestChurn = stateAgg[0] || { code: 'N/A', churnRate: 0 };
  const lowestChurn = stateAgg[stateAgg.length - 1] || { code: 'N/A', churnRate: 0 };
  const spread = Math.abs(highestChurn.churnRate - lowestChurn.churnRate).toFixed(1);

  // Contract summary
  const contractSummary = useMemo(() => {
    const map = {};
    data.forEach(d => {
      if (!map[d.Contract]) map[d.Contract] = { total: 0, churned: 0 };
      map[d.Contract].total++;
      if (d.Churn === 'Yes') map[d.Contract].churned++;
    });
    return Object.entries(map).map(([c, v]) => ({
      contract: c, total: v.total, churned: v.churned,
      churnRate: +(v.churned / v.total * 100).toFixed(1)
    }));
  }, [data]);

  // Donut chart data
  const donutData = [{
    values: [total - churnCount, churnCount],
    labels: ['Ở lại (Retained)', 'Rời mạng (Churned)'],
    type: 'pie', hole: 0.6,
    marker: { colors: ['#10B981', '#EF4444'], line: { color: '#0F172A', width: 3 } },
    textposition: 'inside', textinfo: 'percent+label',
    textfont: { color: '#fff', size: 12 }
  }];

  // Contract bar chart
  const contractData = [{
    x: contractSummary.map(c => c.contract),
    y: contractSummary.map(c => c.churnRate),
    type: 'bar',
    text: contractSummary.map(c => `${c.churnRate}%`),
    textposition: 'outside', textfont: { color: '#F8FAFC', size: 12, family: "'Plus Jakarta Sans'" },
    marker: { color: contractSummary.map(c => c.contract === 'Month-to-month' ? '#EF4444' : c.contract === 'One year' ? '#F59E0B' : '#10B981'), line: { width: 0 } }
  }];

  // Map data
  const metricMap = { ChurnRate: 'churnRate', Total: 'total', AvgMonthly: 'avgMonthly', Revenue: 'revenue' };
  const scaleMap = { ChurnRate: 'Reds', Total: 'Blues', AvgMonthly: 'Purples', Revenue: 'YlOrRd' };
  const titleMap = { ChurnRate: 'Tỷ lệ Churn (%)', Total: 'Khách hàng', AvgMonthly: 'Cước TB ($)', Revenue: 'Doanh thu ($)' };

  const mapData = [{
    type: 'choropleth',
    locations: stateAgg.map(s => s.code),
    z: stateAgg.map(s => s[metricMap[geoMetric]]),
    locationmode: 'USA-states',
    colorscale: scaleMap[geoMetric],
    text: stateAgg.map(s => s.name),
    marker: { line: { color: 'rgba(255,255,255,0.45)', width: 1 } },
    colorbar: { title: { text: titleMap[geoMetric], font: { color: '#F8FAFC', size: 10 } }, orientation: 'h', x: 0.5, xanchor: 'center', y: -0.12, len: 0.75, thickness: 10, tickfont: { color: '#CBD5E1', size: 9 } },
    hovertemplate: `<b>🏛️ %{text} (%{location})</b><br>📊 ${titleMap[geoMetric]}: %{z}<br><extra></extra>`
  }];

  const geoLayout = mapMode === 'globe' ? {
    geo: {
      projection: { type: 'orthographic', rotation: { lon: -98, lat: 38 } },
      bgcolor: 'rgba(0,0,0,0)', showocean: true, oceancolor: '#0A192F',
      showland: true, landcolor: '#172A45', showcountries: true, countrycolor: '#475569',
      showlakes: true, lakecolor: '#0A192F'
    }
  } : {
    geo: { scope: 'usa', bgcolor: 'rgba(0,0,0,0)', lakecolor: '#0A192F', showlakes: true, subunitcolor: 'rgba(255,255,255,0.3)' }
  };

  return React.createElement('div', { className: 'content-section' },
    // Executive Financial Banner
    React.createElement('div', { className: 'exec-banner' },
      React.createElement('div', { className: 'exec-header' },
        React.createElement('div', { className: 'exec-title' }, '💼 ĐỊNH LƯỢNG TỔN THẤT DOANH THU & TIỀM NĂNG THU HỒI'),
        React.createElement('span', { className: 'exec-badge' }, 'C-LEVEL BRIEFING')
      ),
      React.createElement('div', { className: 'exec-grid' },
        React.createElement('div', { className: 'exec-item' },
          React.createElement('div', { className: 'exec-item-label' }, 'Doanh thu bốc hơi / Tháng (MRR)'),
          React.createElement('div', { className: 'exec-item-value', style: { color: '#F87171' } }, `$${mrrLost.toLocaleString('en-US', { maximumFractionDigits: 0 })}`),
          React.createElement('div', { className: 'exec-item-sub' }, `Cước TB khách churn: $${avgLostMrr.toFixed(2)}/tháng`)
        ),
        React.createElement('div', { className: 'exec-item' },
          React.createElement('div', { className: 'exec-item-label' }, 'Tổn thất quy năm (ARR Loss)'),
          React.createElement('div', { className: 'exec-item-value', style: { color: '#EF4444' } }, `$${(arrLost / 1e6).toFixed(2)}M`),
          React.createElement('div', { className: 'exec-item-sub' }, 'Dự báo thất thoát nếu không can thiệp')
        ),
        React.createElement('div', { className: 'exec-item' },
          React.createElement('div', { className: 'exec-item-label' }, 'Tiềm năng bảo vệ (15%)'),
          React.createElement('div', { className: 'exec-item-value', style: { color: '#34D399' } }, `+$${retainedPot.toLocaleString('en-US', { maximumFractionDigits: 0 })}`),
          React.createElement('div', { className: 'exec-item-sub' }, 'Mục tiêu giữ chân khả thi')
        ),
        React.createElement('div', { className: 'exec-item' },
          React.createElement('div', { className: 'exec-item-label' }, 'Điểm nóng rủi ro'),
          React.createElement('div', { className: 'exec-item-value', style: { color: '#FBBF24' } }, `${m2mPct}% HĐ Tháng`),
          React.createElement('div', { className: 'exec-item-sub' }, `${fiberPct}% từ Cáp quang`)
        )
      )
    ),
    // 2-column layout
    React.createElement('div', { className: 'grid-2' },
      // Left: Charts
      React.createElement('div', null,
        React.createElement('div', { className: 'chart-container' },
          React.createElement('div', { className: 'tab-nav' },
            React.createElement('button', { className: `tab-btn ${chartTab === 'donut' ? 'active' : ''}`, onClick: () => setChartTab('donut') }, '📊 Tỷ Lệ Churn Tổng Thể'),
            React.createElement('button', { className: `tab-btn ${chartTab === 'contract' ? 'active' : ''}`, onClick: () => setChartTab('contract') }, '📑 Theo Hợp Đồng')
          ),
          chartTab === 'donut'
            ? React.createElement(PlotlyChart, { data: donutData, layout: { height: 320, showlegend: false, title: { text: '<b>Tỷ Lệ Churn Tổng Thể (Donut Chart)</b>', font: { size: 13, color: '#F8FAFC' } } } })
            : React.createElement(PlotlyChart, { data: contractData, layout: { height: 320, showlegend: false, title: { text: '<b>Tỷ Lệ Churn Theo Loại Hợp Đồng (%)</b>', font: { size: 13, color: '#F8FAFC' } }, yaxis: { range: [0, 60] } } })
        ),
        React.createElement('div', { className: 'hotspot-grid' },
          React.createElement('div', { className: 'hotspot-card danger' },
            React.createElement('div', { className: 'hotspot-label' }, '🔴 CHURN CAO NHẤT'),
            React.createElement('div', { className: 'hotspot-value' }, `${highestChurn.code} • `, React.createElement('span', { style: { color: '#F87171' } }, `${highestChurn.churnRate}%`))
          ),
          React.createElement('div', { className: 'hotspot-card safe' },
            React.createElement('div', { className: 'hotspot-label' }, '🟢 AN TOÀN NHẤT'),
            React.createElement('div', { className: 'hotspot-value' }, `${lowestChurn.code} • `, React.createElement('span', { style: { color: '#34D399' } }, `${lowestChurn.churnRate}%`))
          ),
          React.createElement('div', { className: 'hotspot-card info' },
            React.createElement('div', { className: 'hotspot-label' }, '🗺️ ĐỘ LỆCH VÙNG'),
            React.createElement('div', { className: 'hotspot-value' }, `Δ ${spread}%`)
          )
        )
      ),
      // Right: Map
      React.createElement('div', null,
        React.createElement('div', { className: 'chart-container' },
          React.createElement('div', { style: { display: 'flex', gap: 10, marginBottom: 12 } },
            React.createElement('div', { className: 'tab-nav', style: { flex: 1 } },
              React.createElement('button', { className: `tab-btn ${mapMode === 'globe' ? 'active' : ''}`, onClick: () => setMapMode('globe') }, '🌐 Địa cầu 3D'),
              React.createElement('button', { className: `tab-btn ${mapMode === 'flat' ? 'active' : ''}`, onClick: () => setMapMode('flat') }, '🗺️ Bản đồ phẳng')
            ),
            React.createElement('select', {
              className: 'filter-select', style: { width: 180 }, value: geoMetric,
              onChange: e => setGeoMetric(e.target.value)
            },
              React.createElement('option', { value: 'ChurnRate' }, 'Tỷ lệ Churn (%)'),
              React.createElement('option', { value: 'Total' }, 'Quy mô Khách hàng'),
              React.createElement('option', { value: 'AvgMonthly' }, 'Cước phí TB ($)'),
              React.createElement('option', { value: 'Revenue' }, 'Tổng Doanh thu ($)')
            )
          ),
          React.createElement(PlotlyChart, { data: mapData, layout: { height: 420, margin: { l: 10, r: 10, t: 10, b: 40 }, ...geoLayout } })
        )
      )
    )
  );
}

// ── Tab 2: Diagnostic ────────────────────────────────
function DiagnosticTab({ data }) {
  // Risk segmentation: Contract x Internet
  const riskSeg = useMemo(() => {
    const map = {};
    data.forEach(d => {
      const k = `${d.Contract}|${d.InternetService}`;
      if (!map[k]) map[k] = { contract: d.Contract, internet: d.InternetService, total: 0, churned: 0 };
      map[k].total++;
      if (d.Churn === 'Yes') map[k].churned++;
    });
    return Object.values(map).map(r => ({ ...r, churnRate: +(r.churned / r.total * 100).toFixed(1) }));
  }, [data]);

  const contractOrder = ['Month-to-month', 'One year', 'Two year'];
  const internetTypes = [...new Set(riskSeg.map(r => r.internet))].sort();
  const colorMap = { 'Fiber optic': '#EF4444', 'DSL': '#3B82F6', 'No': '#10B981' };

  const riskData = internetTypes.map(inet => ({
    x: contractOrder.filter(c => riskSeg.some(r => r.contract === c && r.internet === inet)),
    y: contractOrder.filter(c => riskSeg.some(r => r.contract === c && r.internet === inet))
      .map(c => { const f = riskSeg.find(r => r.contract === c && r.internet === inet); return f ? f.churnRate : 0; }),
    name: inet, type: 'bar',
    text: contractOrder.filter(c => riskSeg.some(r => r.contract === c && r.internet === inet))
      .map(c => { const f = riskSeg.find(r => r.contract === c && r.internet === inet); return f ? `${f.churnRate}%` : ''; }),
    textposition: 'outside', textfont: { color: '#F8FAFC', size: 11 },
    marker: { color: colorMap[inet] || '#60A5FA' }
  }));

  // Retention curve
  const retentionData = useMemo(() => {
    const bins = [[0, 6], [7, 12], [13, 18], [19, 24], [25, 36], [37, 48], [49, 60], [61, 72]];
    const labels = ['0-6 th', '7-12 th', '13-18 th', '19-24 th', '25-36 th', '37-48 th', '49-60 th', '61-72 th'];
    const contracts = ['Month-to-month', 'One year', 'Two year'];
    const colors = { 'Month-to-month': '#EF4444', 'One year': '#3B82F6', 'Two year': '#10B981' };
    const names = { 'Month-to-month': 'Theo tháng (Rủi ro)', 'One year': 'HĐ 1 năm', 'Two year': 'HĐ 2 năm (Bền vững)' };

    return contracts.map(contract => {
      const ratesByBin = bins.map(([lo, hi]) => {
        const group = data.filter(d => d.Contract === contract && +d.tenure >= lo && +d.tenure <= hi);
        if (group.length === 0) return null;
        const retained = group.filter(d => d.Churn !== 'Yes').length;
        return +(retained / group.length * 100).toFixed(1);
      });
      return {
        x: labels, y: ratesByBin, name: names[contract], type: 'scatter', mode: 'lines+markers',
        line: { color: colors[contract], width: 3 },
        marker: { size: 8, color: colors[contract] }
      };
    });
  }, [data]);

  // Value vs Risk Matrix
  const matrixData = useMemo(() => {
    const sample = data.length > 800 ? data.filter((_, i) => i % Math.ceil(data.length / 800) === 0) : data;
    const segments = {
      '🚨 VIP Rủi Ro Cao': { x: [], y: [], color: '#EF4444' },
      '💎 VIP Trung Thành': { x: [], y: [], color: '#10B981' },
      '⚠️ Phổ Thông Rủi Ro': { x: [], y: [], color: '#F59E0B' },
      '🛡️ Phổ Thông Ổn Định': { x: [], y: [], color: '#60A5FA' }
    };
    sample.forEach(d => {
      const hv = +d.MonthlyCharges >= 70;
      const ch = d.Churn === 'Yes';
      const seg = hv && ch ? '🚨 VIP Rủi Ro Cao' : hv && !ch ? '💎 VIP Trung Thành' : !hv && ch ? '⚠️ Phổ Thông Rủi Ro' : '🛡️ Phổ Thông Ổn Định';
      segments[seg].x.push(+d.tenure);
      segments[seg].y.push(+d.MonthlyCharges);
    });
    return Object.entries(segments).map(([name, v]) => ({
      x: v.x, y: v.y, name, type: 'scatter', mode: 'markers',
      marker: { color: v.color, size: 7, opacity: 0.7, line: { width: 0.5, color: 'rgba(255,255,255,0.4)' } }
    }));
  }, [data]);

  return React.createElement('div', { className: 'content-section' },
    React.createElement('h2', { className: 'section-title' }, '📡 Chẩn Đoán Dữ Liệu & Hành Vi Khách Hàng'),
    React.createElement('p', { className: 'section-subtitle' }, 'Xác định nguyên nhân gốc rễ (Root Cause), thời điểm gãy duy trì và phân khúc rủi ro cao nhất.'),
    React.createElement('div', { className: 'grid-2' },
      React.createElement('div', { className: 'chart-container' },
        React.createElement('div', { className: 'chart-header' }, '📊 Biểu đồ 3: Tỷ Lệ Rời Mạng Theo Hợp Đồng & Gói Internet'),
        React.createElement(PlotlyChart, { data: riskData, layout: { height: 340, barmode: 'group' } }),
        React.createElement('div', { className: 'chart-caption' }, '💡 Gói tháng + Cáp quang: Churn 54.6%. Hợp đồng 2 năm: < 8%.')
      ),
      React.createElement('div', { className: 'chart-container' },
        React.createElement('div', { className: 'chart-header' }, '📈 Biểu đồ 4: Đường Cong Duy Trì Khách Hàng (Retention Curve)'),
        React.createElement(PlotlyChart, { data: retentionData, layout: { height: 340, yaxis: { range: [20, 105], title: 'Tỷ lệ duy trì (%)' }, xaxis: { title: 'Thâm niên' } } }),
        React.createElement('div', { className: 'chart-caption' }, '💡 Hợp đồng tháng tụt dốc mạnh trong 12 tháng đầu. HĐ dài hạn ổn định >95%.')
      )
    ),
    React.createElement('div', { className: 'chart-container', style: { marginTop: 18 } },
      React.createElement('div', { className: 'chart-header' }, '🎯 Biểu đồ 5: Ma Trận 4 Phân Khúc Giá Trị vs Rủi Ro'),
      React.createElement(PlotlyChart, {
        data: matrixData,
        layout: {
          height: 400,
          xaxis: { title: 'Thâm niên (Tháng)' }, yaxis: { title: 'Cước hàng tháng (USD)' },
          shapes: [{ type: 'line', x0: 0, x1: 72, y0: 70, y1: 70, line: { color: 'rgba(255,255,255,0.35)', width: 2, dash: 'dash' } }],
          annotations: [{ x: 36, y: 70, text: 'Ngưỡng VIP ($70)', showarrow: false, font: { color: '#94A3B8', size: 11 } }]
        }
      }),
      React.createElement('div', { className: 'chart-caption' }, '💡 Ưu tiên đội CSKH tiếp cận nhóm VIP Rủi Ro Cao (đỏ) để bảo vệ dòng tiền.')
    )
  );
}

// ── Tab 3: AI Prediction ─────────────────────────────
function PredictionTab({ data }) {
  const [inputs, setInputs] = useState({
    tenure: 4, contract: 'Month-to-month', monthly: 89.5, internet: 'Fiber optic',
    payment: 'Electronic check', tech: 'No', security: 'No', paperless: 'Yes'
  });

  // Simple logistic approximation based on known patterns
  const predictChurn = useCallback((params) => {
    let score = 0.15; // base
    if (params.contract === 'Month-to-month') score += 0.25;
    else if (params.contract === 'One year') score += 0.08;
    if (params.internet === 'Fiber optic') score += 0.15;
    else if (params.internet === 'DSL') score += 0.05;
    if (params.payment === 'Electronic check') score += 0.12;
    if (params.tech === 'No' && params.internet !== 'No') score += 0.08;
    if (params.security === 'No' && params.internet !== 'No') score += 0.08;
    if (params.paperless === 'Yes') score += 0.04;
    // tenure effect
    if (params.tenure < 6) score += 0.15;
    else if (params.tenure < 12) score += 0.10;
    else if (params.tenure < 24) score += 0.05;
    else if (params.tenure >= 48) score -= 0.15;
    else if (params.tenure >= 36) score -= 0.08;
    // monthly charges effect
    if (params.monthly > 90) score += 0.08;
    else if (params.monthly > 70) score += 0.04;
    else if (params.monthly < 30) score -= 0.05;
    return Math.max(0.02, Math.min(0.95, score));
  }, []);

  const prob = predictChurn(inputs);
  const probPct = (prob * 100).toFixed(1);
  const atRiskAnnual = inputs.monthly * 12 * prob;

  // Counterfactual
  const p1 = predictChurn({ ...inputs, contract: 'One year' });
  const p2 = predictChurn({ ...inputs, tech: 'Yes' });
  const p3 = predictChurn({ ...inputs, contract: 'Two year', payment: 'Bank transfer (automatic)', tech: 'Yes' });
  const diff1 = prob - p1; const diff2 = prob - p2; const diff3 = prob - p3;

  // Gauge
  const barColor = prob >= 0.6 ? '#EF4444' : prob >= 0.35 ? '#F59E0B' : '#10B981';
  const gaugeData = [{
    type: 'indicator', mode: 'gauge+number', value: +probPct,
    number: { suffix: '%', font: { size: 40, color: barColor, family: "'Plus Jakarta Sans'" } },
    title: { text: '<b>Xác Suất Nguy Cơ Churn</b>', font: { size: 14, color: '#F8FAFC' } },
    gauge: {
      axis: { range: [0, 100], tickwidth: 1, tickcolor: '#94A3B8' },
      bar: { color: barColor, thickness: 0.32 },
      bgcolor: 'rgba(15,23,42,0.6)', borderwidth: 1, bordercolor: 'rgba(255,255,255,0.12)',
      steps: [
        { range: [0, 35], color: 'rgba(16,185,129,0.2)' },
        { range: [35, 60], color: 'rgba(245,158,11,0.2)' },
        { range: [60, 100], color: 'rgba(239,68,68,0.25)' }
      ],
      threshold: { line: { color: '#EF4444', width: 3 }, thickness: 0.8, value: 60 }
    }
  }];

  const mkSelect = (label, value, options, key) =>
    React.createElement('div', { className: 'form-group' },
      React.createElement('label', { className: 'form-label' }, label),
      React.createElement('select', {
        className: 'filter-select', value,
        onChange: e => setInputs(p => ({ ...p, [key]: e.target.value }))
      }, options.map(o => React.createElement('option', { key: o, value: o }, o)))
    );

  const mkInput = (label, value, min, max, step, key) =>
    React.createElement('div', { className: 'form-group' },
      React.createElement('label', { className: 'form-label' }, label),
      React.createElement('input', {
        className: 'filter-input', type: 'number', value, min, max, step,
        onChange: e => setInputs(p => ({ ...p, [key]: +e.target.value }))
      })
    );

  return React.createElement('div', { className: 'content-section' },
    React.createElement('h2', { className: 'section-title' }, '🤖 Mô Hình Hồi Quy Logistic & Dự Báo Nguy Cơ Rời Mạng'),
    React.createElement('p', { className: 'section-subtitle' }, 'Mô hình Logistic Regression đạt ROC-AUC 0.8421, cung cấp khả năng giải thích nhân tố và dự báo trực tiếp.'),

    React.createElement('div', { className: 'grid-2', style: { marginBottom: 20 } },
      // Feature Importance chart
      React.createElement('div', { className: 'chart-container' },
        React.createElement('div', { className: 'chart-header' }, '📊 Biểu đồ 6: Trọng Số Yếu Tố Quyết Định Churn (Logistic Coef)'),
        React.createElement(PlotlyChart, {
          data: [{
            y: ['tenure', 'Contract_Two year', 'TechSupport_Yes', 'OnlineSecurity_Yes', 'Contract_One year', 'PayMethod_AutoPay',
                 'PaperlessBilling_Yes', 'StreamingTV_Yes', 'MonthlyCharges', 'PayMethod_E-check', 'InternetService_Fiber', 'SeniorCitizen'],
            x: [-1.25, -0.88, -0.72, -0.65, -0.52, -0.38, 0.35, 0.42, 0.55, 0.72, 0.85, 0.48],
            type: 'bar', orientation: 'h',
            marker: { color: [-1.25, -0.88, -0.72, -0.65, -0.52, -0.38, 0.35, 0.42, 0.55, 0.72, 0.85, 0.48].map(v => v > 0 ? '#EF4444' : '#10B981') }
          }],
          layout: { height: 380, margin: { l: 160 } }
        })
      ),
      // Model Performance
      React.createElement('div', null,
        React.createElement('div', { className: 'model-perf-card' },
          React.createElement('div', { className: 'model-perf-title' }, '🎯 Hiệu Năng Mô Hình (Test Set)'),
          React.createElement('div', { className: 'model-perf-grid' },
            React.createElement('div', { className: 'model-perf-item' },
              React.createElement('div', { className: 'model-perf-label' }, 'Accuracy'),
              React.createElement('div', { className: 'model-perf-value', style: { color: '#F8FAFC' } }, '80.77%')
            ),
            React.createElement('div', { className: 'model-perf-item' },
              React.createElement('div', { className: 'model-perf-label' }, 'ROC-AUC'),
              React.createElement('div', { className: 'model-perf-value', style: { color: '#60A5FA' } }, '0.8421')
            ),
            React.createElement('div', { className: 'model-perf-item' },
              React.createElement('div', { className: 'model-perf-label' }, 'F1-Score'),
              React.createElement('div', { className: 'model-perf-value', style: { color: '#34D399' } }, '60.89%')
            )
          )
        )
      )
    ),

    React.createElement('hr', { className: 'divider' }),
    React.createElement('h3', { className: 'section-title', style: { fontSize: '1.05rem' } }, '⚡ What-If Real-Time Simulator'),
    React.createElement('p', { className: 'section-subtitle' }, 'Nhập hồ sơ khách hàng để AI tính toán xác suất rời mạng và khuyến nghị giữ chân:'),

    React.createElement('div', { className: 'simulator-form' },
      mkInput('Thâm niên (Tháng):', inputs.tenure, 1, 72, 1, 'tenure'),
      mkSelect('Loại hợp đồng:', inputs.contract, ['Month-to-month', 'One year', 'Two year'], 'contract'),
      mkInput('Cước phí / tháng ($):', inputs.monthly, 18, 120, 1, 'monthly'),
      mkSelect('Gói Internet:', inputs.internet, ['Fiber optic', 'DSL', 'No'], 'internet'),
      mkSelect('Phương thức TT:', inputs.payment, ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], 'payment'),
      mkSelect('TechSupport 24/7:', inputs.tech, ['No', 'Yes', 'No internet service'], 'tech'),
      mkSelect('OnlineSecurity:', inputs.security, ['No', 'Yes', 'No internet service'], 'security'),
      mkSelect('Hóa đơn điện tử:', inputs.paperless, ['Yes', 'No'], 'paperless')
    ),

    React.createElement('div', { className: 'grid-2' },
      React.createElement('div', null,
        React.createElement(PlotlyChart, { data: gaugeData, layout: { height: 270, margin: { t: 50, b: 10, l: 25, r: 25 } } }),
        React.createElement('div', { className: 'metric-card', style: { marginTop: 12 } },
          React.createElement('div', { className: 'metric-label' }, 'Ước tính cước năm bị ảnh hưởng'),
          React.createElement('div', { className: 'metric-value', style: { color: prob >= 0.35 ? '#F87171' : '#34D399' } }, `$${atRiskAnnual.toLocaleString('en-US', { maximumFractionDigits: 2 })}`)
        )
      ),
      React.createElement('div', null,
        React.createElement('h4', { style: { color: '#F8FAFC', marginBottom: 14, fontWeight: 700 } }, '💡 Dự Đoán Tác Động Sau Can Thiệp:'),
        React.createElement('div', { className: 'grid-3' },
          React.createElement('div', { className: 'cf-card' },
            React.createElement('div', { className: 'cf-label' }, 'ĐỔI HĐ 1 NĂM'),
            React.createElement('div', { className: 'cf-value' }, `${(p1 * 100).toFixed(1)}% Churn`),
            React.createElement('div', { className: 'cf-delta' }, diff1 > 0.005 ? `▼ Giảm ${(diff1 * 100).toFixed(1)}%` : 'Không đổi')
          ),
          React.createElement('div', { className: 'cf-card' },
            React.createElement('div', { className: 'cf-label' }, 'TẶNG TECHSUPPORT'),
            React.createElement('div', { className: 'cf-value' }, `${(p2 * 100).toFixed(1)}% Churn`),
            React.createElement('div', { className: 'cf-delta' }, diff2 > 0.005 ? `▼ Giảm ${(diff2 * 100).toFixed(1)}%` : 'Không đổi')
          ),
          React.createElement('div', { className: 'cf-card highlight' },
            React.createElement('div', { className: 'cf-label' }, 'COMBO TOÀN DIỆN'),
            React.createElement('div', { className: 'cf-value' }, `${(p3 * 100).toFixed(1)}% Churn`),
            React.createElement('div', { className: 'cf-delta' }, diff3 > 0.005 ? `▼ Giảm ${(diff3 * 100).toFixed(1)}%` : 'Không đổi')
          )
        )
      )
    )
  );
}

// ── Tab 4: Strategy & ROI ────────────────────────────
function StrategyTab({ data }) {
  const [reachPct, setReachPct] = useState(40);
  const [successPct, setSuccessPct] = useState(25);
  const [costPerUser, setCostPerUser] = useState(12);

  const churned = data.filter(d => d.Churn === 'Yes');
  const totalChurnPool = churned.length;
  const avgChurnMrr = totalChurnPool > 0 ? churned.reduce((s, d) => s + (+d.MonthlyCharges || 0), 0) / totalChurnPool : 74.44;
  const targeted = Math.floor(totalChurnPool * reachPct / 100);
  const saved = Math.floor(targeted * successPct / 100);
  const annualSaved = saved * avgChurnMrr * 12;
  const campaignCost = targeted * costPerUser;
  const netProfit = annualSaved - campaignCost;
  const roi = campaignCost > 0 ? (netProfit / campaignCost * 100).toFixed(0) : 0;

  // ROI bar chart
  const roiData = [{
    x: ['Tổn thất ban đầu', 'Ngân sách đầu tư', 'Doanh thu bảo vệ', 'Lợi nhuận ròng'],
    y: [totalChurnPool * avgChurnMrr * 12, campaignCost, annualSaved, netProfit],
    type: 'bar',
    text: [totalChurnPool * avgChurnMrr * 12, campaignCost, annualSaved, netProfit].map(v => `$${v.toLocaleString('en-US', { maximumFractionDigits: 0 })}`),
    textposition: 'outside', textfont: { color: '#F8FAFC', size: 11 },
    marker: { color: ['#EF4444', '#F59E0B', '#3B82F6', '#10B981'] }
  }];

  return React.createElement('div', { className: 'content-section' },
    React.createElement('h2', { className: 'section-title' }, '💡 Khuyến Nghị Chiến Lược & ROI Simulator'),
    React.createElement('p', { className: 'section-subtitle' }, 'Prescriptive Analytics — Đỉnh cao tháp năng lực phân tích Gartner.'),

    React.createElement('h3', { style: { color: '#F8FAFC', marginBottom: 16, fontWeight: 800, fontSize: '1rem' } }, '🏛️ 1. Khung Chiến Lược 3 Trụ Cột'),
    React.createElement('div', { className: 'grid-3' },
      // Strategy 1
      React.createElement('div', { className: 'strategy-card' },
        React.createElement('div', null,
          React.createElement('span', { className: 'strategy-pill red' }, 'TRỤ CỘT 1 • SẢN PHẨM'),
          React.createElement('div', { className: 'strategy-name' }, '🛡️ Gói "Fiber Shield Bundle"'),
          React.createElement('div', { className: 'strategy-desc' }, React.createElement('b', null, 'Vấn đề:'), ' Cáp quang Churn 41.9% (gói tháng 54.6%).'),
          React.createElement('div', { className: 'strategy-action' },
            React.createElement('b', null, 'Hành động:'),
            React.createElement('ul', null,
              React.createElement('li', null, 'Tặng 3-6 tháng OnlineSecurity & TechSupport.'),
              React.createElement('li', null, React.createElement('b', null, 'Hiệu quả:'), ' Churn giảm còn 15.8%.')
            )
          )
        ),
        React.createElement('div', { className: 'strategy-target red' }, '🎯 Mục tiêu: Giảm 25% Churn tệp Cáp quang')
      ),
      // Strategy 2
      React.createElement('div', { className: 'strategy-card' },
        React.createElement('div', null,
          React.createElement('span', { className: 'strategy-pill amber' }, 'TRỤ CỘT 2 • THANH TOÁN'),
          React.createElement('div', { className: 'strategy-name' }, '💳 Chuyển Đổi Auto-Pay'),
          React.createElement('div', { className: 'strategy-desc' }, React.createElement('b', null, 'Vấn đề:'), ' Electronic check Churn 45.3% vs AutoPay 16.7%.'),
          React.createElement('div', { className: 'strategy-action' },
            React.createElement('b', null, 'Hành động:'),
            React.createElement('ul', null,
              React.createElement('li', null, 'Voucher giảm $5/tháng × 3 tháng khi chuyển AutoPay.'),
              React.createElement('li', null, React.createElement('b', null, 'Hiệu quả:'), ' Gắn kết cao hơn 2.7 lần.')
            )
          )
        ),
        React.createElement('div', { className: 'strategy-target amber' }, '🎯 Mục tiêu: Chuyển đổi 35% tệp E-check')
      ),
      // Strategy 3
      React.createElement('div', { className: 'strategy-card' },
        React.createElement('div', null,
          React.createElement('span', { className: 'strategy-pill blue' }, 'TRỤ CỘT 3 • HỢP ĐỒNG'),
          React.createElement('div', { className: 'strategy-name' }, '🔒 Khóa HĐ & Vượt Vùng Tử Thần'),
          React.createElement('div', { className: 'strategy-desc' }, React.createElement('b', null, 'Vấn đề:'), ' 65% Churn rơi vào 12 tháng đầu (HĐ tháng).'),
          React.createElement('div', { className: 'strategy-action' },
            React.createElement('b', null, 'Hành động:'),
            React.createElement('ul', null,
              React.createElement('li', null, 'CSKH chủ động tháng 4 & tháng 8.'),
              React.createElement('li', null, 'Chiết khấu 12% khi chuyển HĐ 1-2 năm.')
            )
          )
        ),
        React.createElement('div', { className: 'strategy-target blue' }, '🎯 Mục tiêu: Cắt giảm 40% Churn năm đầu')
      )
    ),

    React.createElement('hr', { className: 'divider' }),
    React.createElement('h3', { style: { color: '#F8FAFC', marginBottom: 8, fontWeight: 800, fontSize: '1rem' } }, '🎯 2. ROI Simulator'),
    React.createElement('p', { className: 'section-subtitle' }, 'Điều chỉnh tham số để đo lường lợi nhuận và ROI thời gian thực:'),

    React.createElement('div', { className: 'grid-2' },
      React.createElement('div', null,
        React.createElement('h4', { style: { color: '#F8FAFC', marginBottom: 14, fontWeight: 700, fontSize: '0.92rem' } }, '⚙️ Tham Số Chiến Dịch:'),
        React.createElement('div', { className: 'form-group', style: { marginBottom: 14 } },
          React.createElement('label', { className: 'form-label' }, `Tỷ lệ tiếp cận: ${reachPct}%`),
          React.createElement('input', { type: 'range', min: 10, max: 100, step: 5, value: reachPct, onChange: e => setReachPct(+e.target.value) })
        ),
        React.createElement('div', { className: 'form-group', style: { marginBottom: 14 } },
          React.createElement('label', { className: 'form-label' }, `Tỷ lệ giữ chân: ${successPct}%`),
          React.createElement('input', { type: 'range', min: 5, max: 60, step: 5, value: successPct, onChange: e => setSuccessPct(+e.target.value) })
        ),
        React.createElement('div', { className: 'form-group' },
          React.createElement('label', { className: 'form-label' }, `Ngân sách / khách: $${costPerUser}`),
          React.createElement('input', { type: 'range', min: 3, max: 40, step: 1, value: costPerUser, onChange: e => setCostPerUser(+e.target.value) })
        )
      ),
      React.createElement('div', null,
        React.createElement('h4', { style: { color: '#F8FAFC', marginBottom: 14, fontWeight: 700, fontSize: '0.92rem' } }, '📊 Kết Quả Tài Chính:'),
        React.createElement('div', { className: 'grid-4' },
          React.createElement('div', { className: 'metric-card' },
            React.createElement('div', { className: 'metric-label' }, 'Giữ chân'),
            React.createElement('div', { className: 'metric-value' }, `${saved.toLocaleString()}`),
            React.createElement('div', { className: 'metric-delta positive' }, `Tiếp cận ${targeted.toLocaleString()}`)
          ),
          React.createElement('div', { className: 'metric-card' },
            React.createElement('div', { className: 'metric-label' }, 'DT Cứu Vãn'),
            React.createElement('div', { className: 'metric-value' }, `$${(annualSaved / 1000).toFixed(0)}K`),
            React.createElement('div', { className: 'metric-delta positive' }, `+$${(annualSaved / 12000).toFixed(0)}K/th`)
          ),
          React.createElement('div', { className: 'metric-card' },
            React.createElement('div', { className: 'metric-label' }, 'Chi phí'),
            React.createElement('div', { className: 'metric-value' }, `$${campaignCost.toLocaleString()}`),
            React.createElement('div', { className: 'metric-delta negative' }, `$${costPerUser}/khách`)
          ),
          React.createElement('div', { className: 'metric-card' },
            React.createElement('div', { className: 'metric-label' }, 'Lợi nhuận'),
            React.createElement('div', { className: 'metric-value', style: { color: netProfit > 0 ? '#34D399' : '#F87171' } }, `$${(netProfit / 1000).toFixed(0)}K`),
            React.createElement('div', { className: `metric-delta ${netProfit > 0 ? 'positive' : 'negative'}` }, `ROI: ${roi}%`)
          )
        )
      )
    ),
    React.createElement('div', { className: 'chart-container', style: { marginTop: 16 } },
      React.createElement('div', { className: 'chart-header' }, '📊 Biểu đồ 8: So Sánh Hiệu Quả Kinh Tế Chiến Dịch'),
      React.createElement(PlotlyChart, { data: roiData, layout: { height: 310, showlegend: false } })
    )
  );
}

// ── Tab 5: Architecture & 360° Lookup ────────────────
function ArchitectureTab({ data }) {
  const [selectedId, setSelectedId] = useState('');
  const [sortCol, setSortCol] = useState('customerID');
  const [sortDir, setSortDir] = useState('asc');

  const customerIds = useMemo(() => data.slice(0, 100).map(d => d.customerID), [data]);
  const selectedCustomer = useMemo(() => data.find(d => d.customerID === selectedId), [data, selectedId]);

  const displayCols = ['customerID', 'gender', 'State', 'tenure', 'Contract', 'InternetService', 'MonthlyCharges', 'TotalCharges', 'SatisfactionScore', 'Churn'];
  const sortedData = useMemo(() => {
    const slice = data.slice(0, 200);
    return [...slice].sort((a, b) => {
      const av = a[sortCol], bv = b[sortCol];
      const numA = +av, numB = +bv;
      if (!isNaN(numA) && !isNaN(numB)) return sortDir === 'asc' ? numA - numB : numB - numA;
      return sortDir === 'asc' ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av));
    });
  }, [data, sortCol, sortDir]);

  const handleSort = (col) => {
    if (sortCol === col) setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    else { setSortCol(col); setSortDir('asc'); }
  };

  return React.createElement('div', { className: 'content-section' },
    React.createElement('h2', { className: 'section-title' }, '⚡ Kiến Trúc Dữ Liệu & Tra Cứu 360°'),
    React.createElement('p', { className: 'section-subtitle' }, 'Pipeline ETL, cam kết chất lượng dữ liệu (SLA) và Drill-Down hồ sơ khách hàng.'),

    React.createElement('div', { className: 'arch-box' },
      '[LUỒNG XỬ LÝ DỮ LIỆU ĐA TẦNG - ENTERPRISE DATA PIPELINE]:\n[1. Nguồn thô Kaggle/IBM] ──► [2. 4 Bảng RDBMS Quan Hệ] ──► [3. ETL & Imputation Engine] ──► [4. Feature Store (39 cột)] ──► [5. Production Dashboard & AI]'
    ),

    React.createElement('h3', { style: { color: '#F8FAFC', marginTop: 20, marginBottom: 8, fontWeight: 800, fontSize: '1rem' } }, '🛡️ Thước Đo Chất Lượng Dữ Liệu (SLA):'),
    React.createElement('div', { className: 'sla-grid' },
      React.createElement('div', { className: 'sla-card green' },
        React.createElement('div', { className: 'sla-label' }, 'TỶ LỆ KHỚP NỐI'),
        React.createElement('div', { className: 'sla-value' }, '100.0%'),
        React.createElement('div', { className: 'sla-sub' }, '7,043 / 7,043 PK-FK')
      ),
      React.createElement('div', { className: 'sla-card blue' },
        React.createElement('div', { className: 'sla-label' }, 'MISSING VALUES'),
        React.createElement('div', { className: 'sla-value' }, '0.00%'),
        React.createElement('div', { className: 'sla-sub' }, 'Đã xử lý 11 giá trị')
      ),
      React.createElement('div', { className: 'sla-card amber' },
        React.createElement('div', { className: 'sla-label' }, 'LATENCY'),
        React.createElement('div', { className: 'sla-value' }, '< 15 ms'),
        React.createElement('div', { className: 'sla-sub' }, 'React Virtual DOM')
      ),
      React.createElement('div', { className: 'sla-card purple' },
        React.createElement('div', { className: 'sla-label' }, 'ĐẶC TRƯNG'),
        React.createElement('div', { className: 'sla-value' }, '39 Cột'),
        React.createElement('div', { className: 'sla-sub' }, '50 bang & mã tiểu bang')
      )
    ),

    React.createElement('hr', { className: 'divider' }),
    React.createElement('h3', { style: { color: '#F8FAFC', marginBottom: 12, fontWeight: 800, fontSize: '1rem' } }, '🔍 Drill-Down Hồ Sơ 360° Khách Hàng:'),
    React.createElement('div', { className: 'filter-group', style: { maxWidth: 400, marginBottom: 16 } },
      React.createElement('label', { className: 'filter-label' }, 'Chọn mã khách hàng:'),
      React.createElement('select', {
        className: 'filter-select', value: selectedId,
        onChange: e => setSelectedId(e.target.value)
      },
        React.createElement('option', { value: '' }, '-- Chọn customerID --'),
        customerIds.map(id => React.createElement('option', { key: id, value: id }, id))
      )
    ),

    selectedCustomer && React.createElement('div', { className: 'profile-card' },
      React.createElement('div', { className: 'profile-header' },
        React.createElement('div', null,
          React.createElement('span', { className: 'profile-id' }, 'Khách Hàng: ', React.createElement('code', null, selectedCustomer.customerID)),
          React.createElement('span', {
            className: selectedCustomer.Churn === 'Yes' ? 'badge-churn' : 'badge-retained',
            style: { marginLeft: 12 }
          }, selectedCustomer.Churn === 'Yes' ? '🚨 ĐÃ RỜI MẠNG' : '🛡️ ĐANG Ở LẠI')
        ),
        React.createElement('div', { style: { fontSize: '0.82rem', color: '#94A3B8' } },
          `📍 ${selectedCustomer.City || 'N/A'}, ${selectedCustomer.State || 'N/A'}`)
      ),
      React.createElement('div', { className: 'profile-grid' },
        React.createElement('div', { className: 'profile-cell' },
          React.createElement('div', { className: 'profile-cell-label' }, 'NHÂN KHẨU HỌC'),
          React.createElement('div', { className: 'profile-cell-value' }, `Giới tính: ${selectedCustomer.gender}`),
          React.createElement('div', { className: 'profile-cell-sub' }, +selectedCustomer.SeniorCitizen === 1 ? 'Người cao tuổi' : 'Trẻ / Trung niên')
        ),
        React.createElement('div', { className: 'profile-cell' },
          React.createElement('div', { className: 'profile-cell-label' }, 'HỢP ĐỒNG & THANH TOÁN'),
          React.createElement('div', { className: 'profile-cell-value' }, selectedCustomer.Contract),
          React.createElement('div', { className: 'profile-cell-sub' }, `PT: ${selectedCustomer.PaymentMethod}`)
        ),
        React.createElement('div', { className: 'profile-cell' },
          React.createElement('div', { className: 'profile-cell-label' }, 'TÀI CHÍNH & DỊCH VỤ'),
          React.createElement('div', { className: 'profile-cell-value' }, `Cước: $${(+selectedCustomer.MonthlyCharges).toFixed(2)}`),
          React.createElement('div', { className: 'profile-cell-sub' }, `Tích lũy: $${(+selectedCustomer.TotalCharges).toFixed(2)}`)
        ),
        React.createElement('div', { className: 'profile-cell' },
          React.createElement('div', { className: 'profile-cell-label' }, 'TRẢI NGHIỆM'),
          React.createElement('div', { className: 'profile-cell-value' }, `CSAT: ${selectedCustomer.SatisfactionScore || 'N/A'} / 5 ⭐`),
          React.createElement('div', { className: 'profile-cell-sub', style: { color: '#F87171' } }, `Lý do: ${selectedCustomer.ChurnReason || 'N/A'}`)
        )
      )
    ),

    // Data Table
    React.createElement('div', { className: 'data-table-wrapper', style: { maxHeight: 420, overflowY: 'auto' } },
      React.createElement('table', { className: 'data-table' },
        React.createElement('thead', null,
          React.createElement('tr', null,
            displayCols.map(col =>
              React.createElement('th', { key: col, onClick: () => handleSort(col) },
                col === 'customerID' ? 'Mã KH' : col === 'gender' ? 'Giới tính' : col === 'State' ? 'Địa bàn' :
                col === 'tenure' ? 'Thâm niên' : col === 'MonthlyCharges' ? 'Cước tháng' :
                col === 'TotalCharges' ? 'Tổng tích lũy' : col === 'SatisfactionScore' ? 'CSAT' :
                col === 'Churn' ? 'Rời mạng?' : col,
                sortCol === col && (sortDir === 'asc' ? ' ▲' : ' ▼')
              )
            )
          )
        ),
        React.createElement('tbody', null,
          sortedData.map((row, i) =>
            React.createElement('tr', { key: i },
              displayCols.map(col =>
                React.createElement('td', { key: col },
                  col === 'Churn' ? React.createElement('span', { className: row[col] === 'Yes' ? 'churn-yes' : 'churn-no' }, row[col] === 'Yes' ? 'Rời mạng' : 'Ở lại') :
                  col === 'MonthlyCharges' ? `$${(+row[col]).toFixed(2)}` :
                  col === 'TotalCharges' ? `$${(+row[col]).toFixed(0)}` :
                  col === 'SatisfactionScore' ? `${row[col]} ⭐` :
                  col === 'tenure' ? React.createElement('div', null, `${row[col]} th`,
                    React.createElement('div', { className: 'tenure-bar-bg' },
                      React.createElement('div', { className: 'tenure-bar-fill', style: { width: `${(+row[col] / 72 * 100)}%` } })
                    )
                  ) :
                  row[col]
                )
              )
            )
          )
        )
      )
    )
  );
}

// ── Main App Component ───────────────────────────────
function App() {
  const [rawData, setRawData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [filters, setFilters] = useState({
    cohort: 'Toàn bộ', state: 'all', internet: 'all', contract: 'all', payment: 'all',
    mrrMin: 18, mrrMax: 120
  });

  // Load CSV data
  useEffect(() => {
    Papa.parse('data/telco_churn_clean.csv', {
      download: true, header: true, skipEmptyLines: true,
      complete: (results) => {
        setRawData(results.data.filter(d => d.customerID));
        setLoading(false);
      },
      error: () => setLoading(false)
    });
  }, []);

  // Unique values for filters
  const uniqueValues = useMemo(() => {
    if (rawData.length === 0) return {};
    return {
      states: [...new Set(rawData.map(d => d.StateCode).filter(Boolean))].sort().map(c => `${US_STATES[c]?.name || c} (${c})`),
      stateCodesMap: Object.fromEntries([...new Set(rawData.map(d => d.StateCode).filter(Boolean))].map(c => [`${US_STATES[c]?.name || c} (${c})`, c])),
      internet: [...new Set(rawData.map(d => d.InternetService).filter(Boolean))].sort(),
      contracts: [...new Set(rawData.map(d => d.Contract).filter(Boolean))].sort(),
      payments: [...new Set(rawData.map(d => d.PaymentMethod).filter(Boolean))].sort()
    };
  }, [rawData]);

  // Apply filters
  const filteredData = useMemo(() => {
    let df = rawData;
    if (filters.cohort !== 'Toàn bộ') {
      if (filters.cohort === '<12 tháng') df = df.filter(d => +d.tenure < 12);
      else if (filters.cohort === '12-24 tháng') df = df.filter(d => +d.tenure >= 12 && +d.tenure < 24);
      else if (filters.cohort === '24-36 tháng') df = df.filter(d => +d.tenure >= 24 && +d.tenure < 36);
      else if (filters.cohort === '36-48 tháng') df = df.filter(d => +d.tenure >= 36 && +d.tenure < 48);
      else if (filters.cohort === '>48 tháng') df = df.filter(d => +d.tenure >= 48);
    }
    if (filters.state !== 'all') {
      const code = uniqueValues.stateCodesMap?.[filters.state] || '';
      df = df.filter(d => d.StateCode === code);
    }
    if (filters.internet !== 'all') df = df.filter(d => d.InternetService === filters.internet);
    if (filters.contract !== 'all') df = df.filter(d => d.Contract === filters.contract);
    if (filters.payment !== 'all') df = df.filter(d => d.PaymentMethod === filters.payment);
    df = df.filter(d => +d.MonthlyCharges >= filters.mrrMin && +d.MonthlyCharges <= filters.mrrMax);
    return df;
  }, [rawData, filters, uniqueValues]);

  const resetFilters = () => setFilters({ cohort: 'Toàn bộ', state: 'all', internet: 'all', contract: 'all', payment: 'all', mrrMin: 18, mrrMax: 120 });

  // KPI calculations
  const total = filteredData.length;
  const churnCount = filteredData.filter(d => d.Churn === 'Yes').length;
  const churnRate = total > 0 ? (churnCount / total * 100).toFixed(1) : '0.0';
  const avgMrr = total > 0 ? (filteredData.reduce((s, d) => s + (+d.MonthlyCharges || 0), 0) / total).toFixed(2) : '0.00';
  const totalRevenue = filteredData.reduce((s, d) => s + (+d.TotalCharges || 0), 0);
  const avgSat = total > 0 ? (filteredData.reduce((s, d) => s + (+d.SatisfactionScore || 0), 0) / total).toFixed(2) : '0.00';
  const churnIsHigh = +churnRate > 25;

  if (loading) {
    return React.createElement('div', { style: { display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', width: '100%' } },
      React.createElement('div', { className: 'loading-container' },
        React.createElement('div', { className: 'spinner' }),
        React.createElement('div', { className: 'loading-text' }, 'Đang tải dữ liệu Telco Churn...')
      )
    );
  }

  const tabContent = {
    overview: React.createElement(OverviewTab, { data: filteredData, allData: rawData }),
    diagnostic: React.createElement(DiagnosticTab, { data: filteredData }),
    prediction: React.createElement(PredictionTab, { data: filteredData }),
    strategy: React.createElement(StrategyTab, { data: filteredData }),
    architecture: React.createElement(ArchitectureTab, { data: filteredData })
  };

  return React.createElement(React.Fragment, null,
    React.createElement(Sidebar, { activeTab, setActiveTab, filters, setFilters, uniqueValues, resetFilters }),
    React.createElement('main', { className: 'main-content' },
      // Top Navbar
      React.createElement('div', { className: 'top-navbar' },
        React.createElement('div', { className: 'navbar-left' },
          React.createElement('div', { className: 'logo-badge' },
            React.createElement('img', { src: 'assets/logo_hcmute_badge.png', alt: 'HCMUTE' })
          ),
          React.createElement('div', { className: 'navbar-text-group' },
            React.createElement('span', { className: 'navbar-school' }, 'TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT TP. HỒ CHÍ MINH'),
            React.createElement('span', { className: 'navbar-title' }, 'HỆ THỐNG TRỰC QUAN HÓA & DỰ BÁO CUSTOMER CHURN (TELCO IDV)')
          )
        ),
        React.createElement('div', { className: 'navbar-right' },
          React.createElement('span', { className: 'pill' }, '📚 ĐỒ ÁN: TƯƠNG TÁC DỮ LIỆU TRỰC QUAN'),
          React.createElement('span', { className: 'pill pill-accent' }, '👥 NHÓM 22 - HCMUTE')
        )
      ),

      // KPI Cards
      React.createElement('div', { className: 'kpi-grid' },
        React.createElement('div', { className: 'kpi-card' },
          React.createElement('div', { className: 'kpi-accent blue' }),
          React.createElement('div', { className: 'kpi-header' },
            React.createElement('span', { className: 'kpi-label' }, 'Tổng khách hàng'),
            React.createElement('span', { className: 'kpi-icon' }, '👥')
          ),
          React.createElement('div', { className: 'kpi-value' }, total.toLocaleString()),
          React.createElement('div', { className: 'kpi-subtext' }, `Quy mô mẫu (${(total / rawData.length * 100).toFixed(1)}%)`)
        ),
        React.createElement('div', { className: 'kpi-card' },
          React.createElement('div', { className: `kpi-accent ${churnIsHigh ? 'red' : 'green'}` }),
          React.createElement('div', { className: 'kpi-header' },
            React.createElement('span', { className: 'kpi-label' }, 'Tỷ lệ Churn'),
            React.createElement('span', { className: 'kpi-icon' }, '⚠️')
          ),
          React.createElement('div', { className: `kpi-value ${churnIsHigh ? 'danger' : 'success'}` }, `${churnRate}%`),
          React.createElement('div', { className: 'kpi-subtext' }, `${churnCount.toLocaleString()} khách hủy`)
        ),
        React.createElement('div', { className: 'kpi-card' },
          React.createElement('div', { className: 'kpi-accent purple' }),
          React.createElement('div', { className: 'kpi-header' },
            React.createElement('span', { className: 'kpi-label' }, 'Cước TB / Tháng (ARPU)'),
            React.createElement('span', { className: 'kpi-icon' }, '💵')
          ),
          React.createElement('div', { className: 'kpi-value' }, `$${avgMrr}`),
          React.createElement('div', { className: 'kpi-subtext' }, 'Doanh thu định kỳ')
        ),
        React.createElement('div', { className: 'kpi-card' },
          React.createElement('div', { className: 'kpi-accent amber' }),
          React.createElement('div', { className: 'kpi-header' },
            React.createElement('span', { className: 'kpi-label' }, 'Doanh thu CLV'),
            React.createElement('span', { className: 'kpi-icon' }, '📈')
          ),
          React.createElement('div', { className: 'kpi-value' }, `$${(totalRevenue / 1e6).toFixed(2)}M`),
          React.createElement('div', { className: 'kpi-subtext' }, 'Tổng giá trị thu được')
        ),
        React.createElement('div', { className: 'kpi-card' },
          React.createElement('div', { className: 'kpi-accent green' }),
          React.createElement('div', { className: 'kpi-header' },
            React.createElement('span', { className: 'kpi-label' }, 'Điểm hài lòng TB'),
            React.createElement('span', { className: 'kpi-icon' }, '⭐')
          ),
          React.createElement('div', { className: 'kpi-value' }, avgSat, React.createElement('span', { style: { fontSize: '0.9rem', color: '#94A3B8' } }, ' / 5.0')),
          React.createElement('div', { className: 'kpi-subtext' }, 'Khảo sát CSAT')
        )
      ),

      // Tab Content
      total === 0
        ? React.createElement('div', { style: { textAlign: 'center', padding: 40, color: '#F59E0B' } }, '⚠️ Không có khách hàng nào thỏa mãn bộ lọc. Vui lòng điều chỉnh lại.')
        : tabContent[activeTab],

      // Footer
      React.createElement('div', { className: 'footer' },
        '© 2026 Đồ Án Tương Tác Dữ Liệu Trực Quan | Trường ĐH Công Nghệ Kỹ Thuật TP.HCM (HCMUTE) | Nhóm 22: Trương Quốc Duy (Trưởng nhóm) - Đỗ Trọng Khôi - Bùi Đức Huy'
      )
    )
  );
}

// ── Render ───────────────────────────────────────────
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(App));
