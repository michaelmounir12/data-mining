import math

import pandas as pd
from eclat import Eclat
excel_file = "trans.xlsx"

transactions =pd.read_csv
data = pd.read_excel(excel_file, header=None)

transactions = data.values.tolist()

min_support = 2

eclat_instance = Eclat(min_support, 2, transactions)
items = eclat_instance.get_frequent()
for item in items:
    print(item)

frequent_itemsets = eclat_instance.get_frequent()
print("Frequent Itemsets:", frequent_itemsets)
