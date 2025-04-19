import time
from pytrends.request import TrendReq


class GoogleTrendsHelper:
  def __init__(self, hl='ko-KR', tz=540):
    self.pytrends = TrendReq(hl=hl, tz=tz)
    self.last_request = 0
    self.min_wait_time = 1  # 초 단위

  def get_interest_over_time(self, keywords, timeframe='today 1-m', geo='KR'):
    """
    주어진 키워드들의 시간별 검색 관심도를 가져옴
    """
    # API 요청 간 간격 유지
    self._wait_between_requests()

    # API 호출
    try:
      self.pytrends.build_payload(
        kw_list=keywords, timeframe=timeframe, geo=geo)
      result = self.pytrends.interest_over_time()
      return result
    except Exception as e:
      print(f"검색 트렌드 가져오기 실패: {keywords} - {e}")
      return None

  def compare_terms(self, term1, term2, timeframe='today 1-m', geo='KR'):
    """
    두 용어의 검색 관심도 비교
    """
    result = self.get_interest_over_time([term1, term2], timeframe, geo)
    if result is None or result.empty:
      return 0, 0

    term1_avg = result[term1].mean() if term1 in result.columns else 0
    term2_avg = result[term2].mean() if term2 in result.columns else 0

    return term1_avg, term2_avg

  def _wait_between_requests(self):
    """
    API 요청 간 최소 대기 시간 보장
    """
    now = time.time()
    elapsed = now - self.last_request
    if elapsed < self.min_wait_time:
      time.sleep(self.min_wait_time - elapsed)
    self.last_request = time.time()
