import os
import sys
import cv2
import numpy as np
 
from sklearn import cross_validation as cval
from sklearn.base import BaseEstimator
from sklearn.metrics import precision_score
 
def read_images(path, sz=None):
    """Reads the images in a given folder, resizes images on the fly if size is given.
 
    Args:
        path: Path to a folder with subfolders representing the subjects (persons).
        sz: A tuple with the size Resizes 
 
    Returns:
        A list [X,y]
 
            X: The images, which is a Python list of numpy arrays.
            y: The corresponding labels (the unique number of the subject, person) in a Python list.
    """
    c = 0
    X,y = [], []
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    # resize to given size (if given)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(c)
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
    return [X,y]
 
class FaceRecognizerModel(BaseEstimator):
 
    def __init__(self):
        self.model = cv2.createFisherFaceRecognizer()
 
    def fit(self, X, y):
        self.model.train(X,y)
 
    def predict(self, T):
        return [self.model.predict(T[i]) for i in range(0, T.shape[0])]
 
if __name__ == "__main__":
    # You'll need at least some images to perform the validation on:
    if len(sys.argv) < 2:
        print "USAGE: facerec_demo.py </path/to/images> [</path/to/store/images/at>]"
        sys.exit()
    # Read the images and corresponding labels into X and y.
    [X,y] = read_images(sys.argv[1])
    # Convert labels to 32bit integers. This is a workaround for 64bit machines,
    # because the labels will truncated else. This is fixed in recent OpenCV
    # revisions already, I just leave it here for people on older revisions.
    #
    # Thanks to Leo Dirac for reporting:
    y = np.asarray(y, dtype=np.int32)
    # Then we create a 10-fold cross validation iterator:
    cv = cval.StratifiedKFold(y, 10)
    # Now we'll create a classifier, note we wrap it up in the 
    # FaceRecognizerModel we have defined in this file. This is 
    # done, so we can use it in the awesome scikit-learn library:
    estimator = FaceRecognizerModel()
    # And getting the precision_scores is then as easy as writing:
    precision_scores = cval.cross_val_score(estimator, X, y, score_func=precision_score, cv=cv)
    # Let's print them:
    print precision_scores