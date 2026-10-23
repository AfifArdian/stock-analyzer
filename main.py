import numpy as np
import pandas as pd

TRADING_DAYS = 252
RISK_FREE_ANNUAL = 0.06
BENCHMARK = "^JKSE"  # IHSG di Yahoo Finance


# =====================================================================
# Ambil Data dari library yfinance
# =====================================================================
def get_data(ticker, start, end):
    """Download harga harian satu ticker. Fallback ke data simulasi bila gagal."""
    try:
        import yfinance as yf
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if df is None or df.empty:
            raise ValueError(f"Data kosong untuk {ticker}")
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df[["Close"]].dropna()
    except Exception as e:
        print(f"[WARN] {ticker}: gagal download ({type(e).__name__}). Pakai data simulasi.")
        return _generate_dummy(ticker, start, end)


def _generate_dummy(ticker, start, end):
    """
    Data simulasi (BUKAN data asli) agar kode bisa diuji offline.
    Semua saham berbagi satu 'faktor pasar' yang sama, sehingga beta & korelasi
    bernilai masuk akal (bukan nol).
    """
    tanggal = pd.bdate_range(start=start, end=end)
    n = len(tanggal)

    pasar = np.random.default_rng(12345).normal(0.0003, 0.011, n)  # faktor pasar bersama

    beta_sim = {"BBRI.JK": 1.25, "BMRI.JK": 1.10, "BBCA.JK": 0.85, BENCHMARK: 1.0}
    harga0 = {"BBRI.JK": 4000, "BMRI.JK": 6500, "BBCA.JK": 8000, BENCHMARK: 6000}

    seed = sum(ord(c) for c in ticker)  # deterministik (hash() berubah tiap run)
    idio = np.random.default_rng(seed).normal(0.0001, 0.010, n)
    idio = idio if ticker != BENCHMARK else idio * 0

    ret = beta_sim.get(ticker, 1.0) * pasar + idio
    harga = harga0.get(ticker, 5000) * np.exp(np.cumsum(ret))
    return pd.DataFrame({"Close": harga}, index=tanggal)


def calculate_metrics(df, risk_free=RISK_FREE_ANNUAL):
    """Metrik dasar: mean, std, sharpe, max drawdown, total return."""
    close = df["Close"]
    returns = close.pct_change().dropna()

    mean_return = returns.mean()
    std_return = returns.std()
    mean_thn = mean_return * TRADING_DAYS
    std_thn = std_return * np.sqrt(TRADING_DAYS)
    sharpe = (mean_thn - risk_free) / std_thn if std_thn != 0 else np.nan

    cum = (1 + returns).cumprod()
    max_dd = ((cum - cum.cummax()) / cum.cummax()).min()

    return {
        "mean_return": mean_return,
        "std_return": std_return,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
        "total_return_5yr": close.iloc[-1] / close.iloc[0] - 1,
    }

# =====================================================================
# Metrik tambahan
# =====================================================================
def hitung_beta(ret_saham, ret_pasar):
    """Beta = Cov(saham, pasar) / Var(pasar)."""
    return ret_saham.cov(ret_pasar) / ret_pasar.var()


def hitung_var(returns, level=0.95):
    """
    Historical VaR harian: persentil ke-(1-level) dari distribusi return.
    Hasil negatif = kerugian harian yang hanya terlampaui di (1-level) hari terburuk.
    """
    return np.percentile(returns, (1 - level) * 100)


def full_analysis(list_ticker, start="2019-01-01", end="2024-12-31",
                  benchmark=BENCHMARK, risk_free=RISK_FREE_ANNUAL):
    """
    Analisis lengkap: tabel perbandingan 6 metrik + kesimpulan otomatis.

    Catatan definisi:
      - Mean Return   : rata-rata return harian dianualisasi (x 252)
      - Sharpe Ratio  : (mean tahunan - risk free) / volatilitas tahunan
      - Max Drawdown  : penurunan terdalam dari puncak
      - Beta vs IHSG  : sensitivitas return harian terhadap return IHSG
      - VaR 95%       : historical VaR harian (persentil 5)
      - Skewness      : kemiringan distribusi return harian
    """
    # 1. Ambil data semua saham + benchmark, gabung per tanggal yang sama
    harga = {t: get_data(t, start, end)["Close"] for t in list_ticker}
    harga[benchmark] = get_data(benchmark, start, end)["Close"]
    harga_df = pd.DataFrame(harga).dropna()

    returns_df = harga_df.pct_change().dropna()
    ret_pasar = returns_df[benchmark]

    # 2. Hitung metrik per saham
    hasil = {}
    for t in list_ticker:
        r = returns_df[t]
        dasar = calculate_metrics(harga_df[[t]].rename(columns={t: "Close"}), risk_free)

        hasil[t] = {
            "Mean Return": r.mean() * TRADING_DAYS,
            "Sharpe Ratio": dasar["sharpe_ratio"],
            "Max Drawdown": dasar["max_drawdown"],
            "Beta vs IHSG": hitung_beta(r, ret_pasar),
            "VaR 95%": hitung_var(r, 0.95),
            "Skewness": r.skew(),
            "_volatilitas": r.std() * np.sqrt(TRADING_DAYS),  # untuk kesimpulan
        }

    tabel = pd.DataFrame(hasil)  # baris = metrik, kolom = ticker

    # 3. Cetak dalam bentuk tabel 
    nama = [t.replace(".JK", "") for t in list_ticker]
    tampil = tabel.drop(index="_volatilitas").copy()
    tampil.columns = nama

    persen = ["Mean Return", "Max Drawdown", "VaR 95%"]
    fmt = tampil.copy().astype(object)
    for metrik in tampil.index:
        for kol in tampil.columns:
            v = tampil.loc[metrik, kol]
            fmt.loc[metrik, kol] = f"{v*100:.2f}%" if metrik in persen else f"{v:.2f}"

    print("\n" + "=" * 62)
    print(f"ANALISIS LENGKAP  ({start} s/d {end})")
    print("=" * 62)
    print(fmt.to_string())

    # 4. Kesimpulan otomatis
    vol = tabel.loc["_volatilitas"]
    risiko_terendah = vol.idxmin()
    return_terbaik = tabel.loc["Mean Return"].idxmax()

    print("\n" + "-" * 62)
    print(f"Saham dengan risiko terendah: {risiko_terendah.replace('.JK', '')} "
          f"(volatilitas tahunan {vol.min()*100:.2f}%)")
    print(f"Saham dengan return terbaik : {return_terbaik.replace('.JK', '')} "
          f"(mean return tahunan {tabel.loc['Mean Return'].max()*100:.2f}%)")
    print("-" * 62)

    return tabel.drop(index="_volatilitas")


if __name__ == "__main__":
    full_analysis(["BBRI.JK", "BMRI.JK", "BBCA.JK"])
