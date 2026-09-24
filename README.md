# Classificação Precoce de Campanhas Coordenadas em Redes Sociais com Características de Grafos Parciais

Projeto da disciplina de Inteligência Artificial da turma 7N, desenvolvido a
partir do TCC sobre detecção precoce de campanhas coordenadas em redes sociais.

## Integrantes

- Gabriel de Santana Santos - RA 10420595 - 10420595@mackenzista.com.br
- Gabriel Erick Mendes - RA 10420391 - 10420391@mackenzista.com.br
- Matheus Teles Magalhães - RA 10427410 - 10427410@mackenzista.com.br

## Entrega do primeiro bimestre

- `artigo/artigo_parcial.pdf`: artigo parcial no formato da SBC.
- `rubrica/rubrica_analitica_n1.docx`: rubrica analítica preenchida.
- `notebooks/`: análises exploratórias inicial e aprofundada.
- `src/len_eda/`: leitura dos grafos, criação dos estados parciais e extração
  de características.
- `dados/`: descrição do LEN-small e tabelas processadas usadas nas análises.
- `tests/`: testes automatizados do código da análise.

## Como reproduzir a análise

O conjunto bruto LEN-small não é incluído no GitHub porque ocupa cerca de
5,4 GB. As instruções de obtenção e a descrição dos dados estão em
[`dados/README.md`](dados/README.md). Com os JSONs em `small_encoder_final/`:

```bash
python -m pip install -e ".[dev,notebook]"
pytest

len-summary \
  --data-dir small_encoder_final \
  --output dados/processados/len_small_summary.csv

len-features \
  --data-dir small_encoder_final \
  --exclusions config/len_small_exclusions.csv \
  --output dados/processados/partial_graph_features.csv
```

Depois, execute os notebooks na ordem numérica. A divisão definitiva entre
treino, validação e teste ainda não foi congelada, pois o pacote local possui
103 grafos únicos e o artigo do LEN descreve 100 no subconjunto LEN-small.
