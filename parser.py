from urllib import request
import re

site = 'http://www.mosigra.ru'
#site = 'http://www.csd.tsu.ru'
ITERATIONS = 10

mailPattern = '[\w]+@[\w.]+[\w]'
urlPatternt = '(?:' + site + ')?' + '/(?:[a-zA-Z]|[0-9]|[\/\.\?\-])+'
hrefPatternt = '(?<=a href=")'

maillist = []
start = [site]
urllist = [site]
index = 0

def req(urls):
    global index
    urllist.extend(urls)
    #print(urls)
    for i in urls:
        if index < ITERATIONS - 1:
            try:
                if i[:1] == '/':
                    html = request.urlopen(site + i).read().decode('utf-8')
                else:
                    html = request.urlopen(i).read().decode('utf-8')
            except request.HTTPError as e:
                #print(e.code, e.msg)
                continue
            except UnicodeDecodeError:
                #print("Oops, file")
                continue
            index += 1

            newmails = re.findall(mailPattern, html)
            maillist.extend(newmails)

            applicant = re.findall(hrefPatternt + urlPatternt, html)
            urlsNew = set(applicant) - set(urllist)
            req(list(urlsNew))

req(start)
print(set(maillist))
