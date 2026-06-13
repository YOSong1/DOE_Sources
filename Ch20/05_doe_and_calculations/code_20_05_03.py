# code_20_05_03.py
# Chapter 20.05 코드 3: 응답 표면 모형의 정상점 계산
#
# 2차 다항 모형 y = b0 + b'x + 0.5 * x' * 2B * x 에서
# 기울기 ∇y = b + 2B x = 0 을 풀어 정상점 x* = -B⁻¹ b / 2 를 구합니다.
# 정상점이 설계 영역 [-1, 1]^k 밖에 있으면 경계 최적화가 필요하다는 점을
# payload 로 LLM 에 검토 요청합니다.

import json

import numpy as np


# 1) 모형 — 2요인 (Temperature, Pressure) 2차 모형 계수 (예시)
#    y = 50 + 6*x1 + 4*x2 - 3*x1^2 - 2*x2^2 - 1.5*x1*x2
b0 = 50.0
b = np.array([6.0, 4.0])         # 1차 계수
B = np.array([                     # 2차 계수 (대각=제곱항, 비대각=교호작용/2)
    [-3.0, -0.75],
    [-0.75, -2.0],
])


# 2) 정상점 계산:  2 B x* = -b   →   x* = -(2B)^-1 b
x_star = np.linalg.solve(2 * B, -b)


# 3) 정상점에서의 예측 y*
y_star = b0 + b @ x_star + x_star @ B @ x_star


# 4) 설계 영역 안인지 확인 + 경계 최적화 (안에 있으면 같은 점, 밖이면 경계로 투영)
inside = bool(np.all(np.abs(x_star) <= 1.0))
x_bounded = np.clip(x_star, -1.0, 1.0)
y_bounded = b0 + b @ x_bounded + x_bounded @ B @ x_bounded


# 5) eigenvalue 로 정상점 유형 판정 (max / min / saddle)
eigvals, _ = np.linalg.eigh(B)
if np.all(eigvals < 0):
    point_type = "maximum (오목)"
elif np.all(eigvals > 0):
    point_type = "minimum (볼록)"
else:
    point_type = "saddle (안장점)"


payload = {
    "task":   "response surface stationary point review",
    "goal":   "2차 응답표면의 정상점과 설계 영역 적합성 검토",
    "factors": ["Temperature_coded", "Pressure_coded"],
    "stationary_point": {
        "x_star":  x_star.tolist(),
        "y_star":  float(y_star),
        "type":    point_type,
        "inside_design_region": inside,
        "eigenvalues": eigvals.tolist(),
    },
    "bounded_optimum": {
        "x":  x_bounded.tolist(),
        "y":  float(y_bounded),
        "note": "정상점이 영역 안이면 동일, 밖이면 [-1, 1]^k 로 투영",
    },
    "questions": [
        "정상점 유형(max/min/saddle)이 실험 목적과 부합하는지 검토해줘",
        "정상점이 설계 영역 밖이면 추가 실험 영역을 어떻게 잡아야 할지 제안해줘",
        "경계 최적화 결과를 그대로 채택해도 되는지 의견을 줘",
    ],
}
print(json.dumps(payload, ensure_ascii=False, indent=2))
