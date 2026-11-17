# Validação

Verificações automáticas: compilação Python, sintaxe JavaScript e testes de integração de rotas/DAOs com adaptador SQLite em memória. Os testes cobrem hash de senha, cadastro/login/logout, CSRF, permissões, isolamento de listas, não duplicação, estoque inalterado ao salvar, tamanho novo, nova cor e rejeição de estoque negativo.

Na revisão de 17/11/2026, o SQL e a carga de 27 produtos foram executados em MariaDB 11.8.6 real. Foram verificados cadastro, duplicidade, login/logout, permissões, lista sem duplicação e estoque inalterado ao salvar. A configuração específica do XAMPP do usuário ainda exige conferência local.

A interface foi exercitada em Chromium headless com eventos DOM e requisições reais ao Flask/MariaDB. Não foi realizada comparação visual por screenshots nem validação completa de cliques físicos.

## Roteiro no XAMPP

1. Importe o SQL em banco novo; execute carga e criação de gerente conforme README.
2. Abra o site pelo Flask; confira catálogo, busca, todas as marcas e três banners (5 segundos e setas).
3. Cadastre um cliente, abra um produto, escolha tamanho e salve. Recarregue, saia e entre novamente: a lista deve permanecer.
4. Entre com outro cliente: a lista deve estar separada. Remova um item e confira no banco.
5. Compare VARIANTE antes/depois de salvar: estoque deve permanecer igual.
6. Como funcionário, adicione tamanho e altere quantidade; tente cadastrar produto pela API: deve retornar 403.
7. Como gerente, cadastre modelo/cor/foto/tamanho, depois outra cor no mesmo modelo; confira seleção de cores e tabelas no phpMyAdmin.
8. Confira erros com CPF/e-mail duplicado, senha incorreta e quantidade negativa.
9. Teste em janela estreita; confira botões, formulários e fechamento dos diálogos.
10. Pare MySQL e tente carregar catálogo: deve aparecer mensagem de banco indisponível.

## Entrega acadêmica

Publicar código completo no GitHub, conferir convite do professor leonardo.stephan@eaportal.org e demonstrar o fluxo acima. O ZIP não altera o repositório nem envia convites.

Resultado nesta entrega: 2 testes de integração aprovados, compilação Python e sintaxe JavaScript aprovadas.

## Resultado dos testes dos três ajustes (17/11/2026)

| Cenário | Resultado |
|---|---|
| Cor calculada dos botões Entrar, Gerenciar e Sair | Branco no cabeçalho escuro |
| Catálogo propositalmente atrasado | Gerenciar desabilitado; abertura e envio inválido impedidos |
| Catálogo com falha HTTP 503 simulada | Mensagem apresentada; gerenciamento permanece bloqueado |
| Modelo existente | Nome e marca preenchidos automaticamente, somente leitura |
| Cadastro de nova cor sem digitar nome/marca | HTTP 201 no MariaDB real |
| Voltar para novo modelo e reset após cadastro | Campos vazios e editáveis |
| Atualização de estoque pela interface | Quantidade 7 confirmada nos detalhes |
| Lista após recarregar | Item persistiu |
| Busca, setas e viewport de 390 px | Verificados; sem rolagem horizontal da página |
| Erros JavaScript e URLs com undefined | Nenhum detectado nos cenários executados |
| Testes automatizados existentes | 2 aprovados |
| Sintaxe Python e JavaScript | Aprovada |

Esses resultados cobrem os cenários descritos; não são garantia de ausência de todos os erros possíveis. Os arquivos de banco e back-end não foram alterados nesta revisão.
