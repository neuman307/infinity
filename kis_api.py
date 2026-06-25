import requests
import json

# 발급받은 키를 여기에 입력합니다. (실제 키는 절대 외부에 공개되면 안 됩니다!)
APP_KEY = "발급받은_APP_KEY를_여기에_넣으세요"
APP_SECRET = "발급받은_APP_SECRET을_여기에_넣으세요"

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
        "tr_id": "FHKST01010100"  # 해외주식 현재가 조회 암호
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

# --- 여기서부터 메인 테스트 실행 공간 (파일 맨 아래에 한 번만 작성) ---
if __name__ == "__main__":
    print("증권사 API 연동 테스트를 시작합니다...")
    
    # 1. 출입증 발급
    my_token = get_access_token()
    
    if my_token:
        # 2. TQQQ 현재가 조회
        tqqq_price = get_current_price(my_token, "TQQQ")
        
        # 3. 내친김에 SOXL 현재가도 같이 조회해보기
        soxl_price = get_current_price(my_token, "SOXL")
