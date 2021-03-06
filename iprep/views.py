from django.shortcuts import render
from django.http import HttpResponse
import IP2Location
import re
import socket
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# Create your views here.
def home_view(request):
    query = request.GET.get('query')
    data = dict()
    if query is None:
        data = ip2location('127.0.0.1')
    else:
        data = ip2location(query)
    #print(type(data))
    return render(request, "home.html", context={"Data": data})




def multiip(request):
    data_check = []
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file_data')
        if uploaded_file is not None:
            #print(uploaded_file.readlines)
            data_check = handle_uploaded_file(uploaded_file)
    if request.method == 'POST' and 'multiquery' in request.POST:
        multiip_data = request.POST.get('multiquery')
        #print("TextBox {}" .format(multiip_data))
        if multiip_data is not None:
            #print(multiip_data)
            textBoxList = re.split('\r\n',multiip_data)
            for ip in textBoxList:
                if validate_ip(ip):
                    data_check.append(ip)

    renderData = []
    if data_check:
        for data in data_check:
            renderData.append(ip2location(data))

    #print(renderData) #Final Data to be Render in Table

    return render(request, "multiip.html", context={"renderData": renderData})


def handle_uploaded_file(f):
    ip_list = []
    for chunk in f:
        chunk = chunk.decode('ASCII')
        chunk = chunk.rstrip("\n")
        if validate_ip(chunk):
            #print(chunk)
            ip_list.append(chunk)
    return ip_list

#---------------------------------check Ipv4 is valid or not----------------
def validate_ip(s):
    try:
        socket.inet_aton(s)
        return True
    except socket.error:
        return False

def ip2location(ip):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
    
    ip2locdata = dict()

    if(re.search(regex, ip)):
        IP2LocObj = IP2Location.IP2Location()
        IP2LocObj.open('ip2loc.BIN')
        ip2loc_result = IP2LocObj.get_all(ip)
        #print(ip2loc_result)
        ip2locdata['IP'] = ip
        ip2locdata['Country Short'] = ip2loc_result.country_short
        ip2locdata['Country Llong'] = ip2loc_result.country_long
        ip2locdata['Region'] = ip2loc_result.region
        ip2locdata['City'] = ip2loc_result.city
        ip2locdata['ISP'] = ip2loc_result.isp
        ip2locdata['Latitude'] = ip2loc_result.latitude
        ip2locdata['Longitude'] = ip2loc_result.longitude
        ip2locdata['Domain'] = ip2loc_result.domain
        ip2locdata['Zip Code'] = ip2loc_result.zipcode
        ip2locdata['Time Zone'] = ip2loc_result.timezone
        ip2locdata['Net Speed'] = ip2loc_result.netspeed
        ip2locdata['Idd Code'] = ip2loc_result.idd_code
        ip2locdata['Area Code'] = ip2loc_result.area_code
        ip2locdata['Weather Code'] = ip2loc_result.weather_code
        ip2locdata['Weather Name'] = ip2loc_result.weather_name
        ip2locdata['MCC'] = ip2loc_result.mcc
        ip2locdata['MNC'] = ip2loc_result.mnc
        ip2locdata['Mobile Brand'] = ip2loc_result.mobile_brand
        ip2locdata['Elevation'] = ip2loc_result.elevation
        ip2locdata['Usage Type'] = ip2loc_result.usage_type
        return ip2locdata
    else:
        #ip2locdata['IP'] = "Error"
        ip2locdata['IP'] = ip
        ip2locdata['Country Short'] = '-'
        ip2locdata['Country Llong'] = '-'
        ip2locdata['Region'] = '-'
        ip2locdata['City'] = '-'
        ip2locdata['ISP'] = '-'
        ip2locdata['Latitude'] = '-'
        ip2locdata['Longitude'] = '-'
        ip2locdata['Domain'] = '-'
        ip2locdata['Zip Code'] = '-'
        ip2locdata['Time Zone'] = '-'
        ip2locdata['Net Speed'] = '-'
        ip2locdata['Idd Code'] = '-'
        ip2locdata['Area Code'] = '-'
        ip2locdata['Weather Code'] = '-'
        ip2locdata['Weather Name'] = '-'
        ip2locdata['MCC'] = '-'
        ip2locdata['MNC'] = '-'
        ip2locdata['Mobile Brand'] = '-' 
        ip2locdata['Elevation'] = '-'
        ip2locdata['Usage Type'] = '-'
        return ip2locdata



def compendium(request):
    return render(request, "compendium.html")
