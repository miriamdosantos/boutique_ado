from django.shortcuts import render, redirect, reverse, HttpResponse  # Importa funções úteis do Django para renderização de templates e manipulação de requisições

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    # Renderiza a página do carrinho de compras ('bag.html') usando o contexto atual da requisição
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    
    # Obtém a quantidade do produto a partir da requisição POST e converte para inteiro
    quantity = int(request.POST.get('quantity'))  
    # Obtém a URL para redirecionamento após a adição ao carrinho
    redirect_url = request.POST.get('redirect_url')  
    size = None  # Inicializa a variável size como None
    # Verifica se 'product_size' foi enviado na requisição POST
    if 'product_size' in request.POST:  
        size = request.POST['product_size']  # Armazena o tamanho do produto, se disponível
    # Obtém o carrinho da sessão; se não existir, inicializa como um dicionário vazio
    bag = request.session.get('bag', {})  

    # Lógica para adicionar o produto ao carrinho considerando o tamanho
    if size:  
        if item_id in list(bag.keys()):  # Verifica se o item já está no carrinho
            if size in bag[item_id]['items_by_size'].keys():  # Verifica se o tamanho já está registrado
                bag[item_id]['items_by_size'][size] += quantity  # Adiciona a quantidade ao tamanho existente
            else:
                # Se o tamanho não existir, cria uma nova entrada para esse tamanho
                bag[item_id]['items_by_size'][size] = quantity  
        else:
            # Se o item não estiver no carrinho, adiciona o item com o tamanho e a quantidade
            bag[item_id] = {'items_by_size': {size: quantity}}  
    else:  # Se não houver tamanho
        if item_id in list(bag.keys()):  # Verifica se o item já está no carrinho
            bag[item_id] += quantity  # Adiciona a quantidade ao item existente
        else:
            # Se o item não estiver no carrinho, inicializa a quantidade
            bag[item_id] = quantity  

    # Atualiza a sessão com o novo estado do carrinho
    request.session['bag'] = bag  
    # Redireciona para a URL especificada
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    
    # Obtém a nova quantidade do produto a partir da requisição POST
    quantity = int(request.POST.get('quantity'))  
    size = None  # Inicializa a variável size como None
    # Verifica se 'product_size' foi enviado na requisição POST
    if 'product_size' in request.POST:  
        size = request.POST['product_size']  # Armazena o tamanho do produto, se disponível
    # Obtém o carrinho da sessão; se não existir, inicializa como um dicionário vazio
    bag = request.session.get('bag', {})  

    # Lógica para ajustar a quantidade do produto considerando o tamanho
    if size:  
        if quantity > 0:  # Verifica se a nova quantidade é maior que 0
            bag[item_id]['items_by_size'][size] = quantity  # Atualiza a quantidade do tamanho especificado
        else:
            # Se a quantidade for 0 ou negativa, remove o tamanho do item
            del bag[item_id]['items_by_size'][size]  
            # Se não houver mais tamanhos para o item, remove o item do carrinho
            if not bag[item_id]['items_by_size']:  
                bag.pop(item_id)  
    else:  # Se não houver tamanho
        if quantity > 0:  # Verifica se a nova quantidade é maior que 0
            bag[item_id] = quantity  # Atualiza a quantidade do item
        else:
            # Se a quantidade for 0 ou negativa, remove o item do carrinho
            bag.pop(item_id)  

    # Atualiza a sessão com o novo estado do carrinho
    request.session['bag'] = bag  
    # Redireciona para a view que exibe o carrinho
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    
    try:
        size = None  # Inicializa a variável size como None
        # Verifica se 'product_size' foi enviado na requisição POST
        if 'product_size' in request.POST:  
            size = request.POST['product_size']  # Armazena o tamanho do produto, se disponível
        # Obtém o carrinho da sessão; se não existir, inicializa como um dicionário vazio
        bag = request.session.get('bag', {})  

        # Lógica para remover o item do carrinho considerando o tamanho
        if size:  
            # Remove o tamanho do item especificado
            del bag[item_id]['items_by_size'][size]  
            # Se não houver mais tamanhos para o item, remove o item do carrinho
            if not bag[item_id]['items_by_size']:  
                bag.pop(item_id)  
        else:
            # Remove o item do carrinho
            bag.pop(item_id)  

        # Atualiza a sessão com o novo estado do carrinho
        request.session['bag'] = bag  
        # Retorna uma resposta HTTP 200 para indicar sucesso
        return HttpResponse(status=200)  

    except Exception as e:
        # Em caso de erro, retorna uma resposta HTTP 500 para indicar falha
        return HttpResponse(status=500)  
