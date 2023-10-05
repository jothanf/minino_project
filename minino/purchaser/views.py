from django.shortcuts import render, redirect
from .models import PurchaserModel

# Create your views here.
def purchaser_home(request):
    return render(request, 'purchaser_home.html')

def create_purches(request):
    if request.method == 'POST':
        purchaser_name = request.POST.get('purchaser_name')
        phone = request.POST.get('purchaser_phone') 
        new_purchaser = PurchaserModel(name=purchaser_name, phone=phone)
        new_purchaser.save()
        message = 'Purchaser created successfully'
        return render(request, 'create_purchaser.html', {'message': message})
    return render(request, 'create_purchaser.html')

def signin(request):
    purchasers = [] 
    
    if request.method == 'POST':
        search_query = request.POST.get('search_purchase')
        
        if search_query:
            purchasers = PurchaserModel.objects.filter(name__icontains=search_query)
    
    return render(request, 'signin.html', {'purchasers': purchasers})

from django.shortcuts import render
from catalog.models import CartModel, ProductInCart


def admin_home(request):


    return render(request, 'admin_home.html')

def all_purchases(request):
    # Recupera todas las compras (carritos) de la base de datos
    all_carts = CartModel.objects.all()

    # Puedes realizar cualquier procesamiento adicional aquí si es necesario

    return render(request, 'all_purchases.html', {'all_carts': all_carts})

def search_by_user(request):
    purchasers = [] 
    
    if request.method == 'POST':
        search_query = request.POST.get('search_purchase')
        
        if search_query:
            purchasers = PurchaserModel.objects.filter(name__icontains=search_query)
    return render(request, 'search_by_user.html', {'purchasers':purchasers})

def purchases_by_user(request, purchaser_id):
    purchaser = PurchaserModel.objects.get(pk=purchaser_id)
    carts_by_purchaser = CartModel.objects.filter(purchaser=purchaser)
    
    if request.method == 'POST':
        for cart in carts_by_purchaser:
            new_state = request.POST.get(f'new_state_{cart.id}')  # Captura el nuevo estado del carrito específico
            if new_state:
                cart.state = new_state
                cart.save()

    return render(request, 'purchases_by_user.html', {'carts_by_purchaser': carts_by_purchaser, 'purchaser': purchaser})

def search_by_state(request):
    if request.method == 'POST':
        selected_state = request.POST.get('state')  # Obtener el valor del campo 'state' del formulario
        carts_in_state = CartModel.objects.filter(state=selected_state)
        # Ahora puedes hacer lo que necesites con el valor 'selected_state'
        return render(request, 'search_by_state.html', {'carts_in_state': carts_in_state})
    return render(request, 'search_by_state.html')


