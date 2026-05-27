# Automacao Pecuaria

App em Streamlit para apresentar a Fazenda Turvo Grande com leitura visual,
executiva e simples de entender para o produtor rural.

## Estado atual

Hoje o projeto foi reiniciado.

Neste momento, a base nova contem:

- `Pagina 1 | Visao Atual do Negocio`
- leitura direta da planilha `.ods`
- tema visual novo com destaque forte para o `background.png`
- cards, KPIs e graficos com copy voltada ao produtor rural
- navegação simplificada para a primeira entrega

As paginas antigas foram removidas do fluxo atual e a reconstrucao esta sendo feita
por etapas, comecando pela primeira pagina.

## O que a Pagina 1 entrega hoje

A primeira pagina foi pensada como um retrato rapido do negocio, sem entrar ainda
na parte de custos.

Ela mostra:

- hero principal com visual central e copy simples
- KPIs de producao, escala fisica, preco e canal atual
- cards de leitura pratica do momento da fazenda
- grafico de ritmo da producao
- grafico de concentracao do canal de venda

Hoje a pagina 1 esta focada em:

- operacao atual
- receita bruta atual
- dependencia da cooperativa
- potencial de valorizacao do produto

Ela nao cobre neste momento:

- custos detalhados
- lucro liquido
- margem
- paginas 2, 3 e 4 reconstruidas

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

## Proximos passos

- reconstruir a `Pagina 2` com base em pesquisas academicas
- definir a nova abordagem para expansao, mercado e custos nas proximas paginas
- manter o visual valorizando o background e a identidade do projeto
