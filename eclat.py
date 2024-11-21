from collections import defaultdict


class Eclat:
    def __init__(self, min_sup, min_conf, transactions):
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.transactions = transactions
        self.frequent_items = []
        self.vertical_items = defaultdict(set)
        self.fit()

    def fit(self):
        vertical_db = defaultdict(set)
        for tid, items in enumerate(self.transactions):
            for item in items:
                if isinstance(item, float):
                    continue
                vertical_db[item].add(tid)
        self.vertical_items = vertical_db
        for item, tids in vertical_db.items():
            if len(tids) >= self.min_sup:
                self.generate_frequent({item}, tids)

    def generate_frequent(self, items, tids):
        self.frequent_items.append((items, tids))

        for new_item, new_tids in self.vertical_items.items():
            if all(i < new_item for i in items):
                intersection = tids.intersection(new_tids)
                if len(intersection) >= self.min_sup:
                    self.generate_frequent(items | {new_item}, intersection)

    def get_frequent(self):
        return self.frequent_items

    def calculate_confidence(self):
        confidence_values = []

        for items, tids in self.frequent_items:
            if len(items) == 1:
                continue
        for antecedent in items:
            consequent = items - {antecedent}
            antecedent_tids = self.vertical_items[antecedent]
            consequent_tids = self.vertical_items[frozenset(consequent)]
            intersection = antecedent_tids.intersection(consequent_tids)
            confidence = len(intersection) / len(antecedent_tids) if len(antecedent_tids) > 0 else 0
            confidence_values.append((({antecedent}), (consequent), confidence))
        return confidence_values

    def association_representation(self):
        association_rules = []
        for items, tids in self.frequent_items:
            if len(items) > 1:
                for antecedent in items:
                    consequent = items - {antecedent}
                    antecedent_tids = self.vertical_items[antecedent]
                    consequent_tids = self.vertical_items[consequent]
                    print(f"{antecedent_tids}->{consequent_tids}")

    def calculate_lift(self):
        num_of_trans = len(self.transactions)
        lift_values = []
        for items, tids in self.frequent_items:
            if len(items) > 1:
                for antecedent in items:
                    consequent = items - {antecedent}
                    # calc support
                    supp_a = len(self.vertical_items[antecedent]) / num_of_trans
                    supp_b = len(set.intersection(*[self.vertical_items[item] for item in consequent])) / num_of_trans
                    supp_ab = len(tids) / num_of_trans
                    # calc lift
                    lift = supp_ab / (supp_b * supp_a) if supp_b > 0 and supp_a > 0 else 0

                    lift_values.append(({antecedent}, consequent, lift))
        return lift_values
