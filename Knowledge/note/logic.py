from itertools import product
from abc import ABC, abstractmethod


class Sentence(ABC):
    def __init__(self, sentence, operands):
        self.sentence = sentence
        self.operands = operands

    @abstractmethod
    def eval(self):
        pass

    def get_operands(self):
        result_set = set()
        for i in self.operands:
            result_set |= i.get_operands()
        return result_set


class Assert(Sentence):
    def __init__(self, sentence):
        super().__init__(sentence, self)
        self.__truthy = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.sentence

    def get_operands(self):
        return {self.sentence}

    def eval(self, model=None):
        if model is None:
            return self.__truthy
        return model.get(self.sentence) is self.__truthy


class And(Sentence):
    def __init__(self, *args: Sentence):
        super().__init__('All of ' + ' & '.join([str(i) for i in args]), [proposition for proposition in args])

    def __str__(self):
        return f'({self.sentence})'

    def eval(self, model=None):
        return all([i.eval(model) for i in self.operands])


class Or(Sentence):
    def __init__(self, *args: Sentence):
        super().__init__(
            'Either ' + ' or '.join([str(i) for i in args]), [proposition for proposition in args]
        )

    def __str__(self):
        return f'({self.sentence})'

    def eval(self, model=None):
        return any([i.eval(model) for i in self.operands])


class Not(Sentence):
    def __init__(self, statement: Sentence):
        super().__init__(f'~{statement.sentence}', [statement])

    def __str__(self):
        return self.sentence

    def eval(self, model=None):
        return not self.operands[0].eval(model)


class Imply(Sentence):
    def __init__(self, antecedent, consequent):
        super().__init__(f'IF [{antecedent}] THEN {consequent}', [antecedent, consequent])

    def __str__(self):
        return self.sentence

    def eval(self, model=None):
        if self.operands[0].eval(model):
            return self.operands[1].eval(model)
        else:
            return True


class BiCondition(Sentence):
    def __init__(self, antecedent, consequent):
        super().__init__(f'{consequent} IF AND ONLY IF {antecedent}', [antecedent, consequent])

    def __str__(self):
        return self.sentence

    def eval(self, model=None):
        # TODO: Check
        if self.operands[1].eval(model):
            return self.operands[0].eval(model)
        else:
            return not self.operands[0].eval(model)


class KnowledgeBase:
    def __init__(self):
        self.operands = set()
        self.knowledge = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"""
         \rKNOWLEDGE BASE\n{'+=' * 8}\nFACTS\n{'--' * 8}\n{'\n'.join([f'{k}' for k in self.knowledge] or ['No Facts'])}
         \r{'+=' * 8}\nRULES\n{'--' * 8}\n{'\n'.join([f'{k}' for k in self.rules or ['No Rules']])}
        """

    def add_k(self, *args):
        for k in args:
            self.operands |= k.get_operands()
            self.knowledge.append(k)

    def get_facts(self):
        return {
            fact.operands.sentence: fact.eval()
            for fact in self.knowledge
            if isinstance(fact.operands, Assert)
        } if self.knowledge else {}

    def eval(self, model):
        return all([knowledge.eval(model) for knowledge in self.knowledge])


def model_checking(_kb: KnowledgeBase, query: Sentence):
    propositions = _kb.operands
    if query.get_operands() & propositions:
        model = _kb.get_facts()
        unknown_facts = [proposition for proposition in propositions if proposition not in model]
        enums = product((True, False), repeat=len(unknown_facts))

        for combination in enums:
            model.update(list(zip(unknown_facts, combination)))
            if _kb.eval(model):
                if not query.eval(model):
                    return print(f'{str(query)} is False based on known knowledge')

        print(f'{str(query)} is True based on known knowledge ')
    else:
        print(f"No inference can be made because the knowledge base dose not make any observation for {query}")


rain = Assert('rain')  # it is raining
uniben = Assert('uniben')  # israel went to uniben
lagos = Assert('lagos')  # israel went to lagos

kb = KnowledgeBase()
kb.add_k(lagos, Not(And(uniben, lagos)), Imply(Not(rain), uniben), Or(uniben, lagos))
model_checking(kb, uniben)

#  TEST


# print(Or(rain, Not(And(uniben, lagos)), Imply(rain, uniben)).get_operands())
