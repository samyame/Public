# Introduction
Un réseau à convolution est un type de réseau neuronal très utilisé pour la classification d'image ou la reconnaissance visuelle. Le but principal d'un réseau à convolution est d'extraire des caractéristiques d'une image. Nous allons tenter de comprendre le fonctionnement de ce type de réseau.

![Exemple de détéction d'objets](https://scr.sad.supinfo.com/articles/resources/214662/8037/0.png)

# L'image, une matrice
Il faut savoir qu'une image est une matrice de valeurs correspondant aux pixels. 
- Une image en noir et blanc est représentée par une matrice en 2D contenant des valeurs de 0 à 255 (des pixels). Ici, la valeur d'un pixel indique le niveau de gris. Plus la valeur est proche de 255, plus le pixel est noir.

![Image n&b](https://scr.sad.supinfo.com/articles/resources/214662/8037/1.png)

- Une image en couleur possède trois canaux. C'est à dire qu'on a 3 valeurs pour chaque pixels. Ces trois valeurs représentent le niveau de rouge, de vert et de bleu. On peut imaginer 3 matrices constituées de valeurs de pixels superposées, donnant une matrice en 3D. Par exemple, pour une image d'une taille de 200 par 200 pixels, sa matrice correspondante aura une taille de 200 (longueur) par 200 (largeur) par 3 (nombre de canaux).

![Image couleur](https://www.missnumerique.com/blog/wp-content/uploads/color-channels-RGB.jpg)

# Le filtre
Une notion très importante dans les réseau de convolution sont les filtres. Tout comme une image, un filtre est une matrice de valeurs. En général les filtres utilisés sont carrés. Une taille de filtre très utilisée est une taille 3 par 3.
 

![Filtre](https://scr.sad.supinfo.com/articles/resources/214662/8037/2.png)
 

Un filtre va chercher à détécter certaines caractéristiques d'une image (couleur, contour, luminosité, netteté, etc...). Concrètement, le filtre va être déplacé par pas successifs sur l'ensemble de image.

 
![Parcours du filtre](https://scr.sad.supinfo.com/articles/resources/214662/8037/3.png)

 

Pour chaque position du filtre, les valeurs des deux matrices en superposition (filtre et image à traiter) sont multipliées. Chaque valeur ainsi inférée est projetée dans une nouvelle matrice. Cette matrice représente une nouvelle image qui fait ressortir les caractéristiques recherchées au travers du filtre.

 

L'image ci-dessous montre un exemple de calcul. Les valeurs de l'image à traiter sont anormalement petites, mais c'est juste pour comprendre plus facilement le calcul effectué:

![Calcul convolution](https://scr.sad.supinfo.com/articles/resources/214662/8037/4.png)

En fonction des valeurs et de la taille de la matrice du filtre, nous obtenons une nouvelle image plus ou moins modifiée. Le but de ce procédé est de faire ressortir certaines caractéristiques de l'image. Par exemple, avec une première image comme celle affichée ci-dessous, on peut la transformer dans le but de produire plusieurs variantes. Voici le résultat de différentes transformations à l'aide de plusieurs filtres couramment utilisés (détection de bord, floutage, etc...)

![Exemple filtre](https://scr.sad.supinfo.com/articles/resources/214662/8037/5.png)
 

Le seul filtre ne produisant aucune modification est le suivant:

![Filtre identité](https://scr.sad.supinfo.com/articles/resources/214662/8037/6.png)

Le nombre de filtres determinera le nombre de caractéristiques détectées. Ce nombre est appelé la profondeur. C'est à dire que si 10 filtres seront appliqués à une image donnée, la valeur de sa profondeur sera de 10.

 

L'usage de filtres est la base dans un réseau à convolution. En pratique, lors de la phase d'entrainement, plusieurs filtres parcourent l'image pour détécter des éléments qui vont permettre au réseau de déterminer si l'image représente, par exemple un chien ou un chat. Les valeurs des filtres sont successivement modifiées au fur et a mesure de l'entraînement, de la même manière que pour un réseau classique => 
- forward pass 
- calcul de l'erreur 
- descente de gradient 
- modification des poids du réseau qui sont ici les valeurs des filtres!

 

Les paramètres essentiels doivent être précisés avant l'entrainement, notamment: le nombre, la taille des filtres et leur pas de déplacement.

 

Ces paramètres sont à determiner en fonction des images traitées, de leurs aspects, de leurs dimensions, etc... Tout cela pour dire que les valeurs de ces paramètres doivent être adaptées, qu'il n'existe pas de solution universelle et que la recherche des valeurs optimales reste empirique.

 

Il est préférable de ne pas utiliser de filtres trop petits ou un nombre de filtres trop important car cela peut entraîner un sur-apprentissage. C'est à dire que le réseau neuronal serait moins efficace lors de la phase de test. Spécialisé, il serait trop exclusif au jeu d'entrainement.

# Le Pooling
Le Pooling est un procédé important dans un réseau à convolution. Il permet de réduire la taille d'une image tout en conservant les caractéristiques pertinentes. La méthode la plus utilisée est le "Max Pooling". Elle consiste à réduire l'image en conservant les valeurs les plus grandes des pixels au sein d'une zone. Pour ce faire
- une tuile d'une certaine taille se déplace (comme un filtre) sur la surface de notre image. 
- à chaque position de la tuile, on extrait la valeur la plus haute et ne retient que celle là. Cela produit une nouvelle image, plus petite avec uniquement les valeurs remarquables de l'image.



L'image ci dessous montre un exemple de Pooling. La tuile a, ici, des dimensions de 3 par 3. L'image de 9 par 9 pixels de départ est réduite en une image de 7 par 7 pixels.

![Pooling](https://scr.sad.supinfo.com/articles/resources/214662/8037/7.png)


 

Le Pooling est très important. En réduisant l'image, le nombre de données traitées diminue et donc le temps de calcul sera lui aussi réduit. De plus, celà permet au réseau de gagner en abstraction en fournissant pour les couches suivantes des versions "résumées" de l'image

Il existe d'autres méthodes que le "Max Pooling", par exemple:

- "Average Pooling" : Moyenne de toutes les valeurs recouvertes par la tuile.

- "Pooling stochastique" : Ne retient qu'une seule valeur, comme le "Max Pooling", mais en se basant sur une méthode probabiliste.

Cependant, en pratique, le "Max Pooling" est la méthode qui donne le plus souvent les meilleurs resultats. Elle est donc généralement privilégiée.

# La convolution
Le principe d'un réseau à convolution, c'est l'enchainement d'étapes. Chaque étape consiste à appliquer des filtres puis une phase de Pooling sur le résulat de chaque filtre.



__Un niveau, étape élémentaire d'un réseau de convolution:__

L'image ci-dessous représente ces deux phases (filtrage puis Pooling). Dans cet exemple, trois filtres ont été créés donnant trois nouvelles "images". Ensuite, ces dernières sont réduites à l'essentiel par la phase de Pooling.

 
![Etape pooling](https://scr.sad.supinfo.com/articles/resources/214662/8037/8.png)

 

L'étape décrite ci-dessus peut se répéter. L'"image" obtenue après cette première étape est alors réutilisée en entrée de l'étape suivante (filtrage + pooling) et ainsi de suite... Chaque étape est appellé un niveau. Un réseau à convolution peut avoir plusieurs niveaux.

 
__On stacke plusieurs niveaux pour créer un CNN (réseau convolutif):__

L'exemple ci-dessous représente deux niveaux de convolution. On peut observer qu'une que fois les deux niveaux de convolution ont opéré, six nouvelles images sont obtenues à partir de la première.

 
![Stacking pooling](https://scr.sad.supinfo.com/articles/resources/214662/8037/9.png)

 

Les nouvelles images obtenues en sortie représentent certaines caractéristiques particulières de l'image de départ.

 

Lors de l'apprentissage, chaque niveau de convolution doit retenir les filtres les plus pertinents. Cette selection est opérée grâce à un réseau neuronal interne à chaque niveau de convolution. Comme dans une couche dense classique. 

# La classification
Une fois que les étapes de convolutions ont opéré, les patterns obtenus en sortie sont injectés comme données d'entrée dans un réseau neuronal classique. Le but de celui-ci est de classifier les données en déduisant une probabilité sur les différents résultats possibles.

 

Pour injecter les patterns issus du réseau à convolution dans le réseau neuronal, on passe par une étape dite de "Flattening" (ou applatissement). Cette opération consiste à mettre à plat toutes les données dans un seul vecteur.

 

L'image ci-dessous représente cette pratique pour une "image".

![Classif](https://scr.sad.supinfo.com/articles/resources/214662/8037/10.png)

Toutes les "images" sont ainsi mises bout à bout dans ce même vecteur.

 

Ce vecteur permettra la création d'une première couche de neurones entièrement connectée. C'est à dire que chacune des valeurs de ce vecteur sera connectée aux neurones de la première couche du réseau permettant la classification de l'image.

 


# Vue d'ensemble
Représentation du principe dans son intégralité:


![Convolution Globale](https://scr.sad.supinfo.com/articles/resources/214662/8037/12.png)

En pratique, sur un petit exemple:

![Exemple convolution](https://scr.sad.supinfo.com/articles/resources/214662/8037/13.png)

L'image ci-dessus représente très bien le fonctionnement d'un réseau à convolution de manière concrete. Ce réseau sert à classifier des images représentant des chiffres. L'image montre ce qui se passe au niveau des différentes couches quand on lui présente l'image d'un huit en entrée.

 

Il est constitué de deux niveaux de convolution afin d'en extraire les caractèristiques puis deux couches entièrement connectées pour traiter les données après convolution et classifier l'image de départ.


# Les paramètres des filtres de convolution
Les couches de convolution (les filtres) pour les images sont accessibles via la classe __tf.keras.layers.Conv2D__ de tensorflow.


Ces couches possèdent plusieurs paramètres qu'il est nécessaire de spécifier avant de lancer l'entraînement.

- filters: le nombre de filtres que l'on va utiliser dans la couche
- kernel_size: la shape d'un filtre de la couche (au format tuple, par exemple (3,3))
- strides: c'est le pas avec lequel on déplace le filtre sur l'image. Un stride de 1 va déplacer à chaque étape le filtre de 1 pixel par exemple
- padding: On utilisera toujours padding = "same", ce qui signifie que l'image générée après le passage du filtre sera de même taille que l'image lue par le filtre.

# Conclusion
Un réseau à convolution se compose donc d'une ou plusieurs étapes de convolution (filtrage, Pooling) suivi d'une classification. Lors de la phase d'entrainement du modèle, en fonction de chaque image entrante dans le réseau et du résultat produit par l'étape de classification:
- Le coût est calculé (En général la cross-entropy si on est dans le cadre d'une classification multiclasse)
- Sa valeur est utilisée pour mettre à jour les paramètres du réseau afin de l'optimiser, en utilisant comme d'habitude.... La descente de gradient!