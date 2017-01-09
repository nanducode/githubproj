from __future__ import print_function
from github import Github
import urllib,json
import codecs
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
         hreflink=link.get('href')
        # print("LINK IS ",hreflink)
         if(hreflink is not None):
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
def get_url_content(url_for_scrape,username,reponame):
    try:
        response = UrlRequest.Request(url_for_scrape)
        result = UrlRequest.urlopen(response)
        # Convert the html text into proper text
        soup = BeautifulSoup(result.read(), "html.parser")
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        # print(text.encode('utf-8'))
        filename = username + "_" + reponame + "_scrape.txt"
        with open(filename, 'wb') as output:
            output.write(bytes(text, 'utf-8'))
        return filename
    except HTTPError as e:
        print("Error")


def get_wiki(username,reponame):
   # headers = {"Authorization": b" Basic " + base64.b64encode(username + b":" + password),
   #            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

   url="https://github.com/"+username+"/"+reponame+"/wiki"
    #response = UrlRequest.Request(url, headers=headers)
   response = UrlRequest.Request(url)
   listelements=[]
   listelements=scrape_element(url,"Patent","www.google.com/patents",0)
   uniquelist=[]
   #print(listelements)
   for element in listelements:
       if(element not in uniquelist):
           uniquelist.append(element)
   #print (uniquelist)
   try:
        result = UrlRequest.urlopen(response)
        #Convert the html text into proper text
        # soup = BeautifulSoup(result.read(),"html.parser")
        # [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        # text=soup.get_text()
        # lines = (line.strip() for line in text.splitlines())
        # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # text = ' '.join(chunk for chunk in chunks if chunk)
        #print(text.encode('utf-8'))

        filename=username+"_"+reponame+"_wiki.txt"
        with open(filename, 'wb') as output:
            output.write(result.read())
   except HTTPError as e:
             print("Error")

   return (filename,uniquelist)
def print_file(download_url,repourl,appendname):
                    licencef=UrlRequest.urlopen(download_url)

                    licensefiles=repourl
#                    licencef=licencef.read().decode(licencef.info().get_content_charset())
                    licencef=licencef.read().decode(licencef.info().get_content_charset(),errors='ignore')

                    line = re.sub('[^a-zA-Z0-9\.]', ' ', licencef)
                    line = re.sub('\s+', ' ', line)

                    jnk=re.sub("https:\/\/api.github.com\/repos\/","",licensefiles)
                    jnk=jnk.split("/")
     #               print(jnk)
                    licensefiles=jnk[0]+"_"+jnk[1] +"_"+appendname+".txt"
      #              print(licensefiles)
                    with open(licensefiles,'w') as output:
                         output.write(line)
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
           #      print("Trying to get gitmodules")
                 deplist.append(print_file(sub['download_url'],contents_url,"gitmodules"))
                 #print("success")
             if ('README' in sub['name'] and 'pdf' not in sub['name']):
                 if(sub['type'] == 'file'):
         #         print("Trying to get README")
                  deplist.append(print_file(sub['download_url'], contents_url, "README"))
                 #print("success")
             if (sub['name'] == 'package.json'):
          #       print("Trying to get PACKAGE")
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
                    #print("Charater set")
                    #print(licencef.info().get_content_charset())
                    licencef=licencef.read().decode(licencef.info().get_content_charset(),errors='ignore')
                    #print(licencef)
                    line = re.sub('[^a-zA-Z0-9\.]', ' ', licencef)
                    line = re.sub('\s+', ' ', line)
                    #print(line)
                    with open(licensefiles,'w') as output:
                        output.write(line)


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
        #print("Since num",sincenum)
        #print("Rate remaining ",g.get_rate_limit().rate.remaining)

