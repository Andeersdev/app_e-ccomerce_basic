import requests
import base64
import json
import uuid
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderDetail
from core.product.models import Product
from django.views.generic import ListView
# PDF
from fpdf import FPDF
from django.template.loader import get_template


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/list.html'


# Get token authorization
def get_access_token(request):

    PAYPAL_API_CLIENT = 'AVr8s8De32fAIRX-nJhjh7IFz2iGII1_ady2BEm2TPtzXu6YSUp_xz54uVzRygu69W5d574wkERe-7S5'
    PAYPAL_API_SECRET_KEY = 'EG7qy7huGAOTV20tRm0aU5yOR9CbwgFzMK_IwAcBy-Jj81iG3XkEwvfHLjPqlyou3ErK905F_SL8UfqR'

   # Las credenciales deben estar en formato de base64 según la documentación de PayPal
    credentials = f'{PAYPAL_API_CLIENT}:{PAYPAL_API_SECRET_KEY}'
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    # Encabezado de autenticación para la solicitud
    headers = {
        'Authorization': f'Basic {credentials_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Datos para la solicitud de token de acceso
    data = {
        'grant_type': 'client_credentials'
    }

    # Realizar la solicitud POST para obtener el token de acceso
    response = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=data)

    # Verificar el resultado de la solicitud
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        raise ValueError('Error, could not get token')

# Assemble product


def assemble_order(request, products, option):
    capture_url = request.build_absolute_uri(reverse('order:capture'))
    if option == 2:
        capture_url = request.build_absolute_uri(reverse('order:pay'))
    cancel_url = request.build_absolute_uri(reverse('order:cancel'))
    items = []
    total = 0
    subtotal = 0
    for product in products:
        items.append({
            "name": product['name'],
            # Usaremos el ID del producto como SKU
            "sku": product['id'],
            "price": str(product['price']),
            "currency": "USD",
            "quantity": str(product['quantity'])
        })
        subtotal += float(product['price']) * float(product['quantity'])
    # Calcula el impuesto (IVA)
    tax_rate = 0.12  # Por ejemplo, 12%
    tax_total = round(subtotal * tax_rate, 2)

    # Calcula el total incluyendo el impuesto
    total = round(subtotal + tax_total, 2)
    data = {
        "purchase_units": [
            {
                "reference_id": str(uuid.uuid4()),
                "amount": {
                    "currency": "USD",
                    "details": {
                        "subtotal": subtotal,
                        "tax": tax_total
                    },
                    "total": total
                },
                "payee": {
                    "email": "sb-jety4730193837@business.example.com"
                },
                "items": items,
                # Direccion de envio de lo comprado
                "shipping_address": {
                    "line1": "2211 N First Street",
                    "line2": "Building 17",
                    "city": "San Jose",
                    "country_code": "US",
                    "postal_code": "95131",
                    "state": "CA",
                    "phone": "(123) 456-7890"
                },
                "shipping_method": "United Postal Service"
            }
        ],
        "redirect_urls": {
            "return_url": capture_url,
            "cancel_url": cancel_url
        }
    }
    return data

# Pay Order


@csrf_exempt
def pay_order(request):

    try:
        token = request.GET.get('token')
        if token is None:
            raise ValueError('Token not found')

        access_token = get_access_token(request)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.post(
            f'https://api-m.sandbox.paypal.com/v1/checkout/orders/{token}/pay', headers=headers)

        if response.status_code == 200:
            data = requests.get(
                f'https://api-m.sandbox.paypal.com/v1/checkout/orders/{token}', headers=headers)
            confirm = save_order(request, data.json(), 1)
            if confirm:
                return JsonResponse(response.json())
            return JsonResponse(response.json())
        else:
            return JsonResponse(response.json())

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Created order


@csrf_exempt
def create_order(request):

    if request.method == 'POST':
        datos = json.loads(request.body)
        products = datos.get('products')
        option = datos.get('option')
        data = assemble_order(request, products, option)
        try:
            access_token = get_access_token(request)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            response = requests.post(
                'https://api-m.sandbox.paypal.com/v1/checkout/orders', headers=headers, data=json.dumps(data))

            if response.status_code == 201:
                return JsonResponse(response.json())
            return JsonResponse(response.json())
        except:
            raise ValueError('Error: Unable to create PayPal order')

# Capture order


@csrf_exempt
def capture_order(request):

    try:
        token = request.GET.get('token')
        if token is None:
            raise ValueError('Token not found')
        access_token = get_access_token(request)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(
            f'https://api-m.sandbox.paypal.com/v1/checkout/orders/{token}', headers=headers)

        if response.status_code == 200:
            confirm = save_order(request, response.json())
            if confirm:
                return JsonResponse(response.json())
        return JsonResponse(response.json())

    except Exception as e:
        return JsonResponse(str(e), safe=False)

# Save order in database


@csrf_exempt
def save_order(request, data, status=None):

    if data is not None:
        try:
            order_token = data['id']
            subtotal = data['purchase_units'][0]['amount']['details']['subtotal']
            iva = data['purchase_units'][0]['amount']['details']['tax']
            total = data['purchase_units'][0]['amount']['total']
            user = request.user
            items = data['purchase_units'][0]['items']

            order_kwargs = {
                'order_token': order_token,
                'subtotal': subtotal,
                'iva': iva,
                'total': total,
                'user': user,
            }
            if status is not None:
                order_kwargs['status'] = 1

            order = Order.objects.create(**order_kwargs)

            for item in items:
                total = float(item['quantity']) * float(item['price'])
                product = Product.objects.get(id=int(item['sku']))
                OrderDetail.objects.create(
                    quantity=item['quantity'], price=item['price'], total=total, product=product, order=order)
            print(order)
            return True
        except Exception as e:
            print(str(e))
            return False


def cancel_order(request):
    return HttpResponseRedirect(reverse_lazy('cart:index'))


def consult_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        return order
    except Exception as e:
        raise ValueError('Order not found')


def consult_order_detail(order):
    try:
        order_detail = OrderDetail.objects.filter(order=order)
        return order_detail
    except:
        raise ValueError('Order detail not found')


def view_order(request, id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial")
    pdf.set_margins(10, 10, 5)
    order = consult_order(id)
    order_detail = consult_order_detail(order)
    context = {
        'order': order,
        'details': order_detail
    }
    html_template = get_template("order/pdf_template.html")
    html_content = html_template.render(context)
    pdf.write_html(html_content)
    pdf_file_path = "html.pdf"
    pdf.output(pdf_file_path)
    # Devolver una respuesta HTTP
    with open(pdf_file_path, "rb") as pdf_file:
        response = HttpResponse(
            pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="html.pdf"'
        return response
