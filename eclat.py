from collections import defaultdict

class Eclat:
    def __init__(self, min_sup, min_conf, transactions):
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.transactions = transactions
        self.frequent_items = []
        self.vertical_items = defaultdict(set)

    def fit(self):
        vertical_db = defaultdict(set)
        for tid, items in enumerate(self.transactions):
            for item in items:
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
        self.fit()
        return self.frequent_items


