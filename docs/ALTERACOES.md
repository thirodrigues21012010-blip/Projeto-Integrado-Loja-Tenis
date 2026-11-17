# Registro da reestruturação

Base: ZIP recebido, commit de origem 5089af6a2ae210cd5cb79aa9c714dea44acb6b62.

| Parte | Alteração e motivo |
|---|---|
| Banco | Preservadas as sete tabelas e os diagramas originais; conexão usa nomes em maiúsculas exatamente como no SQL, inclusive em Linux. |
| POO | Entidades Usuario, Modelo, Coloracao e Variante; classes Database, UsuarioDAO, CatalogoDAO e ListaDAO. |
| Persistência | SQL parametrizado e transações com rollback. Usuário/lista e modelo/cor/foto/tamanho são cadastrados juntos. |
| Flask | Rotas de sessão, cadastro, login, logout, catálogo, estoque e lista. Flask também entrega os arquivos do front-end. |
| Contas | Cadastro público sempre CLIENTE; contas internas criadas explicitamente pelo terminal; senha com hash Werkzeug. |
| Permissões | Aplicadas no servidor, além de ocultar ações incompatíveis na interface. |
| Fetch | Substituídos catálogo fixo e localStorage por chamadas à API e persistência por conta. |
| Interface | Preservados CSS original, imagens, banners, setas e intervalo de 5 segundos; adicionados diálogos de conta, detalhes e gerenciamento. Catálogo inicia mostrando quatro itens, com opção de expandir. |
| Produtos | Cartão abre detalhes locais; escolha de cor e tamanho. Link externo deixou de ser a ação principal. |
| Lista | Usa id da variante, separada por usuário, sem movimentação de estoque. |
| Dados | products.json movido para dados/catalogo_inicial.json; catalog-data.js removido. Arquivo JSON passa a servir apenas à importação inicial. |
| Demonstração | Importação explícita e transacional; preço ausente passa a 0, sem estoque; tamanhos/quantidades fictícios documentados. |
| Documentação | README de instalação, UML em Mermaid, mapa da API e roteiro de validação. |
| Configuração | requirements.txt, .env.example, .gitignore e execução local sem debug. |

A administração implementa as ações do escopo: cadastrar modelos/cores/fotos e atualizar/adicionar tamanhos e estoque. Exclusão de catálogo e edição geral de descrições/preços não foram incluídas. As fotos são cadastradas por caminho ou URL; não há upload via formulário.

A distribuição de produtos na grade agora segue a ordem do banco, em vez da intercalação fixa anterior por marca. Busca e filtro permanecem locais após buscar o catálogo pela API. O visual não foi validado por comparação de screenshots; confira a responsividade no navegador.

## Revisão de 17/11/2026 — somente três ajustes

1. Botões de conta herdam a cor clara do cabeçalho.
2. Gerenciamento começa desabilitado e é liberado após o catálogo carregar; permanece bloqueado se houver falha. A abertura do diálogo e o envio de estoque também validam esse estado e a seleção de coloração.
3. Ao selecionar modelo existente, nome e marca são preenchidos automaticamente e ficam somente para leitura. Ao retornar a novo modelo ou concluir cadastro, os campos voltam a ficar editáveis.

Nenhuma alteração no back-end, nas tabelas, nos dados iniciais ou nos banners nesta revisão. Os testes e seus limites estão registrados em VALIDACAO.md.

## UML em PDF

Incluído docs/UML.pdf com o diagrama de oito classes, atributos, métodos e relacionamentos do UML.md, em uma página A3 horizontal. Fonte Mermaid preservada. PDF renderizado para inspeção e texto das oito classes conferido. Código-fonte da aplicação inalterado nesta atualização.
