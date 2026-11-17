# Hype. — Projeto Integrado | Entrega final

Thiago Rodrigues, Vinicius Pansonato e Guilherme Ronaldo — 2 TI B.

Vitrine de tênis com Python/POO, DAOs, Flask, MySQL/MariaDB no XAMPP e interface HTML/CSS/JavaScript integrada por Fetch. Sem checkout, pagamento ou reserva de estoque.

## Executar no Windows / VS Code

1. Extraia o ZIP. Abra a pasta que contém `app.py` no VS Code.
2. Instale Python 3.11 ou superior e inicie **MySQL** no painel XAMPP. Apache só é necessário se você usar o phpMyAdmin.
3. No phpMyAdmin, importe `banco_de_dados/Modelo_Fisico_Projeto_Integrado.sql` **somente em banco novo**. Não reimporte sobre suas tabelas existentes. O script original foi preservado e não apaga tabelas. Se já tem o banco, confira nomes e estrutura antes de continuar.
4. Abra o terminal PowerShell na pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

5. Edite `.env`: nome do banco, porta, usuário, senha e uma chave secreta própria. O padrão é `projeto_integrado`, porta 3306, usuário root e senha vazia; confirme os valores do seu XAMPP. Para gerar a chave: `.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"`.
6. Em catálogo vazio, carregue os dados de demonstração:

```powershell
.\.venv\Scripts\python.exe gerenciar.py catalogo
```

7. Crie uma conta interna para demonstrar a administração:

```powershell
.\.venv\Scripts\python.exe gerenciar.py conta
```

Escolha GERENTE ou FUNCIONARIO. Não existem senhas administrativas fixas. O cadastro na página sempre cria CLIENTE.

8. Inicie a aplicação:

```powershell
.\.venv\Scripts\python.exe app.py
```

9. Acesse **http://127.0.0.1:5000**. Use essa URL para todas as funções. Abrir o HTML diretamente ou usar Live Server não conecta a interface à API.

No Linux/macOS, substitua `.\.venv\Scripts\python.exe` por `.venv/bin/python` e `Copy-Item` por `cp`.

## Funcionalidades

- Catálogo, pesquisa, marcas, carrossel de 5 segundos, detalhes e seleção de coloração/tamanho.
- Cadastro, login e logout com hash de senha e sessão HTTP; proteção CSRF.
- Lista persistente por usuário e variante. Inclusão repetida não duplica itens e não altera estoque. É permitido salvar item esgotado.
- Funcionário e gerente adicionam tamanhos e atualizam quantidades.
- Gerente cadastra modelo com cor, foto e tamanho inicial na mesma transação; também adiciona cores a um modelo existente.
- Fotos usam caminhos de arquivos em `frontend/assets/` ou URLs HTTPS. Para incluir imagem local, copie o arquivo para essa pasta e informe `assets/nome.webp`.

## Organização

`app.py`: rotas e validações. `backend/models.py`: entidades POO. `backend/dao.py`: persistência. `backend/database.py`: conexão/transações. `frontend/`: interface e imagens. `dados/`: fonte da carga inicial, não consultada pelo navegador. `banco_de_dados/`: SQL e modelos originais. `docs/`: alterações, UML em PDF (`UML.pdf`) e fonte Mermaid (`UML.md`), API e validação.

## Dados demonstrativos e limites

O catálogo preserva os nomes, imagens e preços de referência do arquivo recebido. Tamanhos 38–42 e quantidades são fictícios (3 por tamanho); produtos originalmente sem preço recebem preço 0 e estoque 0, com a legenda “Consulte a loja”. Esses valores não representam estoque real. A carga é cancelada se o catálogo já tiver registros.

O CPF é validado por formato de 11 dígitos, sem cálculo dos dígitos verificadores. Use dados fictícios na apresentação. O sistema é destinado à execução local acadêmica; não foi preparado para publicação pública. Não inclua `.env` ou dados pessoais em commits.

## Verificação

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest -q
```

Os testes usam adaptador SQLite em memória para exercitar rotas e DAOs; a aplicação entregue usa exclusivamente MySQL. Veja `docs/VALIDACAO.md` para o teste obrigatório no seu XAMPP.

Esta é a versão final do Projeto Integrado, com banco de dados, back-end Flask, front-end integrado por Fetch e diagrama UML em PDF. O convite ao professor deve ser conferido nas configurações do repositório. O histórico de commits registra as alterações reais do projeto.
