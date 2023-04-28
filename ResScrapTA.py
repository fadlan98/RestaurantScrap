import requests
import pandas as pd
from bs4 import BeautifulSoup as soup 


def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    links = []
    name = []
    namefound = []
    location = []
    pNumb = []
    ratings = []
    pageOffset = []

  
    for offset in range(0,610,30):  

        print('processing page '+ str(int((offset/30))+1)+'...')
        html = requests.get('https://www.tripadvisor.com/RestaurantSearch-g297725-oa'+ str(offset)+'-Medan_North_Sumatra_Sumatra.html#EATERY_LIST_CONTENTS', headers = headers)
        bsobj = soup(html.content,'html.parser')
    
        print('processing link in page '+ str(int((offset/30))+1) + '...')
        for review in bsobj.findAll('a',{'class':'_15_ydu6b'}):
            a = review['href']
            a = 'https://www.tripadvisor.com'+ a
            a = a[:(a.find('Reviews')+7)] + '-or{}' + a[(a.find('Reviews')+7):]
           #print(a)a
            #print(offset)
            links.append(a)
    n = 0
    reviewFound = 0
    totalData = 0
    reviewAccuracy = 0
    madamleeFound = 0
    restaurantNameTemp = ""
    for nlink in links:
        n=n+1
        ratsfound = 0
        d = [5,10,15,20,25]
        html2 = requests.get(nlink.format(i for i in d),headers=headers)
        bsobj2 = soup(html2.content,'html.parser')
        print('processing name in ' + str(nlink) +" link...")
        for r in bsobj2.findAll('h1',{'class':'_3a1XQ88S'}): 
            restaurantNameTemp = r.text
            if(r.text == "Madam Lee"):
                madamleeFound = madamleeFound + 1
            if(madamleeFound>1 and restaurantNameTemp=="Madam Lee"):
               print("Madam Lee is already saved")
            else:   
               name.append(r.text) 
        
        print('\nProcessing Location...')
        for r2 in bsobj2.findAll('div',{'_2vbD36Hr _36TL14Jn'}):
            if(madamleeFound>1 and restaurantNameTemp=="Madam Lee"):
               print("Madam Lee is already saved")
            else: 
                location.append(r2.text) 

        print('Processing Phone Number... ')
        pItem = bsobj2.findAll('div',{'_1ud-0ITN'})
        for r3 in pItem:
            try: num = r3.find('a',{'_7c6GgQ6n _22upaSQN _37QDe3gr'}).text
            except: num = 'None'
        if(madamleeFound>1 and restaurantNameTemp=="Madam Lee"):
            print("Madam Lee is already saved")
        else: 
            pNumb.append(num)

        print('Processing Ratings... ')
        for r4 in bsobj2.findAll('span',{'r2Cf69qf'}): 
            print("Ratings Found")
            ratsfound = ratsfound + 1
            
            output = ' '.join([item.text for item in bsobj2.findAll('a',{'_10Iv7dOs'})])
            if(madamleeFound>1 and restaurantNameTemp=="Madam Lee"):
                print("Madam Lee is already save")
            else: 
                reviewFound = reviewFound + 1
                ratings.append(str(float(r4.text)) + ' / ' + output) 

        if ratsfound == 0:
            print("Ratings is not found")
            if(madamleeFound>1 and restaurantNameTemp=="Madam Lee"):
               print("Madam Lee is already save")
            else: 
                ratings.append("0 Ratings / No Reviewer yet")

        totalData = totalData + 1
        
    reviewAccuracy = (reviewFound/totalData) * 100
    print('Review Percentage: ', str(float(reviewAccuracy)) + '%')

    restaurantDF = pd.DataFrame({
    'Nama':name,
    'Alamat':location,
    'No. Telp':pNumb,
    'Rating':ratings})
    writer = pd.ExcelWriter('allRestaurant.xlsx', engine='xlsxwriter')
    restaurantDF.to_excel(writer, sheet_name='Sheet1',index=False)
    writer.save()

if __name__ == '__main__':
    main()
