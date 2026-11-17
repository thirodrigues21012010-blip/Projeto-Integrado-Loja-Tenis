"""Comandos explícitos de carga inicial e criação de contas internas."""
import argparse, json, getpass
from pathlib import Path
from dotenv import load_dotenv
from backend.database import Database
from backend.dao import UsuarioDAO, CatalogoDAO
from backend.models import Modelo, Coloracao, Variante
load_dotenv()
p=argparse.ArgumentParser(); p.add_argument('acao',choices=['catalogo','conta']); args=p.parse_args()
db=Database()
if args.acao=='conta':
    nome=input('Nome: ').strip(); cpf=input('CPF (11 dígitos, use fictício na demonstração): ').strip()
    email=input('E-mail: ').strip().lower(); perfil=input('Perfil (FUNCIONARIO ou GERENTE): ').strip().upper()
    senha=getpass.getpass('Senha (mínimo 8 caracteres): ')
    if perfil not in ('FUNCIONARIO','GERENTE') or len(senha)<8 or len(cpf)!=11 or not cpf.isdigit() or '@' not in email or not nome:
        raise SystemExit('Dados inválidos; nenhuma conta criada.')
    UsuarioDAO(db).cadastrar(nome,cpf,email,'',senha,perfil)
    print('Conta criada.')
else:
    catalog=CatalogoDAO(db)
    if catalog.listar(): raise SystemExit('Catálogo já contém dados; carga cancelada para evitar duplicação.')
    products=json.loads((Path(__file__).parent/'dados/catalogo_inicial.json').read_text(encoding='utf-8'))
    # Toda a carga usa uma transação: falhas não deixam um catálogo parcial.
    with db.transaction() as c:
        for item in products:
            c.execute('INSERT INTO MODELO (nome,marca,descricao) VALUES (%s,%s,%s)',(item['name'],item['brand'],item['model']))
            mid=c.lastrowid
            c.execute('INSERT INTO COLORACAO (id_modelo,cor,preco) VALUES (%s,%s,%s)',(mid,item['color'],item['price'] if item['price'] is not None else 0))
            cid=c.lastrowid
            c.execute('INSERT INTO FOTO (id_coloracao,url) VALUES (%s,%s)',(cid,item['image']))
            for size in ('38','39','40','41','42'):
                c.execute('INSERT INTO VARIANTE (id_coloracao,tamanho,quantidade_estoque) VALUES (%s,%s,%s)',(cid,size,3 if item['price'] is not None else 0))
    print('Catálogo demonstrativo importado.')
