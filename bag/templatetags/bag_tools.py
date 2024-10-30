# --- Django Template Filters: Explicação Detalhada, Benefícios e Uso Prático ---

# Este arquivo serve como uma referência completa para entender a criação, o uso e os benefícios de filtros personalizados em Django.
# Filtros personalizados ajudam a simplificar e a organizar a apresentação de dados nos templates, mantendo a lógica da aplicação fora deles.
# Abaixo, detalhamos o filtro `calc_subtotal` e incluímos explicações sobre os motivos e benefícios de usá-lo dessa forma.

# 1. Importando a biblioteca de templates do Django
# Django disponibiliza `template` para que possamos criar tags e filtros personalizados.
from django import template

# 2. Registrando novos filtros personalizados
# Para criar filtros personalizados, registramos a biblioteca de templates com `template.Library()`.
# Isso cria uma instância `register` que permite adicionar filtros e tags customizadas.

register = template.Library()


# 3. Definindo e Registrando o Filtro `calc_subtotal`
# 
# - O filtro `calc_subtotal` calcula o subtotal de um produto multiplicando o preço pela quantidade.
# - Usamos o decorador `@register.filter` para registrar o filtro e torná-lo disponível nos templates.
# 
# O decorador `@register.filter`:
# - Um decorador é uma função que modifica o comportamento de outra função.
# - `@register.filter(name='calc_subtotal')` indica que estamos registrando uma função como um filtro com o nome 'calc_subtotal'.
# - Esse nome é como chamaremos o filtro no template, usando a sintaxe `| calc_subtotal`.
# 
# Exemplo do código do filtro `calc_subtotal`:

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    O filtro `calc_subtotal` recebe dois parâmetros:
    - `price`: o preço unitário do produto.
    - `quantity`: a quantidade do produto.
    
    Retorna o valor do subtotal para o item, ou seja, `price * quantity`.
    """
    return price * quantity


# 4. Usando o filtro `calc_subtotal` no Template Django
# 
# Para usar este filtro no template, utilizamos a sintaxe:
# 
#     {{ valor | filtro:parametro }}
# 
# No exemplo `calc_subtotal`, `valor` é o preço do produto e `parametro` é a quantidade.
# O Django passa `valor` como primeiro argumento e `parametro` como o segundo, aplicando o filtro.

# Exemplo de uso no template HTML:

# <p class="my-0">${{ item.product.price | calc_subtotal:item.quantity }}</p>
#
# Neste caso:
# - `item.product.price` é passado como o primeiro argumento (price) da função `calc_subtotal`.
# - `item.quantity` é passado como o segundo argumento (quantity).
# - O filtro retorna o subtotal (price * quantity), que será exibido como resultado no template.


# 5. Por que criar um filtro personalizado?
#
# Usar filtros personalizados no Django traz diversas vantagens para o desenvolvimento de aplicações:
# 
# a) **Simplificação da lógica nos templates**: 
#    - Manter a lógica de negócios fora dos templates melhora a legibilidade.
#    - Em vez de fazer cálculos diretamente no template (o que poderia ser complexo e ilegível), o filtro faz a operação e retorna o resultado.
# 
# b) **Reusabilidade**:
#    - Filtros podem ser usados em várias partes da aplicação, economizando tempo e mantendo o código DRY (Don't Repeat Yourself).
#    - Por exemplo, `calc_subtotal` pode ser aplicado a qualquer item com preço e quantidade, em várias páginas.
#
# c) **Organização e manutenção**:
#    - Com a lógica de manipulação de dados separada, os templates ficam mais fáceis de manter e a lógica de cálculos centralizada.
#    - Caso precisemos alterar o cálculo de subtotal, basta ajustar o filtro, e todas as partes que o usam serão atualizadas automaticamente.
#
# d) **Redução de Erros**:
#    - Movendo cálculos para filtros, minimizamos o risco de erros repetitivos que poderiam surgir ao replicar lógica em templates.


# 6. Outros Exemplos de Filtros Personalizados
# 
# a) Filtro de Desconto
# Este filtro aplica um desconto ao preço do produto.
# Para calcular o preço com desconto, é necessário passar o preço e a porcentagem de desconto.
# 
# @register.filter(name='apply_discount')
# def apply_discount(price, discount_percentage):
#     """
#     Calcula o preço final após aplicar um desconto de `discount_percentage`.
#     """
#     discount_amount = price * (discount_percentage / 100)
#     return price - discount_amount
#
# Exemplo de uso no template:
# <p>Preço com desconto: ${{ item.product.price | apply_discount:10 }}</p>  {# Aplica um desconto de 10% #}


# b) Filtro de Formatação de Datas
# Formata uma data para o formato `DD-MM-AAAA` no template.
# 
# @register.filter(name='format_date')
# def format_date(date):
#     """
#     Converte uma data para o formato `DD-MM-AAAA`.
#     """
#     return date.strftime('%d-%m-%Y')
#
# Exemplo de uso no template:
# <p>Data de criação: {{ item.date | format_date }}</p>


