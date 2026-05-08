import ollama

article = """
전 세계적으로 전기차 보급이 빠르게 확산되고 있다. 국제에너지기구(IEA)에 따르면
2023년 전 세계 전기차 판매량은 1,400만 대를 돌파하며 역대 최고치를 기록했다.
한국에서도 현대·기아차가 글로벌 전기차 시장에서 점유율을 꾸준히 높이고 있으며,
배터리 기술 혁신을 통해 1회 충전 주행거리가 700km를 넘어서는 모델도 출시됐다.
그러나 충전 인프라 부족과 배터리 폐기물 처리 문제는 여전히 해결해야 할 과제로
남아 있으며, 정부의 보조금 정책과 규제 정비가 병행되어야 한다는 목소리가 높다.
"""

print("=== 키워드 추출 ===")
response = ollama.chat(
    model="gemma3:4b",
    messages=[
        {"role": "system", "content": "주어진 텍스트에서 핵심 키워드 5개를 추출하세요. 키워드만 쉼표로 구분하여 나열하세요."},
        {"role": "user", "content": article}
    ]
)
print(response["message"]["content"])

print("\n=== 3줄 요약 ===")
response = ollama.chat(
    model="gemma3:4b",
    messages=[
        {"role": "system", "content": "주어진 텍스트를 정확히 3줄로 요약하세요. 각 줄은 한 문장으로 작성하세요."},
        {"role": "user", "content": article}
    ]
)
print(response["message"]["content"])