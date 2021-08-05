import requests
import random


UNSPLASH_KEY = 'xPrX-I8RV8Ckm_2WNqjjAxRrIMU-pu1KFDK4w1gcCYw'

def africanCountry():
    countries = [
        ('DZ', 'Algeria'),
        ('AO', 'Angola'),
        ('BJ', 'Benin'),
        ('BW', 'Botswana'),
        ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'),
        ('CM', 'Cameroon'),
        ('CV', 'Cape Verde'),
        ('CF', 'Central African Republic'),
        ('TD', 'Chad'),
        ('KM', 'Comoros'),
        ('CD', 'Democratic Republic of the Congo'),
        ('CG', 'Republic of the Congo'),
        ('CI', 'Ivory Coast'),
        ('DJ', 'Djibouti'),
        ('EG', 'Egypt'),
        ('GQ', 'Equatorial Guinea'),
        ('ER', 'Eritrea'),
        ('ET', 'Ethiopia'),
        ('GA', 'Gabon'),
        ('GM', 'Gambia'),
        ('GH', 'Ghana'),
        ('GN', 'Guinea'),
        ('GW', 'Guinea Bissau'),
        ('KE', 'Kenya'),
        ('LS', 'Lesotho'),
        ('LR', 'Liberia'),
        ('LY', 'Libya'),
        ('MG', 'Madagascar'),
        ('MW', 'Malawi'),
        ('ML', 'Mali'),
        ('MR', 'Mauritania'),
        ('MU', 'Mauritius'),
        ('MA', 'Morocco'),
        ('MZ', 'Mozambique'),
        ('NA', 'Namibia'),
        ('NE', 'Niger'),
        ('NG', 'Nigeria'),
        ('RW', 'Rwanda'),
        ('ST', 'São Tomé and Príncipe'),
        ('SN', 'Senegal'),
        ('SC', 'Seychelles'),
        ('SL', 'Sierra Leone'),
        ('SO', 'Somalia'),
        ('ZA', 'South Africa'),
        ('SS', 'South Sudan'),
        ('SD', 'Sudan'),
        ('TZ', 'Tanzania'),
        ('TG', 'Togo'),
        ('TN', 'Tunisia'),
        ('UG', 'Uganda'),
        ('ZM', 'Zambia'),
        ('ZW', 'Zimbabwe')
    ]
    print("called!")
    country = random.choice(countries)
    return country[1]

def mediawikiAPI(page):
    url = 'http://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext=1&exintro=1&titles=%s' % (page)
    headers = {'User-Agent': 'AfriXplore'}

    response = requests.get(url, headers=headers)
    data = response.json()
    
    for key in data['query']['pages']:
        return data['query']['pages'][key]['extract']

def unsplashAPI(page):
    url = 'https://api.unsplash.com/search/photos?page=1&query=%s&client_id=%s' % (page, UNSPLASH_KEY)
    response = requests.get(url)
    data = response.json()
    
    linklist = []
    for pic in data['results']:
        linklist.append(pic['urls']['regular'])
        if len(linklist) >= 3:
            break
        
    
    return linklist

