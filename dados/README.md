# Dataset LEN-Small

O projeto usa o [Large Engagement Networks (LEN)](https://github.com/erdemUB/LEN),
dataset público de redes de engajamento do Twitter. A página dos autores também
oferece a descrição e os arquivos para download:
<https://erdemub.github.io/large-engagement-network/>.

Cada JSON representa um tópico. Os nós são usuários, as arestas são interações
direcionadas (como retuítes, respostas e citações) e o campo `campaign` indica
a classe usada na análise.

## Recorte utilizado

O pacote local tem 104 arquivos. Depois da retirada de uma duplicata exata,
restam 103 grafos: 52 campanhas e 51 não campanhas. O artigo do LEN-Small
descreve 100 grafos, portanto a amostra definitiva ainda será conferida.

Os arquivos brutos ocupam cerca de 5,4 GB e não são versionados. As tabelas
usadas no projeto ficam em `dados/processados/`:

- `len_small_summary.csv`: resumo de cada grafo;
- `partial_graph_features.csv`: características dos grafos parciais;
- `len_small_exclusions.csv`: registro da duplicata retirada.

## Referência

GOPALAKRISHNAN, A. A.; HOSSAIN, J.; ELMAS, T.; SARIYÜCE, A. E. Large
Engagement Networks for Classifying Coordinated Campaigns and Organic Twitter
Trends. *Proceedings of the International AAAI Conference on Web and Social
Media*, v. 19, n. 1, p. 688–702, 2025. DOI:
<https://doi.org/10.1609/icwsm.v19i1.35839>.
