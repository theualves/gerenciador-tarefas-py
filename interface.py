import customtkinter
from tkinter import messagebox
from programa import (
    criar_conexao,
    criar_tabela,
    listar_tarefa,
    adicionar_tarefa,
    deletar_tarefa,
    marcar_concluido,
    filtrar_tarefa
)

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("550x550")
app.title("Gerenciador de Tarefas")
app.configure(fg_color="#FFFFFF")



def handle_adicionar_tarefa(nome, descricao, data, janela):
    if not nome or not descricao or not data:
        messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!", parent=janela)
        return

    conexao = criar_conexao()
    if adicionar_tarefa(conexao, nome, descricao, data):
        conexao.close()
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!", parent=janela)
        janela.destroy()  
        exibir_tarefas_na_lista() 
    else:
        conexao.close()
        messagebox.showerror("Erro", "Formato de data inválido. Use AAAA-MM-DD.", parent=janela)


def handle_deletar_tarefa(id_tarefa, nome_tarefa):
    """Pede confirmação e deleta uma tarefa."""
    if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar a tarefa:\n\n'{nome_tarefa}'?"):
        conexao = criar_conexao()
        deletar_tarefa(conexao, id_tarefa)
        conexao.close()
        exibir_tarefas_na_lista()


def handle_marcar_concluido(id_tarefa):
    """Marca uma tarefa como concluída."""
    conexao = criar_conexao()
    marcar_concluido(conexao, id_tarefa)
    conexao.close()
    exibir_tarefas_na_lista()


def abrir_janela_adicionar():
    """Cria e exibe uma nova janela (Toplevel) para adicionar tarefas."""
    janela_add = customtkinter.CTkToplevel(app)
    janela_add.title("Adicionar Nova Tarefa")
    janela_add.geometry("380x320")
    janela_add.transient(app)  
    janela_add.grab_set()  
    janela_add.resizable(False, False)

    label_nome = customtkinter.CTkLabel(janela_add, text="Nome da Tarefa:")
    label_nome.pack(padx=20, pady=(20, 5), anchor="w")
    entry_nome = customtkinter.CTkEntry(janela_add, width=340)
    entry_nome.pack(padx=20, pady=(0, 10))

    label_desc = customtkinter.CTkLabel(janela_add, text="Descrição:")
    label_desc.pack(padx=20, pady=(0, 5), anchor="w")
    entry_desc = customtkinter.CTkEntry(janela_add, width=340)
    entry_desc.pack(padx=20, pady=(0, 10))

    label_data = customtkinter.CTkLabel(janela_add, text="Data de Vencimento (AAAA-MM-DD):")
    label_data.pack(padx=20, pady=(0, 5), anchor="w")
    entry_data = customtkinter.CTkEntry(janela_add, width=340, placeholder_text="Ex: 2025-12-31")
    entry_data.pack(padx=20, pady=(0, 20))

    btn_salvar = customtkinter.CTkButton(
        janela_add,
        text="Salvar Tarefa",
        command=lambda: handle_adicionar_tarefa(
            entry_nome.get(),
            entry_desc.get(),
            entry_data.get(),
            janela_add
        )
    )
    btn_salvar.pack(padx=20, pady=10, fill="x")


