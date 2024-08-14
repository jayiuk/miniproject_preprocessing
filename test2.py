import requests
import pandas as pd

def fetch_reviews_for_station(station_name, api_key, output_csv='reviews.csv'):
    """
    주어진 지하철역 이름과 API 키를 사용하여 반경 1km 내의 맛집 리뷰와 평점을 수집하여 CSV 파일로 저장합니다.

    Args:
        station_name (str): 지하철역 이름.
        api_key (str): 카카오 API 키.
        output_csv (str): 저장할 CSV 파일 이름. 기본값은 'reviews.csv'.
    
    Returns:
        pd.DataFrame: 수집된 리뷰 데이터가 포함된 데이터프레임.
    """
    # 카카오 API URL 설정
    keyword_local_url = "https://dapi.kakao.com/v2/local/search/keyword.json?query={}&radius=1000"
    comment_url = "https://place.map.kakao.com/m/commentlist/v/{}/{}?order=USEFUL&onlyPhotoComment=false"
    
    # 헤더에 인증 정보를 추가
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }

    # 지하철역 주변 맛집 검색
    response = requests.get(keyword_local_url.format(station_name + " 맛집"), headers=headers)
    
    # 검색 결과에서 데이터 추출
    datas = response.json().get('documents', [])
    if not datas:
        print(f"No results found for station: {station_name}")
        return pd.DataFrame()  # 빈 데이터프레임 반환
    
    # 맛집의 ID 리스트 추출
    ids = [data['id'] for data in datas]
    
    all_comments = []
    
    # 각 맛집의 리뷰 수집
    for id in ids:
        comment_id = 0
        has_next = True
        
        while has_next:
            # 리뷰 수집 URL 생성
            scrap_comment_url = comment_url.format(id, comment_id)
            
            # 리뷰 데이터 요청
            response = requests.get(scrap_comment_url)
            comment_datas = response.json().get('comment', {})
            
            # 리뷰 데이터 가져오기
            comment_list = comment_datas.get('list', [])
            all_comments.extend(comment_list)
            
            # 다음 페이지 존재 여부 확인
            has_next = comment_datas.get('hasNext', False)
            
            if has_next:
                comment_id = comment_list[-1]['commentid']
    
    # 리뷰 데이터에서 'contents'와 'point'만 추출
    extracted_reviews = [
        {
            'contents': comment.get('contents', ''),
            'point': comment.get('point', 0)
        }
        for comment in all_comments
    ]
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(extracted_reviews)
    
    # 데이터프레임을 CSV 파일로 저장
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Saved reviews to {output_csv}")
    
    return df

# 사용 예시
if __name__ == "__main__":
    station_name = "홍대입구역"  # 지하철역 이름
    api_key = "YOUR_KAKAO_API_KEY"  # 카카오 API 키

    df = fetch_reviews_for_station(station_name, api_key)
    print(df.head())  # 데이터프레임의 상위 5개 행 출력