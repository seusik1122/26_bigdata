import ollama

reviews = [
    "음식이 너무 맛있었어요! 특히 파스타가 최고였고 직원들도 친절했습니다.",
    "최악의 식당이었어요. 음식이 차갑게 나오고 서비스도 불친절했습니다.",
    "평범한 식당이에요. 가격 대비 그냥 무난한 수준이었습니다.",
    "분위기는 정말 좋았는데 음식 양이 너무 적어서 아쉬웠어요."
]

for review in reviews:
    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "system",
                "content": "당신은 감성 분석 전문가입니다. 주어진 리뷰의 감성을 '긍정', '부정', '중립' 중 하나로 분류하고, 이유를 한 문장으로 설명해주세요."
            },
            {
                "role": "user",
                "content": f"다음 리뷰를 분석해주세요: {review}"
            }
        ]
    )
    print(f"리뷰: {review[:30]}...")
    print(f"분석: {response['message']['content']}")
    print("-" * 60)