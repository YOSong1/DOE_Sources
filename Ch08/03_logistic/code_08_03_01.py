# code_08_03_01.py
# -*- coding: utf-8 -*-
"""
페이지: 8.3 로지스틱 회귀 — 스팸 이메일 분류 예제.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_curve, roc_auc_score)
import statsmodels.api as sm

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 1. 가상 데이터 생성
np.random.seed(42)
n = 500
word_count = np.random.uniform(10, 500, n)
link_count = np.random.uniform(0, 20, n)
caps_ratio = np.random.uniform(0, 1, n)

logit_z = -3 + 0.005 * word_count + 0.1 * link_count + 2 * caps_ratio
prob = 1 / (1 + np.exp(-logit_z))
is_spam = np.random.binomial(1, prob)

data = pd.DataFrame({
    'WordCount': word_count,
    'LinkCount': link_count,
    'CapsRatio': caps_ratio,
    'IsSpam': is_spam
})

# 2. 학습/테스트 분리 및 적합
X = data[['WordCount', 'LinkCount', 'CapsRatio']]
y = data['IsSpam']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 3. 계수 및 오즈비
coef_df = pd.DataFrame({
    '변수': X.columns,
    '계수 (β)': model.coef_[0],
    '오즈비 (e^β)': np.exp(model.coef_[0])
})
print(coef_df.to_string(index=False))
print(f"절편: {model.intercept_[0]:.4f}")

# 4. 예측 및 성능 평가
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]
print("\n분류 보고서:")
print(classification_report(y_test, y_pred, target_names=['정상', '스팸']))

# 5. 혼동 행렬
import seaborn as sns
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['정상(예측)', '스팸(예측)'],
            yticklabels=['정상(실제)', '스팸(실제)'])
plt.title('혼동 행렬')
plt.tight_layout()
plt.show()

# 6. ROC 곡선
fpr, tpr, _ = roc_curve(y_test, y_prob)
auc = roc_auc_score(y_test, y_prob)
plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, color='blue', label=f'ROC 곡선 (AUC = {auc:.3f})')
plt.plot([0, 1], [0, 1], 'r--', label='무작위 분류기')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate (Recall)')
plt.title('ROC 곡선')
plt.legend()
plt.grid(True)
plt.show()

# 7. statsmodels로 계수 유의성
X_sm = sm.add_constant(X)
sm_model = sm.Logit(y, X_sm).fit()
print(sm_model.summary())
