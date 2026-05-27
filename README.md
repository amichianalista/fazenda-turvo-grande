# Automacao Pecuaria

App em Streamlit para apresentar a operacao da Fazenda Turvo Grande com leitura
executiva, contexto de mercado e prontidao financeira para o negocio de Queijo
Minas Artesanal.

## Estado atual

Hoje o projeto esta organizado em quatro paginas:

- `Pagina 1 | Visao Executiva`
- `Pagina 2 | Operacao e Producao`
- `Pagina 3 | Mercado e Expansao`
- `Pagina 4 | Custos e Prontidao`

Cada pagina responde a uma frente de decisao diferente:

- panorama do negocio
- cadencia operacional e escala
- posicionamento, mercado e oportunidades
- maturidade da base de custos

## Fonte de dados

A leitura operacional sai direto da planilha original:

- `Referenciais Iniciais/planilha de gestao.ods`

O contexto estrategico e visual usa tambem:

- `Referenciais Iniciais/queijo_turvo_grande.pdf`
- `assets/queijopremiado.png`

Nao usamos CSV intermediario.

## Como rodar

1. Ative o ambiente virtual:
   - PowerShell: `.\\.venv\\Scripts\\Activate.ps1`
2. Instale as dependencias:
   - `pip install -r requirements.txt`
3. Rode o app:
   - `streamlit run app.py`

## Estrutura principal

- `app.py`: redireciona direto para a pagina principal
- `pages/1_Visao_Executiva.py`: panorama geral do negocio
- `pages/2_Operacao_e_Producao.py`: leitura operacional e escala
- `pages/3_Mercado_e_Expansao.py`: contexto de mercado, concorrencia e expansao
- `pages/4_Custos_e_Prontidao.py`: maturidade dos custos e proximos levantamentos
- `app_core/data.py`: leitura da planilha `.ods`
- `app_core/components.py`: tema e componentes visuais
- `assets/`: imagens e materiais visuais
