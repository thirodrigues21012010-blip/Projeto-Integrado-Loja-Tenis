import os, re, secrets
from pathlib import Path
from functools import wraps
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session, send_from_directory
import pymysql
from werkzeug.security import check_password_hash
from backend.database import Database
from backend.dao import UsuarioDAO, CatalogoDAO, ListaDAO
from backend.models import Modelo, Coloracao, Variante
load_dotenv()
ROOT=Path(__file__).parent

def create_app(db=None):
    app=Flask(__name__, static_folder=None)
    app.config.update(SECRET_KEY=os.getenv('SECRET_KEY') or secrets.token_hex(32),
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', MAX_CONTENT_LENGTH=65536)
    database=db or Database()
    users, catalog, lista=UsuarioDAO(database),CatalogoDAO(database),ListaDAO(database)
    def current():
        uid=session.get('uid')
        return users.buscar('id_usuario',uid) if uid else None
    def permit(*perfis):
        def deco(fn):
            @wraps(fn)
            def wrapped(*args,**kw):
                user=current()
                if not user: return jsonify(error='Entre na sua conta.'),401
                if perfis and user['perfil'] not in perfis: return jsonify(error='Acesso não autorizado.'),403
                return fn(*args,**kw)
            return wrapped
        return deco
    @app.before_request
    def csrf():
        if request.path.startswith('/api/') and request.method not in ('GET','HEAD','OPTIONS'):
            if not secrets.compare_digest(request.headers.get('X-CSRF-Token',''),session.get('csrf','!')):
                return jsonify(error='Sessão inválida. Recarregue a página.'),403
    def data():
        d=request.get_json(silent=True)
        if not isinstance(d,dict): raise ValueError('Envie um objeto JSON.')
        return d
    def text(d,k,limit=150):
        value=d.get(k,'')
        if not isinstance(value,str) or not value.strip() or len(value.strip())>limit:
            raise ValueError(f'Campo inválido: {k}')
        return value.strip()
    def integer(value):
        if isinstance(value,bool) or not re.fullmatch(r'\d{1,9}',str(value)): raise ValueError('Informe um inteiro não negativo.')
        return int(value)
    @app.errorhandler(ValueError)
    def invalid(e): return jsonify(error=str(e)),400
    @app.errorhandler(pymysql.err.IntegrityError)
    def conflict(e): return jsonify(error='Cadastro duplicado ou referência inexistente. Confira CPF, e-mail, cor e tamanho.'),409
    @app.errorhandler(pymysql.err.OperationalError)
    def unavailable(e):
        app.logger.error('Falha de conexão MySQL: %s',e)
        return jsonify(error='Banco indisponível. Inicie o MySQL no XAMPP e confira o arquivo .env.'),503
    @app.get('/api/sessao')
    def sessao():
        session.setdefault('csrf',secrets.token_hex(32))
        user=current()
        return jsonify(usuario=users.publico(user) if user else None,csrf=session['csrf'])
    @app.post('/api/cadastro')
    def cadastro():
        d=data(); nome=text(d,'nome_completo'); cpf=re.sub(r'\D','',text(d,'cpf',20)); email=text(d,'email',191).lower(); senha=text(d,'senha',128)
        if len(cpf)!=11 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email) or len(senha)<8:
            raise ValueError('Informe CPF com 11 dígitos, e-mail válido e senha com pelo menos 8 caracteres.')
        telefone=d.get('telefone','')
        if not isinstance(telefone,str) or len(telefone)>20: raise ValueError('Telefone inválido')
        uid=users.cadastrar(nome,cpf,email,telefone,senha)
        session['uid']=uid
        return jsonify(usuario=users.publico(users.buscar('id_usuario',uid))),201
    @app.post('/api/login')
    def login():
        d=data(); user=users.buscar('email',text(d,'email',191).lower())
        if not user or not check_password_hash(user['senha_hash'],text(d,'senha',128)):
            return jsonify(error='E-mail ou senha inválidos.'),401
        session['uid']=user['id_usuario']
        return jsonify(usuario=users.publico(user))
    @app.post('/api/logout')
    def logout():
        session.clear()
        return jsonify(ok=True)
    @app.get('/api/produtos')
    def produtos(): return jsonify(catalog.listar())
    @app.get('/api/lista')
    @permit()
    def favoritos(): return jsonify(lista.listar(session['uid']))
    @app.route('/api/lista/<int:vid>',methods=['POST','DELETE'])
    @permit()
    def favorito(vid):
        lista.alterar(session['uid'],vid,request.method=='DELETE')
        return jsonify(ok=True)
    @app.put('/api/estoque/<int:cid>')
    @permit('FUNCIONARIO','GERENTE')
    def estoque(cid):
        d=data(); catalog.estoque(cid,text(d,'tamanho',20),integer(d.get('quantidade')))
        return jsonify(ok=True)
    @app.post('/api/produtos')
    @permit('GERENTE')
    def novo():
        d=data()
        try: preco=Decimal(str(d.get('preco')))
        except InvalidOperation: raise ValueError('Preço inválido')
        if not preco.is_finite() or preco<0 or preco>Decimal('99999999.99') or preco.as_tuple().exponent < -2: raise ValueError('Preço inválido; use até duas casas decimais.')
        foto=text(d,'foto',2048)
        if not (foto.startswith('assets/') and '..' not in foto) and not foto.startswith('https://'):
            raise ValueError('Foto deve começar com assets/ ou https://')
        mid=integer(d['id_modelo']) if d.get('id_modelo') else None
        modelo=Modelo(text(d,'nome'),text(d,'marca',100),str(d.get('descricao',''))[:2000])
        cid=catalog.cadastrar(modelo,Coloracao(mid or 0,text(d,'cor',50),preco),Variante(0,text(d,'tamanho',20),integer(d.get('quantidade'))),foto,mid)
        return jsonify(id=cid),201
    @app.get('/')
    def index(): return send_from_directory(ROOT/'frontend','index.html')
    @app.get('/<path:path>')
    def static_file(path): return send_from_directory(ROOT/'frontend',path)
    return app

if __name__=='__main__':
    create_app().run(host='127.0.0.1',port=5000,debug=False)
