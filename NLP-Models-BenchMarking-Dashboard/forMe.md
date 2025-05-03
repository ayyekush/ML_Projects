1. Naive bias is only for classification.
1. smvs have a regression version smvr, nb have too but rarely used
1. BOW with multinomial NB is best here
1. Tfidf doesnt work great with Naive Bias, works better with SVM,Logistic Regresion
1. RNN are useless with Tfidf or BOW. cuz RNNs try to preserve order, but tfidf or bow vectors are orderless themselves.
    so if i feed bow to RNN it would waste computational cost since it will try to m
    aintain order which is not neccessary since bow already out of order, on the other hand ANN wouldnt waste on preserving order

2. Naive-Bayes : Classification Technique
    # works well with small datasets and bow/tfidf
    # it works on X_train only ofc! not dependent on how many classses y_train have, they all support multiclass classification.

2. BernoulliNB: for if only presence of feature matters
    #   like suppose x_train[0]:[0,2,1,0]=>[0,1,1,0]
    #   useful in say spam classificaiton(we need whether spam word present or not)
    #  -movie review me positive review me suppose fantastic 5 baar aa raha hai aur boring ek baar, par dono ki keemat same=>unfair for data like these
  
2. MultiNomialNB: for when frequency matters too
    #   like x_train[0]:[0,2,1,0]=>[0,2,1,0]
    #   works best with textual data(like this example)
    #   -fantastic ki keemat zyada hogi,
  
2. GaussianNB: for when data is in guassian dist,
    ### gusssian dist!=>countinous.
    #   i.e., it follows bell curve(or called Normal Dist.)
    #  -suppose if most movie reviews are 2-3 out of 5,
    #   then gnb will work better than mnb