import sys

from PyRuSH.RuSH import RuSH
from pyConTextNLP import pyConTextGraph
from pyConTextNLP.utils import get_document_markups


from DocumentClassifier_social import FeatureInferencer
from DocumentClassifier_social import DocumentInferencer
from nlp_pneumonia_utils import markup_sentence
from itemData import get_item_data
from visual import convertMarkups2DF


class Mypipe:
    """PyContextNLP pipeline, sentence_rules, target_rules, context_rules, feature_inference_rule, document_inference_rule"""
    def __init__(self, sentence_rules, target_rules, context_rules, feature_inference_rule, document_inference_rule):
        
        self.sentence_rules=sentence_rules
        self.target_rules=target_rules
        self.context_rules=context_rules
        self.feature_inference_rule=feature_inference_rule
        self.document_inference_rule=document_inference_rule
        
        self.sentence_segmenter = RuSH(self.sentence_rules)
        self.feature_inferencer=FeatureInferencer(self.feature_inference_rule)
        self.document_inferencer = DocumentInferencer(self.document_inference_rule)
        self.targets=get_item_data(self.target_rules)
        self.modifiers=get_item_data(self.context_rules)
        
                    
    def process(self, doc_text):    
        """PyContextNLP, return doc_class, context_doc, annotations, relations"""        

        context_doc = pyConTextGraph.ConTextDocument()
        sentences=self.sentence_segmenter.segToSentenceSpans(doc_text)
        

        for sentence in sentences:
            
            sentence_text=doc_text[sentence.begin:sentence.end].lower()
            # Process every sentence by adding markup
            m = markup_sentence(sentence_text, modifiers=self.modifiers, targets=self.targets)
            context_doc.addMarkup(m)
            context_doc.getSectionMarkups()
            # print(m)
            # print(context_doc.getXML())
        
        # convert graphic markups into dataframe    
        markups = get_document_markups(context_doc)
        annotations, relations, doc_txt = convertMarkups2DF(markups) 
        # display(annotations)
        # display(relations)
        
        # apply inferences for document classication
        inferenced_types = self.feature_inferencer.process(annotations, relations)
        # print('After inferred from modifier values, we got these types:\n '+str(inferenced_types))
        doc_class = self.document_inferencer.process(inferenced_types)
        # print('\nDocument classification: '+ doc_class )        
        
        return doc_class, context_doc, annotations, relations