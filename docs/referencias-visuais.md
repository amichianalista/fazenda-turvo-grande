# Referencias visuais para o app Streamlit

Data da pesquisa: 2026-05-26

## Contexto

O objetivo deste projeto e criar uma visualizacao em Streamlit para um produtor rural cliente.
O app precisa transmitir tres coisas ao mesmo tempo:

1. Confianca operacional
2. Clareza de tomada de decisao
3. Sensacao de produto premium, nao de painel generico

## Fontes pesquisadas

### 1. Globo Rural - Agtech

Link: https://globorural.globo.com/agtech/

Leituras principais:
- Forte organizacao editorial por blocos tematicos
- Mistura de conteudo tecnico com sensacao de atualidade
- Uso recorrente de imagens grandes e manchetes curtas
- Presenca clara de secoes como tecnologia, credito, clima e pecuaria

Aplicacao no nosso app:
- Home com blocos bem definidos por tema de decisao
- Cards de alto impacto visual com mensagem curta
- Mistura de indicadores e "insights do dia", sem parecer planilha

Base usada:
- A pagina lista secoes e imagens para temas como agtech, leite, credito e inovacao.
- Tambem destaca ferramentas como previsao do tempo e cotacoes.

Referencia web:
- https://globorural.globo.com/agtech/

### 2. Globo Rural - Futuro do Agro

Link: https://globorural.globo.com/especiais/futuro-do-agro/

Leituras principais:
- Narrativa visual mais aspiracional
- Destaque para sustentabilidade, credito verde e produtividade
- Sensacao de "setor moderno", nao apenas tradicional

Aplicacao no nosso app:
- Precisamos de um topo hero com discurso de futuro, eficiencia e gestao
- Visual deve parecer tecnologia aplicada ao campo
- Bons candidatos: fotos aereas, textura de solo, mapas, status de safra e destaque para sustentabilidade

Base usada:
- A pagina destaca temas como sustentabilidade no agro, agricultura tropical, credito verde e COP30.

Referencia web:
- https://globorural.globo.com/especiais/futuro-do-agro/

### 3. Ministerio da Agricultura e Pecuaria - Painel Zarc

Link:
https://www.gov.br/agricultura/pt-br/assuntos/noticias/novo-painel-do-zarc-moderniza-consulta-as-janelas-de-plantio-e-reforca-gestao-de-riscos-na-agricultura

Publicacao: 2026-02-05

Leituras principais:
- O proprio ministerio destaca interface mais moderna, navegacao mais intuitiva e maior velocidade de resposta
- O painel organiza filtros tecnicos antes da exibicao do mapa e da tabua de risco
- A proposta e reduzir tempo de busca e melhorar a compreensao dos dados

Aplicacao no nosso app:
- Filtros devem ficar no topo e ser extremamente objetivos
- Cada tela precisa responder rapido a uma pergunta pratica do produtor
- Mapas, janelas, comparativos e risco precisam estar em primeira classe no layout

Trecho-chave sintetizado da fonte:
- O novo painel foi desenhado para facilitar consulta, acelerar leitura e deixar a organizacao visual mais clara para o planejamento agricola.

Referencia web:
- https://www.gov.br/agricultura/pt-br/assuntos/noticias/novo-painel-do-zarc-moderniza-consulta-as-janelas-de-plantio-e-reforca-gestao-de-riscos-na-agricultura

### 4. MAPA - Home institucional

Link: https://www.agricultura.gov.br/

Leituras principais:
- Uso de banners fortes com noticias e programas
- Comunicacao de escala nacional e impacto economico
- Mistura de institucionalidade com imagem de produtividade

Aplicacao no nosso app:
- Vale incorporar uma faixa inicial com 1 a 3 KPIs de impacto
- O tom visual pode combinar credibilidade institucional com design mais sofisticado

Referencia web:
- https://www.agricultura.gov.br/

### 5. Embrapa - Agro em Dados

Link: https://www.embrapa.br/agropensa/agro-em-dados

Leituras principais:
- Estrutura orientada por grandes categorias: agricultura, pecuaria, aquicultura, silvicultura, comercio exterior e agroindustria
- Forte associacao entre dados confiaveis e leitura setorial
- Boa logica para separar exploracao de informacao por cadeia ou tema

Aplicacao no nosso app:
- Organizar a navegacao principal por dominios do negocio do cliente
- Exemplo: rebanho, pastagem, custo, receita, clima, sanidade, produtividade
- O usuario nao deve "procurar", e sim bater o olho e encontrar a area certa

Referencia web:
- https://www.embrapa.br/agropensa/agro-em-dados

### 6. Embrapa - Agrivisum

Link: https://www.embrapa.br/en/agrivisum

