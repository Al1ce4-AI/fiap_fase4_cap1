from src.database.models.fazenda import Fazenda
from src.database.models.maquinario import Maquinario
from src.database.models.insumo import Insumo
from src.database.models.relatorio import Relatorio
from typing import List, Optional

def selecionar_entidade(model, prompt: str = "Selecione uma opção: ") -> Optional[object]:
    itens: List[object] = model.fetch_all()
    
    if not itens:
        print(f"Nenhum(a) {model.display_name()} cadastrado(a).")
        return None
    
    print(f"\n--- Selecionar {model.display_name()} ---")
    for i, item in enumerate(itens, 1):
        print(f"{i}) {item.nome}")
    print("0) Voltar")
    
    try:
        escolha = int(input(prompt))
        if escolha == 0:
            return None
        return itens[escolha - 1]
    except (ValueError, IndexError):
        print("Opção inválida!")
        return None

def menu_relatorio_fazenda():
    fazenda = selecionar_entidade(Fazenda, "Selecione a fazenda para ver detalhes (0 para voltar): ")
    if not fazenda:
        return
    
    relatorio = Relatorio.gerar_relatorio_fazenda(fazenda)
    
    print("\n--- Relatório da Fazenda ---")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")

def menu_relatorio_maquinario():
    fazenda = selecionar_entidade(Fazenda, "Selecione a fazenda (0 para voltar): ")
    if not fazenda:
        return
    
    maquinario = selecionar_entidade(Maquinario, "Selecione o maquinário (0 para voltar): ")
    if not maquinario:
        return
    
    relatorio = Relatorio.gerar_relatorio_maquinario(fazenda, maquinario)
    
    print("\n--- Relatório de Maquinário ---")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")

def menu_relatorio_insumo():
    fazenda = selecionar_entidade(Fazenda, "Selecione a fazenda (0 para voltar): ")
    if not fazenda:
        return
    
    insumo = selecionar_entidade(Insumo, "Selecione o insumo (0 para voltar): ")
    if not insumo:
        return
    
    relatorio = Relatorio.gerar_relatorio_insumo(fazenda, insumo)
    
    print("\n--- Relatório de Insumos ---")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")

def menu_relatorio():
    while True:
        print("\n--- Menu de Relatórios ---")
        print("1) Relatório de Fazendas")
        print("2) Relatório de Maquinários")
        print("3) Relatório de Insumos")
        print()
        print("0) Voltar para o menu principal")
        
        escolha = input("Escolha uma opção: ")
        
        match escolha:
            case '0':
                return
            case '1':
                menu_relatorio_fazenda()
            case '2':
                menu_relatorio_maquinario()
            case '3':
                menu_relatorio_insumo()
            case _:
                print("Opção inválida!")