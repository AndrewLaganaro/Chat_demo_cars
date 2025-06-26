from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import random



Base = declarative_base()



class Carro(Base):
    __tablename__ = 'carros'
    id = Column(Integer, primary_key=True)
    marca = Column(String)
    tipo = Column(String)
    modelo = Column(String)
    motor = Column(String)
    portas = Column(Integer)
    cor = Column(String)
    cambio = Column(String)
    ano = Column(Integer)
    combustivel = Column(String)
    preco = Column(Integer, default=0)


def generate_fake_cars_DB():
    
    random_db =   Carro(marca       = random.choice(['Fiat', 'Ford', 'Chevrolet', 'Volkswagen', 'Honda', 'Mitsubishi', 'Toyota', 'Nissan', 'Hyundai', 'Kia']),
                        tipo        = random.choice(['urbano', 'estrada']),
                        modelo      = random.choice(['Uno', 'Palio', 'Fusca', 'Civic', 'Onix']),
                        motor       = random.choice(['1.0', '1.3', '1.6', '2.0']),
                        portas      = random.choice([2, 4]),
                        cor         = random.choice(['branco', 'preto', 'prata', 'vermelho']),
                        cambio      = random.choice(['manual', 'automático']),
                        ano         = random.randint(2015, 2023),
                        combustivel = random.choice(['gasolina', 'álcool', 'flex']),
                        preco       = random.randint(20000, 200000)
                                )
    
    return random_db



if __name__ == "__main__":
    
    engine = create_engine("sqlite:///cars_original.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects([generate_fake_cars_DB() for _ in range(100)])
    session.commit()
    
    print("✅ Database 'cars.db' created with 100 fake car entries.")
    session.close()

