from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import yfinance as yf
import time
import os

# === 실시간 지표 설정 ===
symbols = {
    "VIX": "^VIX",
    "USD/KRW": "KRW=X",
    "10Y 국채금리": "^TNX",
    "비트코인": "BTC-USD"
}

# === 데이터 다운로드 함수 (재시도 포함) ===
def download_recent_2(ticker, max_retries=5):
    wait_times = [3, 5, 10, 15, 20]
    for attempt in range(max_retries):
        try:
            print(f"📡 {ticker} 데이터 다운로드 시도 {attempt + 1}/{max_retries}")
            df = yf.download(ticker, period="2d", interval="1d", progress=False)["Close"]
            if df.dropna().empty:
                raise ValueError("❌ 데이터 없음")
            return df
        except Exception as e:
            print(f"⚠️ 실패: {e}")
            if attempt < max_retries - 1:
                time.sleep(wait_times[attempt])
            else:
                return None

# === 지표 요약 구성 ===
formatted = []
for label, ticker in symbols.items():
    time.sleep(2)  # Rate limit 우회
    df = download_recent_2(ticker)
    if df is None or df.shape[0] < 2:
        formatted.append(f"{label}: 데이터 부족")
    else:
        today, prev = df.iloc[-1], df.iloc[-2]
        diff = today - prev
        pct = diff / prev * 100
        sign = "▲" if diff > 0 else "▼"
        if "USD" in label or "비트코인" in label:
            formatted.append(f"{label}: ${today:,.2f} ({sign}{abs(pct):.2f}%)")
        elif "국채" in label:
            formatted.append(f"{label}: {today:.2f}% ({sign}{abs(pct):.2f}%)")
        else:
            formatted.append(f"{label}: {today:,.2f} ({sign}{abs(pct):.2f}%)")

# === 이미지 설정 ===
width = 480
line_height = 40
height = 40 + len(formatted) * line_height
img = Image.new("RGB", (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# === 박스 배경 추가 ===
box_margin = 20
box_x0 = box_margin
box_y0 = box_margin
box_x1 = width - box_margin
box_y1 = height - box_margin
draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(245, 245, 245), outline=(200, 200, 200))

# === 폰트 설정 ===
font_path = "C:/gitupload/ttf/D2Coding-Ver1.3.2-20180524.ttf"
font = ImageFont.truetype(font_path, 22)
text_color = (34, 34, 34)

# === 텍스트 출력 ===
y = box_y0 + 10
for line in formatted:
    draw.text((box_x0 + 10, y), line, font=font, fill=text_color)
    y += line_height

# === 이미지 저장 ===
output_path = "C:/gitupload/market_indicators_white_bg.png"
img.save(output_path)
print(f"✅ 이미지 저장 완료: {output_path}")

# === GitHub 업로드 ===
os.chdir("C:/gitupload")
os.system("git add market_indicators_white_bg.png")
os.system("git add real_time_indicators_generate.py")
os.system("git commit -m \"자동 업데이트: 주요 실시간 지표\"")
os.system("git push origin main")
print("✅ GitHub 업로드 완료")
