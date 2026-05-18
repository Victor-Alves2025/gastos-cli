# Controle de Gastos CLI

## Problema

Muitas pessoas têm dificuldade em controlar seus gastos diários, especialmente
quando envolvem compras em moeda estrangeira.

## Solução

Aplicação em linha de comando para registrar, listar e calcular gastos, com
integração em tempo real à API de câmbio [AwesomeAPI](https://economia.awesomeapi.com.br/)
para converter automaticamente gastos em USD, EUR, GBP e ARS para reais.

## Público-alvo

Pessoas que querem controlar seus gastos de forma simples, incluindo compras
internacionais ou em sites estrangeiros.

## Funcionalidades

* Adicionar gastos em R$
* Adicionar gastos em moeda estrangeira (conversão automática para BRL)
* Ver cotações em tempo real (USD, EUR, GBP, ARS)
* Listar todos os gastos
* Ver total acumulado

## Integração com API Pública

A aplicação consome a **AwesomeAPI de Câmbio** (`economia.awesomeapi.com.br`),
uma API gratuita e sem necessidade de chave de autenticação, que fornece
cotações em tempo real de diversas moedas em relação ao Real Brasileiro.

Exemplo de endpoint utilizado:
```
GET https://economia.awesomeapi.com.br/json/last/USD-BRL
```

## Tecnologias

* Python 3.10+
* `requests` — consumo da API de câmbio
* `pytest` — testes unitários e de integração
* `flake8` — lint

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python src/app.py
```

## Testes

```bash
python -m pytest
```

## Lint

```bash
python -m flake8 .
```

## Versão

1.1.0

## Autor

Victor Alves
