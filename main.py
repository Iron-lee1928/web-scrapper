from flask import Flask, render_template,request,redirect,send_file
from scrapper import get_jobs #함수호출
from exporter import save_to_file #함수호출
app=Flask("Scrapper")

db={}#fake DB

@app.route("/")
def home():
  return render_template("iron.html")
#임의 클라우드 서버 할당 및 데이터 베이스에 자료넣는 공간 생성
@app.route("/report")
def report():
  word=request.args.get('word')#arg : /report?args=1&args3=2이런식으로 전달되는것

  if word:
    word = word.lower()
    existingJobs = db.get(word)#검색한 word가 db에 있는지 찾아봄
    if existingJobs:
     jobs=existingJobs
    else:
      jobs=get_jobs(word)#scrapping 동작
      db[word]=jobs#scrapping하고 db['word']에 저장됨
  else: #word가 존재하지 않을 경우 home으로 redirect
    return redirect("/")
  #render_templeate함수를 리턴하면서, report.html을 렌더링
  return render_template("report.html",
    searchingBy=word,

    resultsNumber=len(jobs),#fakeDB에서 긁어온 jobs의 개수
    jobs=jobs#report.html에 jobs넘겨주기
  )
# 에러발생 시키기
#모든 에러를 다 잡을 수 없음
@app.route("/export")
def export():
  try:
    word=request.args.get('word')
    if not word:
      raise Exception()
    word=word.lower()
    jobs=db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="0.0.0.0")

#[코드 설명]

#1. 사용자가 home에 있다가 input value를 넣음
#2. report에서 args로 input value인 word를 받음
#3. word를 소문자로 바꿈
#4. 미리 만들어놓은 fake DB에 검색한 word가 있는지 확인
#5. 있으면 바로 출력
#6. 없는경우 scrapping.py에 있는 get_jobs에 word를 매개변수로 넣어서 호출
#7. 사용자가 검색한 word대로 url주소가 바뀌어야 하기 때문에 get_jobs에서

#    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={word}" 로 설정한 후 get_last_page에 url을 매개변수로 넣어서  호출

    #(word가 없으면 home으로 redirect)

#8. get_last_page 에서 url에 대한 requests를보내서 결과를 result에 담고

 #   HTML 에서 특정 정보만 뽑아오기 위해서 Beautiful Soup을 사용

#9. 한화면에 나오는 페이지중 최대 페이지를 찾아서 반환,pages[-2] 해준 이유는 다음이나 더보기를 빼고 카운트 하기 위함
#10. extract_jobs에 last_page와 url값을 매개변수로 넣어 호출 html에서 특정정보를 뽑기위해 beautifulsoup을 사용하고, results = soup.find_all("div", {"class": "item_recruit"}) results에 담아 반복문으로 한페이지씩 scrapping 할 수 있도록 함
#11. 미리 만들어둔 jobs 배열에 jobs.append(job) 해줌 jobs를 리턴함.
#12. db[word]=jobs 스크래핑 한 후에 fakeDB에 저장
#13. render_templeate함수를 리턴하면서, report.html을 렌더링
#14. csv파일로 저장하고싶다면 export클릭 → writer 를 이용하여 csv파일생성

#내 코드를 내가 까먹음,,
