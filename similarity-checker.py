#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 23:25:35 2019

@author: isa
"""
import math 

class TextModel:
    """ a data type for a model of a body text 
    """
    def __init__(self, model_name):
        """ a constructor for TextModel objects """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
        
        
    def __repr__(self):
        """ returns a string representation for TextModel objects
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuation types: ' + str(len(self.punctuation)) + '\n'
        if '.' in self.punctuation:
            s += '  number of periods: ' + str(self.punctuation['.']) + '\n'
        if '?' in self.punctuation:
             s += '  number of question marks: ' + str(self.punctuation['?']) + '\n'
        if '!' in self.punctuation:
             s += '  number of exclamation marks: ' + str(self.punctuation['!'])
        
        return s 
    
    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces
            to all of the dictionaries in this text model.
        """
        count = 0 
        s1 = s.split(' ')
        for w in s1:
            count += 1
            if '.' in w or '!' in w or '?' in w:
                if count in self.sentence_lengths:
                    self.sentence_lengths[count] += 1
                    count = 0
                else:
                     self.sentence_lengths[count] = 1
                     count = 0
        for w in s1:
            if len(w) > 1:
                if w[-1] in '.?!':
                    if w[-1] in self.punctuation:
                        self.punctuation[w[-1]] += 1
                    else:
                        self.punctuation[w[-1]] = 1
               
                              
        word_list = clean_text(s)
        for w in word_list:
            if w in self.words:
               self.words[w] += 1
            else:
               self.words[w] = 1
        for w in word_list:
            w_len = len(w)
            if w_len in self.word_lengths:
                self.word_lengths[w_len] += 1
            else:
                self.word_lengths[w_len] = 1
        for w in word_list:
            stem_w = stem(w)
            if stem_w in self.stems:
                self.stems[stem_w] +=1
            else:
                self.stems[stem_w] = 1
        
                
    def add_file(self, filename):
        """ adds all the text from file filename to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        self.add_string(text)
        
    def save_model(self):
        """ saves the TextModel object self by writing its various feature 
            dictionaries to files
        """
        file_words = self.name + "_words"
        f1 = open(file_words, 'w')
        f1.write(str(self.words))
        f1.close()
        
        file_word_lengths = self.name + '_word_lengths'
        f2 = open(file_word_lengths, 'w')
        f2.write(str(self.word_lengths))
        f2.close()
        
        file_stems = self.name + '_stems'
        f3 = open(file_stems, 'w')
        f3.write(str(self.stems))
        f3.close()
        
        file_sentence_lengths = self.name + '_sentence_lengths'
        f4 = open(file_sentence_lengths, 'w')
        f4.write(str(self.sentence_lengths))
        f4.close()
        
        file_punctuation = self.name + '_punctuation'
        f5 = open(file_punctuation, 'w')
        f5.write(str(self.punctuation))
        f5.close()
        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from 
            their files and assigns them to the attributes of the 
            called TextModel
        """
        file_words = self.name + '_words'
        f1 = open(file_words, 'r')
        words1 = f1.read()
        self.words = dict(eval(words1))
        f1.close()
        
        file_word_lengths = self.name + '_word_lengths'
        f2 = open(file_word_lengths, 'r')
        words2 = f2.read()
        self.word_lengths = dict(eval(words2))
        f2.close()
        
        file_stems = self.name + '_stems'
        f3 = open(file_stems, 'r')
        words3 = f3.read()
        self.stems = dict(eval(words3))
        f3.close()
         
        file_sentence_lengths = self.name + '_sentence_lengths'
        f4 = open(file_sentence_lengths, 'r')
        words4 = f4.read()
        self.sentence_lengths = dict(eval(words4))
        f4.close()
        
        file_punctuation = self.name + '_punctuation'
        f5 = open(file_punctuation, 'r')
        words5 = f5.read()
        self.punctuation = dict(eval(words5))
        f5.close()
        
    def similarity_scores(self, other):
        """ computes and returns a list of similarity scores for all the dictionaries 
            in the method 
        """
        sim_list = []
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        sim_list += [word_score]
        sim_list += [word_lengths_score]
        sim_list += [stems_score]
        sim_list += [sentence_lengths_score]
        sim_list += [punctuation_score]
        return sim_list 
    
    def classify(self, source1, source2):
        """
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        line1 = 'scores for ' + source1.name + ': ' 
        line2 = 'scores for ' + source2.name + ': ' 
        print(line1, scores1)
        print(line2, scores2)
        weight_sum1 = 5*scores1[0] + 3*scores1[1] + 4*scores1[2] + 2*scores1[3] + 1*scores1[4]
        weight_sum2 = 5*scores2[0] + 3*scores2[1] + 4*scores2[2] + 2*scores2[3] + 1*scores2[4]
        line3 = self. name + ' is more likely to have come from'
        if weight_sum1 > weight_sum2:
            print(line3, source1.name)
        else:
            print(line3, source2.name) 
        
    
    
    
