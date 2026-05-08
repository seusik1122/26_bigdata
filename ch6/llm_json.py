import ollama
import json

reviews = [
    "음식이 정말 맛있고 서비스도 친절했어요. 다음에 또 올게요!",
    "웨이팅이 너무 길고 맛도 기대 이하였습니다. 실망이에요.",
    "가격 대비 양은 많은데 맛은 그냥 평범한 편이에요."
]

results = []

for review in reviews:
    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "system",
                "content": """당신은 리뷰 분석 전문가입니다.
주어진 리뷰를 분석하여 반드시 아래 JSON 형식으로만 응답하세요.
다른 텍스트는 포함하지 마세요.

{"sentiment": "긍정/부정/중립", "confidence": 0.0~1.0, "keywords": ["키워드1", "키워드2"]}"""
            },
            {
                "role": "user",
                "content": review
            }
        ]
    )

    raw = response["message"]["content"]

    # JSON 파싱 시도
    try:
        # LLM이 ```json ... ``` 으로 감싸서 응답할 수 있음
        clean = raw.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()

        data = json.loads(clean)
        results.append(data)
        print(f"리뷰: {review[:25]}...")
        print(f"   감성: {data['sentiment']}, 확신도: {data['confidence']}")
        print(f"   키워드: {data['keywords']}")
    except json.JSONDecodeError:
        print(f"JSON 파싱 실패: {raw[:100]}")

    print("-" * 50)

print(f"\n총 {len(results)}개 리뷰 분석 완료")