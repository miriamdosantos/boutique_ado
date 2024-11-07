from django.contrib import admin  # Importa o módulo admin do Django para configurar a administração dos modelos
from .models import Order, OrderLineItem  # Importa os modelos Order e OrderLineItem do módulo models

# Define a classe de configuração para exibir itens de linha de pedido (OrderLineItem) dentro do pedido (Order) no Django Admin
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem  # Especifica que o modelo é OrderLineItem, que será exibido como inline no admin de Order
    readonly_fields = ('lineitem_total',)  # Define o campo 'lineitem_total' como somente leitura para impedir edições

# Define a classe de configuração para personalizar a exibição do modelo Order no Django Admin
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)  # Adiciona OrderLineItem como uma seção inline na página de Order no Admin

    # Define campos de somente leitura, geralmente usados para valores calculados ou gerados automaticamente
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    # Define a ordem de exibição dos campos no formulário de pedido do Admin
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

    # Define os campos que serão exibidos como colunas na lista de pedidos no Admin
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    # Define a ordem de exibição dos pedidos na lista, com os pedidos mais recentes primeiro
    ordering = ('-date',)

# Registra o modelo Order no Admin, utilizando as configurações personalizadas da classe OrderAdmin
admin.site.register(Order, OrderAdmin)
