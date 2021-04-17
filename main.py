import json

global rules


class InputValue:
    def __init__(self, _value):
        self.value = _value
        self.memberships = exchange_rate_membership(self.value)
        print(self)

    def __str__(self):
        return 'Input value {0} <= {1}'.format(round(self.value, 1), self.memberships)

    def __repr__(self):
        return self.__str__()


class Rule:
    def __init__(self, conditions, conclusion=None, veracity=None):
        self.conditions = conditions
        self.conclusion = conclusion
        self.veracity = veracity

    def __str__(self):
        return 'Rule {0} => {1} ({2})'.format(self.conditions, self.conclusion, self.veracity)

    def __repr__(self):
        return self.__str__()


# функция, определяющая к каким термам принадлежат входные переменные
def exchange_rate_membership(x_value):
    # границы нечеткого определения
    if x_value <= 4:
        value = 1.0
        return {
            'term': 'cheap',
            'membership': round(value, 2)
        }
    if x_value >= 12:
        value = 1.0
        return {
            'term': 'expensive',
            'membership': round(value, 2)
        }

    # нечеткая принадлежность
    _result = []
    if 4 < x_value <= 8:
        value = (8 - x_value) / 4
        _result.append({
            'term': 'cheap',
            'membership': round(value, 2)
        })
    if 6 <= x_value <= 10:
        if x_value <= 8:
            value = (x_value - 6) / 2
        else:
            value = (10 - x_value) / 2
        _result.append({
            'term': 'balanced',
            'membership': round(value, 2)
        })
    if x_value >= 9:
        value = (x_value - 9) / 3
        _result.append({
            'term': 'expensive',
            'membership': round(value, 2)
        })
    return _result


# функция, вычислябщая итоговые степени истинности правил
def input_evaluation(input_values):
    memberships = []
    for value in input_values:
        memberships += value.memberships

    print('> Received {0} input values for evaluation containing overall {1} memberships.'.format(
        len(input_values),
        len(memberships)
    ))
    print('Staring evaluation...')

    _new_rules = []
    for item_one in input_values[0].memberships:
        term_one = item_one['term']
        membership_one = item_one['membership']
        for item_two in input_values[1].memberships:
            term_two = item_two['term']
            membership_two = item_two['membership']
            for item_three in input_values[2].memberships:
                term_three = item_three['term']
                membership_three = item_three['membership']
                for item_four in input_values[3].memberships:
                    term_four = item_four['term']
                    membership_four = item_four['membership']

                    # собираем новое правило
                    new_rule = Rule(conditions=[term_one, term_two, term_three, term_four],
                                    veracity=min(
                                        [membership_one, membership_two, membership_three, membership_four]))
                    _new_rules.append(new_rule)

    print('> Evaluation completed. Attained {0} new computed rules.'.format(len(_new_rules)))

    for rule in _new_rules:
        print(rule)

    return _new_rules


# нормализация вычисленных тоговых степеней предпосылок
def generated_rules_normalization(computed_rules):
    print('Starting normalization of computed rules...')
    for rule in computed_rules:
        rule.veracity = rule.veracity / sum(list(map(lambda x: x.veracity, computed_rules)))

    print('> Normalization completed.')
    for rule in computed_rules:
        print(rule)

    return computed_rules


def generated_rules_determination(normalized_computed_rules):
    print('Staring determination of the final degrees of veracity...')


def fill_rules():
    rules = {'rules': []}
    terms = ['cheap', 'balanced', 'expensive']

    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    rules['rules'].append({
                        'conditions': [
                            terms[i],
                            terms[j],
                            terms[k],
                            terms[l],
                        ],
                        'conclusion': 'none'
                    })

    with open('rules.json', 'w') as json_file:
        json.dump(rules, json_file)


def load_rules():
    _rules = []

    with open('rules.json') as json_file:
        data = json.load(json_file)

        for rule in data['rules']:
            _rules.append(Rule(conditions=rule['conditions'], conclusion=rule['conclusion']))

    return _rules


if __name__ == '__main__':
    debug = True
    rules = load_rules()
    inputValues = []

    if debug:
        inputValues.append(InputValue(float(5.67)))
        inputValues.append(InputValue(float(6.2)))
        inputValues.append(InputValue(float(8.3)))
        inputValues.append(InputValue(float(9.72)))
    else:
        for i in range(4):
            print('Enter {0} day exchange rate (0-12):'.format(i + 1))
            inputValues.append(InputValue(float(input())))

    # print(inputValues)
    generated_rules_normalization(input_evaluation(inputValues))
