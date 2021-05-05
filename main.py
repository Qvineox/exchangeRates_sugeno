import json

input_variables = []


def load_rules():
    _rules = []

    with open('rules.json') as json_file:
        data = json.load(json_file)

        for rule in data['rules']:
            _rules.append({
                'conditions': rule['conditions'],
                'conclusion': rule['conclusion']
            })

    return _rules


class FuzzificationNeuron:
    def __init__(self, center, width):
        self.center = float(center)
        self.width = float(width)

    def quantify(self, value):
        result = round((1 / (1 + pow(pow((value - self.center), 2), self.width))), 4)
        return result


class AgregationNeuron:
    @staticmethod
    def compute(values):
        result = min(values)
        return result


class NormalizationNeuron:
    def __init__(self, total):
        self.total = round(total, 4)

    def normalize(self, value):
        result = value / self.total
        return round(result, 4)


class DefuzzifactionNeuron:
    global input_variables

    def __init__(self):
        self.rules = load_rules()

    def defuzzification(self, value, terms):
        power_rule = next(
            item for item in self.rules if item["conditions"] == terms)

        x1, x2, x3, x4 = tuple(input_variables)

        result = value * eval(power_rule['conclusion'])
        return round(result, 4)


# Layer 1 is the input variables, fuzzy sets. Each node in layer 1 fits a function parameter.
def fuzzification_layer():
    global input_variables
    print("0 LAYER: {0}".format(input_variables))

    cheap_fuzzificator = FuzzificationNeuron(9, 1.9)
    fair_fuzzificator = FuzzificationNeuron(10.5, 1.3)
    expensive_fuzzificator = FuzzificationNeuron(12, 1.5)

    results = []

    # 12 Nodes of Layer 1
    for x in input_variables:
        results.append([
            {'membership': cheap_fuzzificator.quantify(x), 'term': 'cheap'},
            {'membership': fair_fuzzificator.quantify(x), 'term': 'fair'},
            {'membership': expensive_fuzzificator.quantify(x), 'term': 'expensive'}
        ])

    print("1 LAYER: {0}".format(results))
    return results


# Layer 2 computes any two memberships acquired by the fuzzy sets to characterize the fuzzy rules.
def agregation_layer(fuzzificated_values):
    agregator = AgregationNeuron

    results = []
    # 81 Node of Layer 2
    for x1 in fuzzificated_values[0]:
        for x2 in fuzzificated_values[1]:
            for x3 in fuzzificated_values[2]:
                for x4 in fuzzificated_values[3]:
                    results.append(
                        {'value': agregator.compute(
                            [x1['membership'], x2['membership'], x3['membership'], x4['membership']]),
                            'terms': [x1['term'], x2['term'], x3['term'], x4['term']]})

    print("2 LAYER: (amount: {0}) {1}".format(len(results), results))
    return results


# Each node in layer 3 is fixed or non-adaptive. Outputs of this layer are called normalized firing strengths.
def normalization_layer(agregated_values):
    normalizator = NormalizationNeuron(sum(item['value'] for item in agregated_values))

    results = []
    # 81 Node of Layer 3
    for x in agregated_values:
        results.append({'value': normalizator.normalize(x['value']), 'terms': x['terms']})

    print("3 LAYER: (sum: {0}) {1}".format(normalizator.total, results))
    return results


# Each node fits an output in layer 4. The parameters in layer 4 are returned as the following parameters.
def defuzzification_layer(normalized_variables):
    defuzzificator = DefuzzifactionNeuron()

    results = []
    for x in normalized_variables:
        results.append(defuzzificator.defuzzification(x['value'], x['terms']))

    print("4 LAYER: (amount: {0}) {1}".format(len(results), results))
    return results


# Layer 5 is the last layer and contains only one node. In this layer, the single node is a non-adaptive or fixed node.
def summary_layer(defuzzificated_variables):
    result = round(sum(defuzzificated_variables), 2)

    print("5 LAYER: {0}".format(result))
    return result


if __name__ == '__main__':
    input_variables = [11.5, 11.9, 10.2, 10.6]
    summary_layer(defuzzification_layer(normalization_layer(agregation_layer(fuzzification_layer()))))
