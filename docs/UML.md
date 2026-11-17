# Diagrama de classes

Versão pronta para leitura e impressão: [UML.pdf](UML.pdf).

O UML complementa os modelos de banco já existentes. Arquivo Markdown com Mermaid, visualizável no GitHub e em extensões Mermaid do VS Code.

```mermaid
classDiagram
class Usuario {
 +int id_usuario
 +str nome_completo
 +str email
 +str perfil
 +publico() dict
}
class Modelo {
 +str nome
 +str marca
 +str descricao
}
class Coloracao {
 +int id_modelo
 +str cor
 +float preco
}
class Variante {
 +int id_coloracao
 +str tamanho
 +int quantidade_estoque
}
class Database {
 +transaction()
}
class UsuarioDAO {
 +buscar(campo, valor)
 +cadastrar(nome, cpf, email, telefone, senha, perfil)
 +publico(row)
}
class CatalogoDAO {
 +listar()
 +cadastrar(modelo, coloracao, variante, foto, id_modelo)
 +estoque(cid, tamanho, quantidade)
}
class ListaDAO {
 +listar(uid)
 +alterar(uid, vid, remover)
}
Modelo "1" --> "1..*" Coloracao
Coloracao "1" --> "1..*" Variante
UsuarioDAO ..> Usuario
CatalogoDAO ..> Modelo
CatalogoDAO ..> Coloracao
CatalogoDAO ..> Variante
UsuarioDAO --> Database
CatalogoDAO --> Database
ListaDAO --> Database
ListaDAO ..> Usuario
ListaDAO ..> Variante
```

Fotos e lista são persistidas pelos DAOs; não têm entidades Python próprias. A API orquestra validações e autenticação em `create_app`. Os relacionamentos de domínio acima são mantidos por IDs e transações, não por coleções de objetos nas dataclasses.
