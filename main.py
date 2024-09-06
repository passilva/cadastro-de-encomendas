from flask import Flask, render_template, request, redirect, jsonify
import datetime
app = Flask(__name__, template_folder="templates", static_folder="templates/static")


encomendas= []

class Encomenda:
  def __init__(self, id, nome, complemento, quantidade, lacrado, responsavel) -> None:
    self.id = id
    self.nome = nome
    self.complemento=complemento
    self.quantidade=quantidade
    self.lacrado=lacrado
    self.responsavel=responsavel
    self.recebidoEm=datetime.datetime.today()
    self.foi_recebido=False
  
  def to_dict(self):
    return {
      'id': self.id,
      'nome': self.nome,
      'complemento': self.complemento,
      'quantidade': self.quantidade,
      'lacrado': self.lacrado,
      'responsavel': self.responsavel,
      'recebidoEm': self.recebidoEm.isoformat(),
      'foi_recebido': self.foi_recebido 
    }

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/baixa")
def baixas():
  global encomendas
  encomendas_sem_baixa = filter(lambda x: not x.foi_recebido, encomendas)
  return render_template("baixa.html", encomendas=encomendas_sem_baixa)

@app.route("/nova-encomenda", methods=['POST'])
def nova_encomenda():
  global encomendas
  encomenda = Encomenda(len(encomendas)+1,
                        request.form['nome'],
                        request.form['complemento'],
                        request.form['quantidade'],
                        request.form.get('lacrado'),
                        request.form['responsavel']
                        )
  encomendas.append(encomenda)
  return redirect("/")

@app.route("/baixas/<int:id>", methods=['POST'])
def dar_baixa(id):
  global encomendas
  for encomenda in encomendas:
    if encomenda.id == id:
      encomenda.foi_recebido = True
  return redirect("/baixa")

@app.route("/encomendas", methods=['GET'])
def get_encomendas():
  global encomendas
  encomendas_dict = [encomenda.to_dict() for encomenda in encomendas]
  return jsonify(encomendas_dict)

if __name__ == "__main__":
  app.run(use_reloader=True)