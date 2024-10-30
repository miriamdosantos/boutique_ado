from decimal import Decimal  # Importa Decimal para cálculos precisos com preços e porcentagens
from django.conf import settings  # Acessa configurações personalizadas do projeto, como limites e taxas de entrega
from django.shortcuts import get_object_or_404  # Busca objetos do banco de dados e exibe erro 404 se não encontrar
from products.models import Product  # Importa o modelo Product para obter informações de produtos

def bag_contents(request):
    # Inicializa variáveis para armazenar dados do carrinho
    bag_items = []  # Lista para armazenar os itens do carrinho
    total = 0  # Soma do preço total dos itens
    product_count = 0  # Quantidade total de itens no carrinho
    
    # Obtém o carrinho armazenado na sessão ou cria um dicionário vazio
    bag = request.session.get('bag', {})

    # Loop para processar cada item no carrinho
    for item_id, item_data in bag.items():
        # Verifica se o item é uma quantidade inteira (sem tamanhos)
        if isinstance(item_data, int):
            # Obtém o produto pelo ID ou retorna erro 404 se não encontrar
            product = get_object_or_404(Product, pk=item_id)
            # Calcula o total multiplicando quantidade pelo preço do produto
            total += item_data * product.price
            # Incrementa a quantidade de produtos
            product_count += item_data
            # Adiciona os dados do item na lista 'bag_items'
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            # Obtém o produto caso item_data tenha tamanhos específicos
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                # Calcula o total multiplicando quantidade e preço para cada tamanho
                total += quantity * product.price
                product_count += quantity
                # Adiciona os dados do item (com tamanho) na lista 'bag_items'
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                    'size': size,
                })

    # Define a taxa de entrega e delta para frete grátis
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    # Calcula o valor final, incluindo entrega
    grand_total = delivery + total

    # Cria o contexto a ser passado para o template, contendo dados do carrinho
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    # Retorna o contexto para uso no template
    return context