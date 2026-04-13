import json
import os

FILE = "gastos.json"


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


def menu():
    while True:
        print("\n1. Adicionar gasto")
        print("2. Listar gastos")
        print("3. Total")
        print("4. Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            valor = float(input("Valor: "))
            descricao = input("Descrição: ")
            adicionar_gasto(valor, descricao)

        elif opcao == "2":
            gastos = listar_gastos()
            for g in gastos:
                print(g)

        elif opcao == "3":
            print("Total:", total_gastos())

        elif opcao == "4":
            break


if __name__ == "__main__":
    menu()
    