# 7. Considerações Importantes sobre Filtros
# 
# - Filtros são executados no momento de renderização do template, então devem ser simples e rápidos.
# - Eles ajudam a manter a lógica fora dos templates, focando a exibição.
# - Filtros são ideais para formatação de strings, cálculos básicos e manipulação de dados de exibição.


# --- Fim da explicação dos filtros personalizados no Django ---

# --- Filtros embutidos do Django ---

# Abaixo, detalhamos os filtros mais comuns do Django, separados por suas categorias e com exemplos práticos.

# 1. Filtros de Texto
# Estes filtros ajudam a manipular strings, formatar texto, e modificar estilos.

# - `lower`: converte o texto para minúsculas.
#     {{ "Exemplo de Texto" | lower }}  # Resultado: "exemplo de texto"
# 
# - `upper`: converte o texto para maiúsculas.
#     {{ "Exemplo de Texto" | upper }}  # Resultado: "EXEMPLO DE TEXTO"
#
# - `title`: converte o texto para o estilo "Title Case".
#     {{ "exemplo de texto" | title }}  # Resultado: "Exemplo De Texto"
#
# - `truncatechars`: limita o texto ao número de caracteres especificado, adicionando "..." no final.
#     {{ "Texto muito longo para exibição" | truncatechars:10 }}  # Resultado: "Texto muit..."

# - `slugify`: converte uma string para um formato slug (URL amigável).
#     {{ "Django é incrível!" | slugify }}  # Resultado: "django-e-incrivel"

# 2. Filtros Numéricos e de Moeda
# Úteis para formatar números e moedas de acordo com convenções comuns.

# - `add`: soma o valor especificado ao número.
#     {{ 5 | add:10 }}  # Resultado: 15
# 
# - `divisibleby`: verifica se um número é divisível pelo valor fornecido (retorna True/False).
#     {{ 10 | divisibleby:3 }}  # Resultado: False
#
# - `floatformat`: formata um número float com o número desejado de casas decimais.
#     {{ 123.4567 | floatformat:2 }}  # Resultado: "123.46"
#
# - `length`: retorna o tamanho de uma lista ou string.
#     {{ "Django" | length }}  # Resultado: 6
#
# - `default_if_none`: define um valor padrão se o valor for None.
#     {{ preco | default_if_none:"N/A" }}

# 3. Filtros de Manipulação de Listas e Dicionários
# Facilitam a manipulação de listas e dicionários diretamente no template.

# - `first`: retorna o primeiro item de uma lista.
#     {{ my_list | first }}
#
# - `last`: retorna o último item de uma lista.
#     {{ my_list | last }}
#
# - `join`: junta os elementos de uma lista em uma string, separados por um delimitador.
#     {{ my_list | join:", " }}
#
# - `length_is`: verifica se o comprimento de uma lista ou string corresponde a um valor específico.
#     {{ my_list | length_is:3 }}
#
# - `slice`: fatiamento de listas (semelhante ao fatiamento de listas em Python).
#     {{ my_list | slice:":3" }}

# 4. Filtros de Manipulação de Data e Tempo
# Oferecem opções para formatar datas e calcular intervalos de tempo.

# - `date`: formata a data para o padrão especificado.
#     {{ my_date | date:"d M Y" }}  # Exemplo: "30 Oct 2024"
#
# - `timesince`: retorna o tempo decorrido desde a data fornecida.
#     {{ my_date | timesince }}  # Exemplo: "2 days ago"
#
# - `time`: formata a hora de um objeto datetime.
#     {{ my_date | time:"H:i" }}  # Resultado: "14:30" (formato de 24 horas)

# 5. Filtros Condicionais e de Lógica
# Usados para avaliações condicionais e manipulação básica de lógica nos templates.

# - `default`: exibe um valor padrão se a variável não estiver definida.
#     {{ nome | default:"Nome não especificado" }}
#
# - `yesno`: retorna "yes", "no" ou um valor alternativo dependendo do valor booleano.
#     {{ item.ativo | yesno:"Sim,Nao,Desconhecido" }}
#
# - `ifchanged`: verifica se um valor mudou em relação ao render anterior.
#     {% for item in lista %}
#         {% ifchanged item.categoria %}  # Exibe apenas se `categoria` mudou
#             <h2>{{ item.categoria }}</h2>
#         {% endifchanged %}
#         <p>{{ item.nome }}</p>
#     {% endfor %}

# 6. Filtros de HTML e Formatação
# Estes filtros ajudam a processar HTML e texto, tornando o conteúdo mais seguro ou formatado.

# - `safe`: marca o conteúdo como seguro, permitindo renderização de HTML no template.
#     {{ "<strong>Importante</strong>" | safe }}
#
# - `linebreaks`: converte quebras de linha em tags `<br>`.
#     {{ "Texto\nCom\nQuebras" | linebreaks }}
#
# - `urlize`: converte URLs em links clicáveis.
#     {{ "Acesse nosso site em http://exemplo.com" | urlize }}

# --- Fim da explicação sobre os filtros embutidos do Django ---
