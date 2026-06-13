# -*- coding: utf-8 -*-
"""
페이지: 8.3 로지스틱 회귀
Excel 활용 버전: sample_spam.xlsx의 raw 스팸 학습 데이터로
로지스틱 회귀 모델을 학습하고, 시그모이드와 로짓 변환을 손계산으로 확인.
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_curve, roc_auc_score, precision_recall_curve)

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(HERE, 'sample_spam.xlsx'))
print(f"[Excel] n = {len(df)},  스팸비율 = {df['스팸여부'].mean():.3f}\n")

features = ['단어수', '링크수', '대문자비율']
X = df[features].values
y = df['스팸여부'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 1) 로지스틱 회귀 학습
clf = LogisticRegression(max_iter=2000)
clf.fit(X_train, y_train)
print("계수 β와 오즈비 e^β:")
for name, b in zip(features, clf.coef_[0]):
    print(f"  {name}: β = {b:.5f}, e^β = {np.exp(b):.4f} "
          f"(1단위 증가 시 오즈가 {(np.exp(b)-1)*100:.2f}% 변화)")
print(f"  절편 β₀ = {clf.intercept_[0]:.4f}")

# 2) 시그모이드 손계산: P(y=1|x) = 1/(1+e^(-z))
x_sample = X_test[0]
z = clf.intercept_[0] + (clf.coef_[0] * x_sample).sum()
p_manual = 1 / (1 + np.exp(-z))
p_sklearn = clf.predict_proba(x_sample.reshape(1, -1))[0, 1]
print(f"\n--- 샘플 1개로 시그모이드 손계산 ---")
print(f"  입력: {dict(zip(features, x_sample))}")
print(f"  z = β₀ + Σ βⱼxⱼ = {z:.4f}")
print(f"  σ(z) = 1/(1+e^-z) = {p_manual:.4f}")
print(f"  sklearn predict_proba = {p_sklearn:.4f}")

# 3) 분류 성능 평가
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]
print("\n분류 보고서:")
print(classification_report(y_test, y_pred, target_names=['정상', '스팸']))
print(f"AUC = {roc_auc_score(y_test, y_prob):.4f}")

# 4) 다양한 임계값에서의 정밀도/재현율
print("\n임계값별 성능 (스팸 분류는 위양성 비용이 큼):")
for thr in [0.3, 0.5, 0.7]:
    pred = (y_prob >= thr).astype(int)
    cm = confusion_matrix(y_test, pred)
    tn, fp, fn, tp = cm.ravel()
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    print(f"  thr={thr}: 정밀도={prec:.3f}, 재현율={rec:.3f}, FP={fp}, FN={fn}")

# 5) ROC, PR 곡선
fpr, tpr, _ = roc_curve(y_test, y_prob)
pre, rec, _ = precision_recall_curve(y_test, y_prob)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(fpr, tpr, label=f'AUC = {roc_auc_score(y_test, y_prob):.3f}')
axes[0].plot([0, 1], [0, 1], 'r--')
axes[0].set_xlabel('FPR'); axes[0].set_ylabel('TPR')
axes[0].set_title('ROC 곡선')
axes[0].legend(); axes[0].grid(alpha=0.3)

axes[1].plot(rec, pre)
axes[1].set_xlabel('Recall'); axes[1].set_ylabel('Precision')
axes[1].set_title('Precision-Recall 곡선')
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.show()
