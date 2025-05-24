from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# 📅 주요 증시 일정 (한국시간 기준)
events = [
    ("2025-05-27 17:00", "엔비디아 실적 발표"),
    ("2025-05-28 08:00", "마이크로소프트 Build 컨퍼런스"),
    ("2025-05-29 03:00", "FOMC 의사록 공개"),
    ("2025-05-30 21:30", "미국 PCE 발표"),
    ("2025-06-01 22:00", "테슬라 AI 데이")
]

# 날짜 변환 함수
def format_kst(date_str, desc):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    m = str(dt.month)
    d = str(dt.day)
    time = dt.strftime("%H:%M")
    return f"- {m}/{d} {time}: {desc}"

# 이미지 라인 구성
lines = ["🗓 이번 주 증시 일정"]
for date_str, desc in events:
    lines.append(format_kst(date_str, desc))

# 이미지 설정
width = 550
line_height = 40
height = 20 + len(lines) * line_height
img = Image.new("RGB", (width, height), color=(20, 20, 20))
draw = ImageDraw.Draw(img)

# 폰트 설정
font_path = "C:/keys/ttf/D2Coding-Ver1.3.2-20180524.ttf"
font = ImageFont.truetype(font_path, 24)
text_color = (255, 255, 255)

# 텍스트 출력
y = 10
for line in lines:
    draw.text((10, y), line, font=font, fill=text_color)
    y += line_height

# 저장
output_path = "market_schedule_darkmode.png"
img.save(output_path)
print(f"✅ 이미지 저장 완료: {output_path}")
