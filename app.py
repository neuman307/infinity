import streamlit as st
import database
import kis_api  # 방금 만든 한투 API 파일을 불러옵니다.

# 1. DB 초기화 (앱이 켜질 때 한 번 실행)
database.init_db()

# 2. 페이지 기본 설정
st.set_page_config(page_title="자동매매 대시보드", layout="wide")
st.title("🤖 VR & 무한매수 자동매매 봇")

# 3. 실시간 데이터 가져오기 (API 연동)
# 토큰을 발급받고, 성공하면 TQQQ 현재가를 조회합니다.
token = kis_api.get_access_token()

if token:
    bot_state = "정상 작동 중 🟢"
    current_price = kis_api.get_current_price(token, "TQQQ")
    
    # 시가총액 계산 (현재가 * 임의의 발행주식수 * 환율 1400원 가정) 후 '조' 단위 변환
    if current_price:
        market_cap_krw = current_price * 380_000_000 * 1400
        tqqq_market_cap = f"{market_cap_krw / 1_000_000_000_000:.1f}조 원"
    else:
        tqqq_market_cap = "계산 불가"
else:
    bot_state = "API 연결 실패 🔴"
    current_price = 0.0
    tqqq_market_cap = "연결 오류"

# 가상의 내 계좌 데이터 (추후 DB와 잔고조회 API로 대체)
yield_rate = "+4.2%"
total_budget = "40,000"
current_balance = "2,500"

# 4. 화면에 데이터 뿌려주기
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="시스템 상태", value=bot_state)
with col2:
    # 기존 '현재 누적 수익률' 자리에 '실시간 현재가'를 띄워봅니다.
    price_text = f"${current_price:.2f}" if current_price else "N/A"
    st.metric(label="TQQQ 현재가 (실시간)", value=price_text)
with col3:
    st.metric(label="대상 ETF 시가총액", value=tqqq_market_cap)

st.divider() # 구분선

# 자금 현황 섹션
st.subheader("💰 자금 현황")
st.write(f"- **총 배정 예산:** ${total_budget}")
st.write(f"- **현재 남은 예수금:** ${current_balance}")
