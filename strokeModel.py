import torch
import torch.nn as nn
import numpy as np

class strokeModelNN(nn.Module):
  def __init__(self, input_size=18, nodes_per_layers=[128], dropout_rate=0.2, lr=5e-4, w=1e-5):
    super(strokeModelNN, self).__init__()

    self.layers = nn.ModuleList()

    # Función de activación
    self.activationFunction = nn.ReLU()

    # Función de pérdida
    self.lossFunction = nn.MSELoss()

    # Dropout
    self.dropout = nn.Dropout(dropout_rate)

    # Capa de entrada
    self.inputLayer = nn.Linear(input_size, nodes_per_layers[0])

    # Capas ocultas
    for i in range(1, len(nodes_per_layers)):
      self.layers.append(nn.Linear(nodes_per_layers[i-1], nodes_per_layers[i]))
      self.layers.append(self.activationFunction)
      self.layers.append(self.dropout)

    # Capa de salida
    self.outputLayer = nn.Linear(nodes_per_layers[-1], 1)

    # Usamos Adam como optimizador
    self.optimizer = torch.optim.Adam(self.parameters(), lr=lr, weight_decay=w)

  def forward(self, x):
    if isinstance(x, np.ndarray):
        x = torch.from_numpy(x)  # Convertir numpy array a Tensor
    x = x.to(torch.float32)
    x = self.inputLayer(x)
    x = self.activationFunction(x)
    x = self.dropout(x)
    for layer in self.layers:
      x = layer(x)
    x = self.outputLayer(x)
    return x

  # Vamos a incluir el entrenamiento de la red en la clase
  def trainModel(self, X, y, BATCH_SIZE=32, EPOCHS=100, validate=None):
    self.train()

    # Parámetros Early Stopping
    bestEpoch = 0
    bestLoss = float('inf')
    epochNoImprovement = 0
    patience = EPOCHS//10 if EPOCHS//10 > 1 else 1

    for epoch in range(EPOCHS):
      for i in range(0, len(X), BATCH_SIZE):
        X_batch = X[i:i+BATCH_SIZE]
        y_batch = y[i:i+BATCH_SIZE]

        self.optimizer.zero_grad()
        y_pred = self.forward(X_batch)
        loss = self.lossFunction(y_pred, y_batch)
        loss.backward()
        self.optimizer.step()

      # El proceso de validación se incluye en el entrenamiento para
      # implementar el Early Stopping, sin embargo, es opcional
      if validate is not None:
        X_val, y_val = validate

        self.eval()
        with torch.no_grad():
          y_pred = self.forward(X_val)
          val_loss = self.lossFunction(y_pred, y_val)

        # Early Stopping
        # El modelo mejora respecto a la época anterior
        if val_loss < bestLoss:
          bestEpoch = epoch
          bestLoss = val_loss
          epochNoImprovement = 0

          # Checkpoint
          torch.save(self.state_dict(), 'bestModel.pth')
        else:
          # El modelo no ha mejorado respecto a la época anterior
          epochNoImprovement += 1

        print(f"Epoch [{epoch+1}/{EPOCHS}]\nTrain | Validation Loss: {loss.item():.6f} - {val_loss.item():.6f}\n")

        # Detenemos el entrenamiento si la validación no mejora
        if epochNoImprovement >= patience:
          print(f"Early stopping en la época {epoch+1}!")
          print(f"No ha habido mejora durante {epochNoImprovement} épocas.")
          self.load_state_dict(torch.load('bestModel.pth'))

          # Imprimimos los valores de pérdida
          print(f"Pérdida mínima: {bestLoss.item():.6f} en Epoch [{bestEpoch + 1}/{EPOCHS}]")
          break

        self.train()
      else:
        print(f"Epoch [{epoch+1}/{EPOCHS}]\nTrain Loss: {loss.item():.6f}\n")

  # Método para generar una predicción sobre un conjunto de datos
  def predict(self, X):
    self.eval()
    with torch.no_grad():
      y_pred = self.forward(X)
      return y_pred