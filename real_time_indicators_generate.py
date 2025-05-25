import requests
from PIL import Image, ImageDraw, ImageFont
import os

# === 데이터 수집 함수 ===

def get_usd_krw():
    try:
        res = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        krw = res.json().get("rates", {}).get("KRW")
        return f"USD/KRW: {krw:,.2f}" if krw else "USD/KRW: 데이터 없음"
    except:
        return "USD/KRW: 데이터 부족"

def get_btc_price():
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10)
        price = float(res.json().get("price"))
        return f"Bitcoin: ${price:,.2f}"
    except:
        return "Bitcoin: 데이터 부족"

def get_fear_and_greed():
    try:
        url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
        headers = {
            "X-RapidAPI-Key": "77f9af025bmsh3dc8d8c273f9d66p141ad1jsn74cd2195b16b",
            "X-RapidAPI-Host": "fear-and-greed-index.p.rapidapi.com"
        }
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()
        value = int(data["fgi"]["now"]["value"])
        label = data["fgi"]["now"]["valueText"].upper()
        return f"Fear & Greed Index: {value} ({label})"
    except:
        return "Fear & Greed Index: 데이터 부족"

# === 지표 정리 ===
lines = [
    get_usd_krw(),
    get_fear_and_greed(),
    get_btc_price()
]

# === 이미지 생성 설정 ===
width = 480
line_height = 45
padding = 30
inner_padding = 20
num_lines = len(lines)
height = num_lines * line_height + padding * 2

# 이미지 생성
img = Image.new("RGB", (width, height), color="white")
draw = ImageDraw.Draw(img)

# ✅ 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font = ImageFont.truetype(font_path, 24)
text_color = (34, 34, 34)

# 텍스트 출력
y = padding
for line in lines:
    draw.text((padding, y), line, font=font, fill=text_color)
    y += line_height

# === 이미지 저장 ===
output_path = "C:/gitupload/market_indicators_white_bg.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path)
print(f"✅ 이미지 저장 완료: {output_path}")

# === GitHub 자동 업로드 ===
os.chdir("C:/gitupload")
os.system("git add market_indicators_white_bg.png")
os.system("git commit -m \"Updated market indicators (removed VIX, added FGI label)\"")
os.system("git push origin main")
print("✅ GitHub 업로드 완료")
