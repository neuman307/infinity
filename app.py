import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="자동매매 대시보드", layout="wide")

st.title("🤖 VR & 무한매수 자동매매 봇")

# 가상의 데이터 (추후 API 연동 시 실제 데이터로 교체)
bot_state = "정상 작동 중 🟢"
yield_rate = "+4.2%"
tqqq_market_cap = "35.4조 원" 
total_budget = "40,000"
current_balance = "2,500"

# 상단 요약 카드 (3개의 컬럼으로 분할)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="시스템 상태", value=bot_state)
with col2:
    st.metric(label="현재 누적 수익률", value=yield_rate)
with col3:
    st.metric(label="대상 ETF 시가총액", value=tqqq_market_cap)

st.divider() # 구분선

# 자금 현황 섹션
st.subheader("💰 자금 현황")
st.write(f"- **총 배정 예산:** ${total_budget}")
st.write(f"- **현재 남은 예수금:** ${current_balance}")

# 추후 여기에 매매 기록을 판다스(Pandas) 데이터프레임으로 예쁘게 띄울 수 있습니다.
