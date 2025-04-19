import numpy as np


def calculate_bonus_points(original_volume, refined_volume):
  """
  원어와 다듬은 말의 검색량 비교에 따른 가산점 계산

  | 대조군(원어) | 다듬은 말 | 가산점 |
  | ---------- | --------- | ----- |
  | 100%       | 50%       | -2    |
  | 100%       | 67%       | 0     |
  | 150%       | 100%      | +1    |
  | 100%       | 100%      | +2    |
  | 80%        | 100%      | +3    |
  | 60%        | 100%      | +4    |
  """
  # 둘 다 검색량이 0인 경우 처리
  if original_volume == 0 and refined_volume == 0:
    return 0

  # 원어 검색량이 0인 경우 (다듬은 말만 검색되는 경우)
  if original_volume == 0:
    return 4 if refined_volume > 0 else 0

  # 다듬은 말의 검색량이 0인 경우
  if refined_volume == 0:
    return -2

  # 검색량 비율 계산
  ratio = refined_volume / original_volume

  # 비율별 가산점 계산 (보간법 사용)
  if ratio <= 0.5:  # 50% 이하
    return -2
  elif ratio <= 0.67:  # 50% ~ 67%
    return -2 + (ratio - 0.5) * (2 / 0.17)  # -2에서 0으로 보간
  elif ratio <= 1.0:  # 67% ~ 100%
    return 0 + (ratio - 0.67) * (2 / 0.33)  # 0에서 2로 보간
  elif ratio <= 1.25:  # 100% ~ 125%
    return 2 + (ratio - 1.0) * (1 / 0.25)  # 2에서 3으로 보간
  elif ratio <= 1.67:  # 125% ~ 167%
    return 3 + (ratio - 1.25) * (1 / 0.42)  # 3에서 4로 보간
  else:  # 167% 이상
    return 4


def get_rounded_bonus(original_volume, refined_volume):
  """
  계산된 가산점을 반올림하여 정수로 반환
  """
  raw_bonus = calculate_bonus_points(original_volume, refined_volume)
  return round(raw_bonus)
