from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from Land_Registry_Portal import ModuleAdvancedEncryptionStandard
from Land_Registry_Portal import ModuleInterPlanetaryFileSystem
from Land_Registry_Portal import ModuleLandRegistryPortal


def index(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html',{ 'error': 'You must Login first' })
            
        user = str(request.user)
        return redirect('/land_registry_portal_index/')
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
        
def login_user(request):
    if request.method == 'POST':
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/land_registry_portal_index/')
        else:
            return render(request, 'login_page.html', { 'error': 'Invalid Login Credentials!' })
    else:
        return render(request, 'login_page.html')
        

def signup_user(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'signup_page.html', { 'error': 'Username Already Exists!' })
            except User.DoesNotExist:
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password'])
                login(request, user)
                return redirect('/land_registry_portal_index')
        else:
            return render(request, 'signup_page.html', { 'error': 'Passwords doesn\'t match!' })
    else:
        return render(request, 'signup_page.html')
        

def land_registry_portal_index(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html',{ 'error': 'You must Login first' })
            
        user = str(request.user)
        return render(request, 'land_registry_portal_index.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
    

def upload_details(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html',{ 'error': 'You must Login first' })
        
        user = str(request.user)
        return render(request,'upload_details.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
        
def upload_file(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html', { 'error': 'You must Login first' })
        
        user = str(request.user)
        
        if request.method == 'POST':
            owner_name = request.POST.get("owner_name")  
            adhar_number = request.POST.get("adhar_number")
            email_id = request.POST.get("email_id")           
            property_name = request.POST.get("property_name")
            file_name = request.POST.get("property_paper")
            
            property_id, encrypted_file = ModuleAdvancedEncryptionStandard.encrypt_file(file_name, property_name)   
            # encrypted_file name format -> /(path)/(property_id)_(property_name).encrypted
            
            property_paper_hash = ModuleInterPlanetaryFileSystem.upload_file_in_ipfs(property_id, property_name, encrypted_file)
            ModuleLandRegistryPortal.update_database(owner_name, adhar_number, email_id, property_name, property_id)
            # ModuleSendEmail.send_mail(hash, email_id)
            
            return render(request, 'successful_msg_page.html', { 'user': user, 'msg': 'All the details are successfully uploaded to the Land Registry Portal!' })        
        else:
            return redirect('/land_registry_portal_index/')   
                  
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
  

def retrieve_details(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html',{ 'error': 'You must Login first' })
        
        user = str(request.user)
        return render(request,'retrieve_details.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
	
def retrieve_file(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html',{ 'error': 'You must Login first' })
        
        user = str(request.user)
        
        if request.method == 'POST':
            property_id = request.POST.get("property_id")
            property_hash = request.POST.get("property_hash")
            email_id = request.POST.get("email_id")
            property_name = request.POST.get("property_name")
            
            ModuleInterPlanetaryFileSystem.retrieve_file_from_ipfs(property_id, property_name, property_hash)
            decrypted_file = ModuleAdvancedEncryptionStandard.decrypt_file(property_id)
            #ModuleSendEmail.send_mail(hash, email_id)
            
            return render(request, 'successful_msg_page.html', { 'user': user, 'msg': 'All the details are successfully retrieved from the Land Registry Portal and mailed to '+str(user)+'!' })
        
        else:
            return redirect('/land_registry_portal_index/')   
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
        
def search_property_by_address(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html',{ 'error': 'You must Login first' })
        
        user = str(request.user)
        
        if request.method == 'POST':
            # district_name = request.POST.get("district_name")  
            # city_name = request.POST.get("city_name")
            # area_name = request.POST.get("area_name")          
            # plot_number = request.POST.get("plot_number")
            # sector_number = request.POST.get("sector_number") 

            property_id, property_name, owner_name, adhar_number,email, registration_time = ModuleSearchProperty.search_property(district_name, city_name, area_name, plot_number, sector_number)
            
            return render(request,'search_report.html', { 'user': user })
            
        else:
            return render(request,'search_property.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
        
def transact(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html',{ 'error': 'You must Login first' })
        
        user = str(request.user)
        return render(request,'transaction.html', { 'user': user })
        
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
            
def trasaction(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'login_page.html', { 'error': 'You must Login first' })
        
        user = str(request.user)
        
        if request.method == 'POST':
            seller_name = request.POST.get("seller_name")  
            seller_adhar_number = request.POST.get("seller_adhar_number")
            seller_email_id = request.POST.get("seller_email_id")
            
            property_name = request.POST.get("property_name")
            
            buyer_name = request.POST.get("buyer_name")  
            buyer_adhar_number = request.POST.get("buyer_adhar_number")
            buyer_email_id = request.POST.get("buyer_email_id")
            buyer_verification = request.POST.get("buyer_verification")

            ModuleTransactProperties.update_owner(seller_name, seller_adhar_number, seller_email_id, property_name, buyer_name, buyer_adhar_number, buyer_email_id, buyer_verification, file_name)
            
            return render(request, 'successful_msg_page.html', { 'user': user, 'msg': 'All the details are successfully uploaded to the Land Registry Portal!' })        
        else:
            return redirect('/land_registry_portal_index/')   
                  
    except BaseException as e:
        return HttpResponseForbidden('Error registering <br> '+ str(e)+'<br>contact administrator')
        
        
def logout_user(request):
    logout(request)
    return render(request, 'login_page.html', { 'error': 'You are logged out!' })
    
    