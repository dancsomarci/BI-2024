import numpy as np
from tensorflow.keras.models import load_model

model = load_model("lstm_model.keras")


def lstm(X: list) -> float:
    return round(model(np.array([X])).numpy()[0][0], 2)
