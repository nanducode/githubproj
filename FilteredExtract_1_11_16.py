from __future__ import print_function
from github import Github
import urllib,json
import urllib.request as UrlRequest
import requests
import base64
from urllib.error import URLError, HTTPError
import re
from bs4 import BeautifulSoup,SoupStrainer
import os

username=b'ananda.kommaraju@gmail.com'
password=b'nellore123'
base64string = base64.b64encode(username + b":" + password)

g = Github(client_id="2357171afb641b05b079",client_secret="444960920c4ace2e6cfefb055fbd4eea6e401438",per_page=100)
#g = Github(client_id="733315384e97db0c41d4",client_secret="b81ad8b8b9cc0eff6210bba7ca249bb75175fc48",per_page=100)
print("Rate remaining ",g.get_rate_limit().rate.remaining)


def get_subscribers(url):
    headers = {"Authorization": b" Basic " + base64.b64encode(username + b":" + password),
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    newurl = url
    #print(newurl)
    response = UrlRequest.Request(newurl, headers=headers)
    try:
        result = UrlRequest.urlopen(response)
        data = result.read().decode('utf8')
        repo = json.loads(data)
        return repo['subscribers_count']
    except HTTPError as e:
        print("Error")

def scrape_element(url,whatfor,endat,level):
    #print("Scrape Level")
    #print(level)

    response = UrlRequest.Request(url)
    endlist=[]
    if (level == 3):
        return endlist
    try:
        result = UrlRequest.urlopen(response)
        soup= BeautifulSoup(result.read(),"html.parser")
        linklist=soup.find_all('a')
        uniquelist=[]

        for link in linklist:
             fulllink=''
             if((link.get('href')).find('www.') == -1):
                fulllink = ("https://github.com" + link.get('href'))
             else:
                 fulllink = link.get('href')
        #     print(fulllink)
             if(fulllink not in uniquelist):
                uniquelist.append(fulllink)
        # print("Length of Unique List")
        # print(len(linklist))
        # print(len(uniquelist))
        for link in uniquelist:
         fulllink=link
         if (endat in fulllink):
             #print("PATENTS")
             #print(fulllink)
             endlist.append(fulllink)
         else:
            if (whatfor in fulllink):
                if((fulllink.find('return_to') == -1) and (fulllink.find('history') == -1)):
                    #print("Next Level of Scraping")
                    #print(fulllink)
                    endlist=endlist+(scrape_element(fulllink,whatfor,endat,level+1))


            # for table in soup.find_all('table'):
            #  for tbody in table.find_all('tbody'):
            #     for tr in tbody.find_all('tr'):
    except HTTPError as e:
        print("Error")
    #print(endlist)
    return (endlist)

def get_wiki(username,reponame):
   # headers = {"Authorization": b" Basic " + base64.b64encode(username + b":" + password),
   #            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

   url="https://github.com/"+username+"/"+reponame+"/wiki"
    #response = UrlRequest.Request(url, headers=headers)
   response = UrlRequest.Request(url)
   listelements=scrape_element(url,"Patent","www.google.com/patents",0)
   uniquelist=[]
   #print(listelements)
   for element in listelements:
       if(element not in uniquelist):
           uniquelist.append(element)
   #print (uniquelist)
   try:
        result = UrlRequest.urlopen(response)
        filename=username+"_"+reponame+"_wiki.txt"
        with open(filename, 'wb') as output:
            output.write(result.read())
   except HTTPError as e:
             print("Error")

   return (filename,uniquelist)
def print_file(download_url,repourl,appendname):
                    licencef=UrlRequest.urlopen(download_url)

                    licensefiles=repourl

                    jnk=re.sub("https:\/\/api.github.com\/repos\/","",licensefiles)
                    jnk=jnk.split("/")
     #               print(jnk)
                    licensefiles=jnk[0]+"_"+jnk[1] +"_"+appendname+".txt"
      #              print(licensefiles)
                    with open(licensefiles,'wb') as output:
                         output.write(licencef.read())
                    return(licensefiles)
                    #Changed it from filename to content
                    #return(licencef.read())
def get_submodules(contents_url):
    headers = {"Authorization": b" Basic " + base64.b64encode(username + b":" + password),
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    newurl = contents_url
    deplist=[]
    response = UrlRequest.Request(newurl, headers=headers)
    try:
        result = UrlRequest.urlopen(response)
        data = result.read().decode('utf8')
        repo = json.loads(data)

        # if('type' in repo):
        #     if (repo['type'] == 'submodule'):
        #         print("success")
        # else:
        #
        for sub in repo:
             if (sub['name'] == '.gitmodules'):
                 deplist.append(print_file(sub['download_url'],contents_url,"gitmodules"))
                 #print("success")
             if ('README' in sub['name']):
                 deplist.append(print_file(sub['download_url'], contents_url, "README"))
                 #print("success")
             if (sub['name'] == 'package.json'):
                 deplist.append(print_file(sub['download_url'], contents_url, "package"))
                 #print("success")
        #     else:
        #         new_url=sub['url']
        #         get_submodules(new_url)
        #

        return(deplist)
    except HTTPError as e:
        print("Error")
     #   glicense = ""
    #return (glicense)


def get_license(repo_url):
    headers = {"Authorization": b" Basic " + base64.b64encode(username + b":" + password),
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    newurl = repo_url+"/license"
    response = UrlRequest.Request(newurl, headers=headers)
    glicense=""
    licensefiles=""
    try:
        result = UrlRequest.urlopen(response)
        data = result.read().decode('utf8')
        repo = json.loads(data)
        if(repo['license']):
                if(repo['license']['name']):
                    glicense=repo['license']['name']
                if(repo['download_url']):
                    licencef=UrlRequest.urlopen(repo['download_url'])
#                    print("Licese")
                    licensefiles=repo_url

                    jnk=re.sub("https:\/\/api.github.com\/repos\/","",licensefiles)
 #                   print(jnk)
                    licensefiles=re.sub("\/","_",jnk) +"_License.txt"
  #                  print(licensefiles)
                    with open(licensefiles,'wb') as output:
                        output.write(licencef.read())


    except HTTPError as e:
        glicense=""
    return glicense,licensefiles;


if (0):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    url="https://api.github.com/organizations?since="
    sincenum=24600;
    while(sincenum):
        newurl=url + str(sincenum)
        response=UrlRequest.Request(newurl, headers= headers)
        result = UrlRequest.urlopen(response)
        data = result.read().decode('utf8')
        listofrepos=json.loads(data)
        if len(listofrepos) is 0:
            sincenum = 0
        else:
         for ijk in listofrepos:
             print(ijk["login"])
         sincenum=sincenum+100
        print("Since num",sincenum)
        print("Rate remaining ",g.get_rate_limit().rate.remaining)

# -----
if (1):
    print("Organization,Name, URL, Forks_Count, Watchers_Count, Stargazers, Release Count, Branch Count, Commit Count, Contrib Count,License, LicenseText, ReadmeText, SubModules, PackageJSON, Patents ")
    #orgs = ['apple','ibm','google','facebook','twitter','mozilla','twbs','github','jquery','h5bp','angular']
    #orgs = ['apple', 'ibm', 'google', 'facebook', 'twitter', 'mozilla', 'twbs', 'github', 'jquery', 'h5bp', 'angular']
    orgs = ['apple']
    for j in orgs:
        print(j)

    for orgname in orgs:
        for repo in g.get_user(orgname).get_repos():
           #print(repo.name)
           #if(repo.name == 'FreeCAD-addons'):
            #print("Repo URL:", repo.url)
            # print("Repo watchers :", repo.watchers_count)
            # print("Repo stargazers: ", repo.stargazers_count)
            # print("Repo forks count : ", repo.forks_count)
            releases = repo.get_releases()
            relcount = 0
            branchcount = 0
            commitcount =0
            contribcount = 0
            watchers=0
            for rel in releases:
                relcount = relcount + 1;


        if (0):

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
            url = "https://api.github.com/organizations?since="
            sincenum = 24600;
            while (sincenum):
                newurl = url + str(sincenum)
                response = UrlRequest.Request(newurl, headers=headers)
                result = UrlRequest.urlopen(response)
                data = result.read().decode('utf8')
                listofrepos = json.loads(data)
                if len(listofrepos) is 0:
                    sincenum = 0
                else:
                    for ijk in listofrepos:
                        print(ijk["login"])
                    sincenum = sincenum + 100
                print("Since num", sincenum)
                print("Rate remaining ", g.get_rate_limit().rate.remaining)

        # -----
        if (1):
            #print(
            #Organization,Name, URL, Forks_Count, Watchers_Count, Stargazers, Release Count, Branch Count, Commit Count, Contrib Count,License )
            # orgs = ['apple','ibm','google','facebook','twitter','mozilla','twbs','github','jquery','h5bp','angular']
            # orgs = ['apple', 'ibm', 'google', 'facebook', 'twitter', 'mozilla', 'twbs', 'github', 'jquery', 'h5bp', 'angular']
            orgs = ['apple']
            #for j in orgs:
            #    print(j)
            filteredrepos=['azonenberg','FreeCAD']

            with open('Listofrepos', "r") as myfile:

                for line in myfile:
                    
            # modified on 01-11-2016 if (repo.name in ('FreeCAD-addons', 'openfpga')):
            #filteredrepos = ['azonenberg']
            for orgname in filteredrepos:
               for repo in g.get_user(orgname).get_repos():
                    # print(repo.name)
                    if(repo.name in deprepos)
                    # print("Repo URL:", repo.url)
                    # print("Repo watchers :", repo.watchers_count)
                    # print("Repo stargazers: ", repo.stargazers_count)
                    # print("Repo forks count : ", repo.forks_count)
                    releases = repo.get_releases()
                    relcount = 0
                    branchcount = 0
                    commitcount = 0
                    contribcount = 0
                    watcherscount=0
                    if(repo.forks_count > 1):
                        for rel in releases:
                            relcount = relcount + 1;
                        for branches in repo.get_branches():
                            branchcount = branchcount + 1;
                        for contrib in repo.get_contributors():
                            contribcount = contribcount + 1;

                        for commits in repo.get_commits():
                            commitcount = commitcount + 1;
                            # print ("Commit", commits.stats.total)
                    #get_submodules(contents_url)
                        watcherscount=get_subscribers(repo.url)
                        glicense,licensefiles = get_license(repo.url)
                        dependsonpatents,listofpatents=get_wiki(orgname,repo.name)
                        dependsonpatents=""
                        depdentrepos=""


                        contents_url = repo.url + "/contents/"

                        #dependentrepos=' '.join(get_submodules(contents_url))
                        readmetext=[]
                        gitmodules=[]
                        packagejson=[]
                        dependentrepos =(get_submodules(contents_url))
                        for i in dependentrepos:
                            if('README' in i):
                                with open(i, "r") as myfile:
                                    for line in myfile:
                                        line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                        line = re.sub('\s+', ' ', line)
                                        line.strip()
                                        readmetext.append(line)
                                readmetext=" ".join(readmetext)

                            if ('modules' in i):
                                with open(i, "r") as myfile:
                                    for line in myfile:
                                        line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                        line = re.sub('\s+', ' ', line)
                                        line.strip()
                                        gitmodules.append(line)
                                gitmodules = " ".join(gitmodules)
                            if ('package' in i):
                                with open(i, "r") as myfile:
                                    for line in myfile:
                                        line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                        line = re.sub('\s+', ' ', line)
                                        line.strip()
                                        packagejson = packagejson.append(line)
                                packagejson=" ".join(packagejson)
                        licensetext = []
                        glicense.strip()
                        #Read license text
                        if(os.path.isfile(licensefiles)):

                         with open(licensefiles,"r") as myfile:

                            for line in myfile:
                                line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                line = re.sub('\s+', ' ', line)
                                line.strip()
                                licensetext.append(line)
                         licensetext=" ".join(licensetext)
                        #print(licensetext)

                        print(orgname, ",", repo.name, ",", repo.html_url, ",", repo.forks_count, ",", watcherscount, ",",
                              repo.stargazers_count, ",", relcount, ",", branchcount, ",", commitcount, ",", contribcount,
                              ",", glicense,",\"", licensetext,"\",\"",readmetext,"\",\"", gitmodules,"\",\"", packagejson,"\",",' '.join(listofpatents))

                    #print(contents_url)


                    # if(repo.has_downloads):
                    #
                    #     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                    #
                    #     response=UrlRequest.Request(release_url, headers= headers)
                    #     result = UrlRequest.urlopen(response)
                    #
                    #     data = result.read().decode('utf8')
                    #     print("Downloads Count ", json.loads(data).downloads_count)
                    #

            # for branches in repo.get_branches():
            #     branchcount = branchcount +1;
            # for contrib in repo.get_contributors():
            #     contribcount = contribcount + 1;
            #
            # for commits in repo.get_commits():
            #    commitcount = commitcount + 1;
            #     #print ("Commit", commits.stats.total)


            # if(repo.has_downloads):
            #
            #     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
            #
            #     response=UrlRequest.Request(release_url, headers= headers)
            #     result = UrlRequest.urlopen(response)
            #
            #     data = result.read().decode('utf8')
            #     print("Downloads Count ", json.loads(data).downloads_count)
            #





