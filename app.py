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

def check_trade_action(current_value, target_value, tolerance=0.05):
    """
    현재 평가금액과 목표 가치를 비교하여 매수/매도 여부를 결정하는 함수
    :param current_value: 현재 내 주식의 총 평가금액
    :param target_value: 오늘 도달해야 할 목표 가치
    :param tolerance: 상/하단 밴드 오차율 (기본값 5%, 즉 0.05)
    :return: (행동, 거래해야 할 금액)
    """
    # 상단 밴드와 하단 밴드 계산
    upper_band = target_value * (1 + tolerance)
    lower_band = target_value * (1 - tolerance)

    if current_value > upper_band:
        # 평가금이 상단 밴드보다 높으면, 그 차액만큼 매도하여 수익 실현
        sell_amount = current_value - upper_band
        return "SELL 🔴", sell_amount
        
    elif current_value < lower_band:
        # 평가금이 하단 밴드보다 낮으면, 그 차액만큼 추가 매수
        buy_amount = lower_band - current_value
        return "BUY 🟢", buy_amount
        
    else:
        # 밴드 안에 있다면 아무것도 하지 않음
        return "HOLD ⚪", 0

# --- 로직 테스트 (가상의 상황) ---
today_target = 1000  # 오늘의 목표 가치: $1000
my_stock_value = 920 # 내 주식의 현재 평가금: $920 (하락장)

action, amount = check_trade_action(my_stock_value, today_target, tolerance=0.05)
print(f"오늘의 추천 행동: {action}, 금액: ${amount:.2f}")
# 출력 결과 예상: BUY 🟢, 금액: $30.00 (하단 밴드 950 - 현재가 920)
