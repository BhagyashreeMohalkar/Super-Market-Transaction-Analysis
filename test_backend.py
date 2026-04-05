from models.preprocessing import prepare_data, get_frequent_products
from models.apriori_model import run_apriori
from models.fpgrowth_model import run_fpgrowth


print("==========================================")
print("TESTING BACKEND - SUPERMARKET ANALYSIS")
print("==========================================\n")


# -------------------------------------------------
# 1️⃣ TEST FREQUENT PRODUCTS
# -------------------------------------------------
print("Fetching Top Frequently Bought Products...\n")

top_products = get_frequent_products()

print(top_products)
print("\n")


# -------------------------------------------------
# 2️⃣ PREPARE DATA FOR ASSOCIATION RULES
# -------------------------------------------------
print("Preparing Transaction Dataset...\n")

basket = prepare_data()

print("Dataset Shape:", basket.shape)
print("\n")


# -------------------------------------------------
# 3️⃣ RUN APRIORI
# -------------------------------------------------
print("Running Apriori Algorithm...\n")

apriori_rules, apriori_time = run_apriori(basket)

# Make readable
apriori_rules['antecedents'] = apriori_rules['antecedents'].apply(lambda x: ', '.join(list(x)))
apriori_rules['consequents'] = apriori_rules['consequents'].apply(lambda x: ', '.join(list(x)))

apriori_rules = apriori_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]

print("Apriori Execution Time:", apriori_time, "seconds\n")
print("Top 5 Apriori Rules:\n")
print(apriori_rules.head())
print("\n")


# -------------------------------------------------
# 4️⃣ RUN FP-GROWTH
# -------------------------------------------------
print("Running FP-Growth Algorithm...\n")

fpgrowth_rules, fpgrowth_time = run_fpgrowth(basket)

# Make readable
fpgrowth_rules['antecedents'] = fpgrowth_rules['antecedents'].apply(lambda x: ', '.join(list(x)))
fpgrowth_rules['consequents'] = fpgrowth_rules['consequents'].apply(lambda x: ', '.join(list(x)))

fpgrowth_rules = fpgrowth_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]

print("FP-Growth Execution Time:", fpgrowth_time, "seconds\n")
print("Top 5 FP-Growth Rules:\n")
print(fpgrowth_rules.head())
print("\n")


# -------------------------------------------------
# 5️⃣ PERFORMANCE SUMMARY
# -------------------------------------------------
print("==========================================")
print("ALGORITHM PERFORMANCE SUMMARY")
print("==========================================")

print("Apriori Time:", apriori_time, "seconds")
print("FP-Growth Time:", fpgrowth_time, "seconds")

if fpgrowth_time < apriori_time:
    print("Result: FP-Growth is faster than Apriori.")
else:
    print("Result: Apriori is faster than FP-Growth.")