# Projeto Integrado — Loja de Tênis

**Aluno:** Thiago Rodrigues · **Turma:** 2 TI B

Este repositório registra o desenvolvimento do Projeto Integrado. A etapa de Banco de Dados reúne a modelagem do catálogo de tênis, usuários, estoque e listas de desejos.

## Banco de Dados

- [Modelo conceitual](banco_de_dados/Modelo_Conceitual_Projeto_Integrado.png)
- [Modelo conceitual no BR Modelo Web](https://app.brmodeloweb.com/conceptual/6af1a5ff3631bd9e55c10029)
- [Modelo lógico relacional](banco_de_dados/Modelo_Logico_Projeto_Integrado.png)
- [Modelo físico SQL](banco_de_dados/Modelo_Fisico_Projeto_Integrado.sql)

Os PNGs dos modelos conceitual e lógico são as mesmas imagens entregues ao professor pelo Google Classroom.

### Estrutura

| Tabela | Finalidade |
| --- | --- |
| USUARIO | Contas de clientes, funcionários e gerentes; CPF e e-mail únicos. |
| LISTA_DESEJOS | Lista persistente vinculada a um usuário, com no máximo uma lista por conta. |
| MODELO | Nome, marca e descrição do modelo de tênis. |
| COLORACAO | Cor e preço de um modelo, sem repetir a mesma cor no modelo. |
| VARIANTE | Tamanho e quantidade em estoque por coloração, sem repetir o tamanho na mesma coloração. |
| FOTO | URLs das fotos de cada coloração. |
| ITEM_LISTA_DESEJOS | Relação entre listas e variantes, com chave primária composta. |

### Regras implementadas

O script cria sete tabelas InnoDB, com chaves primárias e estrangeiras, restrições de unicidade e validações de perfil, preço e estoque não negativos. A inclusão de uma variante na lista de desejos não reserva nem reduz o estoque. Fotos pertencem à coloração; o preço é compartilhado pelos tamanhos dessa coloração.

As regras de participação mínima e as permissões por perfil estão documentadas no SQL para implementação nas transações do futuro back-end. Isso inclui criar a lista junto com o cliente e garantir que modelos e colorações tenham os registros dependentes obrigatórios. As senhas devem ser transformadas em hash pela aplicação antes de serem armazenadas.

### Importação no phpMyAdmin / XAMPP

1. Inicie o MySQL/MariaDB no XAMPP e abra o phpMyAdmin.
2. Na aba **Importar**, selecione `banco_de_dados/Modelo_Fisico_Projeto_Integrado.sql`.
3. Execute a importação uma única vez em um banco novo. O script cria e seleciona `projeto_integrado`.
4. Confira as sete tabelas criadas.

Requisitos: **MariaDB 10.2.1+** ou **MySQL 8.0.16+**, para aplicação das restrições `CHECK`. O script usa `utf8mb4` e cria somente a estrutura, sem dados pessoais ou dados de exemplo.

Em sistemas que diferenciam maiúsculas de minúsculas nos nomes de tabelas, use os nomes em maiúsculas definidos no script ao implementar as consultas do back-end.

### Estado da entrega

Modelo lógico e script físico produzidos; importação no phpMyAdmin realizada e estruturas conferidas durante a etapa de Banco de Dados. Este registro contém o trabalho de BD realizado até 09/11/2026. O front-end e o back-end são etapas posteriores.
