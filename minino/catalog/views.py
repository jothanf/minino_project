from django.shortcuts import render, redirect
from .models import StoreModel, CategoryModel, ProductModel, CartModel, ProviderModel
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .forms import StoreForm, CategoryForm, ProviderForm, ProductForm



from .models import CartModel, PurchaserModel
def catalog_home(request, purchaser_id):
    purchaser, created = PurchaserModel.objects.get_or_create(id=purchaser_id)
    request.session['purchaser_id'] = purchaser.id
    
    # Verificar si el comprador ya tiene un carrito en estado 'in_process'
    existing_cart = CartModel.objects.filter(purchaser=purchaser, state='in_process').first()
    
    if not existing_cart:
        # Si no tiene un carrito en proceso, crea uno nuevo
        new_cart = CartModel.objects.create(purchaser=purchaser, total_price=0, state='in_process')
        print("Nuevo carrito creado:", new_cart)
    else:
        print("Carrito existente:", existing_cart)
        # Para imprimir todos los datos del carrito, puedes acceder a sus campos
        print("ID del carrito:", existing_cart.id)
        print("Estado del carrito:", existing_cart.state)
        print("Productos en el carrito:", existing_cart.products.all())  # Obtener todos los productos en el carrito
        
    print("ID del comprador:", purchaser.id)

    return render(request, 'catalog_home.html')


def catalog_home_(request, purchaser_id):
    purchaser, created = PurchaserModel.objects.get_or_create(id=purchaser_id)
    request.session['purchaser_id'] = purchaser.id
    new_cart = CartModel.objects.create(purchaser=purchaser, total_price=1, state='in_process')
    print(new_cart)
    print(purchaser.id)

    return render(request, 'catalog_home.html')



def select_store(request):
    stores = StoreModel.objects.all() 
    purchaser = request.session.get('purchaser_id')
    print(purchaser)
    return render(request, 'select_store.html', {'stores': stores})

def select_category(request, store_id):
    categories = CategoryModel.objects.filter(store=store_id)
    return render(request, 'select_category.html', {'categories':categories})

from django.shortcuts import render, redirect, get_object_or_404
from .models import StoreModel, CategoryModel, ProductModel, CartModel, ProductInCart

def select_products(request, category_id):
    purchaser_id = request.session.get('purchaser_id')
    products = ProductModel.objects.filter(categories=category_id)
    existing_cart = CartModel.objects.filter(purchaser_id=purchaser_id, state='in_process').order_by('-id').first()
    
    if request.method == 'POST':
        selected_product_ids = request.POST.getlist('selected_products')
        selected_products = ProductModel.objects.filter(id__in=selected_product_ids)
        
        # Verificar si un producto ya existe en el carrito y agregar solo los nuevos
        if existing_cart:
            for product in selected_products:
                if not existing_cart.products.filter(id=product.id).exists():
                    existing_cart.products.add(product)
                    existing_cart.save()
                    print("Producto agregado al carrito:", product)
        
        return redirect('view_cart', existing_cart.id)
    
    return render(request, 'select_products.html', {'products': products})


def select_products_(request, category_id):
    purchaser_id = request.session.get('purchaser_id')
    products = ProductModel.objects.filter(categories=category_id)
    existing_cart = CartModel.objects.filter(purchaser_id=purchaser_id, state='in_process').order_by('-id').first()
    
    if request.method == 'POST':
        selected_product_ids = request.POST.getlist('selected_products')
        selected_products = ProductModel.objects.filter(id__in=selected_product_ids)
        
        # Imprime los datos capturados en la consola
        print("Purchaser ID:", purchaser_id)
        print("Selected Product IDs:", selected_product_ids)
        print("Selected Products:", selected_products)
        print("Existing Cart ID:", existing_cart.id if existing_cart else None)
        
        # Agrega los productos seleccionados al carrito sin eliminar los existentes
        if existing_cart:
            for product in selected_products:
                existing_cart.products.add(product)
            existing_cart.save()
            print("Productos agregados al carrito:", selected_products)
        
        # Imprime todos los productos en el carrito (tanto los existentes como los nuevos)
        all_cart_products = existing_cart.products.all()
        print("Todos los productos en el carrito:", all_cart_products)
        
        return redirect('view_cart', existing_cart.id)
    
    return render(request, 'select_products.html', {'products': products})



from django.shortcuts import get_object_or_404
from .models import ProductInCart

def view_cart_(request, cart_id):
    try:
        cart = CartModel.objects.get(id=cart_id)
        cart_products = cart.products.all()
        purchaser_name = cart.purchaser.name
    except CartModel.DoesNotExist:
        cart_products = []
        purchaser_name = ""
    total_cart = 0

    if request.method == 'POST':
        for product in cart_products:
            input_name = f'product_{product.id}'
            quantity = int(request.POST.get(input_name, 0))
            partial_price = quantity * product.price_purchase
            total_cart += partial_price
            print(f"Product: {product.product_name}, Quantity: {quantity}, Partial Price: {partial_price}")

            # Crear una instancia de ProductInCart y asignar valores
            product_in_cart = ProductInCart(
                product=product,
                cart=cart,
                quantity=quantity,
                partial_price=partial_price
            )
            product_in_cart.save()
            print(f"ProductInCart: Product - {product_in_cart.product.product_name}, Quantity - {product_in_cart.quantity}, Partial Price - {product_in_cart.partial_price}")

        # Calcular el precio total del carrito después de procesar todos los productos
        cart.total_price = total_cart
        cart.save()

        # Redirigir a la vista 'prosses_order' con los datos del carrito
        return HttpResponseRedirect(reverse('prosses_order'))

    return render(request, 'view_cart.html', {'selected_products': cart_products, 'purchaser_name': purchaser_name, 'total_cart': total_cart})

