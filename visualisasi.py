import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# === BACA DATA ===
df = pd.read_csv("tokped.csv")

# === PERSIAPAN DATA ===
df['bulan'] = pd.to_datetime(df['registered_date'], errors='coerce').dt.to_period('M').astype(str)

# === STATISTIK RINGKASAN ===
total_penjualan = df['after_discount'].sum()
total_transaksi = len(df)
kategori_terlaris = df.groupby('category')['after_discount'].sum().idxmax()
metode_pembayaran_terpopuler = df['payment_method'].mode()[0]

# === VISUALISASI 1: TOTAL PENJUALAN PER KATEGORI ===
df_kat = (
    df.groupby('category', as_index=False)['after_discount']
    .sum()
    .sort_values(by='after_discount', ascending=False)
)

fig1 = px.bar(
    df_kat,
    x='category', y='after_discount', color='category',
    title='📦 Total Penjualan Berdasarkan Kategori Produk',
    labels={'category': 'Kategori Produk', 'after_discount': 'Total Penjualan (Rp)'},
    text_auto='.2s',
    height=480,
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig1.update_layout(
    template='plotly_white',
    font=dict(size=14, family='Poppins, sans-serif'),
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=60, r=60, t=80, b=80),
    xaxis_tickangle=30,
)
fig1.update_traces(
    marker=dict(line=dict(width=2, color='rgba(0,0,0,0.1)')),
    hovertemplate='<b>%{x}</b><br>Total: Rp %{y:,.0f}<extra></extra>',
    textfont=dict(size=12)
)

# === VISUALISASI 2: PROPORSI METODE PEMBAYARAN (Top 6 + Lainnya) ===
df_pie = df['payment_method'].value_counts(normalize=True).reset_index()
df_pie.columns = ['payment_method', 'persentase']

top_n = 6
df_top = df_pie.head(top_n)
df_lainnya = pd.DataFrame({
    'payment_method': ['Lainnya'],
    'persentase': [df_pie['persentase'][top_n:].sum()]
})
df_final = pd.concat([df_top, df_lainnya])

fig2 = px.pie(
    df_final,
    names='payment_method',
    values='persentase',
    title='💳 Distribusi Metode Pembayaran (Top 6 + Lainnya)',
    hole=0.55,
    color_discrete_sequence=px.colors.qualitative.Safe
)
fig2.update_traces(
    textposition='inside',
    textinfo='label+percent',
    hovertemplate='<b>%{label}</b><br>%{percent}<extra></extra>',
    pull=[0.08 if i == 0 else 0 for i in range(len(df_final))],
    textfont=dict(size=13)
)
fig2.update_layout(
    template='plotly_white',
    font=dict(size=14, family='Poppins, sans-serif'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=50, r=50, t=80, b=60),
    showlegend=True,
    legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
)

# === VISUALISASI 3: TREND PENJUALAN BULANAN ===
df_bulan = df.groupby(['bulan'], as_index=False)['after_discount'].sum()
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=df_bulan['bulan'], 
    y=df_bulan['after_discount'],
    mode='lines+markers',
    line=dict(color='#06b6d4', width=4, shape='spline'),
    marker=dict(size=10, color='#0ea5e9', symbol='circle'),
    hovertemplate='<b>Bulan:</b> %{x}<br><b>Penjualan:</b> Rp %{y:,.0f}<extra></extra>',
    name='Penjualan'
))
fig3.update_layout(
    title='📈 Tren Total Penjualan per Bulan',
    xaxis_title='Bulan',
    yaxis_title='Total Penjualan (Rp)',
    template='plotly_white',
    font=dict(size=14, family='Poppins, sans-serif'),
    xaxis_tickangle=30,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=60, r=60, t=80, b=60),
    height=480
)

# === INFORMASI TAMBAHAN ===
top_5_kategori = df_kat.head(5).to_dict('records')
rata_rata_penjualan = total_penjualan / total_transaksi if total_transaksi > 0 else 0
bulan_tertinggi = df_bulan.loc[df_bulan['after_discount'].idxmax()]['bulan']

# === HTML OUTPUT ===
html_content = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Penjualan Tokopedia</title>

    <!-- Fonts & CSS -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>

<body>

<nav>
    <div class="logo">
        <i class="fa-solid fa-chart-line"></i> Tokopedia Analytics
    </div>
</nav>

<header>
    <h1>Dashboard Penjualan Tokopedia</h1>
    <p>
        Analisis performa penjualan dan tren dari 
        <b>{df['bulan'].min()}</b> hingga <b>{df['bulan'].max()}</b>.
    </p>
</header>

<div class="summary" id="summary">
    <div class="summary-card">
        <i class="fa-solid fa-sack-dollar"></i>
        <h3>Rp {total_penjualan:,.0f}</h3>
        <p>Total Penjualan</p>
    </div>
    
    <div class="summary-card">
        <i class="fa-solid fa-cart-shopping"></i>
        <h3>{total_transaksi:,}</h3>
        <p>Total Transaksi</p>
    </div>

    <div class="summary-card">
        <i class="fa-solid fa-crown"></i>
        <h3>{kategori_terlaris}</h3>
        <p>Kategori Terlaris</p>
    </div>

    <div class="summary-card">
        <i class="fa-solid fa-credit-card"></i>
        <h3>{metode_pembayaran_terpopuler}</h3>
        <p>Metode Pembayaran</p>
    </div>
</div>

<main id="charts">

    <!-- Line Chart -->
    <div class="grid">
        <div class="card" style="margin: 10px;">
            {fig1.to_html(include_plotlyjs='cdn', full_html=False)}
        </div>
    </div>

    <!-- Pie Chart & Insight Box -->
    <div class="grid-pie">

        <div class="card" style="margin: 10px;">
            {fig2.to_html(include_plotlyjs=False, full_html=False)}
        </div>

        <div class="info-card" style="margin: 10px;">
            <h3><i class="fa-solid fa-lightbulb"></i> Insight Menarik</h3>
            <ul>
                { "".join([f"<li>{i+1}. {item['category']} — Rp {item['after_discount']:,.0f}</li>" 
                           for i, item in enumerate(top_5_kategori)]) }
                <li><b>Rata-rata Penjualan per Transaksi:</b> Rp {rata_rata_penjualan:,.0f}</li>
                <li><b>Bulan Penjualan Tertinggi:</b> {bulan_tertinggi}</li>
                <li><b>Persentase Pembayaran Terpopuler:</b> {df_pie.iloc[0]['persentase']:.1%}</li>
            </ul>
        </div>

    </div>

    <!-- Bar Chart -->
    <div class="grid" style="margin: 10px;">
        <div class="card">
            {fig3.to_html(include_plotlyjs=False, full_html=False)}
        </div>
    </div>

</main>

<footer>
    Dashboard Analitik Tokopedia
</footer>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Dashboard berhasil dibuat: index.html")
