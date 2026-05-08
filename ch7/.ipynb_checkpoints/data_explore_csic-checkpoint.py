"""
CSIC Database 데이터 로드 및 전체 출력
실행: python data_explore_csic.py
"""

import pandas as pd
import os

# ============================================================
# 1. 데이터 로드
# ============================================================
print("=" * 65)
print("  CSIC Database 데이터 로드 및 탐색")
print("=" * 65)

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()

data_path = os.path.join(SCRIPT_DIR, "data", "archive", "csic_database.csv")

if not os.path.exists(data_path):
    print(f"\n  !! 파일을 찾을 수 없습니다: {data_path}")
    exit()

df = pd.read_csv(data_path)

print(f"\n  데이터 로드 완료!")
print(f"  파일: {data_path}")
print(f"  크기: {df.shape[0]:,}행 x {df.shape[1]}열")

# ============================================================
# 2. 기본 정보 확인
# ============================================================
print(f"\n{'─' * 65}")
print("  [1] 컬럼 목록")
print(f"{'─' * 65}")
for i, col in enumerate(df.columns):
    print(f"    {i:2d}. {col}")

print(f"\n{'─' * 65}")
print("  [2] 라벨 분포 (Normal vs Anomalous)")
print(f"{'─' * 65}")
label_counts = df["label"].value_counts()
label_ratio = df["label"].value_counts(normalize=True) * 100
for label in label_counts.index:
    count = label_counts[label]
    ratio = label_ratio[label]
    bar = "█" * int(ratio / 2)
    print(f"  {label:<12s} | {count:>8,} | {ratio:>5.1f}% | {bar}")

# ============================================================
# 3. 만개 데이터 전체 출력
# ============================================================
print(f"\n{'─' * 65}")
print(f"  [3] 전체 데이터 출력 ({len(df):,}건)")
print(f"{'─' * 65}\n")

pd.set_option("display.max_rows", 10000)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 80)
pd.set_option("display.width", 200)

print(df.to_string())

print(f"\n{'=' * 65}")
print(f"  출력 완료: 총 {len(df):,}건")
print(f"{'=' * 65}")
