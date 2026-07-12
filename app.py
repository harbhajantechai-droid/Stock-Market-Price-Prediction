import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="AI Stock Market Predictor", page_icon="📈", layout="wide")

def load_lottie(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

lottie_ai = load_lottie("https://assets5.lottiefiles.com/packages/lf20_49rdyysj.json")

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0f172a,#1e293b,#334155);}
section[data-testid="stSidebar"]{background:#111827;}
div[data-testid="metric-container"]{
background:rgba(255,255,255,.08);
border-radius:15px;padding:12px;}
h1{color:#00E5FF;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📊 Dashboard")
stock = st.sidebar.selectbox("Select Stock",["AAPL","MSFT","GOOGL","TSLA","AMZN"])
model = st.sidebar.selectbox("Model",["XGBoost","LSTM"])

stock_file=f"data/{stock}.csv"

try:
    df=pd.read_csv(stock_file)
except FileNotFoundError:
    st.error(f"{stock_file} not found. Put {stock}.csv inside the data folder.")
    st.stop()

df.columns=df.columns.str.strip()
df["Date"]=pd.to_datetime(df["Date"])
for c in ["Open","High","Low","Close","Volume"]:
    if c in df.columns:
        df[c]=pd.to_numeric(df[c],errors="coerce")
df=df.dropna(subset=["Close"])

left,right=st.columns([2,1])
with left:
    st.title("📈 AI Stock Market Prediction Dashboard")
    st.write("Machine Learning + Deep Learning")
with right:
    if lottie_ai:
        st_lottie(lottie_ai,height=180,key="ai")

c1,c2,c3,c4=st.columns(4)
c1.metric("Rows",len(df))
c2.metric("Current Price",f"${float(df['Close'].iloc[-1]):.2f}")
c3.metric("Highest",f"${float(df['High'].max()):.2f}")
c4.metric("Lowest",f"${float(df['Low'].min()):.2f}")

start=st.date_input("Start",df["Date"].min())
end=st.date_input("End",df["Date"].max())

filtered=df[(df["Date"]>=pd.to_datetime(start))&(df["Date"]<=pd.to_datetime(end))]

st.dataframe(filtered.head())

fig=go.Figure()
fig.add_trace(go.Scatter(x=filtered["Date"],y=filtered["Close"],mode="lines",name="Close"))
fig.update_layout(template="plotly_dark",title=f"{stock} Closing Price")
st.plotly_chart(fig,use_container_width=True)

if all(col in filtered.columns for col in ["Open","High","Low","Close"]):
    st.subheader("Candlestick")
    fig2=go.Figure(data=[go.Candlestick(
        x=filtered["Date"],
        open=filtered["Open"],
        high=filtered["High"],
        low=filtered["Low"],
        close=filtered["Close"]
    )])
    st.plotly_chart(fig2,use_container_width=True)

st.download_button("Download CSV",filtered.to_csv(index=False),file_name=f"{stock}.csv",mime="text/csv")

st.markdown("---")
st.caption("Developed by Harbhajan Singh Guru")
