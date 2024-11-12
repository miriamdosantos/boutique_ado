from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

import stripe

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Se o método da requisição for POST (usuário submeteu o formulário)
    if request.method == 'POST':
        bag = request.session.get('bag', {})  # Recupera o carrinho da sessão do usuário

        # Coleta os dados do formulário preenchidos pelo usuário
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        
        # Cria o formulário de pedido com os dados coletados
        order_form = OrderForm(form_data)
        
        # Se o formulário for válido
        if order_form.is_valid():
            order = order_form.save()  # Salva o pedido no banco de dados e o armazena em `order`
            
            # Itera sobre cada item no carrinho (bag)
            for item_id, item_data in bag.items():
                try:
                    # Tenta recuperar o produto pelo `id`
                    product = Product.objects.get(id=item_id)
                    
                    # Caso o `item_data` seja um inteiro, significa que não há variações (exemplo: tamanho)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,  # Quantidade do produto
                        )
                        order_line_item.save()  # Salva o item do pedido no banco de dados
                    
                    # Caso contrário, `item_data` contém variações, como tamanhos
                    else:
                        # Exemplo de item com variações (exemplo de bag com variação):
                        # item_data = {'items_by_size': {'S': 1, 'M': 3}}
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,  # Quantidade para cada tamanho específico
                                product_size=size,  # Tamanho do produto
                            )
                            order_line_item.save()  # Salva cada variação de item do pedido
                    
                except Product.DoesNotExist:
                    # Se o produto não existir no banco de dados, exibe uma mensagem de erro ao usuário
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()  # Deleta o pedido se ocorrer um erro com algum item
                    return redirect(reverse('view_bag'))  # Redireciona para a visualização do carrinho
            
            # Salva a preferência do usuário sobre guardar as informações
            request.session['save_info'] = 'save-info' in request.POST
            
            # Redireciona para a página de sucesso do checkout
            return redirect(reverse('checkout_success', args=[order.order_number]))
        
        else:
            # Se o formulário não for válido, exibe uma mensagem de erro
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    
    # Se o método da requisição não for POST (possivelmente GET)
    else:
        bag = request.session.get('bag', {})
        if not bag:
            # Se o carrinho estiver vazio, exibe mensagem e redireciona para produtos
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        # Calcula o total do carrinho para gerar o pagamento com Stripe
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)  # Stripe usa valores inteiros em centavos
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Cria um formulário de pedido vazio para renderizar na página de checkout
        order_form = OrderForm()

    if not stripe_public_key:
        # Alerta se a chave pública do Stripe estiver ausente
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    # Renderiza a página de checkout com o formulário e chaves Stripe
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)