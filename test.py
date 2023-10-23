import requests
from bs4 import BeautifulSoup
import pandas as pd
from googlesearch import search
import csv
from playwright.sync_api import sync_playwright

#JOB CLASS
#---------------------------------------------------------------------------------------------------------------------#
class job_object:
    def __init__(self,title,location,link):
        self.title = title
        self.location = location
        self.link = link

#GLOBAL LIST OF JOBS
#---------------------------------------------------------------------------------------------------------------------#
global_job_list = []


#SCRAPPER FOR WORKABLE.COM
#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------# 


#THIS WILL GO THROUGH A LIST OF WORKABLE JOBS 
    #THE LIST WAS SCRAPPED FROM AN EXTERNAL SOURCE
    #NEXT STEP OF THIS WEB SCRAPPER IS TO BE ABLE TO SCRAPE GOOGLE FOR MORE WORKABLE JOBS OR USE WORKABLES JOB XML FILE
csv_data=[]
parent_websites=[]
websites = []
parent_websites.append("https://apply.workable.com/columbia-road/?lng=en")
with open("Workable List.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        csv_data.append(row)
for row in csv_data:
    parent_websites.append(row[0])


for website in parent_websites:
    if "/j/" in website:
        if website[-1] == "/":
            website= website[:-1]
        global_job_list.append(job_object("Title","location",website))

#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------# 



#SCRAPER FOR PYTHON JOBS#
#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

URL = "https://pythonjobs.github.io/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#Gets the html with the tag "ResultsContainer"
results = soup.find("section", class_="job_list")
job_elements=results.find_all("div", class_="job")
for job_element in job_elements:
    link=job_element.find("a")
    title=job_element.find("h1")
    location=job_element.find("span")
    global_job_list.append(job_object(title.text.strip(),location.text.strip(),URL + link.get("href")))

#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#



#SCRAPER FOR REMOTE JOBS#
#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#
isValidLink = True
count = 1
while isValidLink:
    root_URL=""
    if count!=1:
        root_URL = "https://remote.co/remote-jobs/developer/page" + str(count)
    else:
        root_URL = "https://remote.co/remote-jobs/developer/"
    
    page = requests.get(root_URL)
    soup=BeautifulSoup(page.content,"html.parser")
    results= soup.find("div",class_="card bg-light mb-3 rounded-0")

    #This will remove unwanted Links
    unwanted = soup.find(class_="p-3 m-0 border-bottom")
    if unwanted is not None:
        unwanted.extract()
    unwanted = soup.find(class_="page-numbers")
    if unwanted is not None:
        unwanted.extract()
    unwanted = soup.find(class_="next page-numbers")
    if unwanted is not None:
        unwanted.extract()
    unwanted = soup.find(class_="p-3 m-0")
    if unwanted is not None:
        unwanted.extract()


    job_tags=results.find_all("a")



    #job_links is a list of links to each job
        #I will loop through job_links and parse each job for the information I am looking for 
    job_links = []
    for job_tag in job_tags:
        if job_tag.get("href") is None:
            continue
        else:
            job_links.append("https://remote.co" + job_tag.get("href"))
    if len(job_links) == 0:
        break
    job_links.pop()


    #This will loop through all of the URL for each job 
    # and then save those jobs and their information into the global_job_list
    for link in job_links:
        page = requests.get(link)
        soup=BeautifulSoup(page.content,"html.parser")
        results=soup.find("div", class_="card-body loosen")
        title=results.find("h1")
        location=results.find("div",class_="location_sm row")
        applyLinkContainer=soup.find("div",class_="application")
        applyLink=applyLinkContainer.find("a")
        
        global_job_list.append(job_object(title.text.strip(),location.text.strip(),applyLink.get("href")))
    
    job_links.clear()
    count = count + 1


#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#


#THIS SAVES THE JOBS TO A CSV FILE 
data = [{"title": job.title, "location": job.location,"link": job.link} for job in global_job_list]
df=pd.DataFrame(data)
print(df)
df.to_csv('list.csv', index=False)