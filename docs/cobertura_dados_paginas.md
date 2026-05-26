# Cobertura de dados das paginas

Fonte analisada: `Referenciais Iniciais/planilha de gestao.ods`

CSV gerado:
- `data/planilha_gestao.csv`

## Resumo executivo

A planilha atual cobre bem o basico de producao e parte da receita.
Ela ainda nao cobre os dados necessarios para fechar o painel financeiro,
o painel de custos e boa parte do diagnostico inteligente.

## Pagina 1 - Producao

Campo | Situacao | Evidencia
--- | --- | ---
Queijos/dia | Temos | `22 queijos/dia`
Kg/mes | Temos | `616,0 kg/mes`
Evolucao da producao | Nao temos | nao existe serie historica por dia, semana ou mes
Capacidade produtiva | Nao temos | nao existe limite de capacidade instalada ou meta operacional

Conclusao:
- A pagina 1 pode nascer parcialmente preenchida.
- Ja conseguimos mostrar snapshot atual de producao.
- Ainda faltam dados historicos e capacidade para uma leitura executiva completa.

## Pagina 2 - Financeiro

Campo | Situacao | Evidencia
--- | --- | ---
Receita bruta | Temos | `R$ 21.560,00`
Custos | Nao temos | os campos de custo estao vazios e o resumo esta em `R$ 0,00`
Lucro liquido | Nao temos | depende dos custos preenchidos
Margem | Nao temos | depende de receita e custos reais

Conclusao:
- A pagina 2 nao fecha com confianca ainda.
- So a receita bruta mensal pode ser exibida agora.

## Pagina 3 - Custos

Campo | Situacao | Evidencia
--- | --- | ---
Grafico pizza dos custos | Nao temos | categorias existem, mas sem valores
Custos conhecidos vs desconhecidos | Parcial | temos a lista de categorias, mas nao a divisao financeira real
Alertas de custo alto | Nao temos | faltam valores e comparativos

Categorias conhecidas mapeadas:
- Sal e coalho
- Embalagem e rotulo
- Mao de obra
- Frete para a cooperativa

Categorias ainda a descobrir:
- Energia eletrica
- Alimentacao do gado
- Manutencao de equipamentos
- Veterinario e sanidade do rebanho
- Custo/contrato com a cooperativa ainda sem nome claro na planilha

Conclusao:
- A pagina 3 hoje so pode mostrar estrutura de custos, nao analise financeira real.

## Pagina 4 - Diagnostico Inteligente

Campo ou insight | Situacao | Motivo
--- | --- | ---
`Frete representa 18% do custo total` | Nao temos | frete nao tem valor preenchido
`Margem abaixo do ideal` | Nao temos | margem nao pode ser calculada
`Producao alta, mas preco baixo` | Parcial | temos preco atual, mas nao temos benchmark ou serie historica
`Custo energetico ainda nao mapeado` | Temos | energia aparece explicitamente como custo a descobrir

Conclusao:
- O diagnostico inteligente ainda nao pode ser totalmente baseado em dado real.
- Por enquanto, so conseguimos diagnosticos de preenchimento e cobertura de custos.

## O que falta para deixar todas as paginas preenchiveis

- Serie historica de producao por periodo
- Capacidade produtiva atual ou meta mensal
- Valores mensais de sal e coalho
- Valores mensais de embalagem e rotulo
- Valores mensais de mao de obra
- Valores mensais de frete
- Valores mensais de energia
- Valores mensais de alimentacao do gado
- Valores mensais de manutencao
- Valores mensais de veterinario e sanidade
- Definicao do custo ligado ao contrato/cooperativa que aparece sem rotulo textual claro

## Leitura final

Hoje a fonte esta pronta para sustentar:
- cards de producao atual
- peso medio por queijo
- preco pago pela cooperativa
- receita bruta estimada do mes
- mapa de quais custos existem e quais ainda faltam

Hoje a fonte ainda nao sustenta com seguranca:
- evolucao de producao
- capacidade produtiva
- painel financeiro completo
- grafico real de custos
- lucro liquido
- margem
- diagnosticos percentuais de custo
