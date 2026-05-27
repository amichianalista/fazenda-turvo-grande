# Automacao Pecuaria

App em Streamlit para apresentar a operacao da Fazenda Turvo Grande com leitura
executiva, contexto de mercado e prontidao financeira para o negocio de Queijo
Minas Artesanal.

## Estado atual

Hoje o projeto foi reiniciado.

Neste momento, a base nova contem:

- `Pagina 1 | Visao Atual do Negocio`
- leitura direta da planilha `.ods`
- tema visual novo com background dedicado
- cards, KPIs e graficos com copy voltada ao produtor rural

As paginas antigas foram removidas do fluxo atual e a reconstrucao esta sendo feita
por etapas, comecando pela primeira pagina.

## Fonte de dados

A leitura operacional sai direto da planilha original:

- `Referenciais Iniciais/planilha de gestao.ods`

O contexto estrategico e visual usa tambem:

- `Referenciais Iniciais/queijo_turvo_grande.pdf`
- `assets/background.png`
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
- `pages/1_Visao_Executiva.py`: primeira pagina reconstruida, com leitura executiva atual
- `app_core/data.py`: leitura da planilha `.ods`
- `app_core/components.py`: tema e componentes visuais
- `assets/`: imagens e materiais visuais
- `Referenciais Iniciais/levantamento_pagina1_visao_atual_negocio.md`: levantamento da base para a nova pagina 1
