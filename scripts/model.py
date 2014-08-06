import sys

import numpy
import pylab

from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score 

import sklearn

def readExamples(inputFilename):
    queries = []
    labels = []
    first = True
    with open(inputFilename) as inputFile:
        retail = 0
        notRetail = 0
        for line in inputFile:
            if first:
                first = False
            else:
                words = line.strip().split('\t')
                query = words[0]
                if words[1] == "RETAIL":
                    label = 1
                    retail += 1
                    labels.append(label)
                    queries.append(query)
                elif words[1] == "NOT_RETAIL":
                    label = 0
                    notRetail += 1
                    labels.append(label)
                    queries.append(query)
                else:
                    pass
    sys.stdout.write("Total Queries: " + str(len(queries)) + "\n")
    sys.stdout.write("Retail: " + str(retail) + "\n")
    sys.stdout.write("Not Retail: " + str(notRetail) + "\n")    
    return numpy.array(queries), numpy.array(labels)

def computeDensity(vectorizer, examples):
    tokens  = numpy.apply_along_axis(numpy.sum,1,vectorizer.transform(examples).todense())
#     return 1 - numpy.count_nonzero(nonZeros)/float(len(nonZeros))
    return list(tokens) 

def predict(model,normalizer,vectorizer,examples, actual, fold=0, dump=False):
    X = normalizer.transform(vectorizer.transform(examples))
    pred = model.predict(X)
    if dump:
        for i in xrange(0, len(examples)):
            sys.stdout.write(examples[i] + "\t")
            sys.stdout.write(str(fold) + "\t") 
            if actual[i] == 1:
                sys.stdout.write("Retail" + "\t")
            else:
                sys.stdout.write("Non-Retail" + "\t")
            if pred[i] == 1:
                sys.stdout.write("Retail" + "\n")
            else:
                sys.stdout.write("Non-Retail" + "\n")
    return accuracy_score(actual,pred)
def predictF1(model,normalizer,vectorizer,examples, actual):
    X = normalizer.transform(vectorizer.transform(examples))
    pred = model.predict(X)
    return f1_score(actual,pred)

def prettyPrint(givenVector):
    return "%.4f" % givenVector.mean() +  "(" +"%.4f" % givenVector.std() + ")"    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        datafilename = "/Users/nikhil/Code/BING-POC/bing-poc/bingData.tsv"
        histogramfilename = "/Users/nikhil/Code/BING-POC/bing-poc/density.pdf"
    else:
        datafilename = sys.argv[2]
        histogramfilename = sys.argv[3]
    sys.stderr.write(sklearn.__version__ + "\n")
    examples, labels = readExamples(datafilename)
    folds = 2
    skf = StratifiedKFold(labels, folds)
    trainingAccuracy = numpy.zeros(folds)
    trainingBaseline = numpy.zeros(folds)
    testingAccuracy = numpy.zeros(folds)
    testingBaseline = numpy.zeros(folds)
    testingDensity = []
    testingF1 = numpy.zeros(folds)
    
    # sys.stdout.write("Query\tFold\tGround-Truth\tPredicted\n")
    
    for i, (train, test) in enumerate(skf):
        vectorizer = CountVectorizer(min_df=1,dtype='double')
        normalizer = Normalizer()
        classifier = LinearSVC(loss='l1')
        strawMan = DummyClassifier(strategy='most_frequent')
    
        X = normalizer.fit_transform(vectorizer.fit_transform(examples[train]))
        y = labels[train]
        classifier.fit(X, y)
        strawMan.fit(X, y)
    
        testingDensity.extend(computeDensity(vectorizer, examples[test]))
        trainingAccuracy[i] = predict(classifier,normalizer,vectorizer,examples[train], labels[train])
        trainingBaseline[i] = predict(strawMan,normalizer,vectorizer,examples[train], labels[train])
        testingAccuracy[i] = predict(classifier,normalizer,vectorizer,examples[test], labels[test])
        testingBaseline[i] = predict(strawMan,normalizer,vectorizer,examples[test], labels[test])
        testingF1[i] = predictF1(classifier,normalizer,vectorizer,examples[test], labels[test])
    
    print "Training Accuracy:" + prettyPrint(trainingAccuracy)
    print "Test Accuracy:" + prettyPrint(testingAccuracy)
    print "Training Baseline:" + prettyPrint(trainingBaseline)
    print "Test Baseline:" + prettyPrint(testingBaseline)
    print "Testing F1:" + prettyPrint(testingF1)
    
    pylab.hist(testingDensity, bins=[0,1,2,3,4,5,6,7,8,9,10])
    pylab.savefig(histogramfilename)


