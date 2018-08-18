import requests, csv, time, datetime, timing
from bs4 import BeautifulSoup

timeNow = time.time()
outputPath = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/swappa/output/'

swpURL = 'https://swappa.com/specs/'
checked = time.asctime(time.localtime())
loop = 0
deviceCounter = 1

## initialize lists
phoneList, specList, date, processor, storage, resolution, displaysize, rearCamera, frontCamera, \
megapixels, batteryinfo, batteryreplace, devicetype, deviceName= ([] for i in range(14))

with open('swappa_devices.csv', newline='') as r:
    file = csv.reader(r, delimiter =',')
    for row in file:
        for i in row:
            phoneList.append(i)

deviceLength = str(len(phoneList))


## replace with csv from program that gets all phones listed on swappa in future
# phoneList = ['google-pixel-2-xl-unlocked', 'apple-iphone-x-a1901-gsm-att',
#             'oneplus-6-unlocked', 'samsung-galaxy-s9-plus-att']

def specGet (device):
    r = requests.get(swpURL + device)
    s = BeautifulSoup(r.text, 'html.parser')
    carrierGet = s.find_all('div', class_='col-md-6')
    for table in carrierGet:
        for tbody in table('table'):
            for tr in tbody('tr'):
                specList.append(tr.text)

            # for th in tr('th', colspan='2'):
            #     print (th.text)
            # for td in tr('td'):
            #     print ((td.text).split())
    print ('Device ' + str(deviceCounter) + '/' + deviceLength)

def simpValueGet(key, output_list):
    try: 
        tempList = cleanList[startpoints[loop]:]
        valueLoc = tempList.index(key) + 1
        valueStr = tempList[valueLoc]
        output_list.append(valueStr)
    except ValueError:
        output_list.append(' ')        

def rangeValueGet (start, finish, output_list):
    try:
        tempList = cleanList[startpoints[loop]:]
        startLoc = tempList.index(start) + 1
        finishLoc = tempList[startLoc:].index(finish)
        valueStr = ' '.join(tempList[startLoc:finishLoc+startLoc])
        output_list.append(valueStr)
    except ValueError:
        output_list.append(' ')
    except IndexError: 
        pass

for i in phoneList:
    specList.append(i)
    specGet(i)
    deviceCounter+=1

resultStr = ''.join(specList)
resultStr = resultStr.replace('"','').replace('{','') \
                     .replace('}','').replace('\t','').replace('\n',' ')
cleanList = resultStr.split()
startpoints = [i for i, x in enumerate(cleanList) if x == 'General']


for i in phoneList:
    try:
        tempList = cleanList[startpoints[loop]:]

        # for a,b,c in rangeRequests: 
        #     rangeValueGet(a,b,c)

        ## working 
        rangeValueGet('Processor', 'Storage', processor)## Processor (range)
        simpValueGet('Size', displaysize)## Display size (simp)
        simpValueGet('Replaceable', batteryreplace)## Battery replacement (simp)
        simpValueGet('Data', devicetype)## Device type (simp)
        rangeValueGet('Resolution', 'Display', resolution)## Resolution (range)
        rangeValueGet('Rear:', 'Front:', rearCamera)## Rear camera (range)
        rangeValueGet('Front:', 'Megapixels', frontCamera)## Front camera (range)
        rangeValueGet('Ion', 'Replaceable', batteryinfo)## Battery info (range)
        deviceName.append(i)
        date.append(checked)

        ## requires cleaning in excel
        ## make third function to handle multiple keys
        rangeValueGet('Memory', 'Display', storage)## Storage (range)

        loop+=1
        print (str(loop) + '/' + str(len(phoneList)))

    except IndexError:
        pass
    

with open(outputPath+'swappa_specs.csv','a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(zip(date, deviceName, devicetype, storage, processor, resolution, \
                        displaysize, rearCamera, frontCamera, batteryinfo, batteryreplace))
