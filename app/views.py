# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
conn = psycopg2.connect('dbname=sisvenda user=postgres password=flasknao host=127.0.0.1')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
from flask import render_template, request, session
from app import app
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
from base64 import b64encode, b64decode
def geradorChaves(tamanho_chave):
	#2048
	random_generator = Random.new().read
	# criando as chaves. tamanho fixo.
	key = RSA.generate(tamanho_chave, random_generator)
	# chaves publica e privada
	private = key
	public = key.publickey()
	return public, private

chave_publica, chave_privada = geradorChaves(2048)

def encrypt(mensagem, chave_publica):
	#RSA - implementação PKCS#1 OAEP
	cipher = PKCS1_OAEP.new(chave_publica)
	return cipher.encrypt(mensagem)

def decrypt(mensagem, chave_privada):
	#RSA - implementação PKCS#1 OAEP
	cipher = PKCS1_OAEP.new(chave_privada)
	return cipher.decrypt(mensagem)



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	return render_template('homecadastro.html')

@app.route('/caixadeentrada', methods=['GET', 'POST'])
def caixadeentrada():
	cur.execute("SELECT * FROM Mensagem")
	lista_mensagens = cur.fetchall()
	return render_template('caixaentrada.html', caixa=lista_mensagens)

@app.route('/escrever', methods=['GET', 'POST'])
def escrever():
	if (request.method == 'POST'):
		remetente = request.form['remetente']
		destinatario = request.form['destinatario']
		mensagem = request.form['mensagem']
		publi = psycopg2.connect('dbname=public user=postgres password=flasknao host=127.0.0.1')
		t = publi.cursor(cursor_factory=psycopg2.extras.DictCursor)
		t.execute("SELECT chavpublic FROM Public where email= '%s';"%(destinatario))
		x = t.fetchone()
		while x is not None:
			return (x[0])
		t.close()


	return render_template('escrevercliente.html')

@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
	if (request.method == 'POST'):
		chave_publica, chave_privada = geradorChaves(2048)
		nome = request.form['nome']
		senha = request.form['senha']
		email = request.form['email']
		cpf = request.form['cpf']
		cur.execute("INSERT INTO cliente (nome,senha,email,cpf) VALUES ('%s','%s','%s', %s)"%(nome,senha,email,cpf))
		conn.commit()
		cur.close()
		publi = psycopg2.connect('dbname=public user=postgres password=flasknao host=127.0.0.1')
		t = publi.cursor(cursor_factory=psycopg2.extras.DictCursor)
		t.execute("INSERT INTO Public (nome,email,chavpublic) VALUES ('%s','%s','%s')"%(nome,email,chave_publica))
		publi.commit()
		t.close()
		priv = psycopg2.connect('dbname=privat user=postgres password=flasknao host=127.0.0.1')
		e = priv.cursor(cursor_factory=psycopg2.extras.DictCursor)
		e.execute("INSERT INTO Private (nome,email,chavprivat) VALUES ('%s','%s','%s')"%(nome,email,chave_privada))
		priv.commit()
		e.close()
		return render_template('cliente.html')
	return render_template('cliente.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if (request.method == 'POST'):
		email = request.form['email']
		senha = request.form['password']
		conn = psycopg2.connect('dbname=sisvenda user=postgres password=flasknao host=127.0.0.1')
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("SELECT * FROM cliente;")
		x = cur.fetchall()
		for i in x:
			if (i['email'] == email) and (i['senha'] == senha):
				return render_template('homecliente.html')
	return render_template('login.html')
