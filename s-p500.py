import yfinance as yf
import pandas as pd
import warnings
import time
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns

start_time = time.time()

# 忽略 FutureWarning 警告
warnings.simplefilter(action='ignore', category=FutureWarning)

# 使用 simhei.ttf 字型（假設該檔案與此程式在同一目錄下）
# 1. 將 simhei.ttf 加入 fontManager
fm.fontManager.addfont("simhei.ttf")
# 2. 設定 rcParams 使 Matplotlib 使用 SimHei
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 防止負號顯示為方框

# 定義藍籌股的股票代碼 (以S&P 500為例)
blue_chip_tickers = [
    "A",
    "AAPL",
    "ABBV",
    "ABNB",
    "ABT",	
    "ACGL",
    "ACN",	
    "ADBE",
    "ADI",	
    "ADM",	
    "ADP",	
    "ADSK",
    "AEE",	
    "AEP",	
    "AES",	
    "AFL",	
    "AIG",	
    "AIZ",	
    "AJG",	
    "AKAM",
    "ALB",	
    "ALGN",
    "ALL",	
    "ALLE",
    "AMAT",
    "AMCR",
    "AMD",	
    "AME",	
    "AMGN",
    "AMP",	
    "AMT",	
    "AMZN",
    "ANET",
    "ANSS",
    "AON",	
    "AOS",	
    "APA",	
    "APD",	
    "APH",	
    "APO",	
    "APTV",
    "ARE",	
    "ATO",	
    "AVB",	
    "AVGO",
    "AVY",	
    "AWK",	
    "AXON",
    "AXP",	
    "AZO",	
    "BA	",
    "BAC",	
    "BALL",
    "BAX",	
    "BBY",	
    "BDX",	
    "BEN",	
    "BF",
    "BG	",
    "BIIB",
    "BK	",
    "BKNG",
    "BKR",	
    "BLDR",
    "BLK",	
    "BMY",	
    "BR	",
    "BRK",
    "BRO",	
    "BSX",	
    "BWA",	
    "BX	",
    "BXP",	
    "C",
    "CAG",	
    "CAH",	
    "CARR",
    "CAT",	
    "CB",
    "CBOE",
    "CBRE",
    "CCI",	
    "CCL",	
    "CDNS",
    "CDW",	
    "CE",
    "CEG",	
    "CF",
    "CFG",	
    "CHD",	
    "CHRW",
    "CHTR",
    "CI",
    "CINF",
    "CL",
    "CLX",	
    "CMCS",
    "CME",	
    "CMG",	
    "CMI",	
    "CMS",	
    "CNC",	
    "CNP",	
    "COF",	
    "COO",	
    "COP",	
    "COR",	
    "COST",
    "CPAY",
    "CPB",	
    "CPRT",
    "CPT",	
    "CRL",	
    "CRM",	
    "CRWD",
    "CSCO",
    "CSGP",
    "CSX",	
    "CTAS",
    "CTRA",
    "CTSH",
    "CTVA",
    "CVS",	
    "CVX",	
    "CZR",	
    "D",
    "DAL",	
    "DAY",	
    "DD	",
    "DE",
    "DECK",
    "DELL",
    "DFS",	
    "DG",
    "DGX",	
    "DHI",	
    "DHR",	
    "DIS",	
    "DLR",	
    "DLTR",
    "DOC",	
    "DOV",	
    "DOW",	
    "DPZ",	
    "DRI",	
    "DTE",	
    "DUK",	
    "DVA",	
    "DVN",	
    "DXCM",
    "EA",
    "EBAY",
    "ECL",	
    "ED",
    "EFX",	
    "EG",
    "EIX",	
    "EL",
    "ELV",	
    "EMN",	
    "EMR",	
    "ENPH",
    "EOG",	
    "EPAM",
    "EQIX",
    "EQR",	
    "EQT",	
    "ERIE",
    "ES",
    "ESS",	
    "ETN",	
    "ETR",	
    "EVRG",
    "EW",
    "EXC",	
    "EXPD",
    "EXPE",
    "EXR",	
    "F",
    "FANG",
    "FAST",
    "FCX",	
    "FDS",	
    "FDX",	
    "FE",
    "FFIV",
    "FI",
    "FICO",
    "FIS",	
    "FITB",
    "FMC",	
    "FOX",	
    "FOXA",
    "FRT",	
    "FSLR",
    "FTNT",
    "FTV",	
    "GD",
    "GDDY",
    "GE",
    "GEHC",
    "GEN",	
    "GEV",	
    "GILD",
    "GIS",	
    "GL",
    "GLW",	
    "GM",
    "GNRC",
    "GOOG",
    "GOOG",
    "GPC",	
    "GPN",	
    "GRMN",
    "GS",
    "GWW",	
    "HAL",	
    "HAS",	
    "HBAN",
    "HCA",	
    "HD",
    "HES",	
    "HIG",	
    "HII",	
    "HLT",	
    "HOLX",
    "HON",	
    "HPE",	
    "HPQ",	
    "HRL",	
    "HSIC",
    "HST",	
    "HSY",	
    "HUBB",
    "HUM",	
    "HWM",	
    "IBM",	
    "ICE",	
    "IDXX",
    "IEX",	
    "IFF",	
    "INCY",
    "INTC",
    "INTU",
    "INVH",
    "IP",
    "IPG",	
    "IQV",	
    "IR",
    "IRM",	
    "ISRG",
    "IT",
    "ITW",	
    "IVZ",	
    "J",
    "JBHT",
    "JBL",	
    "JCI",	
    "JKHY",
    "JNJ",	
    "JNPR",
    "JPM",	
    "K",
    "KDP",	
    "KEY",	
    "KEYS",
    "KHC",	
    "KIM",	
    "KKR",	
    "KLAC",
    "KMB",	
    "KMI",	
    "KMX",	
    "KO",
    "KR",
    "KVUE",
    "L",
    "LDOS",
    "LEN",	
    "LH",
    "LHX",	
    "LII",	
    "LIN",	
    "LKQ",	
    "LLY",	
    "LMT",	
    "LNT",	
    "LOW",	
    "LRCX",
    "LULU",
    "LUV",	
    "LVS",	
    "LW",
    "LYB",	
    "LYV",	
    "MA",
    "MAA",	
    "MAR",	
    "MAS",	
    "MCD",	
    "MCHP",
    "MCK",	
    "MCO",	
    "MDLZ",
    "MDT",	
    "MET",	
    "META",
    "MGM",	
    "MHK",	
    "MKC",	
    "MKTX",
    "MLM",	
    "MMC",	
    "MMM",	
    "MNST",
    "MO",
    "MOH",	
    "MOS",	
    "MPC",	
    "MPWR",
    "MRK",	
    "MRNA",
    "MS",
    "MSCI",
    "MSFT",
    "MSI",	
    "MTB",	
    "MTCH",
    "MTD",	
    "MU",
    "NCLH",
    "NDAQ",
    "NDSN",
    "NEE",	
    "NEM",	
    "NFLX",
    "NI",
    "NKE",	
    "NOC",	
    "NOW",	
    "NRG",	
    "NSC",	
    "NTAP",
    "NTRS",
    "NUE",	
    "NVDA",
    "NVR",	
    "NWS",	
    "NWSA",
    "NXPI",
    "O",
    "ODFL",
    "OKE",	
    "OMC",	
    "ON",
    "ORCL",
    "ORLY",
    "OTIS",
    "OXY",	
    "PANW",
    "PARA",
    "PAYC",
    "PAYX",
    "PCAR",
    "PCG",	
    "PEG",	
    "PEP",	
    "PFE",	
    "PFG",	
    "PG",
    "PGR",	
    "PH",
    "PHM",	
    "PKG",	
    "PLD",	
    "PLTR",
    "PM",
    "PNC",	
    "PNR",	
    "PNW",	
    "PODD",
    "POOL",
    "PPG",	
    "PPL",	
    "PRU",	
    "PSA",	
    "PSX",	
    "PTC",	
    "PWR",	
    "PYPL",
    "QCOM",
    "RCL",	
    "REG",	
    "REGN",
    "RF",
    "RJF",	
    "RL",
    "RMD",	
    "ROK",	
    "ROL",	
    "ROP",	
    "ROST",
    "RSG",	
    "RTX",	
    "RVTY",
    "SBAC",
    "SBUX",
    "SCHW",
    "SHW",	
    "SJM",	
    "SLB",	
    "SMCI",
    "SNA",	
    "SNPS",
    "SO",
    "SOLV",
    "SPG",	
    "SPGI",
    "SRE",	
    "STE",	
    "STLD",
    "STT",	
    "STX",	
    "STZ",	
    "SW",
    "SWK",	
    "SWKS",
    "SYF",	
    "SYK",	
    "SYY",	
    "T",
    "TAP",	
    "TDG",	
    "TDY",	
    "TECH",
    "TEL",	
    "TER",	
    "TFC",	
    "TFX",	
    "TGT",	
    "TJX",	
    "TMO",	
    "TMUS",
    "TPL",	
    "TPR",	
    "TRGP",
    "TRMB",
    "TROW",
    "TRV",	
    "TSCO",
    "TSLA",
    "TSN",	
    "TT",
    "TTWO",
    "TXN",	
    "TXT",	
    "TYL",	
    "UAL",	
    "UBER",
    "UDR",	
    "UHS",	
    "ULTA",
    "UNH",	
    "UNP",	
    "UPS",	
    "URI",	
    "USB",	
    "V",
    "VICI",
    "VLO",	
    "VLTO",
    "VMC",	
    "VRSK",
    "VRSN",
    "VRTX",
    "VST",	
    "VTR",	
    "VTRS",
    "VZ",
    "WAB",	
    "WAT",	
    "WBA",	
    "WBD",	
    "WDAY",
    "WDC",	
    "WEC",	
    "WELL",
    "WFC",	
    "WM",
    "WMB",	
    "WMT",	
    "WRB",	
    "WST",	
    "WTW",	
    "WY",
    "WYNN",
    "XEL",	
    "XOM",	
    "XYL",	
    "YUM",	
    "ZBH",	
    "ZBRA",
    "ZTS",
]

