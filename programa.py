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


def listar_tarefa(conexao):
  cursor = conexao.cursor()
  cursor.execute('SELECT * FROM tarefas')
  tarefas = cursor.fetchall()
  if len(tarefas) > 0:
    for tarefa in tarefas:
      print(f"\nID: {tarefa[0]} \nNome da Tarefa: {tarefa[1]} \nDescrição: {tarefa[2]} \nData de Vencimento: {tarefa[3]} \nStatus: {tarefa[4]}")
  else:
    print("Nenhuma tarefa foi adicionada")
    
def filtrar_tarefas(conexao):
    cursor = conexao.cursor()
    print("\nFiltrar por:")
    print("1. Status")
    print("2. Data")
    print("3. Nome")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        criterio = "Status"
        valor = input("Digite o status (pendente ou concluído): ")
    elif opcao == '2':
        criterio = "Data"
        valor = input("Digite a data de vencimento (AAAA-MM-DD): ")
    elif opcao == '3':
        criterio = "Nome"
        valor = input("Digite parte do nome da tarefa: ")
    else:
        print("Opção inválida.")
        return

    if criterio == "Status":
        cursor.execute('SELECT * FROM tarefas WHERE status = ?', (valor,))
    elif criterio == "Data":
        cursor.execute('SELECT * FROM tarefas WHERE data_vencimento = ?', (valor,))
    elif criterio == "Nome":
        cursor.execute('SELECT * FROM tarefas WHERE nome_tarefa LIKE ?', (f"%{valor}%",))

    resultados = cursor.fetchall()

    if resultados:
        print("\nResultados do filtro:")
        for tarefa in resultados:
            print(f"\nID: {tarefa[0]}")
            print(f"Nome da Tarefa: {tarefa[1]}")
            print(f"Descrição: {tarefa[2]}")
            print(f"Data de Vencimento: {tarefa[3]}")
            print(f"Status: {tarefa[4]}")
    else:
        print("Nenhuma tarefa encontrada com esse filtro.")

def main():
    conexao = criar_conexao()
    criar_tabela(conexao)

    while True:
        print("\n--------- GERENCIADOR DE TAREFAS ------------")
        print("1. Adicionar uma tarefa")
        print("2. Listar tarefas")
        print("3. Sair do programa")
        print("4. Filtrar tarefa")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome_tarefa = input("\nDigite o nome da tarefa: ")
            descricao = input("Digite a descrição da tarefa: ")
            data_vencimento = input("Digite a data de vencimento (AAAA-MM-DD): ")
            adicionar_tarefa(conexao, nome_tarefa, descricao, data_vencimento)
        elif escolha == '2':
            listar_tarefa(conexao)
        elif escolha == '3':
            break
        elif escolha == '4':
            filtrar_tarefas(conexao)
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
