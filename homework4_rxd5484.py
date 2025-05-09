############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Rakshit Dongre"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: Spam Filter
############################################################
import email
from email import iterators
import math
from collections import defaultdict
import os
from collections import Counter

def load_tokens(email_path):
    
    t = []
    
    with open(email_path, 'r') as file:
        
        m = email.message_from_file(file)
        
        
        for l in iterators.body_line_iterator(m):
            
            t.extend(l.split())
    
    return t







def log_probs(email_paths, smoothing):
    w_c = defaultdict(int)
    t_w = 0

    
    for pt in email_paths:
        a = load_tokens(pt)
        for b in a:
            w_c[b] += 1
            t_w += 1

    
    v_s = len(w_c)
    d = t_w + smoothing * (v_s + 1)

    
    l_p = {}
    for w, c in w_c.items():
        l_p[w] = math.log((c + smoothing) / d)
    
    l_p["<UNK>"] = math.log(smoothing / d)
    
    return l_p




class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        
        spam_paths = [os.path.join(spam_dir, filename) for filename in os.listdir(spam_dir)]
        ham_paths = [os.path.join(ham_dir, filename) for filename in os.listdir(ham_dir)]
        
        self.spam_log_probs = log_probs(spam_paths, smoothing)
        self.ham_log_probs = log_probs(ham_paths, smoothing)
        
        
        num_s = len(spam_paths)
        num_h = len(ham_paths)
        t_f = num_s + num_h
        
        
        self.log_p_spam = math.log(num_s / t_f)
        self.log_p_ham = math.log(num_h / t_f)
    
    
    def is_spam(self, email_path):
        
        tok = load_tokens(email_path)
        
        
        w_c = Counter(tok)
        
        
        lps = self.log_p_spam  
        for w, c in w_c.items():
            
            lps += c * self.spam_log_probs.get(w, self.spam_log_probs["<UNK>"])
        
       
        lph = self.log_p_ham 
        for w, c in w_c.items():
          
            lph += c * self.ham_log_probs.get(w, self.ham_log_probs["<UNK>"])
        
        return lps > lph
    
    def most_indicative_spam(self, n):
        
        i_v = {}
        
        for w in self.spam_log_probs:
            if w in self.ham_log_probs:  
                
                pwgs = math.exp(self.spam_log_probs[w])
                pwgh = math.exp(self.ham_log_probs[w])
                
               
                p_w = pwgs * math.exp(self.log_p_spam) + pwgh * math.exp(self.log_p_ham)
                
                
                i_v[w] = self.spam_log_probs[w] - math.log(p_w)

        
        sort_w = sorted(i_v, key=i_v.get, reverse=True)
        return sort_w[:n]

    def most_indicative_ham(self, n):
        
        i_v = {}
        
        for w in self.ham_log_probs:
            if w in self.spam_log_probs:  
               
                pwgs = math.exp(self.spam_log_probs[w])
                pwgh = math.exp(self.ham_log_probs[w])
                
               
                p_w = pwgs * math.exp(self.log_p_spam) + pwgh * math.exp(self.log_p_ham)
                
            
                i_v[w] = self.ham_log_probs[w] - math.log(p_w)

        
        sort_w = sorted(i_v, key=i_v.get, reverse=True)
        return sort_w[:n]


 



############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent around 12-15 hours
"""

feedback_question_2 = """
The most challenging aspect was implementing the Laplace-smoothed log-probabilities 
and handling unknown tokens. 
Ensuring that the model worked correctly in log-space to avoid underflow was also challening
"""

feedback_question_3 = """
 I enjoyed implementing the naive Bayes classifier.
"""