# 創建空的 DataFrame 來存儲結果
columns = ["股票代碼", "Industry", "股價", "市值", "EPS", "PE Ratio", "股息收益率"]
results = pd.DataFrame(columns=columns)

# 定義一個函數來將數字轉換為 "十億" 單位
def to_billions(value):
    return round(value / 1e9, 2) if pd.notna(value) else None

# 循環處理每隻股票
for ticker_symbol in blue_chip_tickers:
    try:
        # 獲取股票數據
        ticker = yf.Ticker(ticker_symbol)
        balance_sheet = ticker.balance_sheet
        info = ticker.info
        history = ticker.history(period="1d")  # 獲取最新股價

        # 提取所需數據，並檢查是否存在
        cash = to_billions(balance_sheet.loc["Cash And Cash Equivalents", :].iloc[0]) if "Cash And Cash Equivalents" in balance_sheet.index else None
        short_term_liabilities = to_billions(balance_sheet.loc["Current Liabilities", :].iloc[0]) if "Current Liabilities" in balance_sheet.index else None
        long_term_liabilities = to_billions(balance_sheet.loc["Long Term Debt", :].iloc[0]) if "Long Term Debt" in balance_sheet.index else None
        total_assets = to_billions(balance_sheet.loc["Total Assets", :].iloc[0]) if "Total Assets" in balance_sheet.index else None
        total_liabilities = to_billions(balance_sheet.loc["Total Liabilities Net Minority Interest", :].iloc[0]) if "Total Liabilities Net Minority Interest" in balance_sheet.index else None
        net_assets = total_assets - total_liabilities if total_assets and total_liabilities else None

        # 提取數據
        price = history["Close"].iloc[-1] if not history.empty else None
        market_cap = info.get("marketCap", None)
        eps = info.get("trailingEps", None)
        pe_ratio = info.get("trailingPE", None)
        dividend_yield = info.get("dividendYield", None)

        # 取得行業資訊（若有）
        industry = info.get("industry", None)

        # 添加數據到結果
        data = {
            "股票代碼": ticker_symbol,
            "Industry": industry,
            "股價": round(price, 2) if price else None,
            "市值": round(market_cap / 1e9, 2) if market_cap else None,  # 市值以十億為單位
            "現金(十億)": round(cash, 2) if cash else None,
            "短期負債(十億)": round(short_term_liabilities, 2) if short_term_liabilities else None,
            "長期負債(十億)": round(long_term_liabilities, 2) if long_term_liabilities else None,
            "淨資產(十億)": round(net_assets, 2) if net_assets else None,
            "EPS": round(eps, 2) if eps else None,
            "PE Ratio": round(pe_ratio, 2) if pe_ratio else None,
            "股息收益率": round(dividend_yield * 100, 2) if dividend_yield else None  # 股息收益率轉為百分比
        }

        # 過濾掉所有值為 None 的欄位
        filtered_data = {key: value for key, value in data.items() if value is not None or key == "Industry"}

        # 確保過濾後的字典非空且無空欄位
        if filtered_data:  # 如果過濾後的字典非空
            # 進一步過濾掉包含NaN的欄位
            filtered_data = {key: value for key, value in filtered_data.items() if pd.notna(value)}

            # 檢查filtered_data是否非空且有有效數據
            if filtered_data:
                # 將有效數據添加到結果中
                results = pd.concat([results, pd.DataFrame([filtered_data])], ignore_index=True, sort=False)

        time.sleep(1)  # 防止被封鎖

    except Exception as e:
        print(f"處理 {ticker_symbol} 時出錯: {e}")

