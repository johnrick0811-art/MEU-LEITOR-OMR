import flet as ft
from database import *

def main(page: ft.Page):
    page.title = "Gerador de Cartões"
    page.window.width = 400
    page.window.height = 730
    page.window.resizable = False
    page.theme_mode = "light"
    page.theme = ft.Theme(color_scheme_seed="blue")

    # Funções de Navegação por Redesenho de Tela
    def go_to_classes():
        page.clean()
        page.add(render_classes())
    
    def go_to_students(tid, tnome):
        page.clean()
        page.add(render_students(tid, tnome))

    # --- TELA DE CLASSES ---
    def render_classes():
        lista_turmas = ft.ListView(spacing=10, expand=True)
        
        def load_list():
            lista_turmas.controls.clear()
            for t_id, t_nome in get_classes():
                item = ft.Container(
                    content=ft.Row([
                        ft.Icon("school", color="blue700"),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(t_nome, weight="bold", size=15),
                                ft.Text("Toque 2x para abrir", size=11, color="grey500")
                            ], spacing=2),
                            width=210
                        ),
                        ft.IconButton("delete", icon_color="red", on_click=lambda e, id=t_id: (delete_class(id), load_list()))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    width=340,
                    padding=10, 
                    bgcolor="white", 
                    border_radius=10,
                    on_double_tap=lambda e, tid=t_id, tnom=t_nome: go_to_students(tid, tnom)
                )
                lista_turmas.controls.append(item)
            page.update()

        load_list()
        
        campo_nome = ft.TextField(label="Nome da Turma", width=340)
        
        def salvar_e_fechar(e):
            if campo_nome.value:
                add_class(campo_nome.value)
                campo_nome.value = ""
                form_turma.visible = False
                load_list()

        form_turma = ft.Container(
            content=ft.Column([
                ft.Text("Adicionar Nova Turma", size=15, weight="bold", color="blue700"),
                campo_nome,
                ft.Row([
                    ft.TextButton("Cancelar", on_click=lambda e: setattr(form_turma, 'visible', False) or page.update()),
                    ft.Button("Salvar", on_click=salvar_e_fechar, bgcolor="blue700", color="white")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            padding=15, bgcolor="blue50", border_radius=10, visible=False, width=340
        )

        return ft.Column([
            ft.Row([
                ft.Text("Classes", size=24, weight="bold"),
                ft.Button("Nova Turma", icon="add", on_click=lambda e: (setattr(form_turma, 'visible', True), page.update()), bgcolor="blue700", color="white")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            form_turma,
            lista_turmas
        ], expand=True, padding=20)

    # --- TELA DE ESTUDANTES ---
    def render_students(tid, tnome):
        lista_alunos = ft.ListView(spacing=10, expand=True)
        
        def load_students():
            lista_alunos.controls.clear()
            for aid, num, nome, tel, email in get_students_by_class(tid):
                item = ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(f"{num} - {nome}", size=14, weight="bold"),
                            width=240
                        ),
                        ft.IconButton("delete", icon_color="red", on_click=lambda e, id=aid: (delete_student(id), load_students()))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    width=340,
                    padding=10, 
                    bgcolor="white", 
                    border_radius=10
                )
                lista_alunos.controls.append(item)
            page.update()
        
        load_students()

        campo_num = ft.TextField(label="Nº", width=60)
        campo_nome_aluno = ft.TextField(label="Nome do Aluno", width=260)

        def salvar_aluno_form(e):
            if campo_nome_aluno.value:
                num = int(campo_num.value) if campo_num.value.isdigit() else 0
                add_student(tid, num, campo_nome_aluno.value)
                campo_nome_aluno.value = ""
                campo_num.value = ""
                form_aluno.visible = False
                load_students()

        form_aluno = ft.Container(
            content=ft.Column([
                ft.Text("Adicionar Aluno", size=15, weight="bold", color="blue700"),
                ft.Row([campo_num, campo_nome_aluno], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.TextButton("Cancelar", on_click=lambda e: setattr(form_aluno, 'visible', False) or page.update()),
                    ft.Button("Salvar", on_click=salvar_aluno_form, bgcolor="blue700", color="white")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            padding=15, bgcolor="blue50", border_radius=10, visible=False, width=340
        )
        
        return ft.Column([
            ft.Row([
                ft.TextButton("← Voltar", on_click=lambda e: go_to_classes()),
                ft.Text(tnome, size=18, weight="bold")
            ]),
            ft.Divider(),
            ft.Row([
                ft.Button("Novo Aluno", icon="add", on_click=lambda e: (setattr(form_aluno, 'visible', True), page.update()), bgcolor="blue700", color="white")
            ], alignment=ft.MainAxisAlignment.END),
            form_aluno,
            lista_alunos
        ], expand=True, padding=20)

    go_to_classes()

ft.run(main)