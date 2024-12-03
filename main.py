import pandas as pd

from collections import defaultdict
import matplotlib.pyplot as plt


class Eclat:
    def __init__(self, min_sup, min_conf, transactions):
      #  print(len(transactions))
        self.min_sup = int(min_sup * len(transactions))
        self.min_conf = min_conf
        self.transactions = transactions
        self.frequent_itemsets = defaultdict(list)
        self.vertical_items = defaultdict(set)
        self.DFS()

    def calc(self, tids):
        # print("len",len(self.transactions))
        return len(tids) / len(self.transactions) if len(self.transactions) > 0 else 0

    def DFS(self):  # convert to vertical and generate freq using using dfs algo
        vertical_db = defaultdict(set)
        for tid, items in enumerate(self.transactions, start=1):
            for item in items:
                if isinstance(item, float):
                    continue
                vertical_db[item].add(tid)

        self.vertical_items = vertical_db

        for item, tids in vertical_db.items():
            if len(tids) >= self.min_sup:
                self.generate_frequent({item}, tids)

    def generate_frequent(self, items, tids):
        self.frequent_itemsets[len(items)].append((frozenset(items), tids))

        for new_item, new_tids in self.vertical_items.items():
            if all(i < new_item for i in items):
                intersection = tids.intersection(new_tids)
                if len(intersection) >= self.min_sup:
                    self.generate_frequent(items | {new_item}, intersection)

    def get_frequent(self):
        return self.frequent_itemsets

    def calculate_lift(self):
        lift_values = []

        for size, itemsets in self.frequent_itemsets.items():
            if size == 1:
                continue

            for items, tids in itemsets:
                # if items=={'K','M'}:
                #     print("check")
                #     print(items , tids)
                items_set = set(items)
                for antecedent in items_set:
                    consequent = items_set - {antecedent}

                    support_ab = self.calc(tids)
                    support_a = self.calc(self.vertical_items[antecedent])
                    support_b = self.calc(self.vertical_items[next(iter(consequent))])

                    lift = support_ab / (support_a * support_b) if support_a > 0 and support_b > 0 else 0

                    lift_values.append((frozenset([antecedent]), frozenset(consequent), lift))

        return lift_values

    def calculate_strong_rules(self):
        strong_rules = []

        for size, itemsets in self.frequent_itemsets.items():
            if size == 1:
                continue

            for items, tids in itemsets:
                items_set = set(items)
                for antecedent in items_set:
                    consequent = items_set - {antecedent}

                    if not consequent:
                        continue

                    antecedent_tids = self.vertical_items[antecedent]
                    consequent_tids = set.intersection(*[self.vertical_items[item] for item in consequent])
                  #  print("ant ids ",antecedent_tids)
                  #  print("cont ids " , consequent_tids)

                    intersection = antecedent_tids.intersection(consequent_tids)
                   # print("int ids ", intersection)
                    confidence = len(intersection) / len(antecedent_tids) if len(antecedent_tids) > 0 else 0

                    if confidence >= self.min_conf:
                        strong_rules.append((frozenset([antecedent]), frozenset(consequent), confidence))

        return strong_rules


excel_file = "trans.xlsx"
df = pd.read_excel(excel_file, header=None, skiprows=1, names=['TiD', 'items'])

df['items'] = df['items'].apply(lambda x: x.split(',') if isinstance(x, str) else [])

print("Transactions:")
for tid, items in zip(df['TiD'], df['items']):
    print(f"TID {tid}: {items}")

min_support = float(input("enter min support "))
min_confidence = float(input("enter min confidence "))
transactions = df['items'].tolist()

eclat = Eclat(min_support, min_confidence, transactions)

frequent_itemsets = eclat.get_frequent()
print("\nFrequent Itemsets:")
for size, itemsets in frequent_itemsets.items():
    print(f"\n{size}-itemsets:")
    for itemset, tids in itemsets:
        print(f"Itemset: {itemset}, TIDs: {tids}")

lift_values = eclat.calculate_lift()
print("\nLift Values:")
for antecedent, consequent, lift in lift_values:
    print(f"{antecedent} -> {consequent}, Lift: {lift}")

strong_rules = eclat.calculate_strong_rules()
print("\nStrong Association Rules:")
for antecedent, consequent, confidence in strong_rules:
    print(f"Rule: {antecedent} -> {consequent}, Confidence: {confidence:.2f}")

itemsets_df = pd.DataFrame(
    [(frozenset(item), len(tids)) for size, itemsets in frequent_itemsets.items() for item, tids in itemsets],
    columns=['Itemsets', 'Support'])
itemsets_df['Itemsets'] = itemsets_df['Itemsets'].apply(lambda x: ', '.join(sorted(list(x))))

plt.figure(figsize=(10, 6))
plt.bar(itemsets_df['Itemsets'], itemsets_df['Support'], color='pink', width=0.6)
plt.xlabel('Itemsets')
plt.ylabel('Support')
plt.title('Frequent Itemsets and Their Support')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
