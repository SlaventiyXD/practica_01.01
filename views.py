from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'base.html')

def page1(request):
    partners = Partners.objects.all()
    return render(request, 'page1.html', {'partners': partners})

@csrf_exempt
def add_page(request):
    if request.method == 'POST':
        # Получаем данные из формы
        type_partners_id = request.POST.get('type_partners')
        name = request.POST.get('name')
        director = request.POST.get('director')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        inn = request.POST.get('inn')
        rating = request.POST.get('rating')

        region_id = request.POST.get('region')
        city_id = request.POST.get('city')
        street_id = request.POST.get('street')
        home = request.POST.get('home')
        postal_code = request.POST.get('postal_code')


        errors = []
        if not all([type_partners_id, name, director, email, phone_num, inn, rating]):
            errors.append("Все поля обязательны для заполнения")

        if not all([region_id, city_id, street_id, home, postal_code]):
            errors.append("Все поля адреса обязательны")

        if not errors:
            try:
                address = Address.objects.create(
                    street_id=street_id,
                    city_id=city_id,
                    region_id=region_id,
                    home=home,
                    postal_code=postal_code
                )

                partner = Partners.objects.create(
                    type_partner_id=type_partners_id,
                    name=name,
                    director=director,
                    email=email,
                    phone_num=phone_num,
                    address=address,
                    inn=inn,
                    rating=rating
                )
                return redirect('partners')

            except Exception as e:
                errors.append(f"Ошибка при сохранении: {str(e)}")

        # Если есть ошибки, показываем форму снова
        context = get_form_context()
        context['errors'] = errors
        return render(request, 'add_page.html', context)

        # GET запрос - показываем пустую форму
    context = get_form_context()
    return render(request, 'add_page.html', context)

def get_form_context():
    return {
        'type_partners': TypePartners.objects.all(),
        'regions': Region.objects.all(),
        'cities': Cities.objects.all(),
        'streets': Streets.objects.all(),
    }

def edit_page(request, partner_id):
    partner = get_object_or_404(Partners, id=partner_id)

    if request.method == 'POST':
        type_partners_id = request.POST.get('type_partners')
        name = request.POST.get('name')
        director = request.POST.get('director')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        inn = request.POST.get('inn')
        rating = request.POST.get('rating')

        region_id = request.POST.get('region')
        city_id = request.POST.get('city')
        street_id = request.POST.get('street')
        home = request.POST.get('home')
        postal_code = request.POST.get('postal_code')

        # Валидация
        errors = []
        if not all([type_partners_id, name, director, email, phone_num, inn, rating]):
            errors.append("Все поля обязательны для заполнения")

        if not all([region_id, city_id, street_id, home, postal_code]):
            errors.append("Все поля адреса обязательны")

        if not errors:
            try:
                # Обновляем адрес
                partner.address.street_id = street_id
                partner.address.city_id = city_id
                partner.address.region_id = region_id
                partner.address.home = home
                partner.address.postal_code = postal_code
                partner.address.save()

                # Обновляем партнера
                partner.type_partner_id = type_partners_id
                partner.name = name
                partner.director = director
                partner.email = email
                partner.phone_num = phone_num
                partner.inn = inn
                partner.rating = rating
                partner.save()

                return redirect('partners')

            except Exception as e:
                errors.append(f"Ошибка при сохранении: {str(e)}")

        context = get_form_context()
        context.update({
            'partner': partner,
            'errors': errors
        })
        return render(request, 'edit_page.html', context)

        # GET запрос - показываем форму с данными
    context = get_form_context()
    context['partner'] = partner
    return render(request, 'edit_page.html', context)

def history_partners(request):
    partners_products = PartnersProducts.objects.all()

    name_filter = request.GET.get('name','')
    if name_filter:
        partners_products = partners_products.filter(partner__name__icontains = name_filter)

    return render(request, 'history_page.html', {
        'partners_products': partners_products,
        'name_filter': name_filter
    })