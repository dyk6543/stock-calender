from datetime import datetime
import yfinance as yf
from PIL import Image, ImageDraw, ImageFont
import os

# === 주요 지수 설정 ===
indices = {
    "^GSPC": "S&P500",
    "^IXIC": "나스닥",
    "^DJI": "다우",
    "^KS11": "코스피",
    "^KQ11": "코스닥"
}

# === 데이터 다운로드 (최근 거래일 기준 자동 탐색) ===
data = yf.download(list(indices.keys()), period="5d", interval="1d", progress=False)["Close"]
last_valid_idx = data.dropna().index[-1]
prev_valid_idx = data.dropna().index[-2]
today_str = last_valid_idx.strftime("%Y-%m-%d")

# === 데이터 포맷 구성 ===
formatted = []
for ticker, name in indices.items():
    try:
        current = data.loc[last_valid_idx, ticker]
        prev = data.loc[prev_valid_idx, ticker]
        diff = current - prev
        pct = diff / prev * 100
        arrow = "▲" if diff > 0 else "▼"
        formatted.append(f"{name}: {current:,.2f} {arrow}{abs(pct):.2f}%")
    except:
        formatted.append(f"{name}: 데이터 없음")

# === 이미지 생성 ===
width, height = 480, 40 + len(formatted) * 32
img = Image.new("RGB", (width, height), color=(20, 20, 20))
draw = ImageDraw.Draw(img)

font_path = "C:/keys/ttf/D2Coding-Ver1.3.2-20180524.ttf"  # 한글+고정폭 폰트
font = ImageFont.truetype(font_path, 24)

draw.text((10, 10), f"📊 주요 지수 요약 ({today_str})", font=font, fill=(255, 255, 255))
y = 50
for line in formatted:
    draw.text((10, y), line, font=font, fill=(255, 255, 255))
    y += 32

# === 이미지 저장 ===
output_path = "C:/keys/market_indices_darkmode.png"
img.save(output_path)
print(f"✅ 이미지 저장 완료: {output_path}")

# === GitHub 자동 업로드 ===
os.chdir("C:/keys")  # Git 저장소 루트로 이동
os.system("git add market_indices_darkmode.png")
os.system("git commit -m \"자동 업데이트: 주요 지수 요약\"")
os.system("git push origin main")
print("✅ GitHub 업로드 완료")
