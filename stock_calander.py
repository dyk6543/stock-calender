from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

# 📅 주요 증시 일정 (한국시간 기준)
events = [
    ("2025-05-27 17:00", "엔비디아 실적 발표"),
    ("2025-05-28 08:00", "마이크로소프트 Build 컨퍼런스"),
    ("2025-05-29 03:00", "FOMC 의사록 공개"),
    ("2025-05-30 21:30", "미국 PCE 발표"),
    ("2025-06-01 22:00", "테슬라 AI 데이")
]

# 날짜 포맷 변환 함수
def format_kst(date_str, desc):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    m = str(dt.month)
    d = str(dt.day)
    time = dt.strftime("%H:%M")
    return f"- {m}/{d} {time}: {desc}"

lines = [format_kst(date_str, desc) for date_str, desc in events]

# === 이미지 설정 ===
width = 550
line_height = 40
padding = 20
height = padding * 2 + len(lines) * line_height

# 흰 배경 + 연회색 카드박스
img = Image.new("RGB", (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# 라운드 사각형 (배경 박스)
box_x0, box_y0 = padding, padding
box_x1, box_y1 = width - padding, height - padding
draw.rounded_rectangle(
    [box_x0, box_y0, box_x1, box_y1],
    radius=12,
    fill=(245, 245, 245),
    outline=(220, 220, 220)
)

# 폰트 설정 (한글 폰트 사용)
font_path = "C:/gitupload/ttf/D2Coding-Ver1.3.2-20180524.ttf"
font = ImageFont.truetype(font_path, 24)
text_color = (34, 34, 34)

# 텍스트 출력
y = box_y0 + 10
for line in lines:
    draw.text((box_x0 + 10, y), line, font=font, fill=text_color)
    y += line_height

# 이미지 저장
output_path = "C:/gitupload/market_schedule_white_bg.png"
img.save(output_path)
print(f"✅ 이미지 저장 완료: {output_path}")

# GitHub 자동 업로드
os.chdir("C:/gitupload")
os.system("git add market_schedule_white_bg.png")
os.system("git commit -m \"자동 업데이트: 밝은 배경용 증시 일정 카드\"")
os.system("git push origin main")
print("✅ GitHub 업로드 완료")
