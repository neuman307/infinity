import requests
import json

# 1. API 키 및 계좌정보 세팅
APP_KEY = "발급받은_APP_KEY를_여기에_넣으세요"
APP_SECRET = "발급받은_APP_SECRET을_여기에_넣으세요"
ACCOUNT_NO = "모의투자_계좌번호_앞8자리"  # 예: "50001234"

# 모의투자용 기본 URL 
BASE_URL = "https://openapivts.koreainvestment.com:29443"

def get_access_token():
    """한투 API 모의투자 접근 토큰(일일 출입증)을 발급받는 함수"""
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    
    url = f"{BASE_URL}/oauth2/tokenP"
    res = requests.post(url, headers=headers, data=json.dumps(body))
    
    if res.status_code == 200:
        my_token = res.json()["access_token"]
        print("🟢 출입증(토큰) 발급 성공!")
        return my_token
    else:
        print("🔴 토큰 발급 실패:", res.text)
        return None

def get_current_price(token, ticker="TQQQ"):
    """해외주식 현재 체결가를 조회하는 함수"""
    url = f"{BASE_URL}/uapi/overseas-price/v1/quotations/price"
    
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHKST01010100"  
    }
    
    params = {
        "AUTH": "",
        "EXCD": "NAS",
        "SYMB": ticker
    }
    
    res = requests.get(url, headers=headers, params=params)
    
    if res.status_code == 200:
        data = res.json()
        current_price = float(data["output"]["last"])
        print(f"📈 {ticker} 현재가: ${current_price:.2f}")
        return current_price
    else:
        print("🔴 현재가 조회 실패:", res.text)
        return None

def send_order(token, order_type, ticker, quantity, price):
    """
    미국 주식 매수/매도 주문을 전송하는 함수
    :param order_type: "BUY" 또는 "SELL"
    :param ticker: 종목명 (예: "TQQQ")
    :param quantity: 주문 수량 (정수)
    :param price: 주문 단가 (지정가)
    """
    url = f"{BASE_URL}/uapi/overseas-stock/v1/trading/order"
    
    # 매수/매도에 따라 tr_id 분기 처리 (모의투자 기준)
    tr_id = "VTTT1002U" if order_type == "BUY" else "VTTT1006U"
    
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": tr_id
    }
    
    body = {
        "CANO": ACCOUNT_NO,         # 종합계좌번호 앞 8자리
        "ACNT_PRDT_CD": "01",       # 계좌상품코드 (보통 01)
        "OVRS_EXCG_CD": "NAS",      # 거래소코드 (나스닥 NAS)
        "PDNO": ticker,             # 종목코드
        "ORD_QTY": str(quantity),   # 주문 수량 (문자열로 전달해야 함)
        "OVRS_ORD_UNPR": str(price),# 주문 단가 (문자열로 전달해야 함)
        "ORD_DVSN": "00"            # 주문구분 (00: 지정가)
    }
    
    res = requests.post(url, headers=headers, data=json.dumps(body))
    
    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        print(f"✅ [{order_type}] {ticker} {quantity}주 주문 전송 완료!")
        return True
    else:
        print(f"❌ [{order_type}] 주문 실패:", res.text)
        return False

# --- 메인 테스트 실행 공간 ---
if __name__ == "__main__":
    print("증권사 API 연동 테스트를 시작합니다...")
    
    my_token = get_access_token()
    
    if my_token:
        # TQQQ 현재가 조회
        tqqq_price = get_current_price(my_token, "TQQQ")
        
        # [테스트] 방금 조회한 현재가보다 10달러 낮게, TQQQ 1주 지정가 매수 주문 넣어보기
        # (현재가보다 낮게 걸어두므로 실제 체결은 안 되고 주문 접수만 됩니다)
        if tqqq_price:
            test_order_price = tqqq_price - 10 
            send_order(my_token, "BUY", "TQQQ", 1, test_order_price)
