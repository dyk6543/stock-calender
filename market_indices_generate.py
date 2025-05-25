from datetime import datetime
import yfinance as yf
from PIL import Image, ImageDraw, ImageFont
import os
import time

# === 주요 지수 설정 ===
indices = {
    "^GSPC": "S&P500",
    "^IXIC": "나스닥",
    "^DJI": "다우",
    "^KS11": "코스피",
    "^KQ11": "코스닥"
}

# === 데이터 다운로드 함수 (재시도 포함) ===
def download_with_retry(tickers, max_retries=5):
    wait_times = [5, 10, 20, 40, 60]
    for attempt in range(max_retries):
        try:
            print(f"📡 데이터 다운로드 시도 {attempt + 1}/{max_retries}...")
            data = yf.download(tickers, period="5d", interval="1d", progress=False)["Close"]
            if data.dropna().empty:
                raise ValueError("❌ 데이터가 없습니다. Rate Limit 또는 휴장일일 수 있습니다.")
            return data
        except Exception as e:
            print(f"⚠️ 다운로드 실패: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ {wait_times[attempt]}초 후 재시도...")
                time.sleep(wait_times[attempt])
            else:
                print("❌ 최대 재시도 횟수 초과. 종료합니다.")
                exit()

# === 데이터 다운로드 ===
data = download_with_retry(list(indices.keys()))
last_valid_idx = data.dropna().index[-1]
prev_valid_idx = data.dropna().index[-2]

# === 이미지 설정 (밝은 배경 + 연회색 박스) ===
width = 500
line_height = 36
padding = 20
height = padding * 2 + len(indices) * line_height
img = Image.new("RGB", (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# 박스 배경
box_x0, box_y0 = padding, padding
box_x1, box_y1 = width - padding, height - padding
draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=12, fill=(245, 245, 245), outline=(220, 220, 220))

# 폰트 설정
font_path = "C:/gitupload/ttf/D2Coding-Ver1.3.2-20180524.ttf"  # 윈도우용 경로
font = ImageFont.truetype(font_path, 22)

# 텍스트 출력
y = box_y0 + 10
for ticker, name in indices.items():
    try:
        current = data.loc[last_valid_idx, ticker]
        prev = data.loc[prev_valid_idx, ticker]
        diff = current - prev
        pct = diff / prev * 100
        arrow = "▲" if diff > 0 else "▼"
        color = (0, 128, 0) if diff > 0 else (200, 0, 0)
        text = f"{name}: {current:,.2f} {arrow}{abs(pct):.2f}%"
        draw.text((box_x0 + 15, y), text, font=font, fill=color)
    except:
        draw.text((box_x0 + 15, y), f"{name}: 데이터 없음", font=font, fill=(100, 100, 100))
    y += line_height

# 이미지 저장
output_path = "C:/gitupload/market_indices_white_bg.png"
img.save(output_path)
print(f"✅ 이미지 저장 완료: {output_path}")

# GitHub 자동 업로드
os.chdir("C:/gitupload")
os.system("git add market_indices_white_bg.png")
os.system("git commit -m \"자동 업데이트: 밝은 배경 주요 지수 요약\"")
os.system("git push origin main")
print("✅ GitHub 업로드 완료")
