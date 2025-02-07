from flask import Flask, request, render_template_string
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

def generate_chart_html(ticker_symbol, k_period=9, d_period=3, smooth_k=3):
    data = yf.download(ticker_symbol, start="2024-01-01", end="2025-02-08")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    data.index = pd.to_datetime(data.index)
    data.fillna(method="ffill", inplace=True)
    data.fillna(method="bfill", inplace=True)
    
    if data["Close"].isnull().all():
        print(f"{ticker_symbol} 数据缺失，无法计算 MACD")
        return "<p>Error: Missing price data</p>"

    # 计算 KD 指标
    data.ta.stoch(k=k_period, d=d_period, smooth_k=smooth_k, append=True)
    
    for col in data.columns:
        if "STOCHk" in col:
            data.rename(columns={col: "K"}, inplace=True)
        if "STOCHd" in col:
            data.rename(columns={col: "D"}, inplace=True)
    
    # 计算布林带 (Bollinger Bands)
    data.ta.bbands(length=20, append=True)
    
    # 计算 MACD
    data.ta.macd(fast=12, slow=26, signal=9, append=True)
    data.rename(columns={"MACD_12_26_9": "DIF", "MACDs_12_26_9": "MACD_Signal"}, inplace=True)
    
    print(data.tail())  # 调试信息，查看数据是否正确
    print(data.columns) # 检查列名
    
    # 计算均线
    for length in [10, 20, 60, 120, 240]:
        data[f"MA_{length}"] = ta.sma(data["Close"], length=length)

    # 创建图表
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.03,
                        row_heights=[0.5, 0.2, 0.15, 0.15],
                        subplot_titles=(f"{ticker_symbol} - Price & Indicators", "KD Indicator", "MACD", "Volume"))

    # (1) K 线 + 均线
    fig.add_trace(go.Candlestick(x=data.index, open=data["Open"], high=data["High"], 
                                 low=data["Low"], close=data["Close"], name="Candlestick"), row=1, col=1)
    for length in [10, 20, 60, 120, 240]:
        fig.add_trace(go.Scatter(x=data.index, y=data[f"MA_{length}"], name=f"{length}-Day MA"), row=1, col=1)

    # (2) KD 指标
    fig.add_trace(go.Scatter(x=data.index, y=data["K"], name="K Line"), row=2, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data["D"], name="D Line"), row=2, col=1)

    # (3) MACD
    fig.add_trace(go.Scatter(x=data.index, y=data["DIF"], name="DIF"), row=3, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data["MACD_Signal"], name="Signal Line"), row=3, col=1)

    # (4) 成交量
    fig.add_trace(go.Bar(x=data.index, y=data["Volume"], name="Volume"), row=4, col=1)

    # 计算 5 日、10 日均量
    data["Vol_5"] = data["Volume"].rolling(5).mean()
    data["Vol_10"] = data["Volume"].rolling(10).mean()

    # 获取最新数值
    latest_k = round(data["K"].iloc[-1], 2)
    latest_d = round(data["D"].iloc[-1], 2)
    latest_dif = round(data["DIF"].iloc[-1], 2)
    latest_signal = round(data["MACD_Signal"].iloc[-1], 2)
    latest_vol_5 = round(data["Vol_5"].iloc[-1], 0)
    latest_vol_10 = round(data["Vol_10"].iloc[-1], 0)

    # **动态标题**
    chart_title = f"{ticker_symbol} | K: {latest_k} | D: {latest_d} | DIF: {latest_dif} | MACD9: {latest_signal} | 5日均量: {latest_vol_5} | 10日均量: {latest_vol_10}"


    fig.update_layout(title=chart_title, xaxis_rangeslider_visible=False, height=1200, template="plotly_dark")

    return fig.to_html(full_html=False)

@app.route("/chart", methods=["GET"])
def stock_chart():
    tickers = request.args.get("ticker", "AAPL").split(",")
    k_period = int(request.args.get("k", 9))
    d_period = int(request.args.get("d", 3))
    smooth_k = int(request.args.get("smooth_k", 3))

    charts_html = "".join([generate_chart_html(ticker, k_period, d_period, smooth_k) for ticker in tickers])

    return render_template_string(
        "<html><head><title>Stock Charts</title></head><body>{{ charts|safe }}</body></html>",
        charts=charts_html
    )

print('Stock Chart Server is running...')
stock = str(input("stock code: "))
print(f'http://127.0.0.1:5000/chart?ticker={stock}')

if __name__ == "__main__":
    app.run(debug=True)
