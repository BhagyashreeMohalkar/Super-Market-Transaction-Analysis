import pandas as pd
from mlxtend.preprocessing import TransactionEncoder


# ----------- FREQUENT PRODUCTS -----------
def get_frequent_products(sample_size=50000, top_n=20):

    order_products = pd.read_csv(
        "data/raw/order_products__prior.csv",
        usecols=['product_id'],     # load only required column
        nrows=sample_size           # limit size
    )

    products = pd.read_csv(
        "data/raw/products.csv",
        usecols=['product_id', 'product_name']
    )

    merged = pd.merge(order_products, products, on="product_id")

    product_counts = merged["product_name"].value_counts().head(top_n)

    result = product_counts.reset_index()
    result.columns = ["Product", "Purchase_Count"]

    return result


# ----------- PREPARE DATA FOR ASSOCIATION RULES -----------
def prepare_data(min_item_frequency=50, sample_size=50000):

    print("Loading dataset...")

    order_products = pd.read_csv(
        "data/raw/order_products__prior.csv",
        usecols=['order_id', 'product_id'],  # only needed columns
        nrows=sample_size                    # LIMIT DATA
    )

    products = pd.read_csv(
        "data/raw/products.csv",
        usecols=['product_id', 'product_name']
    )

    print("Merging...")
    merged = pd.merge(order_products, products, on='product_id')

    print("Creating transactions...")
    transactions = merged.groupby('order_id')['product_name'].apply(list)

    print("Encoding...")
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    basket = pd.DataFrame(te_array, columns=te.columns_)

    print("Filtering items...")
    item_counts = basket.sum(axis=0)
    frequent_items = item_counts[item_counts >= min_item_frequency].index
    basket = basket[frequent_items]

    print("Done!")

    return basket