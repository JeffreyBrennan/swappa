import requests, timing, csv
from bs4 import BeautifulSoup
# makerList = ['apple','samsung','google', 'oneplus','lg','htc', 'oppo', 'huawei', 'blackberry', 'sony']
swpURL = 'https://swappa.com/mobile/'
swpDeviceURL = 'https://swappa.com/buy/'

outputPath = 'C:/Users/jeffb/Documents/Python/webPrograms/webScraping/swappa/output/'


deviceCounter = 1
## init lists
links, cleanList, matching, matchList, deviceList, makersList= ([] for i in range(6))

## change value based on desired carrier info
desiredCarriers = ['-att', '-verizon', '-unlocked', '-sprint']


def read_makers():
    with open('all_makers.csv', newline='') as r:
        file = csv.reader(r, delimiter =',')
        for row in file:
            for i in row:
                makersList.append(i)
                


## grabs all devices (all by default, carrier specific by uncommenting partial list part 
def deviceGet(device): 
   
    r_car = requests.get(swpDeviceURL+device)
    r_soup = BeautifulSoup(r_car.text, 'html.parser')

    carrierGet = r_soup.find_all('div', class_='col-xs-12 col-sm-6')

    ## for full list
    for content in carrierGet:
        for sup in content('sup'):
            if '$' in sup:
                for a in content('a'):
                    if a.text:
                        ## comment out if partial list desired
                        deviceList.append(a['href'])
                        
                        ## for partial list based on desired carrier(s)
                        # tempLink= a['href']
                        # if any(word in tempLink for word in desiredCarriers):
                        #     deviceList.append(tempLink)
    print ('Device ' + str(deviceCounter) + '/' + trimmedLength)

def fixList (device):
    return device[5:]

def nameGet(maker): 

    r = requests.get(swpURL+maker)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.findAll('a')


    for link in results:
        if link.has_attr('href'):
            links.append(link['href'])

    matching = [s for s in links if '/buy/'+maker+'-' in s]

    matchList.append (matching)

read_makers()
for i in makersList:
    nameGet(i)

flat_list = [item for sublist in matchList for item in sublist]
cleanList = sorted(list(set(flat_list)))
# carrier_list = '\t'.join(cleanList)
trimmedList = [fixList(device) for device in cleanList]
trimmedLength = str(len(trimmedList))
print ('Number of devices:' + trimmedLength)

for i in trimmedList:
    deviceGet(i)
    deviceCounter +=1 

trimmedDevices = [fixList(device) for device in deviceList]

totalList = (trimmedList + trimmedDevices)
uniqueTotal = sorted(list(set(totalList)))



with open(outputPath+'swappa_devices.csv','w', newline='') as f:
    writer = csv.writer(f)
    for i in uniqueTotal:
        writer.writerow([i])