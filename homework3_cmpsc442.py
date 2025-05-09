############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Rakshit Dongre"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
#itertools


############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name
    
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return isinstance(other, Atom) and self.name == other.name
    def __repr__(self):
        return f"Atom({self.name})"
    def atom_names(self):
        return {self.name}
    def evaluate(self, assignment):
        return assignment[self.name]
    def to_cnf(self):
        return self

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg
    
    def __hash__(self):
        return hash(self.arg)
    
    def __eq__(self, other):
        return isinstance(other, Not) and self.arg == other.arg
    def __repr__(self):
        return f"Not({repr(self.arg)})"
    def atom_names(self):
        return self.arg.atom_names()
    def evaluate(self, assignment):
        return not self.arg.evaluate(assignment)
    def to_cnf(self):
        if isinstance(self.arg, Atom):
            return self  
        elif isinstance(self.arg, Not):
            
            return self.arg.arg.to_cnf()
        elif isinstance(self.arg, And):
            
            return Or(*[Not(l).to_cnf() for l in self.arg.conjuncts]).to_cnf()
        elif isinstance(self.arg, Or):
            
            return And(*[Not(u).to_cnf() for u in self.arg.disjuncts]).to_cnf()
        else:
            raise NotImplementedError
        
class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts
    
    def __hash__(self):
        return hash(self.conjuncts)
    
    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts
    def __repr__(self):
        s_c = sorted(self.conjuncts, key=lambda a: repr(a))
        return f"And({', '.join(repr(n) for n in s_c)})"
        
    def atom_names(self):
        names = set()

        for conjunct in self.conjuncts:

            names.update(conjunct.atom_names())
        return names
        
    def evaluate(self, assignment):
        return all(c.evaluate(assignment) for c in self.conjuncts)
    def to_cnf(self):
        conjuncts_cnf = []
        for c in self.conjuncts:
            cnf = c.to_cnf()
            if isinstance(cnf, And):
                conjuncts_cnf.extend(cnf.conjuncts)  
            else:
                conjuncts_cnf.append(cnf)
        return And(*conjuncts_cnf) 
        

class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts
    
    def __hash__(self):
        return hash(self.disjuncts)
    def __eq__(self, other):

        return isinstance(other, Or) and self.disjuncts == other.disjuncts
    def __repr__(self):
        s_d = sorted(self.disjuncts, key=lambda a: repr(a))
        return f"Or({', '.join(repr(b) for b in s_d)})"
       
    def atom_names(self):
        names = set()
        for disjunct in self.disjuncts:
            names.update(disjunct.atom_names())
        return names

        
    def evaluate(self, assignment):
        return any(d.evaluate(assignment) for d in self.disjuncts)
    
    def to_cnf(self):
        d = [k.to_cnf() for k in self.disjuncts]
        result = d[0]
        for disjunct in d[1:]:
            result = assign_or(result, disjunct)

    
        return result
    
   

    
        

def assign_or(expression_1, expression_2):
   
    
    if isinstance(expression_1, And) and isinstance(expression_2, And):
        
        conjuncts = []
        for k1 in expression_1.conjuncts:
            for k2 in expression_2.conjuncts:
                or_expression = Or(k1, k2).to_cnf()
                
                if isinstance(or_expression, And):
                    conjuncts.extend(or_expression.conjuncts)
                else:
                    conjuncts.append(or_expression)
        return And(*conjuncts)

    elif isinstance(expression_1, And):
        
        conjuncts = []
        for k in expression_1.conjuncts:
            or_expression = assign_or(k, expression_2)
           
            if isinstance(or_expression, And):
                conjuncts.extend(or_expression.conjuncts)
            else:
                conjuncts.append(or_expression)
        return And(*conjuncts)

    elif isinstance(expression_2, And):
       
        conjuncts = []
        for k in expression_2.conjuncts:
            or_expression = assign_or(expression_1, k)
            
            if isinstance(or_expression, And):
                conjuncts.extend(or_expression.conjuncts)
            else:
                conjuncts.append(or_expression)
        return And(*conjuncts)

    else:
        
        flat = []
        for e in [expression_1, expression_2]:
            if isinstance(e, Or):
                flat.extend(e.disjuncts)
            else:
                flat.append(e)
        return Or(*flat)

    


    
        

        

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    
    def __hash__(self):
        return hash((self.left, self.right))
    def __eq__(self, other):

        return isinstance(other, Implies) and self.left == other.left and self.right == other.right
    def __repr__(self):
        return f"Implies({repr(self.left)}, {repr(self.right)})"
    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())
    def evaluate(self, assignment):
        return not self.left.evaluate(assignment) or self.right.evaluate(assignment)
    def to_cnf(self):
        return Or(Not(self.left).to_cnf(), self.right.to_cnf()).to_cnf()


