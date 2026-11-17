"""Testes de integração com SQLite como adaptador de teste, nunca como banco da aplicação."""
import sqlite3, re
from decimal import Decimal
sqlite3.register_adapter(Decimal, str)
from contextlib import contextmanager
from pathlib import Path
import pytest
from app import create_app
from backend.dao import UsuarioDAO

class Cursor:
    def __init__(self,c): self.c=c
    def execute(self,sql,args=()): self.c.execute(sql.replace('%s','?'),args); return self
    @property
    def lastrowid(self): return self.c.lastrowid
    def fetchone(self):
        r=self.c.fetchone(); return dict(r) if r else None
    def fetchall(self): return [dict(r) for r in self.c.fetchall()]
class TestDatabase:
    __test__=False
    def __init__(self):
        self.conn=sqlite3.connect(':memory:'); self.conn.row_factory=sqlite3.Row
        sql=(Path(__file__).parents[1]/'banco_de_dados/Modelo_Fisico_Projeto_Integrado.sql').read_text()
        sql=re.sub(r'--[^\n]*','',sql)
        sql=re.sub(r'SET NAMES.*?;|CREATE DATABASE.*?;|USE projeto_integrado;', '',sql,flags=re.S)
        sql=re.sub(r'INT UNSIGNED NOT NULL AUTO_INCREMENT','INTEGER PRIMARY KEY AUTOINCREMENT',sql)
        sql=re.sub(r',\s*CONSTRAINT pk_\w+ PRIMARY KEY \(id_\w+\)','',sql)
        sql=re.sub(r'INDEX idx_item_variante \(id_variante\),','',sql)
        sql=sql.replace(' ENGINE=InnoDB','')
        self.conn.execute('PRAGMA foreign_keys=ON'); self.conn.executescript(sql)
    @contextmanager
    def transaction(self):
        try: yield Cursor(self.conn.cursor()); self.conn.commit()
        except Exception: self.conn.rollback(); raise

@pytest.fixture
def setup():
    db=TestDatabase();app=create_app(db);app.config['TESTING']=True
    return db,app,app.test_client()
def token(c): return {'X-CSRF-Token':c.get('/api/sessao').json['csrf']}
def register(c,h,n='1'):
    return c.post('/api/cadastro',headers=h,json=dict(nome_completo='Aluno',cpf=n*11,email=n+'@teste.local',senha='Teste1234',telefone=''))
def test_contas_csrf_e_isolamento(setup):
    db,app,c=setup;h=token(c)
    assert c.post('/api/cadastro',json={}).status_code==403
    assert register(c,h).status_code==201
    assert c.get('/api/sessao').json['usuario']['perfil']=='CLIENTE'
    assert c.post('/api/produtos',headers=h,json={}).status_code==403
    assert c.put('/api/estoque/1',headers=h,json={}).status_code==403
    assert c.get('/.env').status_code==404
    assert c.get('/app.py').status_code==404
    c.post('/api/logout',headers=h)
    assert c.get('/api/lista').status_code==401
    h=token(c)
    assert c.post('/api/login',headers=h,json={'email':'1@teste.local','senha':'errada'}).status_code==401
    assert c.post('/api/login',headers=h,json={'email':'1@teste.local','senha':'Teste1234'}).status_code==200
    row=UsuarioDAO(db).buscar('email','1@teste.local')
    assert row['senha_hash']!='Teste1234'
def test_catalogo_lista_estoque(setup):
    db,app,c=setup
    UsuarioDAO(db).cadastrar('Gerente','12345678901','g@teste.local','','Teste1234','GERENTE')
    h=token(c);c.post('/api/login',headers=h,json={'email':'g@teste.local','senha':'Teste1234'})
    item=dict(nome='Tênis',marca='Nike',descricao='Linha',cor='Preto',preco='100.50',foto='assets/product-0.webp',tamanho='40',quantidade=3)
    assert c.post('/api/produtos',headers=h,json=item).status_code==201
    produto=c.get('/api/produtos').json[0];cid=produto['id'];vid=produto['variantes'][0]['id_variante']
    assert c.post('/api/lista/'+str(vid),headers=h).status_code==200
    assert c.post('/api/lista/'+str(vid),headers=h).status_code==200
    assert len(c.get('/api/lista').json)==1
    assert c.get('/api/produtos').json[0]['variantes'][0]['quantidade_estoque']==3
    other=app.test_client();oh=token(other);assert register(other,oh,'2').status_code==201
    assert other.get('/api/lista').json==[]
    assert c.put('/api/estoque/'+str(cid),headers=h,json={'tamanho':'40','quantidade':-1}).status_code==400
    assert c.put('/api/estoque/'+str(cid),headers=h,json={'tamanho':'41','quantidade':0}).status_code==200
    assert len(c.get('/api/produtos').json[0]['variantes'])==2
    item.update(id_modelo=produto['id_modelo'],cor='Branco')
    assert c.post('/api/produtos',headers=h,json=item).status_code==201
    assert c.get('/api/produtos').json[1]['id_modelo']==produto['id_modelo']
    assert c.delete('/api/lista/'+str(vid),headers=h).status_code==200
    assert c.get('/api/lista').json==[]
    UsuarioDAO(db).cadastrar('Funcionário','33333333333','f@teste.local','','Teste1234','FUNCIONARIO')
    f=app.test_client();fh=token(f);f.post('/api/login',headers=fh,json={'email':'f@teste.local','senha':'Teste1234'})
    assert f.post('/api/produtos',headers=fh,json=item).status_code==403
    assert f.put('/api/estoque/'+str(cid),headers=fh,json={'tamanho':'40','quantidade':8}).status_code==200
