
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests, json,time
from .models import Opportunity
from django.db import IntegrityError
from datetime import datetime


tags = ["Architecture", "Engineering", "Arts", "Design", "Entertainment", "Sports", "Media", "Building", "Grounds", "Cleaning", "Maintenance", "Business", "Financial", "Operations", "Community", "Social", "Computer", "Mathematical", "Construction", "Extraction", "Education", "Training", "Library", "Farming", "Fishing", "Forestry", "Food", "Preparation", "Serving", "Related", "Healthcare", "Practitioners", "Technical", "Healthcare", "Support", "Installation", "Maintenance", "Repair", "Legal", "Life", "Physical", "Social", "Science", "Management", "Military", "Office", "Administrative", "Support", "Personal Care", "Service", "Production", "Protective", "Sales", "Related"]


def scraping(search):
    
    URL = "https://www.indeed.com/jobs?q={}".format(search)
    
    payload = {}
    headers= {}
    
    page  = requests.request("GET", URL, headers=headers, data = payload)
    
    soup = BeautifulSoup(page.text, "html.parser")

    return soup


def scrapingAndPopulating(search, numelems,random, scrape):
    titles =  extract_job_title_from_result(scrape(search), numelems,random)
    links = extract_job_link_from_result(scrape(search),numelems,random)
    locations =extract_location_from_result(scrape(search),numelems,random)
    companies = extract_company_from_result(scrape(search),numelems,random)

    for i in range(numelems):
        try:
            Title,Link,Location,Company = titles[i], links[i],locations[i], companies[i]
            print(titles[i], links[i],locations[i], companies[i])
            if len(list(Opportunity.objects.all().filter(link = Link))) > 0:
                print("it is trying to insert duplicates, retrying")
                raise IntegrityError
            Opportunity.objects.create(title = Title, link= Link, location = Location, company = Company )
        except IntegrityError:
            scrapingAndPopulating(search+ ("{}".format("jt=parttime")), numelems, random, scrape)
        except Exception as e:
            print(e)
            print("Opportunity could not be created due to an non-duplicates exception")
            
        
def scraper(*args, **kwargs):
    # print(kwargs["rando"])
    # for i in :
    # tagBeingPopulatedWithJobs = tags[i]
        
    tagBeingPopulatedWithJobs =kwargs["tags"][kwargs["rando"](0,len(kwargs["tags"])-1)]
    kwargs["scrapingAndPopulatingDb"](tagBeingPopulatedWithJobs, kwargs["numelem"](1,2), kwargs["selectRandom"], kwargs["scraping"])
    # print("Database being populated with new opportunities from Indeed")
    
        
   
        


def extract_job_title_from_result(soup,numelems,random): 
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"})[random(0,numelems-1):numelems]:
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
            
    return(jobs)


def extract_job_link_from_result(soup,numelems,random):
    links = []
    for div in soup.find_all(name="div", attrs={"class":"row"})[random(0,numelems-1):numelems]:
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            links.append("https://www.indeed.com/viewjob"+ a["href"][7:])
    return(links)

def extract_company_from_result(soup,numelems,random): 
    companies = []
    for div in soup.find_all(name="div", attrs={"class":"row"})[random(0,numelems-1):numelems]:
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
            else:
                sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        for span in sec_try:
            companies.append(span.text.strip())
    return(companies)
 

def extract_location_from_result(soup,numelems,random): 
  locations = []
  spans = soup.findAll("span", attrs={"class": "location"})[random(0,numelems):numelems]
  for span in spans:
    locations.append(span.text)
  return(locations)


# def extract_salary_from_result(soup,numelems): 
#   salaries = []
#   for div in soup.find_all(name="div", attrs={"class":"row"}):
#     try:
#       salaries.append(div.find("nobr").text)
#     except:
#       try:
#         div_two = div.find(name="div", attrs={"class":"sjcl"})
#         div_three = div_two.find("div")
#         salaries.append(div_three.text.strip())
#       except:
#         salaries.append("Nothing_found")
#   return(salaries)




# extract_salary_from_result(scrape("web"))
# print(extract_job_link_from_result(scrape("web"),2))
#print(extract_location_from_result(scrape("web"),3))

# print(extract_company_from_result(scrape("web"),3))
#print(extract_job_title_from_result(scrape("web"), 3))

# max_results_per_city = 100
# city_set = ["New+York","Chicago","San+Francisco", "Austin", "Seattle", "Los+Angeles", "Philadelphia", "Atlanta", "Dallas", "Pittsburgh", "Portland", "Phoenix", "Denver", "Houston", "Miami", "Washington+DC", "Boulder"]
# columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
# # sample_df = pd.DataFrame(columns = columns)

# for city in city_set:
#   for start in range(0, max_results_per_city, 10):
#     page = requests.get("http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=" + str(city) + "&start=" + str(start))
#     time.sleep(1)  #ensuring at least 1 second between page grabs
#     soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
#     for div in soup.find_all(name="div", attrs={"class":"row"}): 
#         #specifying row num for index of job posting in dataframe
#         num = (len(sample_df) + 1) 
#         #creating an empty list to hold the data for each posting
#         job_post = [] 
#         #append city name
#         job_post.append(city) 
#         #grabbing job title
#         for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
#             job_post.append(a["title"]) 
#             #grabbing company name
#             company = div.find_all(name="span", attrs={"class":"company"}) 
#         if len(company) > 0: 
#             for b in company:
#                 job_post.append(b.text.strip()) 
#         else: 
#             sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
#             for span in sec_try:
#                 job_post.append(span.text) 
#         #grabbing location name
#         c = div.findAll("span", attrs={"class": "location"}) 
#         for span in c: 
#             job_post.append(span.text) 
#         #grabbing summary text
#         d = div.findAll("span", attrs={"class": "summary"}) 
#         for span in d:
#             job_post.append(span.text.strip()) 
#         #grabbing salary
#         try:
#             job_post.append(div.find("nobr").text) 
#         except:
#             try:
#                 div_two = div.find(name="div", attrs={"class":"sjcl"}) 
#                 div_three = div_two.find("div") 
#                 job_post.append(div_three.text.strip())
#             except:
#                 job_post.append("Nothing_found") 
#         #appending list of job post info to dataframe at index num
#         sample_df.loc[num] = job_post

    #saving sample_df as a local csv file — define your own local path to save contents 
    # sample_df.to_csv("Iloveyou.csv", encoding="utf-8")
            
        

    
    # final_postings = []

    # for opportunity in jsonResponse:
    #     post_
#         post_title = post.find(class_='strong truncate text-dark flex-auto line-height-4').text
#         post_url = post.find('a').get('href')

#         if post.find(class_='truncate-block-4-lines pre-wrap break-word overflow-hidden'):
#             post_desc = post.find(class_='truncate-block-4-lines pre-wrap break-word overflow-hidden').text
#         else:
#             post_desc = 'N/A'
        
#         post_type_and_tags = post.find(_class='flex-auto truncate')
#         post_type= post_type_and_tags[0].text
#         post_tags = [ x.text for x in post_type_and_tags[1:] ]

#         final_postings.append((post_title, post_url, post_desc, post_type, post_tags))
#         print(x for x in final_postings)


# def scraper():
#     # scrape("web developer")
#     print("I will scrape habibe")