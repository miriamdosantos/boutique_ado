from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Lower  # Importa 'Q' para consultas complexas e 'Lower' para ordenação case-insensitive.
from .models import Product, Category

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Inicializa o queryset com todos os produtos.
    products = Product.objects.all()
    query = None  # Variável para armazenar termos de busca.
    categories = None  # Variável para armazenar categorias selecionadas.
    sort = None  # Variável para armazenar a chave de ordenação.
    direction = None  # Variável para armazenar a direção da ordenação ('asc' ou 'desc').

    if request.GET:  # Verifica se há parâmetros na URL enviados por meio de uma query string.
        # Verifica se o parâmetro 'sort' está presente na URL.
        if 'sort' in request.GET:
            sortkey = request.GET['sort']  # Obtém o valor do parâmetro 'sort' da URL e armazena na variável 'sortkey'.
            sort = sortkey  # Armazena o valor de 'sortkey' para uso no template.

            # Caso a ordenação seja pelo nome, cria uma nova chave 'lower_name' com todos os nomes em minúsculas.
            if sortkey == 'name':
                sortkey = 'lower_name'  # Altera 'sortkey' para 'lower_name' para garantir que a ordenação considere letras minúsculas.
                # O método 'annotate' adiciona um campo temporário a cada item do queryset.
                # Neste caso, adiciona 'lower_name', que é o nome do produto em minúsculas, permitindo ordenação case-insensitive.
                products = products.annotate(lower_name=Lower('name'))

            # Verifica se há um parâmetro 'direction' na URL para saber se a ordenação deve ser ascendente ou descendente.
            if 'direction' in request.GET:
                direction = request.GET['direction']  # Obtém o valor de 'direction' da URL.
                # Se a direção for 'desc', adiciona um '-' antes de 'sortkey' para ordenar de forma decrescente.
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            # Aplica a ordenação ao queryset 'products' usando o valor de 'sortkey'.
            products = products.order_by(sortkey)

        # Verifica se o parâmetro 'category' está presente na URL.
        if 'category' in request.GET:
            # Divide os valores das categorias em uma lista (ex: 'jeans,shirts' vira ['jeans', 'shirts']).
            categories = request.GET['category'].split(',')
            # Filtra os produtos para exibir apenas aqueles que pertencem às categorias selecionadas.
            products = products.filter(category__name__in=categories)
            # Armazena as categorias filtradas para exibir no template.
            categories = Category.objects.filter(name__in=categories)

        # Verifica se há um termo de busca na query string 'q'.
        if 'q' in request.GET:
            query = request.GET['q']  # Obtém o termo de busca inserido pelo usuário.
            if not query:
                # Exibe uma mensagem de erro se a busca estiver vazia e redireciona para a página de todos os produtos.
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            # Cria uma consulta que procura o termo de busca no nome ou na descrição dos produtos.
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # Filtra os produtos que correspondem ao termo de busca.
            products = products.filter(queries)

    # Cria uma string para manter a ordenação atual (ex: 'price_asc' ou 'name_desc').
    current_sorting = f'{sort}_{direction}'

    # Cria o contexto a ser passado para o template, incluindo os produtos, o termo de busca, categorias e a ordenação atual.
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    # Renderiza a página 'products.html' passando o contexto.
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    # Obtém o produto correspondente ao 'product_id' ou retorna um erro 404 se não for encontrado.
    product = get_object_or_404(Product, pk=product_id)

    # Cria o contexto com o produto a ser exibido.
    context = {
        'product': product,
    }

    # Renderiza a página 'product_detail.html' passando o contexto.
    return render(request, 'products/product_detail.html', context)
