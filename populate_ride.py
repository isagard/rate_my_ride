import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rate_my_ride.settings')
import django
django.setup()
from ride.models import Review,ServicePage

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories. 
    # This might seem a little bit confusing, but it allows us to iterate 
    # through each data structure, and add the data to our models.

    glasgow_reviews = {'Uber':{'userID':'001','location':'glasgow','service':'Uber','rating':5,'title':'my experience','body':'my experience was great'},
                        'GlasGo':{'UserID':'003','location':'glasgow','service':'GlasGo','rating':1,'title':'my experience','body':'my experience was bad'},
                        'BlackCabs':{'UserID':'001','location':'glasgow','service':'BlackCabs','rating':3,'title':'my experience','body':'my experience was good'}}
    edinburgh_reviews = {'Uber':{'UserID':'002','location':'edinburgh','service':'Uber','rating':5,'title':'my experience','body':'my experience was great'},
                        'EdinburghCityTaxis':{'UserID':'004','location':'glasgow','service':'EdinburghCityTaxis','rating':3,'title':'my experience','body':'my experience was ok'},
                        'BlackCabs':{'UserID':'002','location':'edinburgh','service':'BlackCabs','rating':4,'title':'my experience','body':'my experience was good'}}
    aberdeen_reviews = {'Uber':{'UserID':'005','location':'aberdeen','service':'Uber','rating':5,'title':'my experience','body':'my experience was great'}}

    glasgow_services = [
        {'name': 'GlasGo',
         'location':'glasgow','body':"we are GlasGo",'logo':'cat.jpg','reviews':glasgow_reviews},
        {'name':'Uber',
         'location':'glasgow','body':"we are Uber",'logo':'cat.jpg','reviews':glasgow_reviews},
        {'name':'BlackCabs',
         'location':'glasgow','body':"we are BlackCabs",'logo':'cat.jpg','reviews':glasgow_reviews} ]

    edinburgh_services = [
        {'name':'Uber',
         'location':'edinburgh','body':"we are Uber",'logo':'cat.jpg','reviews':edinburgh_reviews},
        {'name':'BlackCabs',
          'location':'edinburgh','body':'we are BlackCabs','logo':'cat.jpg','reviews':edinburgh_reviews},
        {'name':"EdinburghCityTaxis",
        'location':'edinburgh','body':'we are EdinburghCityTaxis','logo':'cat.jpg','reviews':edinburgh_reviews}]

    aberdeen_services = [
        {'name':'Uber',
         'location':'aberdeen','body':"we are Uber",'logo':'cat.jpg','reviews':aberdeen_reviews['Uber']}]

    locations = [glasgow_services,edinburgh_services,aberdeen_services]

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category, 
    # and then adds all the associated pages for that category.

    for location in locations:
        for service in location:
            serviceID = add_ServicePage(service['name'],service['location'],service['body'],service['logo'])
            # for review in service['reviews']:
            #     add_Review(serviceID,service['reviews'][review]['userID'],service['reviews'][review]['location'],service['reviews'][review]['service'],service['reviews'][review]['rating'],service['reviews'][review]['title'],service['reviews'][review]['body'])

    # Print out the categories we have added.
    for s in ServicePage.objects.all():
        for r in Review.objects.filter(serviceID=s):
            print(f'- {s}: {r}')

def add_ServicePage(name,location,body,logo):
    s = ServicePage.objects.get_or_create(name=name, location=location, body=body,logo=logo)[0] 
    s.save()
    return s

def add_Review(serviceID,userID,location, service, rating, title, body):
    r = Review.objects.get_or_create(serviceID=serviceID,userID=userID,location=location,service=service,rating=rating,title=title,body=body)[0] 
    r.save()
    return c

#Startexecutionhere!
if __name__=='__main__':
    print('Starting Ride population script...') 
    populate()


