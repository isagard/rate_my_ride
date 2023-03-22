import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rate_my_ride.settings')
import django
django.setup()
from ride.models import Review,ServicePage
from django.contrib.auth.models import User

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories. 
    # This might seem a little bit confusing, but it allows us to iterate 
    # through each data structure, and add the data to our models.

    user1 = User.objects.create_user(username='user001', email='user001@example.com', password='password')
    user2 = User.objects.create_user(username='user002', email='user002@example.com', password='password')
    user3 = User.objects.create_user(username='user003', email='user003@example.com', password='password')
    user4 = User.objects.create_user(username='user004', email='user004@example.com', password='password')

    glasgow_reviews = {'Uber':{'userID':user1.id,'location':'glasgow','service':'Uber','rating':5,'title':'my experience','body':'my experience was great'},
                        'GlasGo':{'userID':user3.id,'location':'glasgow','service':'GlasGo','rating':1,'title':'my experience','body':'my experience was bad'},
                        'BlackCabs':{'userID':user1.id,'location':'glasgow','service':'BlackCabs','rating':3,'title':'my experience','body':'my experience was good'}}
    edinburgh_reviews = {'Uber':{'userID':user2.id,'location':'edinburgh','service':'Uber','rating':5,'title':'my experience','body':'my experience was great'},
                        'EdinburghCityTaxis':{'userID':user4.id,'location':'glasgow','service':'EdinburghCityTaxis','rating':3,'title':'my experience','body':'my experience was ok'},
                        'BlackCabs':{'userID':user2.id,'location':'edinburgh','service':'BlackCabs','rating':4,'title':'my experience','body':'my experience was good'}}
    aberdeen_reviews = {'Uber':{'userID':user4.id,'location':'aberdeen','service':'Uber','rating':5,'title':'my experience','body':'my experience was great'}}

    glasgow_services = [
        {'name': 'GlasGo',
         'location':'Glasgow','body':"we are GlasGo",'logo':'cat.jpg','reviews': {'GlasGo': glasgow_reviews['GlasGo'], 'Uber': glasgow_reviews['Uber'], 'BlackCabs': glasgow_reviews['BlackCabs']}},
        {'name':'Uber',
         'location':'Glasgow','body':"we are Uber",'logo':'cat.jpg','reviews': {'GlasGo': glasgow_reviews['GlasGo'], 'Uber': glasgow_reviews['Uber'], 'BlackCabs': glasgow_reviews['BlackCabs']}},
        {'name':'BlackCabs',
         'location':'Glasgow','body':"we are BlackCabs",'logo':'cat.jpg','reviews': {'GlasGo': glasgow_reviews['GlasGo'], 'Uber': glasgow_reviews['Uber'], 'BlackCabs': glasgow_reviews['BlackCabs']}} ]

    edinburgh_services = [
        {'name':'Uber',
         'location':'Edinburgh','body':"we are Uber",'logo':'cat.jpg','reviews': {'Uber': edinburgh_reviews['Uber'], 'EdinburghCityTaxis': edinburgh_reviews['EdinburghCityTaxis'], 'BlackCabs': edinburgh_reviews['BlackCabs']}},
        {'name':'BlackCabs',
          'location':'Edinburgh','body':'we are BlackCabs','logo':'cat.jpg','reviews': {'Uber': edinburgh_reviews['Uber'], 'EdinburghCityTaxis': edinburgh_reviews['EdinburghCityTaxis'], 'BlackCabs': edinburgh_reviews['BlackCabs']}},
        {'name':"EdinburghCityTaxis",
        'location':'Edinburgh','body':'we are EdinburghCityTaxis','logo':'cat.jpg','reviews': {'Uber': edinburgh_reviews['Uber'], 'EdinburghCityTaxis': edinburgh_reviews['EdinburghCityTaxis'], 'BlackCabs': edinburgh_reviews['BlackCabs']}}]

    aberdeen_services = [
        {'name':'Uber',
         'location':'Aberdeen','body':"we are Uber",'logo':'cat.jpg','reviews': {'Uber': aberdeen_reviews['Uber']}}]

    locations = [glasgow_services,edinburgh_services,aberdeen_services]

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category, 
    # and then adds all the associated pages for that category.

    for location in locations:
        for service in location:
            serviceID = add_ServicePage(service['name'],service['location'],service['body'],service['logo'])
            for review_key, review_data in service['reviews'].items():
                user_instance = User.objects.get(id=review_data['userID'])
                add_Review(serviceID, user_instance, review_data['location'], review_data['service'], review_data['rating'], review_data['title'], review_data['body'])
                          
    # Print out the categories we have added.
    # for s in ServicePage.objects.all():
    #     for r in Review.objects.filter(serviceID=s):
    #         print(f'- {s}: {r}')

def add_ServicePage(name,location,body,logo):
    s = ServicePage.objects.get_or_create(name=name, location=location, body=body,logo=logo)[0] 
    s.save()
    return s

def add_Review(serviceID, user_instance, location, service, rating, title, body):
    r = Review.objects.get_or_create(serviceID=serviceID, userID=user_instance, location=location, service=service, rating=rating, title=title, body=body)[0]
    r.save()
    return r

#Startexecutionhere!
if __name__=='__main__':
    print('Starting Ride population script...') 
    populate()


