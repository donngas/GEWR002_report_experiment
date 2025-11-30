## 가상 과제 지시문

CSV 형식으로 제공된 가상의 영화 평점 데이터를 분석하고 시각화하는 Python Class를 완성하시오. Pandas와 Matplotlib 라이브러리를 이용하시오.

movies.csv

```csv
Title,Genre,Release_Date,Rating
The Grand Adventure,Action,2020-05-15,8.5
Cybernetic Dreams,Sci-Fi,2021-08-22,7.9
Laugh Riot,Comedy,2019-11-30,6.8
```

MovieAnalyzer 클래스에서 구현해야 할 메소드:

- \_\_init\_\_(self, filename) [총 25점]
  - 주어진 CSV 파일에서 데이터를 읽기 [부분 10점]
  - Release_Date 열을 datetime으로 변환 [부분 10점]
  - Rating 결측치는 해당 열의 중앙값으로 대체하여 처리 [부분 5점]
- get_top_genres(self, top_n) [총 25점]
  - Genre별 영화 빈도 수를 계산하여 가장 영화 수가 많은 top_n개의 장르와 그 장르의 개수를 리스트의 리스트로 반환 [부분 15점]
  - 반환 형식: `[['장르1', 개수1], ['장르2', 개수2], ...]` (개수 기준 내림차순 정렬)
    - 장르명: str
    - 개수: int
  - Genre 결측치는 분석에서 제외 [부분 10점]
- calculate_average_by_year(self, start_year, end_year) [총 25점]
  - 지정된 start_year와 end_year 사이 구간에 개봉된 영화들의 연도별 평점 평균을 계산하여 딕셔너리 형태로 반환
  - 반환 형식: `{연도1: 평균평점1, 연도2: 평균평점2, ...}`
    - 연도: int
    - 평균평점: float
- visualize_yearly_rating_trend(self) [총 25점]
  - 연도별 평균 평점의 변화 추이를 나타내는 선 그래프를 Matplotlib으로 생성하고, rating_trend.png 파일로 저장
  - 이 메소드는 값을 반환하지 않음 (None)
