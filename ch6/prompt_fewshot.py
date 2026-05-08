import ollama

fewshot_prompt = """다음은 음식점 리뷰를 카테고리로 분류하는 예시입니다.

리뷰: "파스타가 정말 맛있었어요"
카테고리: 음식

리뷰: "직원이 너무 불친절했어요"
카테고리: 서비스

리뷰: "가격이 너무 비싸서 부담됐어요"
카테고리: 가격

리뷰: "인테리어가 예쁘고 분위기가 좋았어요"
카테고리: 분위기

이제 다음 리뷰를 분류해주세요. 카테고리만 답하세요.

리뷰: "자리가 좁고 너무 시끄러웠어요"
카테고리:"""

response = ollama.generate(model="gemma3:4b", prompt=fewshot_prompt)
print("분류 결과:", response["response"].strip())