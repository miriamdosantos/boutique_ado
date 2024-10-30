# views.py

from django.shortcuts import render, redirect  # Importa funções para renderizar templates e redirecionar URLs

def view_bag(request):
    """ View que renderiza a página com os conteúdos do carrinho """
    
    # Renderiza o template 'bag.html' na pasta 'bag', exibindo os itens do carrinho
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Adiciona uma quantidade do produto especificado ao carrinho """

    # Extrai a quantidade enviada pelo formulário e a converte em um inteiro
    quantity = int(request.POST.get('quantity'))

    # Extrai a URL de redirecionamento do formulário para retornar ao usuário após adicionar o item
    redirect_url = request.POST.get('redirect_url')

    # Inicializa a variável de tamanho com valor None; pode ser modificada se o produto tiver tamanhos
    size = None
    if 'product_size' in request.POST:
        # Se o formulário contiver um tamanho, armazena o valor
        size = request.POST['product_size']
    
    # Obtém o carrinho atual da sessão ou cria um novo dicionário vazio se ainda não existir
    bag = request.session.get('bag', {})

    # Se o produto tiver tamanho especificado:
    if size:
        # Se o item já estiver no carrinho:
        if item_id in list(bag.keys()):
            # Se o tamanho já estiver registrado, aumenta a quantidade
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # Caso contrário, adiciona o novo tamanho com a quantidade
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # Se o item não estiver no carrinho, cria nova entrada com tamanhos
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # Se o produto não tiver tamanho (item padrão):
        if item_id in list(bag.keys()):
            # Se o item já estiver no carrinho, aumenta a quantidade
            bag[item_id] += quantity
        else:
            # Se o item não estiver no carrinho, cria nova entrada com a quantidade
            bag[item_id] = quantity

    # Salva o carrinho atualizado na sessão
    request.session['bag'] = bag

    # Redireciona o usuário para a URL especificada
    return redirect(redirect_url)