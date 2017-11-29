#!/usr/bin/python3.5

from bs4 import BeautifulSoup
import requests
import argparse
import sys


def getarg():
    parser = argparse.ArgumentParser(description="NITC Library searching tool")
    parser.add_argument('-s', '--search', help='Name of the book to be searched', dest='s')
    parser.add_argument('-a', '--available', help="Display the book iff available", action='store_true', default=False, dest='a')
    parser.add_argument('-l', '--login', help="Login with your account", action='store_true', default=False, dest='l')
    parser.add_argument('-d', '--display', help="Display the due books ", action='store_true', default=False, dest='d')
    args = parser.parse_args()
    return args


def getbook():

    args = getarg()
    if args.l is False:
        siteurl = "http://124.124.70.124/cgi-bin/koha/opac-search.pl?idx=kw&q="
        print("Connecting to NITC library server.")
        if args.a:

            url = siteurl + args.s + "&amp;sort_by=relevance_dsc&amp;limit=available"
        else:
            url = siteurl + args.s
        try:
            src = requests.get(url, timeout=60).text
        except ConnectionError:
            print("There was a problem connecting,please check your network cables")
            sys.exit(0)
        except TimeoutError:
            print("Connection timed-out")
            sys.exit(0)
        except:
            print("Unable to connect,please check your network cables.\nAborting")
            sys.exit(0)
    else:
        src = login().text

    scrap = BeautifulSoup(src, 'lxml')
    i = 1
    for data in scrap.find_all('a',{'xmlns:str':'http://exslt.org/strings'}):
        books = [book for book in data.stripped_strings]
        print(i, ': ' + books[0].strip('/')+books[1])
        i += 1


def login():
    r=requests.Session()
    print("Enter the user name")
    name=input()
    print("Enter password")
    password=input()
    payload={'userid': name, 'password': password}
    session = r.post("http://124.124.70.124/cgi-bin/koha/opac-user.pl", data=payload)
    return session


def checkouts(src):
    for n in src.find_all('div', {'id': 'userdetails'}):
        temp = [ns for ns in n.stripped_strings]
        name = temp[0].strip('Hello,').lstrip()
        print("Hello "+name)
        print("The item checked-out are :")
        i=1
    for books in src.find_all('td', class_="title"):
        temp = [te for te in books.stripped_strings]
        print(i," : "+temp[0].strip('/')+"by "+temp[1])
        i+=1


argss = getarg()
if argss.d==True:
    s = BeautifulSoup(login().text,'lxml')
    checkouts(s)
if argss.s is not None:
    getbook()

