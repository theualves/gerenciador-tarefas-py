import customtkinter
from programa import criar_tabela, criar_conexao, listar_tarefa

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("500x400")
app.configure(fg_color="#FFFFFF")

def exibir_tarefas_na_lista():
    conexao = criar_conexao()
    criar_tabela(conexao)
    tarefas = listar_tarefa(conexao)
    conexao.close()

    for widget in frame_lista.winfo_children():
        widget.destroy()

    if not tarefas:
        label_vazia = customtkinter.CTkLabel(master=frame_lista, text="Nenhuma tarefa encontrada.", text_color="#666666")
        label_vazia.pack(pady=10)
        return

    for tarefa in tarefas:
        id_tarefa, nome, descricao, data, status = tarefa
        
        card_tarefa = customtkinter.CTkFrame(master=frame_lista, corner_radius=10)
        card_tarefa.pack(pady=6, padx=10, fill="x", anchor="w")
        
        # --- CONFIGURAÇÃO DA GRADE ---
        # Dizemos que a coluna 0 deve se expandir para preencher o espaço, enquanto a coluna 1 não.
        card_tarefa.grid_columnconfigure(0, weight=1)
        card_tarefa.grid_columnconfigure(1, weight=0)

        # Coluna 0 (Nome)
        label_nome = customtkinter.CTkLabel(
            master=card_tarefa,
            text=f"{nome.upper()}",
            font=("", 16, "bold"),
            justify="left"
        )
        # sticky="w" (west) alinha o widget à esquerda da sua célula na grade
        label_nome.grid(row=0, column=0, sticky="w", padx=15, pady=(7, 0))

        # Coluna 1 (Status) - NOVO LABEL SÓ PARA O STATUS

        if status.lower() == "pendente":
            status_color = "#FE9E00"
        elif status.lower() == "concluido":
            status_color = "#00CE45"
        else:
            status_color = "gray"

        label_status = customtkinter.CTkLabel(
            master=card_tarefa,
            text=status.capitalize(),
            font=("", 12, "bold"),
            text_color=status_color
        )
        # sticky="e" (east) alinha o widget à direita da sua célula na grade
        label_status.grid(row=0, column=1, sticky="e", padx=15, pady=(7, 0))


        line_card_separator = customtkinter.CTkFrame(master=card_tarefa, height=3, fg_color="gray75")
        line_card_separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=5)


        label_descricao = customtkinter.CTkLabel(
            master=card_tarefa,
            text=descricao,
            font=("", 14),
            text_color="#555555",
            justify="left",
            wraplength=600
        )
        label_descricao.grid(row=2, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 5))


        label_vencimento = customtkinter.CTkLabel(
            master=card_tarefa,
            text=f"Vencimento: {data}",
            font=("", 12, "italic"),
            text_color="#333333"
        )
        label_vencimento.grid(row=3, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 7))


# --- Widgets da Interface ---

label_titulo = customtkinter.CTkLabel(master=app, text="Minhas Tarefas", font=("", 24, "bold"))
label_titulo.pack(pady=(20, 10))

frame_lista = customtkinter.CTkScrollableFrame(master=app, fg_color="#FFFFFF")
frame_lista.pack(pady=10, padx=20, fill="both", expand=True)


exibir_tarefas_na_lista()

app.mainloop()