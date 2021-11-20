import requests
from bs4 import BeautifulSoup


#URL을 정해놨었는데, URL이 바뀔 수 있도록 get_jobs에 넣어줌
def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    #예) 총 10페이지 : -1 은 0 페이지 -2는 10페이지(페이지 마지막 부분) 
    return int(last_page)  #range에 인자로 넣어주기 위해 int로 형변환


def extract_job(html): #데이터 가공 코드 
    title = html.find("h2", {"class": "job_tit"}).find("a")["title"]
    print(title)
    company = html.find("strong", {"class": "corp_name"}).find("a")["title"]
    location = html.find("div", {
        "class": "job_condition"
    }).find("a").get_text()
    job_id = html["value"]
    return {
        "title":
        title,
        "company":
        company,
        "location":
        location,
        "apply_link":
        f"https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={job_id}"
    }
 ##-- 웹 데이터 데이터 수집 완료 -- ##

def extract_jobs(last_page, url): # 2중 for문 사용 / 1번째 for문은 위 매개변수 활용하여 url 페이지의 데이터를 하나씩 읽는 과정수행
    jobs = [] #배열 생성
    for page in range(last_page): #int로 형 변환된 range 값을 page 변수에 삽입
        print(f"Scrapping {page+1}")
        result = requests.get(f"{url}&recruitPage={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"}) #자료를 1페이지 부터  마지막 페이지 까지 하나씩 찾아오는 과정

        for result in results:
            job = extract_job(result) #수집된 웹 데이터 활용(results) 가공 값을 인자로 호출 웹 페이지를 한페이지씩 읽고 extract_job에서 리턴한 값들에 배치함
            jobs.append(job) # 이 모든 자료를 위에서 만든 jobs 배열에 자료를 하나씩 추가
    return jobs # 지정 배열에 값을 리턴

 ##-- 가공 끝 -- ##
 
def get_jobs(word): #주소 값을 할당받아 각 페이지의 값을 넣어줌
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={word}"
    last_page = get_last_page(url) #url 주소값을  페이지 변수에 할당
    print(last_page)
    jobs = extract_jobs(last_page, url) #모든 가공 값을 배열 jobs에 새롭게 삽입
    return jobs # 값 리턴