from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="  
  response = get(f"{base_url}{keyword}")
  if response.status_code != 200:
    print("Error, cannot read website")
    exit()
  else:
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('section', class_='jobs')
    result = []
    for job in jobs:
      job_post = job.find_all('li')
      for post in job_post:
        if 'view-all' not in post.get('class', []):
          anchors = post.find_all('a')
          anchor = anchors[1]
          link = anchor['href']
          company, time, region = anchor.find_all('span', class_= 'company')
          title = anchor.find('span', class_='title')
          job_data = {
            'link': f"https://weworkremotely.com{link}",
            'company': company.string.replace(",", " "),
            'title': title.string.replace(",", " "),
            'time': time.string.replace(",", " "),
            'region': region.string.replace(",", " "),
          }
          result.append(job_data)
    return result