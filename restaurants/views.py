# restaurants/views.py

from django.shortcuts import render, HttpResponse, render_to_response
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import restaurants_db, regex, BoroughNY, groupByAndCount
from .forms import RestaurantForm
from bson.objectid import ObjectId

# Create your views here.

def index(request):
    return render(request,'index.html',{})

def restaurants(request):
    context = {'range': range(10)}   # Aquí van las variables para la plantilla
    return render(request,'restaurants.html', context)

def query_restaurants(request):
    arg_keys = ["type","zone","cp","name","street","page"]
    query = {}

    page = 0
    for arg in arg_keys:
        if request.GET.get(arg):
            insens_query = regex.compile('^' + regex.escape(request.GET.get(arg)) + '$', regex.IGNORECASE)
            if arg  == "type":
                query['cuisine']=insens_query
            elif arg == "zone":
                query['borough']=insens_query
            elif arg == "cp":
                query['address.zipcode']=insens_query
            elif arg == "name":
                query['name']=insens_query
            elif arg == "street":
                query['address.street']=insens_query
            elif arg == "page":
                page = int(request.GET.get(arg))

   
    query_cursor = restaurants_db.find(query)
    tot = query_cursor.count()
    first = page*10
    last = min((page+1)*10,tot)
    metadata = {'page': page, 'first': first+1, 'last': last, 'tot': tot}
    send_list = []

    for r in query_cursor[first:last]:
        send_list.append({'type': r['cuisine'],'zone':r['borough'],'name':r['name'],'street':r['address']['street'],
        'cp': r['address']['zipcode'],'e_coord': r['address']['coord'][0],'n_coord': r['address']['coord'][1],'number':r['address']['building'], 'id':str(r["_id"])})
    send_list.append(metadata)
    
    return JsonResponse(send_list, safe=False)

def search_restaurant(request):
    return render(request,'restaurants_search.html',{})

@login_required
def new_restaurant(request):
    default_form = form = RestaurantForm()
    form_errors = None

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            new_entry={
                "address": {
                    "building": data['building'],
                    "coord": [float(data['e_coord']),float(data['n_coord'])],
                    "street": data['street'],
                    "zipcode": data['zipcode'],
                },
                "borough": BoroughNY.BOROUGH_DICT[data['borough']],
                "cuisine": data['cuisine'],
                "name": data['name'],
                "grades":[],
                "restaurant_id":"Undefined",
            }

            restaurants_db.insert(new_entry)

            #new_entry["restaurant_id"]
            #new_entry["grades"]=[{"date":{"$date": ...}, "grade": "-", "score": _}, ...]

            context = {'success_title': 'Restaurante añadido', 'success_msg': 'El nuevo restaurante ha sido añadido correctamente.', 'success_link': '/restaurants/', 'success_link_text': 'Volver a Restaurantes'}
            return render(request,"success.html",context)



    context = {'dform': default_form, 'form': form}

    return render(request,'new_restaurant.html', context)

@login_required
def edit_restaurant(request,pk):
    print(pk)
    try:
        obj_pk = ObjectId(pk)
    except:
        context = {'fail_title': 'Restaurante inválido', 'fail_msg': 'El restaurante especificado no es válido.', 'fail_link': '/restaurants/', 'fail_link_text': 'Volver a Restaurantes'}
        return render(request,"fail.html",context)

    modif = restaurants_db.find_one({'_id':obj_pk})

    if not modif:
        context = {'fail_title': 'Restaurante inválido', 'fail_msg': 'El restaurante especificado no es válido.', 'fail_link': '/restaurants/', 'fail_link_text': 'Volver a Restaurantes'}
        return render(request,"fail.html",context)

    initial = {
        'name': modif['name'],
        'cuisine': modif['cuisine'],
        'street': modif['address']['street'],
        'borough': modif['borough'],
        'building': modif['address']['building'],
        'zipcode': modif['address']['zipcode'],
        'n_coord': modif['address']['coord'][1],
        'e_coord': modif['address']['coord'][0],
    }

    default_form = form = RestaurantForm(initial = initial)
    form_errors = None

    if request.method == 'POST':
        form = RestaurantForm(request.POST, initial = initial)
        if form.is_valid():
            data = form.cleaned_data

            edited_entry={
                "address": {
                    "building": data['building'],
                    "coord": [float(data['e_coord']),float(data['n_coord'])],
                    "street": data['street'],
                    "zipcode": data['zipcode'],
                },
                "borough": BoroughNY.BOROUGH_DICT[data['borough']],
                "cuisine": data['cuisine'],
                "name": data['name'],
                "grades":[],
                "restaurant_id":"Undefined",
            }

            restaurants_db.update({'_id':obj_pk},edited_entry)

            #new_entry["restaurant_id"]
            #new_entry["grades"]=[{"date":{"$date": ...}, "grade": "-", "score": _}, ...]

            context = {'success_title': 'Restaurante añadido', 'success_msg': 'El restaurante ha sido editado correctamente.', 'success_link': '/restaurants/', 'success_link_text': 'Volver a Restaurantes'}
            return render(request,"success.html",context)

    context = {'dform': default_form, 'form': form, 'id': pk}

    return render(request,'edit_restaurant.html', context)
    
def remove_restaurant(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        obj_pk = ObjectId(pk)
        restaurants_db.remove({'_id':obj_pk})
        context = {'success_title': 'Restaurante eliminado', 'success_msg': 'El restaurante ha sido eliminado correctamente.', 'success_link': '/restaurants/', 'success_link_text': 'Volver a Restaurantes'}        
        return render(request,"success.html",context)

def view_restaurant(request):
    context={}
    if request.GET.get('lat') and request.GET.get('lng'):
        context = {'lat': request.GET.get('lat'), 'lng': request.GET.get('lng')}
    return render(request,"map_view.html",context)

def stats_restaurants(request):
    context = {}
    return render(request,"restaurants_stats.html",context)

def stats_query(request):
    attr = request.GET.get('type')
    if attr == 'borough':
        stats = groupByAndCount(restaurants_db,'borough')
        metadata = {'typetext': 'Barrio'}
    elif attr == 'cuisine':
        stats = groupByAndCount(restaurants_db,'cuisine')
        metadata = {'typetext': 'Tipo de Cocina'}
#    elif attr == 'name':
#        stats = groupByAndCount(restaurants_db,['name'])

    return JsonResponse([metadata,stats],safe=False)
