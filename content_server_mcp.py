from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from generate_fake_db import Carro
from sqlalchemy import and_



app = Flask(__name__)
engine = create_engine("sqlite:///cars_original.db")
Session = sessionmaker(bind = engine)
session = Session()



@app.route("/mcp", methods = ["POST"])
def mcp():
    
    data = request.get_json()
    params = data.get("params", {})
    marca = params.get("marca")
    tipo = params.get("tipo")
    
    if not all([marca, tipo]):
        
        return jsonify({"error": "Campos obrigatórios ausentes."}), 400
    
    #resultados = session.query(Carro).filter_by(marca = marca, tipo = tipo).all()
    
    resultados = session.query(Carro).filter(and_(Carro.marca == marca, Carro.tipo == tipo)).all()
    
    carros = [{"marca": car.marca, "tipo": car.tipo, "modelo": car.modelo, "motor": car.motor, "portas": car.portas,
                "cor": car.cor, "cambio": car.cambio, "ano": car.ano, "combustivel": car.combustivel, "preco": car.preco
            } for car in resultados]
    
    return jsonify({"carros": carros})



if __name__ == "__main__":
    
    app.run(port = 5000)
