import sqlite3
import os

DB_NAME = "trading_bot.db"

def init_db():
    """데이터베이스 파일과 테이블을 초기화하는 함수"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. 자금 상태 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_budget REAL NOT NULL,      -- 총 배정 원금 (예: 40000)
            current_cash REAL NOT NULL,      -- 현재 보유 중인 달러 예수금
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. 봇 전략 상태 테이블 (무한매수/VR 상태 저장)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bot_status (
            strategy_name TEXT PRIMARY KEY,  -- 전략 이름 (예: 'infinite_tqqq', 'vr_soxl')
            current_cycle INTEGER DEFAULT 1, -- 현재 진행 중인 사이클/회차 (예: 1~40)
            target_value REAL DEFAULT 0,     -- VR 전략의 현재 목표 가치 (Vt)
            average_price REAL DEFAULT 0,    -- 현재 보유 주식의 평단가
            holding_quantity REAL DEFAULT 0  -- 현재 보유 주식 수량
        )
    """)

    # 3. 매매 기록 이력 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trading_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            strategy_name TEXT NOT NULL,     -- 어떤 봇이 주문했는지
            ticker TEXT NOT NULL,            -- 종목명 (TQQQ, SOXL 등)
            action TEXT NOT NULL,            -- BUY / SELL
            quantity REAL NOT NULL,          -- 수량
            price REAL NOT NULL,             -- 체결 가격
            amount REAL NOT NULL             -- 총 거래 금액 (수량 * 가격)
        )
    """)

    # 초기 데이터 세팅 (테이블이 비어있을 때만 기본값 입력)
    cursor.execute("SELECT COUNT(*) FROM assets")
    if cursor.fetchone()[0] == 0:
        # 최초 자금 세팅: 총 원금 $40,000 / 예수금 $40,000
        cursor.execute("INSERT INTO assets (total_budget, current_cash) VALUES (40000, 40000)")
        
        # 최초 봇 상태 세팅
        cursor.execute("INSERT INTO bot_status (strategy_name, current_cycle, target_value) VALUES ('infinite_tqqq', 1, 0)")
        cursor.execute("INSERT INTO bot_status (strategy_name, current_cycle, target_value) VALUES ('vr_tqqq', 1, 1000)")

    conn.commit()
    conn.close()
    print("데이터베이스 초기화 완료!")

if __name__ == "__main__":
    init_db()
