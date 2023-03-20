import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')
import django
django.setup()
from ride.models import Reviews,ServicePage

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories. 
    # This might seem a little bit confusing, but it allows us to iterate 
    # through each data structure, and add the data to our models.

    locations = [glasgow_services,edinburgh_services,aberdeen_services]

    glasgow_services = [
        {'name': 'GlasGo',
         'location':'glasgow','body':"we are GlasGo",'logo':'cat.jpg','reviews':glasgow_reviews['GlasGo']},
        {'name':'Uber',
         'location':'glasgow','body':"we are Uber",'logo':'cat.jpg','reviews':glasgow_reviews['Uber']},
        {'name':'BlackCabs',
         'location':'glasgow','body':"we are BlackCabs",'logo':'cat.jpg','reviews':glasgow_reviews['BlackCabs']} ]

    edinburgh_services = [
        {'name':'Uber',
         'location':'edinburgh','body':"we are Uber",'logo':'cat.jpg','reviews':edinburgh_reviews['Uber']},
        {'name':'BlackCabs',
         'location':'edinburgh','body':"we are BlackCabs",'logo':'cat.jpg',edinburgh_reviews['BlackCabs']},
        {'name': 'EdinburghCityTaxis',
         'location':'edinburgh','body':"we are EdinburghCityTaxis",'logo':'cat.jpg',edinburgh_reviews['EdinburghCityTaxis']}, ]

    aberdeen_services = [
        {'name':'Uber',
         'location':'glasgow','body':"we are Uber",'logo':'cat.jpg',aberdeen_reviews['Uber']}]

    glasgow_reviews = []
    edinburgh_reviews = []
    aberdeen_reviews = []

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category, 
    # and then adds all the associated pages for that category.

    for location in locations:
        for service in location:
            add_ServicePage(service['name'],service['location'],service['body'],service['logo'])
            for review in service['reviews']:
                add_Review(review['location'],review['service'],review['rating'],review['title'],review['body'])

    # Print out the categories we have added.
    for s in ServicePage.objects.all():
        for r in Review.objects.filter(serviceID=s):
            print(f'- {s}: {r}')

def add_ServicePage(name,location,body,logo):
    s = ServicePage.objects.get_or_create(name=name, location=location, body=body,logo=logo)[0] 
    s.save()
    return s

def add_Review(location, service, rating, title, body):
    r = Review.objects.get_or_create(location=location,service=service,rating=rating,title=title,body=body)[0] 
    r.save()
    return c

#Startexecutionhere!
if __name__=='__main__':
    print('Starting Rango population script...') 
    populate()




    # glasgow_services = {'GlasGo' : {'reviews':glasgow_reviews,'location':'glasgow','body':"we are GlasGo"},
    #     'Uber' : {'location':'glasgow','body':"we are Uber"},
    #     'BlackCabs' : {'location':'glasgow','body':"we are BlackCabs"} 
    #     }

    # edinburgh_services = {'Uber' : {'location':'edinburgh','body':"we are Uber"},
    #     'BlackCabs' : {'location':'edinburgh','body':"we are BlackCabs"},
    #     'EdinburghCityTaxis' : {'location':'edinburgh','body':"we are EdinburghCityTaxis"}
    #     }

    # aberdeen_services ={'Uber' : {'location':'glasgow','body':"we are Uber"}}




