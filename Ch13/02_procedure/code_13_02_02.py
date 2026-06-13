# code_13_02_02.py
# -*- coding: utf-8 -*-
"""
페이지: 13.2 응답 표면 방법론의 일반적인 절차
설명: 적합된 2차 모형의 반응 표면 등고선도 시각화 예시.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# 적합된 모형: y_hat = 90 - 5*x1^2 - 3*x2^2 + 2*x1*x2 + 1*x1 + 2*x2
def y_hat(x1, x2):
    return 90 - 5*x1**2 - 3*x2**2 + 2*x1*x2 + 1*x1 + 2*x2

x1 = np.linspace(-2, 2, 100)
x2 = np.linspace(-2, 2, 100)
X1, X2 = np.meshgrid(x1, x2)
Y = y_hat(X1, X2)

plt.figure(figsize=(8, 6))
cp = plt.contourf(X1, X2, Y, levels=20, cmap='RdYlGn')
plt.colorbar(cp)
plt.xlabel('$x_1$ (코드화된 요인 1)')
plt.ylabel('$x_2$ (코드화된 요인 2)')
plt.title('반응 표면 등고선도')
plt.show()