# 顯示所有股票的數據
print("各股票數據：")
print(results)

# 若要計算行業內的各項數值，首先需排除行業為 None 的資料
industry_data = results.dropna(subset=["Industry"])

# 對數字欄位進行分組統計：計算各行業的平均值
numeric_cols = ["股價", "市值", "現金(十億)", "短期負債(十億)", "長期負債(十億)", "淨資產(十億)", "EPS", "PE Ratio", "股息收益率"]
industry_summary = industry_data.groupby("Industry")[numeric_cols].mean().round(2).reset_index()

print("行業統計：")
print(industry_summary)

# 保存為 CSV 文件
results.to_csv("blue_chip_stocks.csv", index=False)
industry_summary.to_csv("blue_chip_industry_summary.csv", index=False)

# ---------- 繪製圖表 ----------
# 1. 熱力圖顯示各行業各指標的平均值
heatmap_data = industry_summary.set_index("Industry")[numeric_cols]

plt.figure(figsize=(14, 10))  # 調整圖表尺寸
ax = sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="viridis",
                 annot_kws={"size": 12},  # 調整註解字型大小
                 linewidths=0.5)
ax.set_title("各行業各項指標平均值熱力圖", fontsize=18)
ax.set_xlabel("指標", fontsize=16)
ax.set_ylabel("行業", fontsize=16)
plt.xticks(fontsize=14, rotation=45)  # 調整 X 軸標籤字型及旋轉角度
plt.yticks(fontsize=14)  # 調整 Y 軸標籤字型
plt.tight_layout()
plt.show()

# 2. 分面條形圖：為每個指標繪製一個條形圖
fig, axs = plt.subplots(3, 3, figsize=(24, 20))
axs = axs.flatten()

for i, col in enumerate(numeric_cols):
    axs[i].bar(industry_summary["Industry"], industry_summary[col], color="skyblue")
    axs[i].set_title(col, fontsize=16)
    axs[i].set_xlabel("行業", fontsize=16)
    axs[i].set_ylabel("平均值", fontsize=16)
    # 旋轉 X 軸標籤，避免重疊
    axs[i].tick_params(axis="x", labelsize=12, rotation=45)
    axs[i].tick_params(axis="y", labelsize=12)

plt.tight_layout()
plt.show()

# 執行一些程式碼
end_time = time.time()
execution_time = end_time - start_time
print("程式執行時間：", execution_time, "秒")