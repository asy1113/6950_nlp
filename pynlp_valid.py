import os

class Validnote:
    """document level validation"""
    def __init__(self):
        """init"""
    
    def readstd(self, posPath, negPath, posLab, negLab):
        """Read annotator classified documents and save the text name and classifer into a dict()"""
        
        std_doc = dict()

        path1 = posPath
        files1 = os.listdir(path1)
        for j1 in files1[:]:
            if ".txt" in j1:
                std_doc[j1]=posLab

        path2 = negPath 
        files2 = os.listdir(path2)
        for j2 in files2[:]:
            if ".txt" in j2:
                std_doc[j2]=negLab
                
        return std_doc
                
    def validation(self, results, standard, plabel, nlabel):
        """Documents Validation"""
        
        tp=0
        tn=0
        fp=0
        fn=0
        Precision=0
        Recall=0
        F1=0
        for v in results:
            if results[v]==standard[v] and results[v]==plabel:
                tp=tp+1
            elif results[v]==standard[v] and results[v]==nlabel:
                tn=tn+1
            elif results[v]!=standard[v] and results[v]==plabel:
                fp=fp+1
                print("fp: " + v)
            else: # results[v]!=standard[v] and results[v]==nlabel:
                fn=fn+1
                print("fn: " + v)
                
        if (tp + fp != 0):
            Precision = tp / (tp + fp)
        if (tp + fn != 0):
            Recall = tp / (tp + fn)
        if (Precision+Recall != 0):
            F1 = 2*Precision*Recall/(Precision+Recall)
        
        return Precision, Recall, F1 