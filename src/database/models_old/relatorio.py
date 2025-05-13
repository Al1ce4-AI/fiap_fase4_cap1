from typing import Dict, Any
from src.database.models.fazenda import Fazenda
from src.database.models.maquinario import Maquinario
from src.database.models.insumo import Insumo

class Relatorio:
    
    @staticmethod
    def gerar_relatorio_fazenda(fazenda: Fazenda) -> Dict[str, Any]:
        return {
            'Nome': fazenda.nome,
            'Tipo de Cultura': fazenda.tipo.value,
            'Formato': fazenda.formato.value,
            'Base (m)': fazenda.base,
            'Altura (m)': fazenda.altura,
            'Área (m²)': fazenda.area()
        }
    
    @staticmethod
    def gerar_relatorio_maquinario(fazenda: Fazenda, maquinario: Maquinario) -> Dict[str, Any]:
        try:
            rota = maquinario.calcular_rota(fazenda)
            
            distancia_metros = maquinario.calcular_distancia(rota)
        
            distancia_km = distancia_metros / 1000
            
            consumo_litros = maquinario.calcular_consumo(distancia_km, maquinario.consumo)
            
            velocidade_media = maquinario.valocidademax * 0.7
            tempo_horas = distancia_km / velocidade_media
            tempo_formatado = f"{int(tempo_horas)}h {int((tempo_horas % 1) * 60)}min"
            
            maquinario.desenhar_rota(rota, titulo=f"Rota {maquinario.nome} - {fazenda.nome}")
            
            return {
                'Fazenda': fazenda.nome,
                'Maquinário': maquinario.nome,
                'Área da fazenda (m²)': fazenda.area(),
                'Formato da fazenda': fazenda.formato.name,
                'Largura do equipamento (m)': maquinario.largura,
                'Velocidade máxima (km/h)': maquinario.valocidademax,
                'Distância total (km)': round(distancia_km, 2),
                'Eficiência (km/l)': maquinario.consumo,
                'Consumo estimado (litros)': round(consumo_litros, 2),
                'Tempo estimado': tempo_formatado,
                'Número de voltas': len(rota)//2,
                'Rota gerada': f"Ver arquivo Rota_{maquinario.nome}_{fazenda.nome}_*.png"
            }
        
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar relatório: {str(e)}")
    
    @staticmethod
    def gerar_relatorio_insumo(fazenda: Fazenda, insumo: Insumo) -> Dict[str, Any]:
        try:
            area_hectares = fazenda.area() / 10000
            
            unidade = insumo.unidade.value.lower()

            consumo_total_base = area_hectares * insumo.consumo
            
            fator_conversao = Relatorio._get_fator_conversao(unidade)
            consumo_total_unidade = consumo_total_base / fator_conversao
            
            custo_total = consumo_total_unidade * insumo.custo
            
            simbolo_unidade = Relatorio._get_simbolo_unidade(unidade)
            
            return {
                'Fazenda': fazenda.nome,
                'Insumo': insumo.nome,
                'Tipo de Cultura': insumo.tipo.value,
                'Área total (hectares)': round(area_hectares, 2),
                'Unidade de medida': simbolo_unidade,
                'Consumo por hectare': f"{insumo.consumo} {simbolo_unidade}/ha",
                'Consumo total estimado': round(consumo_total_unidade, 2),
                'Custo por unidade': f"R${insumo.custo}/{simbolo_unidade}",
                'Custo total estimado': f"R${round(custo_total, 2)}",
                'Detalhes': f"Equivalente a {round(consumo_total_base, 2)} {Relatorio._get_unidade_base(unidade)}"
            }
            
        except AttributeError as e:
            raise AttributeError(f"Erro no relatório: {str(e)}")

    @staticmethod
    def _get_fator_conversao(unidade: str) -> float:
        return {
            't': 0.001,
            'kg': 1,
            'g': 1000, 
            'l': 1, 
            'ml': 1000      
        }.get(unidade, 1)    

    @staticmethod
    def _get_unidade_base(unidade: str) -> str:
        return 'kg' if unidade in ['t', 'kg', 'g'] else 'L'

    @staticmethod
    def _get_simbolo_unidade(unidade: str) -> str:
        return {
            't': 'ton',
            'kg': 'kg',
            'g': 'g',
            'l': 'L',
            'ml': 'ml'
        }.get(unidade, unidade)