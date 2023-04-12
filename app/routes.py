from flask import Flask, render_template, jsonify, request, send_file, url_for, redirect
from forms import CadastroProduto
from PIL import Image
import os
import json

app = Flask(__name__)
file_path = './JSONFiles/mercadinho.json'
carrinho_path = './JSONFiles/carrinho.json'

app.config['SECRET_KEY'] = 'top10senhasfodas'
app.config['UPLOAD_FOLDER'] = './static/Imagens'

@app.route('/')
def index():
    return render_template('index.html', title = "Mercado")

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html', title = "Carrinho")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroProduto()
    if form.validate_on_submit():
        TipoEXists = False
        with open(file_path,'r') as f:
            mercadinho = json.load(f)
        file1 = request.files['imagem']
        print(type(file1))
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        produto = {
                "nome": form.nome.data,
                "preco": form.preco.data,
                "descricao": form.descricao.data,
                "quantidade": form.quantidade.data,
                "imagem":path[1:]
                }
        for tipo in mercadinho['mercado']:
            if tipo['tipo'] == form.tipo.data:
                mercadinho['mercado'][mercadinho['mercado'].index(tipo)]['produtos'].append(produto)
                TipoEXists = True
        if not TipoEXists:
            produtos = []
            produtos.append(produto)
            mercadinho['mercado'].append({"tipo":form.tipo.data,"produtos": produtos})

        with open(file_path,'w') as f:
            f.write(json.dumps(mercadinho, indent=4))
        return redirect(url_for('index'))
    return render_template('cadastro.html', title = "Cadastro", form=form)

@app.route('/carrinho_items')
def carrinho_items():
    return send_file(carrinho_path, mimetype='application/json')


@app.route('/process', methods=['POST'])
def process():
    engual = False
    data = request.json
    with open(carrinho_path,'r') as f:
        carrinho = json.load(f)
    #adiciona no Json
    for produto in carrinho['items']:
        if produto['produto'] == data['produto']:
            carrinho['items'][carrinho['items'].index(produto)]['quantidade'] = data['quantidade']
            engual = True
    if not engual:
        carrinho['items'].append({'produto':data['produto'],'quantidade':data['quantidade']})
    with open(carrinho_path,'w') as f:
        f.write(json.dumps(carrinho, indent=4))

    return jsonify(carrinho)

@app.route('/process', methods=['DELETE'])
def delete_process():
    data = request.json
    with open(carrinho_path,'r') as f:
        carrinho = json.load(f)
    for produto in carrinho['items']:
        if produto['produto'] == data['produto']:
            del carrinho['items'][carrinho['items'].index(produto)]
    with open(carrinho_path,'w') as f:
        f.write(json.dumps(carrinho, indent=4))
        
    return jsonify(carrinho)

@app.route('/data')
def data():
    # This function returns a JSON file
    return send_file(file_path, mimetype='application/json')

@app.route('/produtos/<produto>')
def produtos(produto):
    with open(file_path,'r') as f:
        my_data = json.load(f)
    for tipo in my_data['mercado']:
        for i in tipo['produtos']:
            if i['nome'] == produto:
                return jsonify(produto=i)

if __name__ == '__main__':
    app.run(debug=True)