class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    
    def __hash__(self):
        return hash(self.hashable)
    
    def __eq__(self, other):
          return (isinstance(other, Iff) and 
                (self.left == other.left and self.right == other.right or 
                 self.left == other.right and self.right == other.left))
        
    def __repr__(self):
        return f"Iff({repr(self.left)}, {repr(self.right)})"
    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())
    def evaluate(self, assignment):
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)
    def to_cnf(self):
        l_r = Implies(self.left, self.right).to_cnf()
        r_f = Implies(self.right, self.left).to_cnf()
        return And(l_r, r_f ).to_cnf()
        






print(Atom("a") == Atom("a"))  
print(Atom("a") == Atom("b"))  
print(And(Atom("a"), Not(Atom("b"))) == And(Not(Atom("b")), Atom("a")))  


a, b, c = map(Atom, "abc")
print(Implies(a, Iff(b, c)))
 
a, b, c = map(Atom, "abc")
print(And(a, Or(Not(b), c))) 


print(Atom("a").atom_names())
set(['a'])
print(Not(Atom("a")).atom_names())
set(['a'])

a, b, c = map(Atom, "abc")
expr = And(a, Implies(b, Iff(a, c)))
print(expr.atom_names())
set(['a', 'c', 'b'])

e = Implies(Atom("a"), Atom("b"))

print(e.evaluate({"a": False, "b": True}))

print(e.evaluate({"a": True, "b": False}))


a, b, c = map(Atom, "abc")
e = And(Not(a), Or(b, c))
print(e.evaluate({"a": False, "b": False, "c": True}))



print(Atom("a").to_cnf())
a, b, c = map(Atom, "abc")
print(Iff(a, Or(b, c)).to_cnf())


print(Or(Atom("a"), Atom("b")).to_cnf())
a, b, c, d = map(Atom, "abcd")
print(Or(And(a, b), And(c, d)).to_cnf())





 

import itertools
def satisfying_assignments(expr):
    
    at = sorted(expr.atom_names())
    
    
    for val in itertools.product([False, True], repeat=len(at)):
        asgn = dict(zip(at, val))
        
        
        if expr.evaluate(asgn):
            
            yield asgn

e = Implies(Atom("a"), Atom("b"))
a = satisfying_assignments(e)

print(next(a))

print(next(a))

print(next(a))

e = Iff(Iff(Atom("a"), Atom("b")), Atom("c"))
print(list(satisfying_assignments(e)))


class KnowledgeBase:
    def __init__(self):
        
        self.facts = set()
        
    def get_facts(self):
       
        return self.facts
        
    def tell(self, expr):
       
        cnf_expression = expr.to_cnf()
        d = self.pull_expressions(cnf_expression)
        self.facts.update(d)
        
    def ask(self, query):
        
        nq = Not(query).to_cnf()
        qc = self.pull_clauses(nq)
        
        
        e = set(self.cfe(self.facts))
        e.update(qc)
        
        
        return self.resolution_algo(e)
        
    def pull_expressions(self, expr):
        
        if isinstance(expr, And):
            
            return expr.conjuncts
        else:
            
            return {expr}
        
    def cfe(self, expressions):
        
        g = set()
        for expr in expressions:
            clause = self.pull_clause(expr)
            g.add(clause)
        return g
        
    def pull_clauses(self, expr):
        
        if isinstance(expr, And):
            
            clauses = set()
            for conjunct in expr.conjuncts:
                clause = self.pull_clause(conjunct)
                clauses.add(clause)
            return clauses
        else:
            
            return {self.pull_clause(expr)}
        
    def pull_clause(self, expr):
        
        if isinstance(expr, Or):
            
            k = set()
            for disjunct in expr.disjuncts:
                k.add(self.g_l(disjunct))
            return frozenset(k)
        else:
            
            return frozenset({self.g_l(expr)})
        
    def g_l(self, expr):
        
        if isinstance(expr, Atom):
            return expr
        elif isinstance(expr, Not) and isinstance(expr.arg, Atom):
            return expr
        else:
            raise ValueError(f"{expr}")
        
    def resolution_algo(self, p):
        
        new = set()
        cl_list = list(p)
        
        while True:
            x = len(cl_list)
            pairs = [(cl_list[a], cl_list[b]) for a in range(x) for b in range(a+1, x)]
            for (hi, hj) in pairs:
                r = self.pl_resolve(hi, hj)
                if frozenset() in r:
                    
                    return True
                new.update(r)
            if new.issubset(p):
                
                return False
            p.update(new)
            cl_list.extend(new)
        
    def pl_resolve(self, hi, hj):
       
        r = set()
        for ei in hi:
            for ej in hj:
                if self.is_complement(ei, ej):
                    
                    resolvent = (hi - {ei}) | (hj - {ej})
                    r.add(frozenset(resolvent))
        return r
        
    def is_complement(self, ai, aj):
       
        return (isinstance(ai, Atom) and isinstance(aj, Not) and ai == aj.arg) or \
               (isinstance(ai, Not) and isinstance(aj, Atom) and ai.arg == aj)


    
    


    
    

