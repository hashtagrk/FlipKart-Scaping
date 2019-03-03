
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
#from textblob import TextBlob

#input item name from user and remove spaces 
print("Search for item..?")
item_name_full = input()
item_name = item_name_full.replace(' ', '')

#link to scrap data from
my_url = 'https://www.flipkart.com/search?q=' + item_name + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

#open connection
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#Use BeautigulSoup to parse the html site
page_soup = soup(page_html, "html.parser")

#on web browser 'inspect element' to get the class of part which we want to scrap
no_page_soup = page_soup.findAll("div", {"class": "_2zg3yZ"})

#print total no of page like 'Page 1 of 8'
'''print(no_page_soup[0].span.text)'''

#Find only total no. of pages. like '8' and then convert to int
num_pages_str = no_page_soup[0].span.text

#['Page',  '1', 'of', '8']
num_pages_strtolist = num_pages_str.split()

#extract last num
total = int(num_pages_strtolist[len(num_pages_strtolist)-1].replace(',',''))
print(total)

'''print(soup.prettify(containers[0]))'''


#iterate over pages to scape all the data
for i in range(1, total + 1):
    my_url_loop = 'https://www.flipkart.com/search?q=' + item_name + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=' + str(i)    
    uClient_in = uReq(my_url_loop)
    page_html_in = uClient_in.read()
    uClient_in.close()
    page_soup = soup(page_html_in, "html.parser")
    '''containers_in = page_soup.findAll("div", {"class": "_1UoZlX"})'''
    containers_in = page_soup.findAll("div", {"class": "_3O0U0u"})
    
    try:
        #check if page has anyhing that could be parsed. if no, control goes to 'except'
        container = containers_in[0]
        '''print(soup.prettify(containers_in[0]))'''
    except:
        print("No More " + item_name_full + "  Avaliable")
        
    for container_in in containers_in:
        
        #get product id,name,features,price, etc.
        rating_star = container_in.findAll("div", {"class": "hGSR34"})
        prod_name = container_in.findAll("div", {"class": "_3BTv9X"})
        name = prod_name[0].img["alt"]
        feature = container_in.findAll("li", {"class": "tVe95H"})
        print("ITEM" )
        print("NAME - " + name )
        print("PRODUCT ID - " + container_in.div.attrs['data-id'])
        try:
            price = container_in.findAll("div", {"class": "_3auQ3N _2GcJzG"})
            print("PRICE = " + price[0].text)
        except:
            print("PRICE = NOT MENTIONED")
        
        print("FEATURES : ")
        try:
            print(feature[0].text, end="|")
            print(feature[1].text, end="|")
            print(feature[2].text, end="|")
            print(feature[3].text)
        except:
            print("Feature NA")
        p_rating = container_in.findAll("span", {"class": "_38sUEc"})
        try:
            print("PEOPLE RATED = " + p_rating[0].span.span.text)
        except:
            print("PEOPLE RATED = NONE")
        try:
            print("Rating : " + rating_star[0].text + "/5")
        except:
            print("Rating /5 : NOT YET RATED")
        
        print('\n')
    



