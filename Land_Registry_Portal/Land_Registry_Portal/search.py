
def search():
	district_name = request.POST.get("district_name")  
    city_name = request.POST.get("city_name")
    area_name = request.POST.get("area_name")          
    plot_number = request.POST.get("plot_number")
    sector_number = request.POST.get("sector_number") 

   property_id,property_name,owner_name,adhar_number,email,registration_time = ModuleSearchProperty.search_property(district_name,city_name,area_name, plot_number, sector_number)
   



search()