from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CartModel, ProductInCart

def view_cart(request, cart_id):
    try:
        cart = CartModel.objects.get(id=cart_id)
        cart_products = cart.products.all()
        purchaser_name = cart.purchaser.name
    except CartModel.DoesNotExist:
        cart_products = []
        purchaser_name = ""
    total_cart = 0

    if request.method == 'POST':
        for product in cart_products:
            input_name = f'product_{product.id}'
            quantity = int(request.POST.get(input_name, 0))

            if quantity == 0:
                # Si la cantidad es 0, elimina el producto del carrito
                product_in_cart = ProductInCart.objects.get(cart=cart, product=product)
                product_in_cart.delete()
            else:
                partial_price = quantity * product.price_sale
                total_cart += partial_price

                try:
                    existing_product_in_cart = ProductInCart.objects.get(cart=cart, product=product)
                    existing_product_in_cart.quantity = quantity
                    existing_product_in_cart.partial_price = partial_price
                    existing_product_in_cart.save()
                except ProductInCart.DoesNotExist:
                    new_product_in_cart = ProductInCart(
                        product=product,
                        cart=cart,
                        quantity=quantity,
                        partial_price=partial_price
                    )
                    new_product_in_cart.save()

        cart.total_price = total_cart
        cart.save()

        return HttpResponseRedirect(reverse('prosses_order'))

    return render(request, 'view_cart.html', {'selected_products': cart_products, 'purchaser_name': purchaser_name, 'total_cart': total_cart})


from django.shortcuts import get_object_or_404, render
from .models import CartModel

def prosses_order(request):
    purchaser_id = request.session.get('purchaser_id')
    existing_cart = CartModel.objects.filter(purchaser_id=purchaser_id, state='in_process').order_by('-id').first()

    # Verificar si existe un carrito en proceso
    if existing_cart:
        cart_items = existing_cart.productincart_set.all()  # Acceder a los elementos de ProductInCart relacionados con el carrito
        return render(request, 'prosses_order.html', {'cart': existing_cart, 'cart_items': cart_items})
    else:
        # Manejar el caso en el que no haya un carrito en proceso
        return render(request, 'no_cart.html')

from django.contrib import messages

# Resto de tu código...

def finish_purchase(request):
    purchaser_id = request.session.get('purchaser_id')
    existing_cart = CartModel.objects.filter(purchaser_id=purchaser_id, state='in_process').order_by('-id').first()

    # Verificar si existe un carrito en proceso
    if existing_cart:
        # Cambiar el estado del carrito a 'pendiente'
        existing_cart.state = 'pending'
        # Establecer la fecha de compra en la hora actual
        existing_cart.purchase_datetime = datetime.now()
        existing_cart.save()
        
        # Eliminar el 'purchaser_id' de la sesión para cerrar la identificación del comprador
        del request.session['purchaser_id']

        cart_items = existing_cart.productincart_set.all()
        return render(request, 'finish_purchase.html', {'cart': existing_cart, 'cart_items': cart_items})
    else:
        # Manejar el caso en el que no haya un carrito en proceso
        messages.error(request, "No se encontró un carrito en proceso.")
        return render(request, 'no_cart.html')

def admin_stores(request):
    return render(request, 'admin_stores.html')

def create_store(request):
    form = StoreForm()
    if request.method == 'POST':
        form = StoreForm(request.POST)

        if form.is_valid():
            store_name = form.cleaned_data['store_name']
            # Verificar si ya existe una tienda con el mismo nombre
            if StoreModel.objects.filter(store_name=store_name).exists():
                alert = 'Ya existe una tienda con este nombre.'
            else:
                form.save()
                alert = 'Tienda creada exitosamente.'

        return render(request, 'create_store.html', {'form': form, 'alert': alert})
    return render(request, 'create_store.html', {'form': form})

def create_category(request):
    form = CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            if CategoryModel.objects.filter(category_name=category_name).exists():
                alert = 'Ya existe una categoria con este nombre'
            else:
                form.save()
                alert = 'Categoria creada'

        return render(request, 'create_category.html', {'form': form, 'alert': alert})
    return render(request, 'create_category.html', {'form':form})

def create_provider(request):
    form = ProviderForm
    if request.method == 'POST':
        form = ProviderForm(request.POST)

        if form.is_valid():
            provider_name = form.cleaned_data['provider_name']
            if ProviderModel.objects.filter(provider_name=provider_name).exists():
                alert = 'Ya existe un provedor con este nombre'
            else:
                form.save()
                alert = 'Provedor creado satisfactoriamente'
            return render(request, 'create_provider.html', {'form': form, 'alert': alert})

    return render(request, 'create_provider.html', {'form':form})

def create_product(request):
    form = ProductForm
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            alert = 'Producto creado'
            return render(request, 'create_product.html', {'form':form, 'alert':alert})
        else:
            alert = 'Los campos no se llenaron correctamente'
            return render(request, 'create_product.html', {'form':form, 'alert':alert})
    return render(request, 'create_product.html', {'form':form})


