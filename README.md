# 🏦 Risk Analysis & Return of Indonesian Banking Shares

## 🎯 Project Description

This project analyzes and compares the performance of BBRI, BMRI and BBCA banking shares against the IHSG benchmark (^JKSE) during the 2019-2024 period using Python, with a focus on return, volatility, Sharpe Ratio, Max Drawdown, Beta, VaR 95%, and Skewness.

## ❓ Questions Answered

- Which shares provide higher returns?
- Which stocks are more stable (low volatility)?
- Which stock is more efficient (Sharpe Ratio)?
- Which stocks are most sensitive to market movements (Beta vs JCI)?
- What is the worst potential daily loss (VaR 95%) and deepest drop (Max Drawdown)?

## 🛠️ Tools & Library

- Python 3.10+
- pandas, numpy
- yfinance

## 📁 Project Structure

```
idx-bank-stock-risk-analysis/
├── README.md
├── requirements.txt
└── main.py
```

## 🔍 How to Run

1. Clone this repository
   ```bash
   git clone https://github.com/username/idx-bank-stock-risk-analysis.git
   ```
2. Install library
   ```bash
   pip install -r requirements.txt
   ```
3. Run script
   ```bash
   python main.py
   ```

## 📈 Main Results

| Metrik | BBRI | BMRI | BBCA |
|---|---|---|---|
| Mean Return (annual) | 13.69% | 17.60% | 15.65% |
| Sharpe Ratio | 0.24 | 0.35 | 0.40 |
| Max Drawdown | -52.43% | -52.05% | -35.56% |
| Beta vs IHSG | 1.48 | 1.50 | 1.07 |
| VaR 95% | -2.82% | -3.11% | -2.07% |
| Skewness | 0.87 | 0.20 | 1.03 |

- **Conclusion:** During the 2019-2024 period, BMRI shares provided the best return with a Sharpe Ratio of 0.35 while BBCA shares had the lowest risk with annual volatility of 24.34%

> **Note:** If the message `[WARN]` appears when the program is running, it means that the download of yfinance failed and the program used **simulation data (not original data)**. Don't use these results for conclusions.

## ⚠️ Disclaimer

This project is educational and not an investment recommendation. Past performance does not guarantee future results.

## 👤 Author

Afif Ardian Saputra
