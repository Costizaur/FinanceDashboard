import streamlit as st
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Finance Dashboard", layout="wide")
st.title("Live Finance Dashboard")

conn = st.connection("gsheets", type=GSheetsConnection)

def create_gauge(raw_value, title_text):
    val_str = str(raw_value).strip()
    
    try:
        if '%' in val_str:
            score = float(val_str.replace('%', '')) / 100.0
        else:
            score = float(val_str.replace(',', '.'))
    except ValueError:
        score = 0.0

    if score > 0.40:
        signal = "🚀 STRONG BUY"
    elif score > 0.10:
        signal = "✅ BUY / ACCUMULATE"
    elif score > -0.20:
        signal = "⚠️ HOLD / CAUTION"
    else:
        signal = "🛑 SELL / DEFENSIVE"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': f"{title_text}<br><span style='font-size:16px;color:gray'>{signal}</span>"},
        number={'valueformat': ".2f"}, 
        gauge={
            'axis': {'range': [-1, 1]}, 
            'bar': {'color': "black"}, 
            'steps': [
                {'range': [-1, -0.2], 'color': "#ff4b4b"},  
                {'range': [-0.2, 0.1], 'color': "#ffa600"}, 
                {'range': [0.1, 0.4], 'color': "#a3e047"},  
                {'range': [0.4, 1.0], 'color': "#27ae60"}   
            ],
        }
    ))
    
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
    return fig

if st.button("Refresh Live Data"):
    with st.spinner("Pulling latest data..."):
        df = conn.read(worksheet="Sheet6", header=None)
        
  
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_fred = create_gauge(df.iloc[0, 0], "Fred")
        st.plotly_chart(fig_fred, use_container_width=True)
        
    with col2:
        fig_etf = create_gauge(df.iloc[1, 0], "ETF")
        st.plotly_chart(fig_etf, use_container_width=True)
        
    with col3:
        fig_clasic = create_gauge(df.iloc[2, 0], "Clasic")
        st.plotly_chart(fig_clasic, use_container_width=True)
    
    with st.expander("📂 View Raw Spreadsheet Data"):
        st.dataframe(df, use_container_width=True)