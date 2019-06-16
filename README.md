# test-python-microservices

Demonstrar integração entre micro serviços em Python 3 utilizando RabbitMQ.

Toda inserção de registro na base de dados é publicada em uma exchange no RabbitMQ, com o objetivo de notificar todas as aplicações inscritas, que novo registro foi alterado ou modificado.


# Motivos

Por que replicar os dados nos micros serviços?

* Evitar de implementar circuit breakers;
* Otimizar a base de dados de acordo com cada micro serviço. Armzenar a informação desnormalizada e apenas o que é pertinente ao domínio. Poder escolher outras formas de armazenamento de dados. Ex: uso de cache, banco não relacional, arquivo, etc;
* Serviços devem ser independentes, devem fazer uma coisa só e muito bem feita (aka SOLID);
* Escalar um serviço sem impactar outros;
* Tempo de resposta do meu serviço não é impactada por lentidão de outro serviço;

# Problemas

* Atraso nas informações entre os serviço (vide youtube onde após clicar like e atualizar a pagina, seu like ainda não está "salvo");
* Ponto de falha no RabbitMQ (se cair, comunicação acaba);
* Complexidade aumenta (muito);
* Problemas de rede;
* Retry de mensagens;
* Publicar a mensagem para o Broker pode falhar, precisa implementar mecanismo de replay em cada serviço;
* Controle de estado de um registro é complexo (ativo, inativo, saldo, etc)

Os dados entre os serviço na minha opinião não está OK.
Não acredito que seja certo o serviço de score receber dados de renda e patrimônio diretamente.
Essas informações deveriam vir sempre a partir do Broker, e ele apenas calcular o score dessa informação.