a, b, c = map(Atom, "abc")
kb = KnowledgeBase()
kb.tell(a)
kb.tell(Implies(a, b))
print(kb.get_facts())
set([Or(Atom(b), Not(Atom(a))),Atom(a)])
print([kb.ask(x) for x in (a, b, c)])


a, b, c = map(Atom, "abc")
kb = KnowledgeBase()
kb.tell(Iff(a, Or(b, c)))

kb.tell(Not(a))
print([kb.ask(x) for x in (a, Not(a))])

print([kb.ask(x) for x in (b, Not(b))])

print([kb.ask(x) for x in (c, Not(c))])


    







############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1


mythical = Atom("mythical")
mortal = Atom("mortal")
immortal = Atom("immortal")
mammal = Atom("mammal")
horned = Atom("horned")
magical = Atom("magical")


kb1 = KnowledgeBase()


kb1.tell(Implies(mythical, immortal))            
kb1.tell(Implies(Not(mythical), And(mortal, mammal)))  
kb1.tell(Implies(Or(immortal, mammal), horned))  
kb1.tell(Implies(horned, magical))               


###mythical_query = mythical
###magical_query = magical
###horned_query = horned


###is_mythical = kb1.ask(mythical_query) 
###is_magical = kb1.ask(magical_query)    
###is_horned = kb1.ask(horned_query)      

###print(f"Is unicorn mythical? {is_mythical}")
###print(f"Is unicorn magical? {is_magical}")
###print(f"Is unicorn horned? {is_horned}")###


# Puzzle-2
a = Atom("a") 
j = Atom("j")  
m = Atom("m")  


party_constraints = And(
    Implies(Or(m, a), j),      
    Implies(Not(m), a),        
    Implies(a, Not(j))        
)

valid_scenarios = list(satisfying_assignments(party_constraints))


for s in valid_scenarios:
    print(s)


puzzle_2_question = """

1. John comes if either Mary or Ann comes.
2. Ann comes if Mary does not come.
3. If Ann comes, then John will not come.



1. {'a': False, 'j': True, 'm': True}:
   - Mary comes (`m=True`), John comes (`j=True`), and Ann does not come (`a=False`).
   - Since Mary is attending, John must attend to satisfy the first condition. Ann does not need to attend.

2. {'a': True, 'j': False, 'm': False}:
   - Ann comes (`a=True`), and both Mary and John do not come (`m=False`, `j=False`).
  

"""

# Puzzle-3

p1 = Atom("p1")  
e1 = Atom("e1")  
p2 = Atom("p2")  
e2 = Atom("e2")  
s1 = Atom("s1")  
s2 = Atom("s2")  


kb3 = KnowledgeBase()


kb3.tell(Implies(s1, And(p1, e2)))

kb3.tell(Implies(s2, And(Or(p1, p2), Or(e1, e2))))


kb3.tell(Iff(s1, Not(s2)))  

kb3.tell(Iff(p1, Not(e1)))  
kb3.tell(Iff(p2, Not(e2)))  


##fr_prize = kb3.ask(p1)
##fr_empty = kb3.ask(e1)


##sr_prize = kb3.ask(p2)
##sr_empty = kb3.ask(e2)


##fs_true = kb3.ask(s1)
##ss_true = kb3.ask(s2)


##print(f"Does the first room contain a prize? {fr_prize}")
##print(f"Is the first room empty? {fr_empty}")
##print(f"Does the second room contain a prize? {sr_prize}")
##print(f"Is the second room empty? {sr_empty}")
##print(f"Is the first sign true? {fs_true}")
##print(f"Is the second sign true? {ss_true}")

puzzle_3_question = """

So basically,we wanna see exactly one of the signs is true. 
And, based on the constraints and queries made to the knowledge base, 
the contestant can then deduce that the prize is in Room 1 or Room 2, 
and if the first or second sign  is true .

"""




#Puzzle-4
ia = Atom("ia") 
ib = Atom("ib")  
ic = Atom("ic")  

ka = Atom("ka") 
kb = Atom("kb")  
kc = Atom("kc")  


kb4 = KnowledgeBase()


kb4.tell(Implies(ia, And(kb, Not(kc))))  
kb4.tell(Implies(ib, Not(kb))) 
kb4.tell(Implies(ic, And(ka, kb)))  


kb4.tell(Or(And(ia, ib, Not(ic)), And(ia, ic, Not(ib)), And(ib, ic, Not(ia))))


g_adam = kb4.ask(Not(ia))
g_brown = kb4.ask(Not(ib))
g_clark = kb4.ask(Not(ic))


print(f"Is Adam guilty? {g_adam}")
print(f"Is Brown guilty? {g_brown}")
print(f"Is Clark guilty? {g_clark}")

if g_adam:
    guilty_suspect = "Adams"
elif g_brown:
    guilty_suspect = "Brown"
elif g_clark:
    guilty_suspect = "Clark"

print(f"The guilty suspect is: {guilty_suspect}")

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
# guilty_suspect = "Brown" **
# guilty_suspect = "Clark"




puzzle_4_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""



############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """


"""

feedback_question_2 = """

"""

feedback_question_3 = """

"""
