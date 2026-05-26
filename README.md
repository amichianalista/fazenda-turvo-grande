# Automacao Pecuaria

App em Streamlit para apresentar, de forma visual e simples, os dados atuais da
Fazenda Turvo Grande sobre producao e venda de Queijo Minas Artesanal.

## Estado atual

Hoje o projeto tem uma unica tela:

- `Pagina 1 | Visao Geral`

Essa pagina mostra tres blocos principais:

- identidade e contexto da fazenda
- producao
- comercial

## Fonte de dados

A leitura sai direto da planilha original:

- `Referenciais Iniciais/planilha de gestao.ods`

Nao usamos mais CSV intermediario.

## Como rodar

1. Ative o ambiente virtual:
   - PowerShell: `.\\.venv\\Scripts\\Activate.ps1`
2. Instale as dependencias:
   - `pip install -r requirements.txt`
3. Rode o app:
   - `streamlit run app.py`

## Estrutura principal

- `app.py`: redireciona direto para a pagina principal
- `pages/1_Visao_Geral.py`: tela atual do projeto
- `app_core/data.py`: leitura da planilha `.ods`
- `app_core/components.py`: tema e componentes visuais
- `assets/`: imagens e materiais visuais
