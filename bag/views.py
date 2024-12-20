from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
# Importa funções para renderizar templates, redirecionar, retornar respostas HTTP e obter um objeto ou retornar 404.

from django.contrib import messages
# Importa o módulo de mensagens para enviar feedbacks ao usuário.

from products.models import Product
# Importa o modelo Product que contém informações sobre os produtos disponíveis.

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    # Define a função que renderiza a página da sacola de compras.

    return render(request, 'bag/bag.html')
    # Renderiza o template 'bag.html' e retorna a resposta HTTP para o usuário.

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    # Define a função para adicionar um produto à sacola de compras.

    product = get_object_or_404(Product, pk=item_id)
    # Recupera o produto do banco de dados usando o item_id como chave primária. Se não encontrado, retorna 404.

    quantity = int(request.POST.get('quantity'))
    # Obtém a quantidade do produto a ser adicionada a partir do formulário (POST), convertendo para inteiro.

    redirect_url = request.POST.get('redirect_url')
    # Obtém a URL para onde o usuário será redirecionado após adicionar o produto.

    size = None
    # Inicializa a variável size como None para verificar se um tamanho foi especificado.

    if 'product_size' in request.POST:
        size = request.POST['product_size']
        # Se 'product_size' está presente no POST, armazena seu valor na variável size.

    bag = request.session.get('bag', {})
    # Obtém a sacola de compras da sessão do usuário. Se não existir, inicializa como um dicionário vazio.

    if size:
        # Verifica se um tamanho foi especificado.
        if item_id in list(bag.keys()):
            # Se o item já estiver na sacola:
            if size in bag[item_id]['items_by_size'].keys():
                # Se o tamanho do item já existe, incrementa a quantidade e exibe mensagem de sucesso.
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                # Se o tamanho não existe, adiciona-o com a quantidade especificada e exibe mensagem de sucesso.
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            # Se o item não está na sacola, cria uma nova entrada para ele e exibe mensagem de sucesso.
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        # Se nenhum tamanho foi especificado:
        if item_id in list(bag.keys()):
            # Se o item já estiver na sacola, incrementa a quantidade total e exibe mensagem de sucesso.
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            # Se o item não está na sacola, adiciona o item com a quantidade e exibe mensagem de sucesso.
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    # Atualiza a sessão do usuário com a nova sacola.

    return redirect(redirect_url)
    # Redireciona o usuário para a URL especificada após adicionar o produto.

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    # Define a função para ajustar a quantidade de um produto na sacola.

    product = get_object_or_404(Product, pk=item_id)
    # Recupera o produto do banco de dados usando o item_id como chave primária. Se não encontrado, retorna 404.

    quantity = int(request.POST.get('quantity'))
    # Obtém a nova quantidade a partir do formulário (POST), convertendo para inteiro.

    size = None
    # Inicializa a variável size como None.

    if 'product_size' in request.POST:
        size = request.POST['product_size']
        # Se um tamanho foi especificado, armazena seu valor na variável size.

    bag = request.session.get('bag', {})
    # Obtém a sacola de compras da sessão do usuário.

    if size:
        # Verifica se um tamanho foi especificado.
        if quantity > 0:
            # Se a nova quantidade é maior que 0, atualiza a quantidade desse item e exibe mensagem de sucesso.
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            # Se a quantidade é 0 ou menor, remove o item do tamanho especificado da sacola.
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                # Se não há mais itens desse tamanho, remove o item da sacola.
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    else:
        # Se nenhum tamanho foi especificado:
        if quantity > 0:
            # Se a nova quantidade é maior que 0, atualiza a quantidade total do item e exibe mensagem de sucesso.
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            # Se a quantidade é 0 ou menor, remove o item da sacola e exibe mensagem de sucesso.
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    # Atualiza a sessão do usuário com a nova sacola.

    return redirect(reverse('view_bag'))
    # Redireciona o usuário para a página da sacola.

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    # Define a função para remover um item da sacola.

    try:
        product = get_object_or_404(Product, pk=item_id)
        # Recupera o produto do banco de dados usando o item_id como chave primária. Se não encontrado, retorna 404.

        size = None
        # Inicializa a variável size como None.

        if 'product_size' in request.POST:
            size = request.POST['product_size']
            # Se um tamanho foi especificado, armazena seu valor na variável size.

        bag = request.session.get('bag', {})
        # Obtém a sacola de compras da sessão do usuário.

        if size:
            # Verifica se um tamanho foi especificado.
            del bag[item_id]['items_by_size'][size]
            # Remove o tamanho do item da sacola.

            if not bag[item_id]['items_by_size']:
                # Se não há mais tamanhos desse item, remove o item da sacola.
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            # Se nenhum tamanho foi especificado, remove o item da sacola.
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        # Atualiza a sessão do usuário com a nova sacola.

        return HttpResponse(status=200)
        # Retorna uma resposta HTTP 200 (OK) para indicar que a remoção foi bem-sucedida.

    except Exception as e:
        # Captura qualquer exceção que ocorra.
        messages.error(request, f'Error removing item: {e}')
        # Adiciona uma mensagem de erro ao contexto da requisição.
        return HttpResponse(status=500)
        # Retorna uma resposta HTTP 500 (Erro Interno do Servidor) em caso de erro.
