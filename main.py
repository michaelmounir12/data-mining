import math

import pandas as pd
from eclat import Eclat

excel_file = "trans.xlsx"

transactions = pd.read_csv
data = pd.read_excel(excel_file, header=None)

transactions = data.values.tolist()

min_support = 2

eclat_instance = Eclat(min_support, 2, transactions)
items = eclat_instance.get_frequent()
for item in items:
    print(item)

frequent_itemsets = eclat_instance.get_frequent()
print("Frequent Itemsets:", frequent_itemsets)

lift_values = eclat_instance.calculate_lift()
print("lift values : ")
for antecedent, consequent, lift in lift_values:
    print(f"Antecedent: {antecedent}, Consequent: {consequent}, Lift: {lift}")

eclat_instance.association_representation()

confidence_values = eclat_instance.calculate_confidence()
print("Confidence Values:")
for antecedent, consequent, confidence in confidence_values:
    print(f"Antecedent: {antecedent}, Consequent: {consequent}, Confidence: {confidence}")
