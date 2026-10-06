# ☁️ Cloud Data Engineering — GCP

Projeto completo de Engenharia de Dados desenvolvido para simular um ambiente corporativo de ingestão, transformação, qualidade e disponibilização de dados em nuvem.

O projeto implementa um pipeline **end-to-end**, partindo de um banco transacional PostgreSQL até um Data Warehouse analítico no Google BigQuery, utilizando **Python, Google Cloud Storage, BigQuery, Apache Airflow e dbt**.

---

## 🎯 Objetivo

Construir uma arquitetura de dados moderna e reprodutível capaz de:

- Extrair dados de um banco PostgreSQL;
- Realizar ingestão incremental utilizando controle de *watermark*;
- Armazenar dados brutos no Google Cloud Storage;
- Disponibilizar a camada Bronze no BigQuery;
- Transformar os dados utilizando dbt;
- Construir as camadas Silver e Gold;
- Implementar um modelo dimensional para análise;
- Aplicar testes de qualidade de dados;
- Realizar reconciliação financeira;
- Utilizar particionamento e clustering no BigQuery;
- Orquestrar o pipeline com Apache Airflow;
- Enviar notificações de sucesso e falha;
- Documentar e versionar todo o projeto com Git.

---

## 🏗️ Arquitetura

```text
                    ┌─────────────────────┐
                    │   PostgreSQL OLTP   │
                    │                     │
                    │ clientes            │
                    │ produtos            │
                    │ pedidos             │
                    │ itens_pedido        │
                    │ pipeline_control    │
                    └──────────┬──────────┘
                               │
                               │ Python
                               │ Incremental
                               ▼
                    ┌─────────────────────┐
                    │         GCS         │
                    │    Raw / Parquet    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   BigQuery Bronze   │
                    │     Dados brutos    │
                    └──────────┬──────────┘
                               │
                               │ dbt
                               ▼
                    ┌─────────────────────┐
                    │   BigQuery Silver   │
                    │    Dados tratados   │
                    └──────────┬──────────┘
                               │
                               │ dbt
                               ▼
                    ┌─────────────────────┐
                    │    BigQuery Gold    │
                    │ Modelo dimensional  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       BI / SQL      │
                    │    Análises/KPIs    │
                    └─────────────────────┘


              ┌──────────────────────────────┐
              │        Apache Airflow        │
              │        Orquestração          │
              └──────────────────────────────┘
```

---

## 🧰 Tecnologias

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python |
| Banco transacional | PostgreSQL 16 |
| Armazenamento | Google Cloud Storage |
| Data Warehouse | Google BigQuery |
| Transformação | dbt Core |
| Orquestração | Apache Airflow |
| Containerização | Docker |
| Cloud | Google Cloud Platform |
| API | Open-Meteo |
| Formato de dados | Parquet |
| Versionamento | Git / GitHub |

---

## 📁 Estrutura do projeto

