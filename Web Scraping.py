'''import requests
from bs4 import BeautifulSoup
import pandas as pd
url="https://www.flipkart.com/search?q=MOBILE+UNDER+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"
web=requests.get(url)
print(web)
soup=BeautifulSoup(web.content,'html.parser')
#print(soup.prettify())
#to get links of page 2
next_page=soup.find('a',class_='_9QVEpD').get('href')
print(next_page)
complete_next_page_link="https://www.flipkart.com/"+next_page
print(complete_next_page_link)
new_page_url=complete_next_page_link
web1=requests.get(new_page_url)
soup1=BeautifulSoup(web1.content,'html.parser')
#print(soup1.prettify())  '''

    #to get all the completed links from page 2 to 10
'''for i in range(2,10):
        url="https://www.flipkart.com/search?q=MOBILE+UNDER+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(i)
        web1=requests.get(url)
        soup1=BeautifulSoup(web1.content,'html.parser')
        next_page=soup1.find('a',class_='_9QVEpD').get('href')
        complete_next_page_link="https://www.flipkart.com/"+next_page
        print(complete_next_page_link)  '''
        

# to get data from page 2 to 10:

'''for i in range(2,10):
        url="https://www.flipkart.com/search?q=MOBILE+UNDER+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(i)
        product_name=[]
        product_price=[]
        product_reviews=[]
        product_description=[]
        r=requests.get(url)
        s=BeautifulSoup(r.text,'html.parser') # it include  reviews of all product present in the page
        box=s.find("div",class_="DOjaWF gdgoEp")
        names=box.find_all('div',class_='KzDlHZ')
        #print(names)  # it is a list ...so we iterate names of product

        # to find names of product
        for i in names:
            product_name.append(i.text)
        print(product_name)
        print(len(product_name))
        # to find price of product

        price=box.find_all('div',class_='Nx9bqj _4b5DiR')
        for i in price:
            product_price.append(i.text)
        print(product_price)
        print(len(product_price))
        #to find description of product
        description=box.find_all('ul',class_='G4BRas')  #ul=unordered list which is a tag in html for description # li is list item
        for i in description:
            product_description.append(i.text)
        print(product_description)
        print(len(product_description))
        # to find ratings of product
        reviews=box.find_all('div',class_='XQDdHH')   
        for i in reviews:
            product_reviews.append(i.text)
        print(product_reviews)
        print(len(product_reviews)) # if length of all data are not equal then we cant create dataframe in csv file
# Now creating dataframe
df=pd.DataFrame({'Product Name':product_name,'Product Price':product_price,'Product Description':product_description,'Product Reviews':product_reviews})
print(df)   '''


import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest  # To handle missing data

# zip_longest() makes sure all lists have the same length by filling missing values with "N/A".
#zip(*zipped_data) splits the big table into separate lists.
#map(list, ...) turns them into normal lists that Python can understand.
# page_product_name, page_product_price, page_product_description, page_product_reviews = ... stores them separately for further use.
# Lists to store data from all pages
product_name = []
product_price = [] 
product_reviews = []
product_description = []

# Loop through pages 2 to 10
for i in range(2, 11):  
    url = "https://www.flipkart.com/search?q=MOBILE+UNDER+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=" + str(i)
    
    r = requests.get(url)
    
    if r.status_code != 200:
        print(f"Failed to fetch page {i}")
        continue  

    s = BeautifulSoup(r.text, 'html.parser')  
    box = s.find("div", class_="DOjaWF gdgoEp")  
    
    # Extracting product names
    names = box.find_all('div', class_='KzDlHZ')
    page_product_name = []
    for name in names:
        page_product_name.append(name.text)

    # Extracting product prices
    prices = box.find_all('div', class_='Nx9bqj _4b5DiR')
    page_product_price = []
    for price in prices:
        page_product_price.append(price.text)

    # Extracting product descriptions
    descriptions = box.find_all('ul', class_='G4BRas')  
    page_product_description = []
    for desc in descriptions:
        page_product_description.append(desc.text)

    # Extracting product ratings/reviews
    reviews = box.find_all('div', class_='XQDdHH')   
    page_product_reviews = []
    for review in reviews:
        page_product_reviews.append(review.text)

    # Ensuring all lists have 24 elements per page
    zipped_data = list(zip_longest(page_product_name, page_product_price, page_product_description, page_product_reviews, fillvalue="N/A"))
    
    # Unzipping correctly into four lists
    page_product_name, page_product_price, page_product_description, page_product_reviews = map(list, zip(*zipped_data))

    # Extend the main lists with the processed data
    product_name.extend(page_product_name)
    product_price.extend(page_product_price)
    product_description.extend(page_product_description)
    product_reviews.extend(page_product_reviews)

# Create a DataFrame and save it to a CSV file
df = pd.DataFrame({
    'Product Name': product_name,
    'Product Price': product_price,
    'Product Description': product_description,
    'Product Reviews': product_reviews
})

df.to_csv("C:/Users/mishr/Downloads/flipkart_mobiles.csv", index=False, encoding="utf-8")  # // yahi symbol hona chahiye
print(df)
print("Data successfully saved to flipkart_mobiles.csv")
