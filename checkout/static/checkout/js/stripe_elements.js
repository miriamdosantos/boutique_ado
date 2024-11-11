/*
    A lógica principal do pagamento (fluxo e autenticação) segue as instruções da Stripe:
    https://stripe.com/docs/payments/accept-a-payment
    
    O CSS para estilizar os campos de pagamento vem da documentação:
    https://stripe.com/docs/stripe-js
*/

// Coleta o valor da chave pública do Stripe a partir do script com o id "id_stripe_public_key"
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);  // .text() pega o conteúdo JSON, slice(1, -1) remove aspas externas

// Coleta o valor do client_secret do script com o id "id_client_secret"
var client_secret = $('#id_client_secret').text().slice(1, -1);  // Também remove aspas para que seja uma string pronta para uso

// Inicializa o Stripe com a chave pública coletada, autorizando a sessão
var stripe = Stripe(stripe_public_key);

// Cria uma instância de "elements" do Stripe, que gerará e controlará os campos de pagamento de forma segura
var elements = stripe.elements();

// Define o estilo dos campos de pagamento, seguindo as sugestões de formatação da Stripe
var style = {
    base: {
        color: '#000',  // Cor do texto nos campos
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',  // Fonte a ser usada
        fontSmoothing: 'antialiased',  // Suavização do texto para melhorar a aparência
        fontSize: '16px',  // Tamanho da fonte
        '::placeholder': {
            color: '#aab7c4'  // Cor do texto do placeholder
        }
    },
    invalid: {
        color: '#dc3545',  // Cor do texto de erro
        iconColor: '#dc3545'  // Cor do ícone de erro (como o ícone de cartão inválido)
    }
};

// Cria um campo de entrada de cartão de crédito, aplicando o estilo especificado
var card = elements.create('card', {style: style});

// Monta o campo de cartão no elemento HTML com o id "card-element"
card.mount('#card-element');
