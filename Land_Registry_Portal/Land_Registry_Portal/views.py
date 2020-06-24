from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.clickjacking import xframe_options_exempt
import hashlib
import random
from numpy.random import randint

from Land_Registry_Portal import ModuleAdvancedEncryptionStandard
from Land_Registry_Portal import ModuleInterPlanetaryFileSystem
from Land_Registry_Portal import ModuleLandRegistryPortal
from Land_Registry_Portal import ModuleTransactProperties
from Land_Registry_Portal import ModuleSearchProperty
from Land_Registry_Portal import ModuleSmartContracts
from Land_Registry_Portal import ModuleSendEmail


def index(request):
    try:
        if not request.user.is_authenticated:
            return redirect('/login_user/')
            
        user = str(request.user)
        return redirect('/land_registry_portal_index/')
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
        
def login_user(request):

    username = request.POST.get('username')
    password = request.POST.get('hash_all')
    client_random_number_hash = str(request.POST.get('client_random_number_hash'))
    
    if username == None:
        key = int(random.uniform(0,100000))
        fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
        fh.write(str(key))
        print(key)
        fh.close()
        return render(request, 'login_page.html', { 'key': key })
    
    else:
        print(username, password, client_random_number_hash)
        
        try:
            u = User.objects.get(username__exact=username)
            hash_from_db = u.password
            #print(hash_from_db)
        except:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
                
        #hash of the server_key
        fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'r')
        key = fh.read()
        fh.close()
        server_key_hash = str(hashlib.sha256(str(key).encode()).hexdigest())
        
        #generate the combined hash of hashed server_key, hashed client_key and hashed password
        h = str(hash_from_db+server_key_hash+client_random_number_hash).encode('utf8')
        hash_all = (hashlib.sha256(h)).hexdigest()
        print(hash_all, password)
        # if the combined hash generated here and extracted from request is matched, then details are correct and redirect user to next page
        # or else send an error message
        if hash_all == password:
            print('correct password')
            user = User.objects.get(username = request.POST['username'])
            login(request, user)
            return redirect('/land_registry_portal_index/')

        else:
            print('wrong password')
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'Wrong password!' })    
      

def signup_user(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'signup_page.html', { 'error': 'Username Already Exists!' })
            except User.DoesNotExist:
                password = str(hashlib.sha256(str(request.POST['password']).encode()).hexdigest())
                user = User.objects.create_user(username = request.POST['username'], password = password)
                login(request, user)
                return redirect('/land_registry_portal_index/')
        else:
            return render(request, 'signup_page.html', { 'error': 'Passwords doesn\'t match!' })
    else:
        return render(request, 'signup_page.html')
        

