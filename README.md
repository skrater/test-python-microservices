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

A implementação de Consumer e Producer do RabbitMQ está replicada em cada servico. Não é certo fazer isso.

O ideal é criar uma abstração e reutilizar em outros serviços. Fiz assim porquê não encontrei uma lib em python que trabalhe assim.

Não tem nenhum teste unitário também, não fiz porquê não estava com tempo para fazer, se fosse pra fazer, faria somente no score por enquanto,
onde tem alguma lógica de negócio mais importante, o resto é praticamente código de infra.


# Modo de usar

```bash
docker-compose up
```

## Curl

### Inserir Person
```bash
curl -i -H 'Content-Type: application/json' http://localhost/person --data @payloads/new_person.json
```

### Inserir Income
```bash
curl -i -H 'Content-Type: application/json' http://localhost/person/11111/income --data @payloads/new_income.json
```

### Inserir Asset
```bash
curl -i -H 'Content-Type: application/json' http://localhost/person/11111/asset --data @payloads/new_asset.json
```

### Inserir Debt
```bash
curl -i -H 'Content-Type: application/json' http://localhost/person/11111/debt --data @payloads/new_debt.json
```

### Consultar Score
```bash
curl -i http://localhost:81/11111/score
```
