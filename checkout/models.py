import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product

# Modelo que representa um pedido completo feito pelo cliente
class Order(models.Model):
    # Campo para armazenar o número exclusivo do pedido. É gerado automaticamente e não pode ser editado pelo usuário
    order_number = models.CharField(max_length=32, null=False, editable=False)
    
    # Armazena o nome completo do cliente, campo obrigatório
    full_name = models.CharField(max_length=50, null=False, blank=False)
    
    # E-mail do cliente, campo obrigatório e validado para formato de e-mail
    email = models.EmailField(max_length=254, null=False, blank=False)
    
    # Número de telefone do cliente, campo obrigatório
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    
    # País do cliente, obrigatório
    country = models.CharField(max_length=40, null=False, blank=False)
    
    # Código postal do cliente. Campo opcional, permite nulo ou vazio
    postcode = models.CharField(max_length=20, null=True, blank=True)
    
    # Cidade ou município do cliente, obrigatório
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    
    # Primeira linha do endereço do cliente, obrigatório
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    
    # Segunda linha do endereço, opcional
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    
    # Estado ou condado, opcional
    county = models.CharField(max_length=80, null=True, blank=True)
    
    # Data e hora de criação do pedido. Preenchido automaticamente quando o pedido é criado
    date = models.DateTimeField(auto_now_add=True)
    
    # Custo de entrega do pedido, campo obrigatório com valor padrão 0
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    
    # Total de todos os itens do pedido, sem o custo de entrega. Campo obrigatório com valor padrão 0
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    
    # Total final do pedido incluindo o custo de entrega. Campo obrigatório com valor padrão 0
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Gera um número exclusivo de pedido usando UUID
        - uuid.uuid4() cria um identificador aleatório.
        - .hex converte para string hexadecimal.
        - .upper() transforma em letras maiúsculas.
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Atualiza o total do pedido sempre que um item é adicionado,
        considerando os custos de entrega.
        - Calcula order_total somando o campo lineitem_total dos itens de linha associados.
        - Se order_total é menor que o limite de entrega gratuita, calcula delivery_cost.
        - Define grand_total como a soma de order_total e delivery_cost.
        """
        # Soma dos totais dos itens de linha usando agregação no banco de dados
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        # Calcula taxa de entrega, se order_total for menor que o limite de entrega gratuita
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        # Soma o total do pedido com o custo de entrega para obter o total geral
        self.grand_total = self.order_total + self.delivery_cost
        # Salva a instância com os valores atualizados
        self.save()

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para definir o número do pedido, se ele não estiver definido.
        - Verifica se order_number está ausente e, se sim, gera um novo número.
        - Chama super().save() para salvar a instância.
        """
        # Define o número do pedido apenas se ainda não estiver definido
        if not self.order_number:
            self.order_number = self._generate_order_number()
        # Chama o método save original para salvar a instância no banco de dados
        super().save(*args, **kwargs)

    def __str__(self):
        # Retorna o número do pedido como a representação em string da instância
        return self.order_number
    
# Modelo que representa cada item de produto específico dentro de um pedido
class OrderLineItem(models.Model):
    # Cria uma relação com o pedido (Order). Cada pedido pode ter vários OrderLineItems
    # related_name='lineitems' permite acessar todos os itens de um pedido com 'order.lineitems'
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    
    # Referência ao produto específico (Product) que está sendo comprado
    # Se o produto for excluído, o item de linha também será excluído
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    
    # Tamanho do produto (XS, S, M, L, XL), se aplicável. Campo opcional
    product_size = models.CharField(max_length=2, null=True, blank=True)
    
    # Quantidade do produto sendo comprada. Campo obrigatório, com valor padrão de 0
    quantity = models.IntegerField(null=False, blank=False, default=0)
    
    # Total para este item específico (produto * quantidade), sem incluir custos adicionais
    # max_digits=6 permite até 6 dígitos, incluindo 2 casas decimais
    # editable=False indica que não pode ser editado diretamente pelo usuário
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para definir o total do item de linha e atualizar o total do pedido.
        - Calcula lineitem_total multiplicando o preço do produto pela quantidade.
        - Chama super().save() para salvar o item de linha.
        - Chama update_total no pedido para atualizar o total do pedido após salvar o item de linha.
        """
        # Define o total do item de linha multiplicando o preço do produto pela quantidade
        self.lineitem_total = self.product.price * self.quantity
        # Salva o item de linha com o total atualizado
        super().save(*args, **kwargs)
        # Atualiza o total do pedido chamando o método update_total da instância de Order
        self.order.update_total()

    def __str__(self):
        # Retorna uma string que identifica o SKU do produto e o número do pedido associado
        return f'SKU {self.product.sku} on order {self.order.order_number}'