# code_20_08_03.py
# Chapter 20.08 코드 3: DOE 결과 payload 구성 + LLM 리뷰 프롬프트

import json

analysis_payload = {
    "task": "DOE result review",
    "goal": "수축률을 낮추고 인장강도를 유지하는 공정 조건 해석",
    "design": "2^4 factorial design with center points",
    "responses": ["Shrinkage", "TensileStrength"],
    "significant_effects": {
        "Shrinkage": ["Temperature", "Pressure", "Temperature:Pressure"],
        "TensileStrength": ["CoolingTime"]
    },
    "model_fit": {
        "Shrinkage_R2": 0.84,
        "TensileStrength_R2": 0.76
    },
    "draft_interpretation": "온도와 압력을 낮추면 수축률이 감소하며, 냉각 시간은 인장강도 유지에 중요하다.",
    "questions": [
        "이 해석이 과도한지 검토해줘",
        "상호작용 해석에서 주의할 점이 있는지 알려줘",
        "다중 응답 최적화를 위해 어떤 후속 분석이 필요한지 제안해줘"
    ]
}

prompt = f"당신은 실험계획법 리뷰어입니다. JSON 으로 답하세요.\n\n{json.dumps(analysis_payload, ensure_ascii=False, indent=2)}"

print(prompt)
