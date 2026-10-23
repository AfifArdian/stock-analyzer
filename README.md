# 🏦 Analisis Risiko & Return Saham Perbankan Indonesia

## 🎯 Deskripsi Project

Project ini menganalisis dan membandingkan performa saham perbankan BBRI, BMRI, dan BBCA terhadap benchmark IHSG (^JKSE) selama periode 2019-2024 menggunakan Python, dengan fokus pada return, volatilitas, Sharpe Ratio, Max Drawdown, Beta, VaR 95%, dan Skewness.

## ❓ Pertanyaan yang Dijawab

- Saham mana yang memberikan return lebih tinggi?
- Saham mana yang lebih stabil (volatilitas rendah)?
- Saham mana yang lebih efisien (Sharpe Ratio)?
- Saham mana yang paling sensitif terhadap pergerakan pasar (Beta vs IHSG)?
- Berapa potensi kerugian harian terburuk (VaR 95%) dan penurunan terdalam (Max Drawdown)?

## 🛠️ Tools & Library

- Python 3.10+
- pandas, numpy
- yfinance

## 📁 Struktur Project

```
idx-bank-stock-risk-analysis/
├── README.md
├── requirements.txt
└── main.py
```

## 🔍 Cara Menjalankan

1. Clone repository ini
   ```bash
   git clone https://github.com/username/idx-bank-stock-risk-analysis.git
   ```
2. Install library
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan script
   ```bash
   python main.py
   ```

## 📈 Hasil Utama

| Metrik | BBRI | BMRI | BBCA |
|---|---|---|---|
| Mean Return (tahunan) | 13.69% | 17.60% | 15.65% |
| Sharpe Ratio | 0.24 | 0.35 | 0.40 |
| Max Drawdown | -52.43% | -52.05% | -35.56% |
| Beta vs IHSG | 1.48 | 1.50 | 1.07 |
| VaR 95% | -2.82% | -3.11% | -2.07% |
| Skewness | 0.87 | 0.20 | 1.03 |

- **Kesimpulan:** Selama periode 2019-2024, saham BMRI memberikan return terbaik dengan Sharpe Ratio 0.35 sedangkan saham BBCA memiliki risiko terendah dengan volatilitas tahunan 24.34%

> **Catatan:** Jika muncul pesan `[WARN]` saat program dijalankan, artinya download yfinance gagal dan program memakai **data simulasi (bukan data asli)**. Jangan gunakan hasil tersebut untuk kesimpulan.

## ⚠️ Disclaimer

Project ini bersifat edukasi dan bukan rekomendasi investasi. Performa masa lalu tidak menjamin hasil di masa depan.

## 👤 Author

Afif Ardian Saputra
