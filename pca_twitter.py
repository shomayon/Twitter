from sklearn.decomposition import PCA
import numpy as np

X = np.random.normal(size=(500,1000))
pca = PCA(n_components=10)
pca.fit(X)

components = pca.components_
print(components.shape)
explained_variance = pca.explained_variance_ratio_
print(np.sum(explained_variance))