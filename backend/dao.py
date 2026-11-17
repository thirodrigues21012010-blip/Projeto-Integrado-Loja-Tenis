from werkzeug.security import generate_password_hash
from .models import Usuario, Modelo, Coloracao, Variante

class UsuarioDAO:
    def __init__(self, db): self.db = db
    def buscar(self, campo, valor):
        if campo not in ('email', 'id_usuario'): raise ValueError('Campo inválido')
        with self.db.transaction() as c:
            c.execute(f'SELECT * FROM USUARIO WHERE {campo}=%s', (valor,))
            return c.fetchone()
    def cadastrar(self, nome, cpf, email, telefone, senha, perfil='CLIENTE'):
        with self.db.transaction() as c:
            c.execute('INSERT INTO USUARIO (nome_completo,cpf,email,telefone,senha_hash,perfil) VALUES (%s,%s,%s,%s,%s,%s)',
                (nome,cpf,email,telefone,generate_password_hash(senha),perfil))
            uid = c.lastrowid
            c.execute('INSERT INTO LISTA_DESEJOS (id_usuario) VALUES (%s)', (uid,))
            return uid
    @staticmethod
    def publico(row):
        return Usuario(**{k:row[k] for k in ('id_usuario','nome_completo','email','perfil')}).publico()

class CatalogoDAO:
    def __init__(self, db): self.db = db
    def listar(self):
        with self.db.transaction() as c:
            c.execute("""SELECT c.id_coloracao AS id, m.id_modelo, m.nome AS name, m.marca AS brand,
                m.descricao AS model, c.cor AS color, c.preco AS price,
                (SELECT url FROM FOTO f WHERE f.id_coloracao=c.id_coloracao ORDER BY id_foto LIMIT 1) AS image
                FROM COLORACAO c JOIN MODELO m ON m.id_modelo=c.id_modelo ORDER BY c.id_coloracao""")
            rows=c.fetchall()
            c.execute('SELECT * FROM VARIANTE ORDER BY tamanho')
            variantes=c.fetchall()
            c.execute('SELECT * FROM FOTO ORDER BY id_foto')
            fotos=c.fetchall()
            for row in rows:
                row['price']=float(row['price'])
                row['variantes']=[v for v in variantes if v['id_coloracao']==row['id']]
                row['fotos']=[f['url'] for f in fotos if f['id_coloracao']==row['id']]
            return rows
    def cadastrar(self, modelo, coloracao, variante, foto, id_modelo=None):
        with self.db.transaction() as c:
            if id_modelo is None:
                c.execute('INSERT INTO MODELO (nome,marca,descricao) VALUES (%s,%s,%s)', (modelo.nome,modelo.marca,modelo.descricao))
                id_modelo=c.lastrowid
            else:
                c.execute('SELECT id_modelo FROM MODELO WHERE id_modelo=%s', (id_modelo,))
                if not c.fetchone(): raise ValueError('Modelo não encontrado')
            c.execute('INSERT INTO COLORACAO (id_modelo,cor,preco) VALUES (%s,%s,%s)', (id_modelo,coloracao.cor,coloracao.preco))
            cid=c.lastrowid
            c.execute('INSERT INTO FOTO (id_coloracao,url) VALUES (%s,%s)', (cid,foto))
            c.execute('INSERT INTO VARIANTE (id_coloracao,tamanho,quantidade_estoque) VALUES (%s,%s,%s)', (cid,variante.tamanho,variante.quantidade_estoque))
            return cid
    def estoque(self, cid, tamanho, quantidade):
        with self.db.transaction() as c:
            c.execute('SELECT id_coloracao FROM COLORACAO WHERE id_coloracao=%s',(cid,))
            if not c.fetchone(): raise ValueError('Coloração não encontrada')
            c.execute('SELECT id_variante FROM VARIANTE WHERE id_coloracao=%s AND tamanho=%s',(cid,tamanho))
            row=c.fetchone()
            if row:
                c.execute('UPDATE VARIANTE SET quantidade_estoque=%s WHERE id_variante=%s',(quantidade,row['id_variante']))
            else:
                c.execute('INSERT INTO VARIANTE (id_coloracao,tamanho,quantidade_estoque) VALUES (%s,%s,%s)',(cid,tamanho,quantidade))

class ListaDAO:
    def __init__(self, db): self.db=db
    def listar(self, uid):
        with self.db.transaction() as c:
            c.execute("""SELECT v.*, m.nome, co.cor, co.preco FROM ITEM_LISTA_DESEJOS i
                JOIN LISTA_DESEJOS l ON l.id_lista=i.id_lista JOIN VARIANTE v ON v.id_variante=i.id_variante
                JOIN COLORACAO co ON co.id_coloracao=v.id_coloracao JOIN MODELO m ON m.id_modelo=co.id_modelo
                WHERE l.id_usuario=%s""",(uid,))
            rows=c.fetchall()
            for r in rows: r['preco']=float(r['preco'])
            return rows
    def alterar(self, uid, vid, remover=False):
        with self.db.transaction() as c:
            c.execute('SELECT id_variante FROM VARIANTE WHERE id_variante=%s',(vid,))
            if not c.fetchone(): raise ValueError('Tamanho não encontrado')
            c.execute('SELECT id_lista FROM LISTA_DESEJOS WHERE id_usuario=%s',(uid,))
            lid=c.fetchone()['id_lista']
            c.execute('DELETE FROM ITEM_LISTA_DESEJOS WHERE id_lista=%s AND id_variante=%s',(lid,vid))
            if not remover:
                c.execute('INSERT INTO ITEM_LISTA_DESEJOS (id_lista,id_variante) VALUES (%s,%s)',(lid,vid))
