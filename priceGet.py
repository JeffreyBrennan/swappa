import requests, csv, time, datetime, timing
from bs4 import BeautifulSoup

timeNow = time.time()
fileName = datetime.datetime.fromtimestamp(timeNow).strftime('%m_%d_%H_%M_')
outputPath = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/swappa/output/'


swpURL = 'https://swappa.com/buy/'
checked = time.asctime(time.localtime())
loop = 0
deviceCounter = 1

## initialize lists
phoneList, resultList, deviceID, date, maker, model, offers, \
lowPrice, highPrice, url= ([] for i in range(10))

with open('swappa_devices.csv', newline='') as r:
    file = csv.reader(r, delimiter =',')
    for row in file:
        for i in row:
            phoneList.append(i)

deviceLength = str(len(phoneList))

# gets page text and puts string of results into a list
def dataGet(phone):
    try:
        r = requests.get(swpURL+phone)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find('script', attrs={'type':'application/ld+json'}).string

        for x in [results]:
            resultList.append(x)
    except AttributeError:
        resultList.append(" ")
    
    print ('Device ' + str(deviceCounter) + '/' + deviceLength)

def simpValueGet(key, name):
    try: 
        tempList = cleanList[startpoints[loop]:]
        valueLoc = tempList.index(key) + 1
        valueStr = tempList[valueLoc]
        name.append(valueStr)
    except ValueError:
        name.append(' ')        


for i in phoneList:
    dataGet(i)
    deviceCounter+=1


## cleans string and converts back into list, counts number of entries
resultStr = ''.join(resultList)
resultStr = resultStr.strip('\t').replace('"','').replace('{','') \
                     .replace('}','').replace(',','')

cleanList = resultStr.split()
startpoints = [i for i, x in enumerate(cleanList) if x == '@context:']

print (cleanList)
## parses list for needed information (b/c swappa html is cheeks and bs4 didn't work)
## test making it into a function 

try: 
    for i in phoneList:
        tempList = cleanList[startpoints[loop]:]

        try: 
            makerLoc = tempList.index('Thing')
            makerStr = tempList[makerLoc+2]
            maker.append(makerStr)
        except ValueError:
            maker.append(' ')

        try:
            nameStart = tempList.index('name:') 
            nameFinish = tempList.index('image:')
            nameStr = ' '.join(tempList[nameStart+1:nameFinish])
            model.append(nameStr)
        except ValueError:
            model.append(' ')

        simpValueGet('offerCount:', offers)
        simpValueGet('lowPrice:', lowPrice)
        simpValueGet('highPrice:', highPrice)

        date.append(checked)
        deviceID.append(loop+1)

        loop+=1
except IndexError:
    print('finshed')

# Appends results to master csv
with open(outputPath+'swappa_prices.csv','a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(zip(deviceID, date, maker, model, offers, lowPrice, highPrice))

print (timing)