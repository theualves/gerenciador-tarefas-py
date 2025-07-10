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
    return True
  except ValueError:
    print("ERRO! verifique coloque a data nesse formato (AAAA-MM-DD)")
    return False

def deletar_tarefa(conexao, id_tarefa):
   cursor = conexao.cursor()
   try:
      cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
      conexao.commit()
      return cursor.rowcount > 0
   except sqlite3.Error as e:
      print("Erro ao deletar uma tarefa: {e}")
      return False

def listar_tarefa(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()
    return tarefas

def marcar_concluido(conexao, id_tarefa):
    cursor = conexao.cursor()
    novo_status = 'concluido'
    try:
        cursor.execute('UPDATE tarefas SET status = ? where id = ?',(novo_status, id_tarefa))
        conexao.commit()
        if cursor.rowcount > 0:
           print(f"A tarefa: {id_tarefa} marcada como concluida com sucesso!")
           return True
        else:
           print(f"Erro! Nenhuma tarefa com ID:{id_tarefa} foi encontrada!")
           return False
    except sqlite3.Error as e:
       print(f"Erro ao atualizar a tarefa: {e}")
       return False
    
def filtrar_tarefa(conexao, status):
   cursor = conexao.cursor()
   try:
      cursor.execute('SELECT * FROM tarefas WHERE status = ?', (status,))
      tarefas_filtradas = cursor.fetchall()
      return tarefas_filtradas
   except sqlite3.Error as e:
      print(f"Erro ao filtrar a tarefa por status: {e}")
      return []