Leituras principais:
- Uso de filtros geograficos e saidas em mapas e planilhas
- Posicionamento claro de sistema para analise e tomada de decisao
- Valor em combinar territorio, serie historica e comparacao

Aplicacao no nosso app:
- O projeto ganha muito se trouxer comparativos temporais e espaciais
- Mesmo que o cliente nao use mapas no dia 1, o layout deve comportar isso no futuro

Referencia web:
- https://www.embrapa.br/en/agrivisum

### 7. Embrapa - AgroTag

Link: https://www.agrotag.cnptia.embrapa.br/

Leituras principais:
- Narrativa de campo -> dado -> relatorio -> mapa
- Valor percebido sobe quando o sistema mostra fluxo operacional e nao apenas numero
- Uso de pilares simples: coleta, relatorio online e webgis

Aplicacao no nosso app:
- Nossa visualizacao deve contar uma historia operacional:
  coleta / registro -> leitura -> alerta -> decisao
- Isso ajuda o cliente a sentir que comprou uma ferramenta de gestao, nao apenas um dashboard

Referencia web:
- https://www.agrotag.cnptia.embrapa.br/

### 8. CNA - Panorama do Agro

Link: https://cnabrasil.org.br/cna/panorama-do-agro

Leituras principais:
- Uso de publicacoes recorrentes com identidade consistente
- Conteudo numerico acompanhado de narrativa
- Visual de "panorama executivo" e nao de tela excessivamente tecnica

Aplicacao no nosso app:
- Precisamos de secoes com leitura executiva:
  "o que melhorou", "o que preocupa", "onde agir"
- Cards de contexto funcionam melhor do que tabelas cruas na entrada

Dados recentes observados na pagina:
- Edicao 16 em 2026-05-22
- Edicao 15 em 2026-05-15
- Edicao 14 em 2026-05-08

Referencia web:
- https://cnabrasil.org.br/cna/panorama-do-agro

### 9. IBGE - Producao Agropecuaria

Link: https://www.ibge.gov.br/explica/producao-agropecuaria/se

Leituras principais:
- Interface orientada por ranking, mapa, serie historica e downloads
- Excelente referencia para combinar comparacao, geografia e historico em um mesmo produto
- Reforca a importancia de disponibilizar graficos e tabelas exportaveis

Aplicacao no nosso app:
- O painel ideal deve equilibrar:
  visao geral + historico + detalhe + exportacao
- O produtor precisa poder bater o olho e depois aprofundar, sem trocar de sistema

Referencia web:
- https://www.ibge.gov.br/explica/producao-agropecuaria/se

### 10. Conab - Portal de Informacoes Agropecuarias

Link: https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas

Leituras principais:
- Valor alto de mapas e visualizacoes por safra e cultura
- Forte foco em mapeamento agricola e monitoramento
- Boa referencia para telas com camadas visuais de territorio

Aplicacao no nosso app:
- Se existir dado georreferenciado ou por talhao/regiao, vale muito investir nisso
- Mesmo em Streamlit, um mapa bem usado pode virar a tela mais memoravel do projeto

Referencia web:
- https://portaldeinformacoes.conab.gov.br/mapeamentos-agricolas

## Sintese de direcao visual recomendada

### O que copiar da linguagem dessas referencias

- Hero forte com imagem ampla do campo, gado ou area produtiva
- KPIs grandes no topo, com poucos numeros e alto contraste
- Navegacao por temas de decisao, nao por tipo de grafico
- Mistura de mapas, serie historica, cards e alertas
- Linguagem de produto moderno do agro, nao de sistema burocratico

### O que evitar

- Cara de planilha exportada
- Tela branca demais com blocos pequenos
- Graficos padrao sem hierarquia visual
- Excesso de tabelas na home
- Paleta genrica de dashboard SaaS

## Direcao de design proposta para este cliente

### Conceito

"Centro de comando do produtor"

O app deve parecer uma cabine de decisao do negocio rural:
forte, claro, confiavel e valorizando o tamanho da operacao.

### Linguagem visual

- Base em verde profundo, areia, off-white e acentos em laranja queimado ou amarelo safra
- Tipografia com personalidade e leitura limpa
- Fotos aereas, textura de pasto, mapas e divisores com cara territorial
- Cards grandes com sombra suave e bordas discretas

### Estrutura sugerida da home

1. Hero com nome da fazenda ou operacao + mensagem executiva
2. Faixa de KPIs principais
3. Bloco de alertas e oportunidades
4. Bloco de desempenho historico
5. Bloco geografico ou operacional
6. Bloco final com insights acionaveis

## Proximo passo sugerido

Na proxima rodada, estruturar um wireframe inicial do app Streamlit com:
- capa de alto impacto
- menu lateral orientado por decisao
- paleta definida
- componentes base reutilizaveis
- placeholders para dados reais do cliente
