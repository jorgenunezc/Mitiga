
from keras.models import load_model

def Load_model(ruta_model):
    model = model = load_model(ruta_model)
    return model
