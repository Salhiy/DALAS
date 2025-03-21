Projet Dalas
Memebre : Younes Salhi

1)* il faut d'abord executer le script pour recuperer les données (si data.xlsx n'est pas déja present) et pour ce, dans modules/load_data il ya un fichier python load.py qu'il faut executer
ce dernier va scrapper et envoyer des requetes Api + CSV pour generer les données
	python ./modules/load_data/load.py

2)* ensuite une fois data.xlsx crée, vous pouvez lancer les notebook
	)* Anaylse : represente une analyse statistiques des données
	)* DashBorad : pour la generation du dash
	)* EDA : etudes des données
	)* LSTM : model deep learning de type RNN avec tenserflow
	)* LinearRegression : une regression linaire sur nos données
	)* OtherModels : d'autre models pour les tests 
						- KNN
						- Gradiant Boosting
						- Desicion Tree