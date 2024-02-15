from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from scrap_actions import scrap_page_action

df = scrap_page_action()

print(df)

#on garde que les dernieres 7 colones
df_updated = df.iloc[:, -7:]

#initialisation de l'algorithme PCA
pca = PCA(n_components=2)

#generation des nouvelles données
data_transformed = pca.fit_transform(df_updated)

print(data_transformed)