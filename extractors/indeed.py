from bs4 import BeautifulSoup
from selenium import webdriver

def get_page_count(keyword):
    browser = webdriver.Chrome()
    base_Url = 'https://kr.indeed.com/jobs?q='
    browser.get(f"{base_Url}{keyword}")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("ul", class_="css-1g90gv6 eu4oa1w0")
    if pagination == None:
        return 1  
    pages = pagination.find_all("li", recursive=False)
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count    
def extractor_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    all_results=[]
    for page in range(0, pages): #에를들어 pages의 숫자가 3이라면 range(3)은 [0,1,2,3]을 만들어준다
        browser = webdriver.Chrome()
        baseUrl='https://kr.indeed.com/jobs'
        browser.get(f"{baseUrl}?q={keyword}&start={page * 10}")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        ul = soup.find("ul", class_="css-zu9cdh eu4oa1w0")

        #class를 css-zu9cdh eu4oa1w0를 가진 ul아래에 있느 li들의 숫자들이 print(len(ul))로 나온다.
        for li in ul:
            mosaic_zone = li.find("div", class_="mosaic-zone")
            if mosaic_zone == None:
                anchor = li.select_one("h2 a")
                link = anchor['href']
                title = li.select_one("h2 a span") #indeed 에서 title을 가져오는 방법을 css selector 방식을 이용함
                company = li.find("span", {'data-testid': 'company-name'})
                region = li.find("div", {'data-testid': 'text-location'})
                job_data = {
                    'title': title.string.replace(",", " "),
                    'company': company.string.replace(",", " "),
                    'region': region.string.replace(",", " "),
                    'link': f"https://kr.indeed.com{link}",
                }
                all_results.append(job_data)        
    return all_results #for loop 밖에서 all_results를 정의하고 for loop 안에서 그 리스트 안으로 값을 넣어주는 형식으로 오류 해결!

