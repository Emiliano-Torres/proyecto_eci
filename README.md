# 📊 Predicción de Demanda con XGBoost  

Este proyecto implementa un modelo de **Machine Learning supervisado** para predecir la demanda de productos en base a datos históricos de ventas. Se utiliza **XGBoost**, uno de los algoritmos más potentes para problemas de regresión y series temporales.  

---

## 🚀 Objetivo  

El objetivo es **anticipar la demanda en $ de ventas futuras** de cada subgrupo de productos por tienda y dar un precio optimo para la siguiente semana.  

---

## 🛠️ Tecnologías y librerías  

- Python 3.10+  
- [pandas](https://pandas.pydata.org/) → Manipulación de datos  
- [numpy](https://numpy.org/) → Operaciones numéricas  
- [scikit-learn](https://scikit-learn.org/) → Preprocesamiento y métricas  
- [xgboost](https://xgboost.readthedocs.io/) → Algoritmo principal de predicción  
- [matplotlib](https://matplotlib.org/) → Visualización  


---

## 🔑 Principales características  

- **Feature Engineering avanzado**:  
  - **Lags** de ventas y precios  
  - **Ventanas móviles (rolling means/sums)**  
  - **Fourier Features** para capturar estacionalidad compleja  
  - **Variables calendarias** (día de la semana, mes, etc.)  

- **Estrategias de predicción**:  
  - **Recursiva**: se alimenta de sus propias predicciones para generar horizontes largos.  
  - **No recursiva (directa)**: se entrena un modelo específico para cada horizonte de predicción.  

- Entrenamiento con **XGBRegressor** y early stopping.  
- Evaluación del rendimiento con **RMSE**.  
 

---