def land_registry_portal_index(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
            
        user = str(request.user)
        return render(request, 'land_registry_portal_index.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
    

def upload_details(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        return render(request,'upload_details.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
        
def upload_file(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        
        if request.method == 'POST':
            owner_name = request.POST.get("owner_name")  
            adhar_number = request.POST.get("adhar_number")
            email_id = request.POST.get("email_id")
            property_name = request.POST.get("property_name")
            file_name = request.POST.get("property_paper")
            
            plot_number = request.POST.get("plot_number")
            sector_number = request.POST.get("sector_number")
            road_name = request.POST.get("road_name")
            area_name = request.POST.get("area_name")
            city_name = request.POST.get("city_name")
            state_name = request.POST.get("state_name")  
            country_name = request.POST.get("country_name")
            pin_code = request.POST.get("pin_code")
            
            property_id, encrypted_file = ModuleAdvancedEncryptionStandard.encrypt_file(file_name, property_name)   
            # encrypted_file name format -> /(path)/(property_id)_(property_name).encrypted        
            
            property_paper_hash = ModuleInterPlanetaryFileSystem.upload_file_in_ipfs(property_id, property_name, encrypted_file)
            
            ModuleLandRegistryPortal.update_database(owner_name, adhar_number, email_id, property_name, property_id, plot_number, sector_number, road_name, area_name, city_name, state_name, country_name, pin_code)
            
            ModuleSmartContracts.add_details_to_blockchain(property_id, property_name)
            print(property_id, property_name)
            
            address = 'Plot no. : ' + str(plot_number) + ', Sector no. : ' + str(sector_number) + ', ' + road_name + ', ' + area_name + ', ' + city_name + ', ' + state_name + ', ' + country_name + ' - ' + str(pin_code)
            
            subject = 'Property Registration Details'
            body = 'Registration Process done by ' + user + '\n\n\nProperty Details: \n' + '      Property Name: ' + property_name + '\n      Address: ' + address + '\n\n\nOwner Details: \n' + '      Owner Name: ' + owner_name + '\n      Adhar Number: ' + str(adhar_number) + '\n      Email Id: ' + email_id
            
            ModuleSendEmail.send_mail(owner_name, 'snehalpadekar0@gmail.com', subject, body)
            
            return render(request, 'successful_msg_page.html', { 'user': user, 'msg': 'All the details are successfully uploaded to the Land Registry Portal! Mail sent to the owner!' })        
        else:
            return redirect('/land_registry_portal_index/')   
                  
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')


def search_property_by_user_details(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        
        if request.method == 'POST':
            name = request.POST.get("name")
            adhar_number = request.POST.get("adhar_number")
            email_id = request.POST.get("email_id")
            
            property_details = ModuleSearchProperty.retrieve_property_details_by_name(name, adhar_number, email_id)

            return render(request, 'retrieve_details.html', { 'user': user, 'property_details': property_details})
        else:
            return render(request, 'retrieve_details.html')
        
    except BaseException as e:
        return HttpResponseForbidden('Error searching <br> '+ str(e)+'<br>contact administrator')
        
        
def search_property_by_address(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        
        if request.method == 'POST':
            plot_number = request.POST.get("plot_number")
            sector_number = request.POST.get("sector_number")
            road_name = request.POST.get("road_name")
            area_name = request.POST.get("area_name")
            city_name = request.POST.get("city_name")
            state_name = request.POST.get("state_name")  
            country_name = request.POST.get("country_name")
            pin_code = request.POST.get("pin_code")            

            property_details = ModuleSearchProperty.retrieve_property_details_by_address(plot_number, sector_number, road_name, area_name, city_name, state_name, country_name, pin_code)
            
            return render(request,'search_property.html', { 'user': user, 'property_details': property_details })
            
        else:
            return render(request,'search_property.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error searching <br> '+ str(e)+'<br>contact administrator')
        

@xframe_options_exempt
def view_property_details(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        
        if request.method == 'GET':
            property_name = request.GET.get("property_name")
            
            property_details = ModuleSearchProperty.view_property(property_name)
            return render(request,'search_report.html', { 'user': user, 'property_details': property_details })
            
        else:
            return redirect('/search_property_by_address/')
        
    except BaseException as e:
        return HttpResponseForbidden('Error viewing the property <br> '+ str(e)+'<br>contact administrator')

        
def transact(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        return render(request,'transaction.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
            
def transaction(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        print('here')
        
        if request.method == 'POST':
            seller_name = request.POST.get("seller_name")  
            seller_adhar_number = request.POST.get("seller_adhar_number")
            seller_email_id = request.POST.get("seller_email_id")
            
            property_name = request.POST.get("seller_property_name")
            
            buyer_name = request.POST.get("buyer_name")  
            buyer_adhar_number = request.POST.get("buyer_adhar_number")
            buyer_email_id = request.POST.get("buyer_email_id")
            
            file_name = request.POST.get("property_paper")
            
            witness1_name = request.POST.get("witness1_name")
            witness1_aadhar_number = request.POST.get("witness1_aadhar_number")
            witness1_email_id = request.POST.get("witness1_email_id")
            witness1_mobno = request.POST.get("witness1_mobno")
            
            witness2_name = request.POST.get("witness2_name")
            witness2_aadhar_number = request.POST.get("witness2_aadhar_number")
            witness2_email_id = request.POST.get("witness2_email_id") 
            witness2_mobno = request.POST.get("witness2_mobno")
            
            print(seller_name, seller_adhar_number, seller_email_id, property_name, buyer_name, buyer_adhar_number, buyer_email_id, file_name, witness1_name, witness1_aadhar_number, witness1_email_id, witness1_mobno, witness2_name, witness2_aadhar_number, witness2_email_id, witness2_mobno)

            msg = ModuleTransactProperties.update_owner(seller_name, seller_adhar_number, seller_email_id, property_name, buyer_name, buyer_adhar_number, buyer_email_id, file_name, witness1_name, witness1_aadhar_number, witness1_email_id, witness1_mobno, witness2_name, witness2_aadhar_number, witness2_email_id, witness2_mobno)
            
            return render(request, 'successful_msg_page.html', { 'user': user, 'msg': msg })        
        else:
            return redirect('/land_registry_portal_index/')   
                  
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
     
def about_land_registry_portal(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        
        return render(request, 'about.html', { 'user': user })
        
        
    except BaseException as e:
        return HttpResponseForbidden('Error loading page <br> '+ str(e)+'<br>Contact administrator')
  

def contact_us(request):
    try:
        if not request.user.is_authenticated:
            key = int(random.uniform(0,100000))
            fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
            fh.write(str(key))
            fh.close()
            return render(request, 'login_page.html', { 'key': key, 'error': 'You must Login first!' })
        
        user = str(request.user)
        
        if request.method == 'POST':
            name = request.POST.get("name")  
            email = request.POST.get("email")
            subject = request.POST.get("subject")            
            message = request.POST.get("message")
            
            body = 'Name: ' + name + '\nEmail ID: ' + email + '\nQuery: \n      ' + message
            #ModuleSendEmail.send_mail('dishashinde17@gmail.com', 'snehalpadekar0@gmail.com', subject, body)
            
            return render(request, 'successful_msg_page.html', { 'user': user, 'msg': 'Our team will come back to you within a matter of hours to help you!' })  
        
        return render(request, 'contact.html', { 'user': user })        
        
    except BaseException as e:
        return HttpResponseForbidden('Error loading page <br> '+ str(e)+'<br>Contact administrator')
     
    
def logout_user(request):
    logout(request)
    key = int(random.uniform(0,100000))
    fh = open(r'C:\Users\DISHA\Documents\GitHub\BE Project\Land_Registry_Portal\Land_Registry_Portal\serverkey.txt', 'w')
    fh.write(str(key))
    fh.close()
    return render(request, 'login_page.html', { 'key': key, 'error': 'You are logged out!' })
    
    