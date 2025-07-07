import sqlite3
from datetime import datetime

def criar_conexao():
  return sqlite3.connect('tarefas.db')

def criar_tabela(conexao):
  cursor = conexao.cursor()
  cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tarefas (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nome_tarefa TEXT NOT NULL,
          descricao TEXT NOT NULL,
          data_vencimento TEXT,
          status TEXT NOT NULL
          )
        ''')
  conexao.commit()


def adicionar_tarefa(conexao, nome_tarefa, descricao, data_vencimento):
  cursor = conexao.cursor()
  status = "pendente"
  data_vencimento = data_vencimento.strip()

  try:
    datetime.strptime(data_vencimento, "%Y-%m-%d")

    cursor.execute(''' 
        INSERT INTO tarefas(nome_tarefa, descricao, data_vencimento, status)
        VALUES (?,?,?,?) ''',(nome_tarefa, descricao, data_vencimento, status))
    conexao.commit()
    print("Adicionada com sucesso!")
  except ValueError:
    print("ERRO! verifique coloque a data nesse formato (AAAA-MM-DD)")

def main():
  conexao = criar_conexao()
  criar_tabela(conexao)

  while True:
    print("--------- GERENCIADOR DE TAREFAS ------------")
    print("1. Adicionar uma tarefa")
    print("2. Sair do programa")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
      nome_tarefa =  input("\nDigite o nome da tarefa: ")
      descricao = input("Digite a descrição da tarefa: ")
      data_vencimento = input("Digite a data de vencimento (AAAA-MM-DD): ")
      adicionar_tarefa(conexao, nome_tarefa, descricao, data_vencimento)
    elif escolha == '2':
      break

if __name__ == "__main__":
    main()