def exibir_tarefas_na_lista(filtro_status=None):
    """Busca as tarefas no DB e as exibe na tela, aplicando um filtro se necessário."""
    conexao = criar_conexao()
    criar_tabela(conexao)

    if filtro_status:
        tarefas = filtrar_tarefa(conexao, filtro_status)
    else:
        tarefas = listar_tarefa(conexao)

    conexao.close()

    for widget in frame_lista.winfo_children():
        widget.destroy()

    if not tarefas:
        label_vazia = customtkinter.CTkLabel(master=frame_lista, text="Nenhuma tarefa encontrada.",
                                             text_color="#666666", font=("", 14))
        label_vazia.pack(pady=20)
        return

    for tarefa in tarefas:
        id_tarefa, nome, descricao, data, status = tarefa

        card_tarefa = customtkinter.CTkFrame(master=frame_lista, corner_radius=10, fg_color="gray95")
        card_tarefa.pack(pady=6, padx=10, fill="x")
        
        info_frame = customtkinter.CTkFrame(card_tarefa, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=(7, 0))
        info_frame.grid_columnconfigure(0, weight=1)

        label_nome = customtkinter.CTkLabel(info_frame, text=f"{nome.upper()}", font=("", 16, "bold"), justify="left")
        label_nome.grid(row=0, column=0, sticky="w")

        status_color = "#FE9E00" if status.lower() == "pendente" else "#00CE45"
        label_status = customtkinter.CTkLabel(info_frame, text=status.capitalize(), font=("", 12, "bold"), text_color=status_color)
        label_status.grid(row=0, column=1, sticky="e", padx=(10, 0))
        
        line_card_separator = customtkinter.CTkFrame(card_tarefa, height=2, fg_color="gray85")
        line_card_separator.pack(fill="x", padx=15, pady=5)
        
        label_descricao = customtkinter.CTkLabel(card_tarefa, text=descricao, font=("", 14), text_color="#555555",
                                                 justify="left", wraplength=450)
        label_descricao.pack(padx=15, pady=(0, 5), anchor="w")

        label_vencimento = customtkinter.CTkLabel(card_tarefa, text=f"Vencimento: {data}", font=("", 12, "italic"),
                                                    text_color="#333333")
        label_vencimento.pack(padx=15, pady=(0, 10), anchor="w")

        botoes_frame = customtkinter.CTkFrame(card_tarefa, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=15, pady=(0, 10))
        botoes_frame.grid_columnconfigure((0, 1), weight=1)

        if status.lower() == 'pendente':
            btn_concluir = customtkinter.CTkButton(
                botoes_frame,
                text="Marcar como Concluída",
                command=lambda id=id_tarefa: handle_marcar_concluido(id)
            )
            btn_concluir.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        btn_deletar = customtkinter.CTkButton(
            botoes_frame,
            text="Deletar",
            fg_color="#D80032", hover_color="#B20028",
            command=lambda id=id_tarefa, n=nome: handle_deletar_tarefa(id, n)
        )
        
        coluna_span = 2 if status.lower() != 'pendente' else 1
        coluna_pos = 0 if status.lower() != 'pendente' else 1
        padding_esquerdo = 5 if status.lower() == 'pendente' else 0
        btn_deletar.grid(row=0, column=coluna_pos, columnspan=coluna_span, sticky="ew", padx=(padding_esquerdo, 0))



label_titulo = customtkinter.CTkLabel(master=app, text="Minhas Tarefas", font=("", 24, "bold"), text_color="gray10")
label_titulo.pack(pady=(20, 10))

frame_lista = customtkinter.CTkScrollableFrame(master=app, fg_color="#FFFFFF")
frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

frame_controles = customtkinter.CTkFrame(master=app, fg_color="transparent")
frame_controles.pack(pady=(5, 15), padx=20, fill="x")

def filtro_selecionado(status_selecionado):
    if status_selecionado == "Todas":
        exibir_tarefas_na_lista()
    elif status_selecionado == "Pendentes":
        exibir_tarefas_na_lista("pendente")
    elif status_selecionado == "Concluídas":
        exibir_tarefas_na_lista("concluido")

filtro = customtkinter.CTkSegmentedButton(
    master=frame_controles,
    values=["Todas", "Pendentes", "Concluídas"],
    command=filtro_selecionado,
    font=("", 14)
)
filtro.pack(side="left", padx=(0, 10), expand=True)

btn_adicionar = customtkinter.CTkButton(
    master=frame_controles,
    text="+ Nova Tarefa",
    font=("", 14, "bold"),
    command=abrir_janela_adicionar,
    width=150
)
btn_adicionar.pack(side="right", expand=True)

exibir_tarefas_na_lista()

app.mainloop()