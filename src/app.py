import json
import os
import requests

FILE = "gastos.json"

# API de câmbio gratuita (sem chave necessária)
API_CAMBIO_URL = "https://economia.awesomeapi.com.br/json/last/{}"


def carregar_gastos():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def salvar_gastos(gastos):
    with open(FILE, "w") as f:
        json.dump(gastos, f)


def adicionar_gasto(valor, descricao):
    if valor < 0:
        raise ValueError("Valor não pode ser negativo")

    gastos = carregar_gastos()
    gastos.append({"valor": valor, "descricao": descricao})
    salvar_gastos(gastos)


def listar_gastos():
    return carregar_gastos()


def total_gastos():
    return sum(g["valor"] for g in carregar_gastos())


def buscar_cotacao(moeda):
    """Busca a cotação de uma moeda em relação ao Real (BRL).

    Args:
        moeda: código do par, ex: 'USD-BRL', 'EUR-BRL'

    Returns:
        dict com 'nome', 'bid' (compra) e 'ask' (venda),
        ou None em caso de erro.
    """
    try:
        resposta = requests.get(API_CAMBIO_URL.format(moeda), timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        chave = moeda.replace("-", "")
        cotacao = dados[chave]
        return {
            "nome": cotacao["name"],
            "bid": float(cotacao["bid"]),
            "ask": float(cotacao["ask"]),
        }
    except (requests.RequestException, KeyError, ValueError):
        return None


def converter_para_brl(valor, moeda):
    """Converte um valor em moeda estrangeira para BRL usando cotação atual.

    Args:
        valor: valor na moeda de origem
        moeda: código do par, ex: 'USD-BRL'

    Returns:
        tuple (valor_brl, cotacao_usada) ou (None, None) em caso de erro.
    """
    cotacao = buscar_cotacao(moeda)
    if cotacao is None:
        return None, None
    valor_brl = round(valor * cotacao["bid"], 2)
    return valor_brl, cotacao["bid"]


MOEDAS_SUPORTADAS = {
    "1": ("USD-BRL", "Dólar Americano (USD)"),
    "2": ("EUR-BRL", "Euro (EUR)"),
    "3": ("GBP-BRL", "Libra Esterlina (GBP)"),
    "4": ("ARS-BRL", "Peso Argentino (ARS)"),
}


def menu():
    while True:
        print("\n=== Controle de Gastos CLI ===")
        print("1. Adicionar gasto (R$)")
        print("2. Adicionar gasto em moeda estrangeira")
        print("3. Ver cotações")
        print("4. Listar gastos")
        print("5. Total")
        print("6. Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            valor = float(input("Valor (R$): "))
            descricao = input("Descrição: ")
            adicionar_gasto(valor, descricao)
            print(f"✓ Gasto de R$ {valor:.2f} adicionado.")

        elif opcao == "2":
            print("\nMoedas disponíveis:")
            for k, (_, nome) in MOEDAS_SUPORTADAS.items():
                print(f"  {k}. {nome}")
            escolha = input("Escolha a moeda: ")
            if escolha not in MOEDAS_SUPORTADAS:
                print("Moeda inválida.")
                continue
            par, nome_moeda = MOEDAS_SUPORTADAS[escolha]
            sigla = par.split("-")[0]
            valor_ext = float(input(f"Valor em {sigla}: "))
            descricao = input("Descrição: ")
            print(f"Buscando cotação de {nome_moeda}...")
            valor_brl, cotacao = converter_para_brl(valor_ext, par)
            if valor_brl is None:
                print("Erro ao buscar cotação. Tente novamente.")
                continue
            print(
                f"Cotação: 1 {sigla} = R$ {cotacao:.4f} → "
                f"{valor_ext} {sigla} = R$ {valor_brl:.2f}"
            )
            descricao_completa = (
                f"{descricao} ({valor_ext} {sigla} @ R${cotacao:.4f})"
            )
            adicionar_gasto(valor_brl, descricao_completa)
            print(f"✓ Gasto de R$ {valor_brl:.2f} adicionado.")

        elif opcao == "3":
            print("\n=== Cotações em Tempo Real ===")
            for _, (par, nome) in MOEDAS_SUPORTADAS.items():
                sigla = par.split("-")[0]
                cotacao = buscar_cotacao(par)
                if cotacao:
                    print(
                        f"  {nome}: compra R$ {cotacao['bid']:.4f} | "
                        f"venda R$ {cotacao['ask']:.4f}"
                    )
                else:
                    print(f"  {nome}: cotação indisponível")

        elif opcao == "4":
            gastos = listar_gastos()
            if not gastos:
                print("Nenhum gasto registrado.")
            else:
                print("\n=== Gastos Registrados ===")
                for i, g in enumerate(gastos, 1):
                    print(f"  {i}. R$ {g['valor']:.2f} — {g['descricao']}")

        elif opcao == "5":
            print(f"\nTotal: R$ {total_gastos():.2f}")

        elif opcao == "6":
            break


if __name__ == "__main__":
    menu()
