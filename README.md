<<<<<<< HEAD
Gerenciador de Tarefas
Este é um aplicativo de desktop simples para gerenciar tarefas, desenvolvido em Python usando Tkinter para a interface gráfica e SQLite como banco de dados. Ele permite adicionar, editar, excluir e filtrar tarefas, além de definir prazos de conclusão.

Funcionalidades
    Adicionar novas tarefas com informações detalhadas:
    Nome da tarefa
    Descrição
    Status (Não Iniciado, Em Andamento, Concluído)
    Pedido (Request)
    Prioridade (Baixo, Médio, Alto)
    Data de conclusão
    Editar tarefas existentes.
    Excluir tarefas.
    Filtrar tarefas com base no status.
    Visualização em uma tabela interativa.

Pré-requisitos
    Python 3.7 ou superior.

Bibliotecas necessárias:
    tkinter (incluso na instalação padrão do Python)
    sqlite3 (incluso na instalação padrão do Python)
    tkcalendar (instalar separadamente)
    ttk (padrão do Tkinter)


Adicionar uma tarefa:
    Clique em "Adicionar Tarefa".
    Preencha os campos e selecione uma data no calendário.
    Clique em "Salvar"

Editar uma tarefa:
    Selecione uma tarefa na tabela.
    Clique em "Editar Tarefa".
    Modifique os campos desejados e clique em "Salvar".

Excluir uma tarefa:
    Selecione uma tarefa na tabela.
    Clique em "Excluir Tarefa".

Filtrar tarefas:
    Use o menu suspenso acima da tabela para filtrar por status.


Estrutura do Código
TaskDB: Classe que gerencia o banco de dados SQLite.
Criação da tabela de tarefas.
Inserção, edição, exclusão e recuperação de dados.
TaskApp: Classe principal da interface gráfica.
Gerencia a tabela de tarefas.
Define janelas de adicionar/editar tarefas.
Conecta a interface ao banco de dados.

Instalar as biblioteca
    pip install -r requirements.txt
    
Licença
Este projeto está licenciado sob a Licença FMU.

=======
# FMU_Tasks
Gerenciador de Tarefas Este é um aplicativo de desktop simples para gerenciar tarefas, desenvolvido em Python usando Tkinter para a interface gráfica e SQLite como banco de dados. 
>>>>>>> f97d1090b6a8c673f3e7a63a6d38b9af6109bd1b
