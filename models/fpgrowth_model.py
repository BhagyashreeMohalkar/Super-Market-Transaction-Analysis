from mlxtend.frequent_patterns import fpgrowth, association_rules
import time


def run_fpgrowth(basket, min_support=0.01, min_confidence=0.3):

    start_time = time.time()

    frequent_itemsets = fpgrowth(
        basket,
        min_support=min_support,
        use_colnames=True
    )

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence
    )

    end_time = time.time()
    execution_time = round(end_time - start_time, 2)

    rules = rules.sort_values(by="lift", ascending=False)

    return rules, execution_time