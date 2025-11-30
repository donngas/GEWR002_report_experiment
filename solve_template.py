import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict

class MovieAnalyzer:
    """
    CSV 형식의 영화 평점 데이터를 분석하고 시각화합니다.
    """
    df: pd.DataFrame
    
    def __init__(self, filepath: str):
        """
        주어진 CSV 파일에서 데이터를 읽고, 'Release_Date' 열을 datetime으로 변환하며,
        'Rating' 결측치를 해당 열의 중앙값으로 대체합니다.
        """
        pass

    def get_top_genres(self, top_n: int):
        """
        Genre별 영화 빈도 수를 계산하여 가장 영화 수가 많은 top_n개의 장르와 개수를
        리스트의 리스트로 반환합니다. Genre 결측치는 분석에서 제외합니다.
        """
        pass

    def calculate_average_by_year(self, start_year: int, end_year: int):
        """
        지정된 연도 구간에 개봉된 영화들의 연도별 평점 평균을 계산하여 딕셔너리 형태로 반환합니다.
        """
        pass

    def visualize_yearly_rating_trend(self):
        """
        연도별 평균 평점의 변화 추이를 나타내는 선 그래프를 생성하고, 'rating_trend.png' 파일로 저장합니다.
        """
        pass