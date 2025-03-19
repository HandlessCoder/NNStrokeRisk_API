import torch
from strokeModel import strokeModelNN
import os
from fastapi import FastAPI
import shap
import pandas as pd
import numpy as np
import base64
from io import BytesIO


model = strokeModelNN()
try:
    model.load_state_dict(torch.load('./strokeModelFinal.pth'))
    datos = pd.read_csv('./X_train_NN.csv')
except:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model.load_state_dict(torch.load(current_dir + '/strokeModelFinal.pth'))
    datos = pd.read_csv(current_dir+'/X_train_NN.csv')

X_train = datos.values

explainer = shap.DeepExplainer(model,torch.tensor(X_train[:100]))

columnas = ['Femenino', 'Masculino', 'Edad', 'Dolor de pecho', 'Presión arterial elevada', 'Latidos Irregulares', 'Falta de Aire', 'Fatiga', 'Mareo', 'Hinchazón', 'Dolor en cuello o mandíbula', 'Sudoración excesiva', 'Tos persistente', 'Náuseas', 'Malestar en el pecho', 'Extremidades frías', 'Ronquidos o apnea', 'Ansiedad']

app = FastAPI()

@app.post("/predict")

async def predict(data: dict):
    input_data = data['informacion_usuario']
    input_data = np.float32(list(input_data.values()))
    tensorInput = torch.tensor(np.array(input_data).reshape((1,18)))

    prediction = model.predict(torch.tensor(input_data))[0].item()
    shap_values = explainer.shap_values(tensorInput)[0]
    shap_values = [ shap_value[0] for shap_value in shap_values ]
    shap_values = np.array(shap_values)

    shap.initjs()

    p = shap.force_plot(base_value=explainer.expected_value,shap_values= shap_values,matplotlib=True, feature_names = columnas, show = False, out_names = f"Factores de riesgo de un Accidente Cerebro Vascular (ACV) en su caso, {'Sr. ' if input_data[1] != 0.0 else 'Sra. '}{''}", text_rotation=15)

    buf = BytesIO()
    p.savefig(buf, format='png')
    buf.seek(0)

    # Convierte la imagen a base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # 4. Visualizar la explicación

    return {
        "prediction": prediction,
        "imagen": image_base64
    }