```text
projeto_cloud_gcp_data_engineering/
│
├── dags/
│   ├── pipeline_cloud.py
│   ├── load_bronze.py
│   ├── load_weather.py
│   └── load_metas.py
│
├── include/
│   ├── notifications.py
│   │
│   └── projeto_dw/
│       ├── dbt_project.yml
│       ├── models/
│       │   ├── sources.yml
│       │   ├── silver/
│       │   └── gold/
│       │       └── schema.yml
│       │
│       └── tests/
│           ├── fato_vendas_quantidade_positiva.sql
│           └── fato_vendas_reconciliacao.sql
│
├── plugins/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🔄 Pipeline de dados

## 1. Extração

Os dados são extraídos do PostgreSQL utilizando Python, `psycopg2`, pandas e PyArrow.

Os arquivos são convertidos para **Parquet**, reduzindo o volume armazenado e mantendo um formato adequado para processamento analítico.

A extração utiliza controle incremental baseado no campo `updated_at`.

### Watermark

O controle da última execução é armazenado na tabela:

```text
pipeline_control
```

A lógica utilizada é:

```sql
updated_at > watermark
```

Dessa forma, o pipeline não precisa processar novamente todos os registros a cada execução.

---

## 2. Google Cloud Storage

Os arquivos Parquet são armazenados no bucket:

```text
cloud-data-engineering-raw-tony
```

O GCS funciona como camada de armazenamento dos dados brutos antes da carga no Data Warehouse.

---

# 🥉 Bronze

A camada Bronze mantém os dados em sua forma mais próxima possível da origem.

Dataset:

```text
bronze
```

Principais entidades:

- `clientes`
- `produtos`
- `pedidos`
- `itens_pedido`

Volumes validados:

| Tabela | Registros |
|---|---:|
| clientes | 500 |
| produtos | 100 |
| pedidos | 5.000 |
| itens_pedido | 15.078 |

---

# 🥈 Silver

A camada Silver é construída utilizando **dbt**.

Responsabilidades:

- Padronização;
- Tratamento dos dados;
- Tipagem;
- Aplicação das regras de transformação;
- Preparação dos dados para consumo analítico.

Dataset:

```text
silver
```

O dbt é responsável pela transformação entre as camadas Bronze e Silver.

---

# 🥇 Gold

A camada Gold contém os dados preparados para análise.

Dataset:

```text
gold
```

### Modelo dimensional

#### Fatos

- `fato_vendas`
- `fato_metas`

#### Dimensões

- `dim_clientes`
- `dim_produtos`
- `dim_calendario`

#### KPIs

- `kpi_mensal`

O modelo foi estruturado seguindo princípios de **modelagem dimensional**, facilitando consultas analíticas e consumo por ferramentas de BI.

---

# ⚡ Particionamento e Clustering

A tabela:

```text
gold.fato_vendas
```

utiliza:

- **Particionamento mensal** por `data_pedido`;
- **Clustering** por `cliente_id` e `produto_id`.

Essa estratégia reduz o volume de dados processado em consultas que utilizam filtros temporais e melhora a organização dos dados analíticos.

---

# 🧪 Data Quality

O projeto possui testes de qualidade implementados no dbt.

São utilizados testes como:

- `not_null`
- `unique`
- `relationships`

Além disso, existem testes customizados para regras específicas do negócio:

```text
fato_vendas_quantidade_positiva.sql
fato_vendas_reconciliacao.sql
```

### Resultado

```text
20 testes executados
20 PASS
0 WARN
0 ERROR
0 SKIP
```

Os testes estão distribuídos entre os modelos dimensionais, fatos e indicadores.

---

# 💰 Reconciliação financeira

Foi implementada uma validação independente entre os pedidos e seus respectivos itens.

### Resultado

| Origem | Valor |
|---|---:|
| Total dos pedidos | R$ 110.682.385,35 |
| Total dos itens | R$ 110.682.385,35 |
| Diferença | **R$ 0,00** |

A reconciliação garante que o valor financeiro dos pedidos está consistente com a composição dos itens.

Também foram validados:

- Pedidos sem itens;
- Itens órfãos;
- Produtos inexistentes;
- Pedidos com valor zero;
- Integridade referencial.

---

# 🌦️ Dados externos

O projeto também possui uma etapa de ingestão de dados meteorológicos utilizando a API **Open-Meteo**.

A ingestão é orquestrada pelo Airflow e integrada ao ambiente de dados do projeto.

---

# 🎯 Metas

Foi implementada uma carga de metas para complementar os dados transacionais e permitir análises comparativas entre:

- Realizado;
- Meta;
- Desempenho mensal.

O modelo resultante é:

```text
gold.fato_metas
```

---

# 🔄 Orquestração

O **Apache Airflow** é responsável pela execução e coordenação dos processos.

Entre as responsabilidades estão:

- Extração incremental;
- Upload para GCS;
- Carga da Bronze;
- Carga de dados externos;
- Carga de metas;
- Transformações dbt;
- Validações;
- Notificações.

O pipeline principal:

```text
pipeline_cloud
```

foi executado com sucesso após a validação final do projeto.

---

# 📧 Notificações

Foram implementadas notificações por e-mail para acompanhamento das execuções.

O projeto possui tratamento para:

- Sucesso;
- Falha controlada;
- Monitoramento das principais etapas do pipeline.

---

# 📚 Documentação dbt

A documentação do dbt foi gerada utilizando:

```bash
dbt docs generate
```

Resultado da geração:

- 12 modelos;
- 20 testes;
- 6 sources;
- Macros do projeto e dependências documentadas.

---

# 🚀 Como executar

## Pré-requisitos

- Docker
- Python
- Git
- Astro CLI
- Conta Google Cloud
- Projeto GCP com BigQuery e Cloud Storage habilitados

---

## Clonar o projeto

```bash
git clone https://github.com/tonymiguelsilva/projeto-cloud-gcp-data-engineering.git
cd projeto-cloud-gcp-data-engineering
```

---

## Inicializar o ambiente

O projeto utiliza Apache Airflow executado com Docker/Astro.

```bash
astro dev start
```

Verifique os containers:

```bash
astro dev ps
```

---

## Executar o pipeline

O DAG principal é:

```text
pipeline_cloud
```

Ele pode ser executado pelo Airflow para processar o fluxo completo.

---

## Executar dbt

Dentro do ambiente Airflow:

```bash
dbt debug
```

Executar modelos:

```bash
dbt run
```

Executar testes:

```bash
dbt test
```

Gerar documentação:

```bash
dbt docs generate
```

---

# 📊 Resultados do projeto

O projeto foi validado com sucesso em um ambiente GCP, contemplando:

- Ingestão incremental;
- Armazenamento em GCS;
- Data Warehouse no BigQuery;
- Arquitetura Bronze / Silver / Gold;
- Modelagem dimensional;
- Orquestração com Airflow;
- Transformações com dbt;
- Data Quality;
- Reconciliação financeira;
- Particionamento;
- Clustering;
- Dados externos;
- Metas;
- Notificações;
- Documentação;
- Versionamento Git.

### Indicadores finais

```text
5.000 pedidos
15.078 itens de pedido
500 clientes
100 produtos

20/20 testes de qualidade

R$ 110.682.385,35
reconciliados

Diferença financeira:
R$ 0,00
```

---

# 🧠 Principais conceitos aplicados

Este projeto foi desenvolvido para praticar conceitos presentes em ambientes reais de Engenharia de Dados:

- ETL / ELT;
- Data Lake;
- Data Warehouse;
- Arquitetura Medallion;
- Ingestão incremental;
- Watermark;
- Modelagem dimensional;
- Data Quality;
- Data Lineage;
- Orquestração;
- Cloud Data Engineering;
- Particionamento;
- Clustering;
- Observabilidade;
- Versionamento;
- Automação.

---

## 👨‍💻 Autor

**Tony Miguel Silva**

Analista de Dados | Engenharia de Dados

Projeto desenvolvido como parte da evolução prática em **Data Engineering, Cloud, Analytics e Data Architecture**.

---

## 📌 Status

**Projeto concluído ✅**

Pipeline validado de ponta a ponta em ambiente Google Cloud.

```text
PostgreSQL
    ↓
Python
    ↓
GCS
    ↓
BigQuery Bronze
    ↓
dbt Silver
    ↓
dbt Gold
    ↓
Analytics / BI
```