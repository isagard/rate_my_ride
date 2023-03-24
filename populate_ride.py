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

    glasgow_reviews = {'Uber':[{'userID':user1.id,'location':'Glasgow','service':'Uber','rating':3,'title':'Slow connection to uber','body':"Took a while to connect to an uber and the driver as not as friendly as other taxis I've taken.",'likes':2}, 
                               {'userID':user2.id,'location':'Glasgow','service':'Uber','rating':5,'title':'Excellent!','body':"Excellent service, the driver arrived within 5 minutes of booking and was very friendly. The car was clean and comfortable. Will definitely use Uber again!",'likes':4},
                               {'userID':user3.id,'location':'Glasgow','service':'Uber','rating':2,'title':'Terrible :(','body':"Had a terrible experience with Uber. The driver was rude and the car was dirty. Would not recommend.",'likes':3},
                               {'userID':user4.id,'location':'Glasgow','service':'Uber','rating':3,'title':'OK','body':"Overall good experience with Uber, but the prices can be quite high during peak hours.",'likes':3}],
                       'GlasGo':[{'userID':user3.id,'location':'Glasgow','service':'GlasGo','rating':1,'title':'Would not recommend this taxi','body':"Absolutely shocking service! App is telling me I have a 4 minute wait for a taxi so I booked! Iv waited the best part of an hour for the taxi to arrive! When I phoned they couldn't tell me how long I will be waiting! I could have got a bus faster!",'likes':2},
                                 {'userID':user4.id,'location':'Glasgow','service':'GlasGo','rating':1,'title':'Not reccomendable','body':"Had a terrible experience with GlasGo. The driver was very late and the customer service was not helpful at all.",'likes':3}],
                       'Glasgow Taxi':[{'userID':user1.id,'location':'Glasgow','service':'Glasgow Taxi','rating':5,'title':'Quick and reliable','body':"Needed taxi quick,as it started bucketing down and had to get the wain to nursery. Tried phoning private taxi, couldn't even get an answer said no cars in area. Then phoned glasgow taxi and they arrived in 5 minutes.",'likes':8},
                                       {'userID':user2.id,'location':'Glasgow','service':'Glasgow Taxi','rating':5,'title':'Great!','body':"Great service from Glasgow Taxi! The driver was friendly and arrived on time. The price was also very reasonable. Highly recommend.",'likes':8}]
    }
    edinburgh_reviews = {'Uber':[{'userID':user2.id,'location':'Edinburgh','service':'Uber','rating':5,'title':'Speedy cab with friendly and helpful. driver','body':"Was fast and easy to find an uber. The driver was very friendly and gave us good recommendations for places to go and eat.",'likes':13},
                                 {'userID':user3.id,'location':'Edinburgh','service':'Uber','rating':4,'title':'Great','body':"Overall good experience with Uber, but the prices can be quite high during peak hours.",'likes':2},
                                 {'userID':user1.id,'location':'Edinburgh','service':'Uber','rating':5,'title':'Excellent!','body':"Excellent service, the driver arrived within 5 minutes of booking and was very friendly. The car was clean and comfortable. Will definitely use Uber again!",'likes':8}],
                         'City Cabs':[{'userID':user4.id,'location':'Edinburgh','service':'City Cabs','rating':3,'title':'Not great for booking a cab in advanced','body':'I could only book on the app if I wanted to book the taxi to the airport for the next morning, so I had to call and hope for a taxi to come at 4am.','likes':4},
                                      {'userID':user4.id,'location':'Edinburgh','service':'City Cabs','rating':3,'title':'Okay','body':"City Cabs is an okay service, but the prices are a bit high compared to other taxi services in Glasgow.",'likes':2}],
                         'Central Taxis':[{'userID':user2.id,'location':'Edinburgh','service':'Central Taxis','rating':4,'title':'Excellent service','body':"Drivers will get out and help with doors or bags too. Smidgen more expensive than Uber etc but if you wanna arrive somewhere in a wee bit style a Black Cab fae Central Taxi's is a must.",'likes':6},
                                          {'userID':user3.id,'location':'Edinburgh','service':'Central Taxis','rating':5,'title':'Fab!','body':"Lovely driver, had a great time",'likes':10}]
    }
    aberdeen_reviews = {'Uber':[{'userID':user4.id,'location':'Aberdeen','service':'Uber','rating':5,'title':'Great, dependable taxi service','body':'Always quick and reliable to get an uber. The drivers in aberdeen are very friendly.','likes':3},
                                {'userID':user3.id,'location':'Aberdeen','service':'Uber','rating':5,'title':'Really good','body':"Dependable taxi service from Uber in Aberdeen. The drivers are always professional and friendly.",'likes':4}], 
                        'Aberdeen Taxis':[{'userID':user4.id,'location':'Aberdeen','service':'Aberdeen Taxis','rating':1,'title':'The worst','body':'Was staying in aberdeen to attend a concert at P&J live. While at hotel reception they phoned and booked us a taxi to be picked up at 19:00 from the hotel and then at 22:30 from the venue, they got us there ok but where nowhere to be seen at 22:30. We tried phoning them ourselves but got no answer so contacted the hotel who phoned them only to be told there was no record of the booking on their system, which seems a bit strange as they sent a text to my wifes mobile to confirm the pick up. After attempting in vain to get a taxi we had to walk the 1.5miles back to the hotel, thankfully it was not raining but was cold. SO WOULD NOT USE THIS FIRM.','likes':3},
                                          {'userID':user1.id,'location':'Aberdeen','service':'Aberdeen Taxis','rating':1,'title':'Terrible','body':"Had a terrible experience with Aberdeen Taxis. The driver was very rude and the car was dirty. Would not recommend this service.",'likes':2}]
    }

    glasgow_services = [
        {'name': 'GlasGo',
         'location':'Glasgow','body':"GlasGO Cabs | Taxis Glasgow & Airport Transfers – the largest in Scotland and will allowing us to provide an improved service to all our customers old and new.",'logo':'/static/images/glasgo.png','reviews': {'GlasGo': glasgow_reviews['GlasGo']},'views':12},
        {'name':'Uber',
         'location':'Glasgow','body':"Get a ride in minutes. Or become a driver and earn money on your schedule. Uber is finding you better ways to move, work, and succeed in the UK.",'logo':'/static/images/uber.jpeg','reviews': {'Uber': glasgow_reviews['Uber']},'views':19},
        {'name':'Glasgow Taxi',
         'location':'Glasgow','body':"With a fleet of over 800 taxis, we are the largest supplier of licensed taxis in Glasgow, Scotland, and the largest in the UK outside London. Nobody knows Glasgow like we do and that means whether you are an individual or a business, large or small, if you’re looking for taxis in Glasgow we can provide you with an efficient, reliable taxi service, 24 hours a day, every day of the year.",'logo':'/static/images/glasgowTaxi.png','reviews': {'Glasgow Taxi': glasgow_reviews['Glasgow Taxi']},'views':18} ]

    edinburgh_services = [
        {'name':'Uber',
         'location':'Edinburgh','body':"Get a ride in minutes. Or become a driver and earn money on your schedule. Uber is finding you better ways to move, work, and succeed in the UK.",'logo':'/static/images/uber.jpeg','reviews': {'Uber': edinburgh_reviews['Uber']},'views':24},
        {'name':'Central Taxis',
          'location':'Edinburgh','body':'For 50 years we have been Edinburgh’s most reliable taxi company. A co-operative with over 1100 drivers from the local community, Central Taxis is proud to operate Edinburgh’s biggest fleet with over 465 black taxis serving you 24/7.','logo':'/static/images/central_taxis.png','reviews': {'Central Taxis': edinburgh_reviews['Central Taxis']},'views':13},
        {'name':"City Cabs",
        'location':'Edinburgh','body':'With over 90 years experience City Cabs provide a fast, efficient, reliable and safe taxi service in Edinburgh that is backed up by the best technology.','logo':'/static/images/city_cabs.png','reviews': {'City Cabs': edinburgh_reviews['City Cabs']},'views':15}]

    aberdeen_services = [
        {'name':'Uber',
         'location':'Aberdeen','body':"Get a ride in minutes. Or become a driver and earn money on your schedule. Uber is finding you better ways to move, work, and succeed in the UK.",'logo':'/static/images/uber.jpeg','reviews': {'Uber': aberdeen_reviews['Uber']},'views':11},
         {'name':'Aberdeen Taxis',
         'location':'Aberdeen','body':"Welcome to Aberdeen Taxis, your specialist taxi company covering the whole of Aberdeen and the local area. Taxi bookings can be made fast, easily and securely online using this website or by using the phone number at the top of the page.",'logo':'/static/images/aberdeenTaxis.jpeg','reviews': {'Aberdeen Taxis': aberdeen_reviews['Aberdeen Taxis']},'views':11}]

    locations = [glasgow_services,edinburgh_services,aberdeen_services]

   
    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category, 
    # and then adds all the associated pages for that category.

    for location in locations:
        for service in location:
            serviceID = add_ServicePage(service['name'],service['location'],service['body'],service['logo'],service['views'])
            for review_key, review_data in service['reviews'].items():
                for i in range(len(review_data)):
                    user_instance = User.objects.get(id=review_data[i]['userID'])
                    add_Review(serviceID, user_instance, review_data[i]['location'], review_data[i]['service'], review_data[i]['rating'], review_data[i]['title'], review_data[i]['body'], review_data[i]['likes'])
                          
    # Print out the categories we have added.
    # for s in ServicePage.objects.all():
    #     for r in Review.objects.filter(serviceID=s):
    #         print(f'- {s}: {r}')

def add_ServicePage(name,location,body,logo,views):
    s = ServicePage.objects.get_or_create(name=name, location=location, body=body,logo=logo,views=views)[0] 
    s.save()
    return s

def add_Review(serviceID, user_instance, location, service, rating, title, body,likes):
    r = Review.objects.get_or_create(serviceID=serviceID, userID=user_instance, location=location, service=service, rating=rating, title=title, body=body,likes=likes)[0]
    r.save()
    return r

#Startexecutionhere!
if __name__=='__main__':
    print('Starting Ride population script...') 
    populate()
    print('Population Script Complete')


