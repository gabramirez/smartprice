# SmartPrice 

O **SmartPrice** é um motor de precificação automática baseado em preços de concorrentes. O objetivo é manter competitividade de mercado sem comprometer a margem mínima dos produtos.

O sistema recebe preços externos, calcula uma sugestão automática e disponibiliza essas oportunidades para aprovação do gerente.

---

## Como funciona

Ao receber preços de concorrentes:

1. Calcula a média de mercado.
2. Define o preço sugerido como média - 10%.
3. Aplica uma regra de segurança: o valor nunca pode ser menor que custo + 5%.
4. Gera uma sugestão com status "Pendente".

No dashboard, o gerente pode:

- Visualizar sugestões pendentes
- Aprovar com um clique
- Atualizar automaticamente o preço do produto

---

## Tecnologias Utilizadas

### Backend:
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### Frontend:
- React (Vite)
- Axios

### Infraestrutura:
- Docker
- Docker Compose

---

## Como Executar o Projeto

### Pré-requisitos

- Docker Desktop instalado
- Docker Compose habilitado

### Subindo o ambiente

Na raiz do projeto, execute:

```bash
docker compose up --build
```

Após subir:

- **Backend**: [http://localhost:8000](http://localhost:8000)
- **Documentação da API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend**: [http://localhost:5173](http://localhost:5173)

---

## Inserindo Produtos para Teste

Acesse o banco:

```bash
docker compose exec db psql -U postgres -d smartprice
```

Execute:

```sql
INSERT INTO products (sku, name, cost_price, current_sales_price)
VALUES 
('MED-101', 'Dipirona 500mg', 3.00, 8.50),
('MED-102', 'Vitamina C Efervescente', 10.00, 25.00),
('MED-103', 'Protetor Solar FPS 50', 40.00, 60.00);
```

---

## Testando a Ingestão

Acesse:

[http://localhost:8000/docs](http://localhost:8000/docs)

Use o endpoint:

`POST /prices/ingest`

### Exemplo de payload:

```json
[
  {
    "sku": "MED-101",
    "competitor": "Farmácia A",
    "price": 5.00
  },
  {
    "sku": "MED-101",
    "competitor": "Farmácia B",
    "price": 5.20
  },
  {
    "sku": "MED-102",
    "competitor": "Farmácia A",
    "price": 18.00
  },
  {
    "sku": "MED-102",
    "competitor": "Supermercado X",
    "price": 17.50
  },
  {
    "sku": "MED-103",
    "competitor": "Farmácia C",
    "price": 35.00
  }
]
```

Após a ingestão, as sugestões aparecerão automaticamente no dashboard.

---

## Regras de Negócio

- Competitividade baseada na média de mercado
- Desconto estratégico de 10%
- Proteção de margem mínima (custo + 5%)
- Aprovação manual antes da atualização final

---

## Arquitetura para Alta Escala (Visão GCP)

Para suportar cenários com alto volume de eventos:

- A API publica eventos no **Cloud Pub/Sub**
- Workers no **Cloud Run** processam de forma assíncrona
- **Cloud SQL** armazena dados transacionais
- **BigQuery** armazena histórico para análises
- **Cloud Tasks** pode ser utilizado para retries

Essa abordagem desacopla ingestão do processamento e permite escalabilidade horizontal.

---

## Objetivo do Projeto

O foco foi:

- Clareza na regra de negócio
- Separação de responsabilidades
- Execução simples via Docker
- Código organizado e fácil de evoluir

A interface foi mantida simples por priorização de arquitetura e qualidade de código.