def clean_text(txt):
    """ takes a string of text, txt, as input and returns a list
        of all teh words that has all punctuation removed and has changed all 
        the letters to lowercase
    """
    list_words = []
    s = txt
    s = s.lower()
    s = s.replace('.', '')
    s = s.replace('!', '')
    s = s.replace('?', '')
    s = s.replace(',', '')
    s = s.replace('"', '')
    s = s.replace("'", '')
    s = s.split()
    for word in s:
        if word != '':
            list_words += [word]
    return list_words 

def stem(s):
    """ accepts a string s as parameter and returns the stem of that string 
    """
    while len(s) > 3:
        if s[-1] == 's':
            s = s[:-1]
            stem_rest = stem(s)
            s = stem_rest 
            break
        elif s[-3:] == 'ing':
            s = s[:-3]
            if len(s) > 3 and s[-1] == s[-2]:
                s = s[:-1]
            break
        elif s[-2:] == 'er':
            s = s[:-2]
            if len(s) > 3 and s[-1] == s[-2]:
                s = s[:-1]
            break
        elif s[-2:] == 'ly':
            s = s[:-2]
            if len(s) > 3 and s[-3:] == 'ing':
                s = s[:-3]
            break
        elif s[-1] == 'y':
            s = s[:-1]
            s += 'i'
            break
        break
           
    
    if len(s) > 3:
        if s[:2] == 're':
            s = s[2:]
        elif s[:2] == 'un':
            s = s[2:]
        elif s[:3] == 'pre':
            s = s[3:]
        elif s[:3] == 'dis':
            s = s[3:]
        elif s[:3] == 'mis':
            s = s[3:]
        elif s[:3] == 'non':
            s = s[3:] 
        
    return s
        
def compare_dictionaries(d1, d2):
    """ takes two dictionaries d1 and d2, and computes 
    """
    score = 0
    total = 0
    for item in d1:
       total += d1[item] 
   
    for item in d2:
        if item in d1:
            d1_prob = d1[item] / total
            score += d2[item] * math.log(d1_prob)
        else:
            d1_prob = 0.5 / total
            score += d2[item] * math.log(d1_prob)
    return score 
    
    
    

def run_tests():
    """ your docstring goes here """
    source1 = TextModel('divergent')
    source1.add_file('divergent_source1_text.txt')
    source1.add_file('divergent_source2_text.txt')
    source1.add_file('divergent_source3_text.txt')

    source2 = TextModel('cnn')
    source2.add_file('cnn_source1_text.txt')
    source2.add_file('cnn_source2_text.txt')

    new1 = TextModel('selection')
    new1.add_file('selection_source1_text.txt')
    new1.add_file('selection_source2_text.txt')
    new1.classify(source1, source2)    
    print()
    new2 = TextModel('handle_care')
    new2.add_file('jodi_source1_text.txt')
    new2.classify(source1, source2)    
    print()
    new3 = TextModel('pride_and_prejudice')
    new3.add_file('pride_source_text.txt')
    new3.classify(source1, source2)    
    print()
    new4 = TextModel('wr120')
    new4.add_file('essay_source_text.txt')
    new4.classify(source1, source2)    
    
    
        
    
    