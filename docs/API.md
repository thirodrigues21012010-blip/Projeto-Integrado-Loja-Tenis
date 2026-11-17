# API

Base `/api`. Respostas JSON. Solicite `GET /sessao` e use o campo `csrf` no cabeçalho `X-CSRF-Token` em todas as mutações. Cookies mantêm a sessão na mesma origem.

| Método | Rota | Acesso | Dados |
|---|---|---|---|
| GET | /sessao | Público | Usuário público e token |
| POST | /cadastro | Público | nome_completo, cpf, email, telefone, senha |
| POST | /login | Público | email, senha |
| POST | /logout | Público | Limpa sessão |
| GET | /produtos | Público | Cores, modelos, fotos, variantes e estoque |
| POST | /produtos | Gerente | nome, marca, descricao, cor, preco, foto, tamanho, quantidade; id_modelo opcional |
| PUT | /estoque/id_coloracao | Funcionário ou gerente | tamanho, quantidade |
| GET | /lista | Autenticado | Itens da própria conta |
| POST | /lista/id_variante | Autenticado | Adiciona sem duplicar |
| DELETE | /lista/id_variante | Autenticado | Remove apenas da própria lista |

Erros: 400 validação, 401 login necessário, 403 permissão/CSRF, 409 integridade MySQL, 503 conexão indisponível. Ao selecionar um modelo existente, o formulário preenche nome/marca automaticamente e os mantém somente para leitura. Esses campos não alteram o modelo selecionado.
