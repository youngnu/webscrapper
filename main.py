from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extractor_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app=Flask("JobScrapper")

db ={}

@app.route('/')
def home():
    return render_template('home.html', name="yonnu")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extractor_indeed_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = indeed + wwr
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")  # 어째서 여기서 keyword가 필요한 건지 정확히 이해가 가질않는다. export 버튼을 누르면 /export?keyword= 로 가는 것인가?
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)