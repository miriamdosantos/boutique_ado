from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    # A classe Meta define a configuração básica do formulário, associando-o ao modelo Order
    class Meta:
        # O formulário será baseado no modelo Order
        model = Order
        # Definimos os campos que serão exibidos no formulário, ou seja, os dados que o usuário precisará preencher.
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    # O método __init__ é chamado toda vez que o formulário é criado, e aqui estamos personalizando o comportamento do formulário.
    def __init__(self, *args, **kwargs):
        """
        Personaliza o formulário com placeholders, classes e o foco no primeiro campo.
        """
        # Chama o método __init__ da classe pai (forms.ModelForm) para garantir que a configuração básica do formulário seja aplicada
        super().__init__(*args, **kwargs)
        
        # Definimos um dicionário de placeholders para associar cada campo a um texto de exemplo ou dica.
        placeholders = {
            'full_name': 'Full Name',  # Nome completo
            'email': 'Email Address',  # Endereço de e-mail
            'phone_number': 'Phone Number',  # Número de telefone
            'country': 'Country',  # País
            'postcode': 'Postal Code',  # Código postal
            'town_or_city': 'Town or City',  # Cidade ou município
            'street_address1': 'Street Address 1',  # Endereço da rua 1
            'street_address2': 'Street Address 2',  # Endereço da rua 2 (caso exista)
            'county': 'County',  # Condado (se aplicável)
        }

        # Definimos o atributo 'autofocus' no campo 'full_name' para que o cursor seja colocado automaticamente nesse campo ao carregar a página
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Este loop percorre todos os campos do formulário e aplica configurações personalizadas a cada um.
        for field in self.fields:
            # Se o campo for obrigatório, adiciona um asterisco ao final do placeholder para indicar que é necessário.
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'  # Adiciona '*' aos campos obrigatórios
            else:
                placeholder = placeholders[field]  # Para campos não obrigatórios, só o texto do placeholder

            # Atribui o texto de placeholder no campo atual.
            self.fields[field].widget.attrs['placeholder'] = placeholder

            # Atribui uma classe CSS aos campos para que eles possam ser estilizados de maneira uniforme.
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'

            # Remove o label padrão do campo. Em vez disso, estamos usando o placeholder para guiar o usuário.
            self.fields[field].label = False
