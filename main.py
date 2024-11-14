import pandas as pd
from eclat import Eclat
transactions = [
    ['A', 'B', 'D'],
    ['B', 'C', 'E'],
    ['A', 'B', 'C', 'E'],
    ['B', 'E'],
    ['A', 'B', 'C', 'E'],
]

min_support = 2

eclat_instance = Eclat(min_support, 2, transactions)
items = eclat_instance.get_frequent()
for item in items:
    print(item)

frequent_itemsets = eclat_instance.get_frequent()
print("Frequent Itemsets:", frequent_itemsets)
