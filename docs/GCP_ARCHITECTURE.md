SmartPrice – Arquitetura GCP para 50 Milhões de Eventos por Dia

Estratégia

Se o sistema começar a receber milhões de atualizações de preço por dia, não podemos deixar a API fazer todo o trabalho sozinha. Se cada requisição tentar salvar no banco e calcular preço na mesma hora, a API vai virar gargalo.

Por isso, a ideia é separar a entrada dos dados do processamento.

Como funcionaria:

1. API (Cloud Run)
A API recebe os preços e apenas publica uma mensagem no Pub/Sub.
Ela responde rápido para o cliente e não fica presa fazendo cálculo.

2. Pub/Sub
Funciona como uma fila inteligente.
Ele segura os eventos e distribui para os processadores conforme a capacidade do sistema.

3. Workers (Cloud Run)
Os workers consomem as mensagens e fazem o trabalho pesado:

- Salvam o preço do concorrente

- Calculam a nova sugestão

- Atualizam o banco

- Eles escalam automaticamente quando o volume aumenta.

4. Cloud SQL (PostgreSQL)
Continua sendo o banco principal, responsável pelos dados transacionais do sistema.

5. BigQuery
Usado para armazenar histórico grande de dados e permitir análises futuras, como tendência de preço ou estudos de margem.

Fluxo

Cliente → API → Pub/Sub → Workers → Banco