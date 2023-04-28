import requests
import pandas as pd
from bs4 import BeautifulSoup as soup 

NO_OF_CHARS = 256
 
def badCharHeuristic(string, size):
    '''
    The preprocessing function for
    Boyer Moore's bad character heuristic
    '''
 
    # Initialize all occurrence as -1
    badChar = [-1]*NO_OF_CHARS
 
    # Fill the actual value of last occurrence
    for i in range(size):
        badChar[ord(string[i])] = i;
 
    # retun initialized list
    return badChar
 
def search(txt, pat):
    '''
    A pattern searching function that uses Bad Character
    Heuristic of Boyer Moore Algorithm
    '''
    m = len(pat)
    n = len(txt)
 
    # create the bad character list by calling
    # the preprocessing function badCharHeuristic()
    # for given pattern
    badChar = badCharHeuristic(pat, m)
 
    # s is shift of the pattern with respect to text
    s = 0
    while(s <= n-m):
        j = m-1
 
        # Keep reducing index j of pattern while
        # characters of pattern and text are matching
        # at this shift s
        while j>=0 and pat[j] == txt[s+j]:
            j -= 1
 
        # If the pattern is present at current shift,
        # then index j will become -1 after the above loop
        if j<0:
            '''   
                Shift the pattern so that the next character in text
                      aligns with the last occurrence of it in pattern.
                The condition s+m < n is necessary for the case when
                   pattern occurs at the end of text
               '''
            s += (m-badChar[ord(txt[s+m])] if s+m<n else 1)
            return s
        else:
            '''
               Shift the pattern so that the bad character in text
               aligns with the last occurrence of it in pattern. The
               max function is used to make sure that we get a positive
               shift. We may get a negative shift if the last occurrence
               of bad character in pattern is on the right side of the
               current character.
            '''
            s += max(1, j-badChar[ord(txt[s+j])])
    return -1

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

    #get max page
    # size = 30
    # url = 'https://www.tripadvisor.com/RestaurantSearch?Action=PAGE&ajax=1&availSearchEnabled=false&sortOrder=popularity&geo=297725&itags=10591&o=a'+ str(size)
    # r = requests.get(url)
    # soup1 = soup(r.text, "html.parser")
    # linkw = soup1.find_all('a')[-1]
    # page_number = linkw.get('data-page-number')
    # maxPage = int(page_number) # *30
    

    # for pn in range(int(maxPage)):
    #     pageOffset.append((pn) * 30)

    #print(pageOffset)
    # #get all the links from the page
    
    #for offset in (pageOffset): ##This one's for get all the page
    for offset in range(0,610,30):  
        # if offset == 0:
        #     print('processing page 1...')
        #     html = requests.get('https://www.tripadvisor.com/Restaurants-g297725-Medan_North_Sumatra_Sumatra.html', headers = headers)
        # elif offset > 0:
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
            #sleep(randint(1,5))

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

        
    #print("Restaurant Found")
#print(len(pNumb),len(name),len(location),len(ratings))
    # restaurantDF = pd.DataFrame({
    # 'Nama':name,
    # 'Alamat':location,
    # 'No. Telp':pNumb,
    # 'Rating':ratings})
    # restaurantDF.to_csv('restaurantcth2.csv',index=False)

if __name__ == '__main__':
    main()