# -----
if (1):
    print("Organization,Name, URL, Forks_Count, Watchers_Count, Stargazers, Release Count, Branch Count, Commit Count, Contrib Count,License, LicenseText, ReadmeText, SubModules, PackageJSON, Patents ")
    #orgs = ['apple','ibm','google','facebook','twitter','mozilla','twbs','github','jquery','h5bp','angular']
    #orgs = ['apple', 'ibm', 'google', 'facebook', 'twitter', 'mozilla', 'twbs', 'github', 'jquery', 'h5bp', 'angular']
    orgs = []

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
                #print("Since num", sincenum)
                #print("Rate remaining ", g.get_rate_limit().rate.remaining)

        # -----
    if (1):
        #print(
        #Organization,Name, URL, Forks_Count, Watchers_Count, Stargazers, Release Count, Branch Count, Commit Count, Contrib Count,License )
        # orgs = ['apple','ibm','google','facebook','twitter','mozilla','twbs','github','jquery','h5bp','angular']
        # orgs = ['apple', 'ibm', 'google', 'facebook', 'twitter', 'mozilla', 'twbs', 'github', 'jquery', 'h5bp', 'angular']
        orgs = ['apple']
        #for j in orgs:
        #    print(j)
        #filteredrepos=['azonenberg','FreeCAD']
        filteredrepos=[]
        deprepos=[];
        print("Just be ")
        repoid=0
        urldict={}
        repodict={}
        #with open('Listofrepos', "r") as myfile:
        with open('Repos3', "r") as myfile:
            for line in myfile:
                lines=line.split("/")
                filteredrepos.append(lines[3])

                repoid=repoid+1
                deprepos.append(lines[4])
                repodict[lines[3]]=lines[4]
                key=lines[3]+"_"+lines[4]
                linestr = line.replace('\n', '')

                urldict[key]=linestr
                #print(lines[3]," ",lines[4])
        # modified on 01-11-2016 if (repo.name in ('FreeCAD-addons', 'openfpga')):
        #filteredrepos = ['azonenberg']
        #for k, v in urldict.items():
        #    print("Key ", k," Value ", v)
        orgrepos=[]
        repoid=0
        #print("Just before scraping",len(filteredrepos))
        filteredrepos=[]
        with open('orglist.k','r') as myfile:
            for line in myfile:
                line=line.replace('\n','')
                #if(re.match(r'^d',line)):
                filteredrepos.append(line)

        for orgname in filteredrepos:
            try:
                try:
               #  print("Getting ",orgname)
                 orguser=g.get_user(orgname)
                except HTTPError as e:
                 print("Error")
                orgrepos=orguser.get_repos()
                #orgrepos.append('activemq')
            except HTTPError as e:
                print("Error")

            #for repo in orgrepos:
            for repo in orgrepos:
                #if(repo.name in ['activemq']):

                    print("Repo ", repo.name, " orgname", orgname)
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
                    if(repo.forks_count > 1 and repo.fork == 0):
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
            #            print("LICENSE")
                        glicense,licensefiles = get_license(repo.url)
             #           print("DEPS")
                        dependsonpatents,listofpatents=get_wiki(orgname,repo.name)
              #          print("After WIKI")
                        wikitext=[]
                        wikitextfull=""
                        if (os.path.isfile(dependsonpatents)):

                            with open(dependsonpatents, "r", encoding="utf8") as myfile:

                                for line in myfile:
                                    line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                    line = re.sub('\s+', ' ', line)
                                    line.strip()
                                    wikitext.append(line)
                        wikitextfull = " ".join(wikitext)
                        wikitextfull= (wikitextfull[:32000] + '..') if len(wikitextfull) > 32000 else wikitextfull

                        # soup = BeautifulSoup(wiki)
                        # data = soup.findAll(text=True)
                        #
                        #
                        # def visible(element):
                        #     if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                        #         return False
                        #     elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                        #         return False
                        #     return True
                        #
                        #
                        # result = filter(visible, data)


                        dependsonpatents=""
                        depdentrepos=""


                        contents_url = repo.url + "/contents/"

                        #dependentrepos=' '.join(get_submodules(contents_url))
                        readmetext=[]
                        readmetext1=""
                        gitmodules=[]
                        packagejson=[]
                #        print("Before getting submodules",contents_url)
                        dependentrepos =(get_submodules(contents_url))
                 #       print("Printing DEPS")
                        if(type(dependentrepos) == type(list()) and (len(dependentrepos) > 0)):
                         for i in dependentrepos:

                            if('README' in i):
                                print("printing README")
                                with open(i, "r",encoding="utf8") as myfile:
                                    for line in myfile:
                                        line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                        line = re.sub('\s+', ' ', line)
                                        line.strip()
                                        readmetext.append(line)
                                readmetext1=" ".join(readmetext)
                                readmetext1=(readmetext1[:32000] + '..') if len(readmetext1) > 32000 else readmetext1

                            if ('modules' in i):
                   #             print("printing MODULES")
                                with open(i, "r") as myfile:
                                    for line in myfile:
                                        line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                        line = re.sub('\s+', ' ', line)
                                        line.strip()
                                        gitmodules.append(line)
                                gitmodules = " ".join(gitmodules)
                                gitmodules = (gitmodules[:32000] + '..') if len(gitmodules) > 32000 else gitmodules
                            if ('package' in i):
                    #            print("printing PACKAGE")
                                if (os.path.isfile(i)):
                                    with open(i, "r") as myfile:
                                        for line in myfile:
                                            line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                            line = re.sub('\s+', ' ', line)
                                            line.strip()
                                            packagejson.append(line)
                                    packagejson=" ".join(packagejson)
                                    packagejson = (packagejson[:32000] + '..') if len(packagejson) > 32000 else packagejson
                        licensetext = []
                        glicense.strip()
                        #Read license text
                        #print("Reading License Text")
                        if(os.path.isfile(licensefiles)):

                            with codecs.open(licensefiles,"r",encoding="utf8") as myfile:

                                for line in myfile:
                                    line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                                    line = re.sub('\s+', ' ', line)
                                    line.strip()
                                    licensetext.append(line)
                            licensetext=" ".join(licensetext)
                            licensetext = (licensetext[:32000] + '..') if len(licensetext) > 32000 else licensetext
                        apps_using = []
                        #if( (orgname+"_"+repo.name) in urldict):

                         # apps_using_file=get_url_content(urldict[orgname+"_"+repo.name],orgname,repo.name)
                         #
                         # if (os.path.isfile(apps_using_file)):
                         #
                         #    with open(apps_using_file, "r", encoding="utf8") as myfile:
                         #
                         #        for line in myfile:
                         #            line = re.sub('[^a-zA-Z0-9\.]', ' ', line)
                         #            line = re.sub('\s+', ' ', line)
                         #            line.strip()
                         #            apps_using.append(line)
                         #    apps_using = " ".join(apps_using)

                        #print(licensetext)

                        print("FINALSTATS",orgname, ",", repo.name, ",", repo.html_url, ",", repo.forks_count, ",", watcherscount, ",",
                              repo.stargazers_count, ",", relcount, ",", branchcount, ",", commitcount, ",", contribcount,
                              ",", glicense,",\"", licensetext,"\",\"",readmetext1,"\",\"", gitmodules,"\",\"", packagejson,"\",\"", wikitextfull,"\",",' '.join(listofpatents),",\"",apps_using,"\"")

        repoid=repoid+1
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





