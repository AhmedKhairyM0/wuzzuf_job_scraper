import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest


query = input("Enter the job title:\t") # "flutter", "backend", "Android" or "IOS", ...
numberOfPages =  5

path = f"./wuzzuf_{query}_jobs.csv"

# store of the jobs
job_title = []
company_name = []
location = []
job_skill = []
job_date = []
links = []
salaries = []
resposibilities = []

with open(path, "a") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Publication date", "Job title", "Job Skills","Company name", "Company location",  "Appplication Link"])

    for i in range(numberOfPages):

        # 1st step: use requests to get the html of the page
        url = f"https://wuzzuf.net/search/jobs/?a=navbl&q={query}&start={i}"
        result = requests.get(url)

        # 2nd step: get content/markup of the page [HTML code of the page]
        src = result.content

        # 3rd step: create BeautifulSoup object to parse the content
        soup = BeautifulSoup(src, "lxml")

        # 4th step: find the elemenst that containing info we need
        job_titles = soup.find_all("h2", {"class": "css-m604qf"})
        company_names = soup.find_all("a", {"class": "css-17s97q8"})
        locations = soup.find_all("span", {"class": "css-5wys0k"})
        job_skills = soup.find_all("div", {"class": "css-y4udm8"})
        job_dates = soup.find_all("div", {"class": "css-d7j1kk"})

        # 5th step: gethering text data from html tags
        base_url = "http://www.wuzzuf.net"
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(base_url + job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            location.append(locations[i].text)
            job_skill.append(job_skills[i].text)

            info = job_dates[i].text.split()
            n = len(info)
            date = info[n-3] + " " + info[n-2] + " " + info[n-1]
            job_date.append(date)

   
    # 6th step: save jobs descriptions to a csv file

    file_list = [job_date, job_title, job_skill, company_name, location, links]
    exported = zip_longest(*file_list)

    wr.writerows(exported)
    
    result_color = '\033[92m'
    print(f"{result_color}Done ✨, See search result in {path}")