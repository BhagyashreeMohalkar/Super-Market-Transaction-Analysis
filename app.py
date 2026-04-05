from flask import Flask, render_template, request
from models.preprocessing import prepare_data, get_frequent_products
from models.apriori_model import run_apriori
from models.fpgrowth_model import run_fpgrowth

app = Flask(__name__)

print("Preparing dataset...")
basket = prepare_data(sample_size=50000)   # LIMIT SIZE HERE
print("Dataset ready!")


@app.route("/")
def home():
    top_products = get_frequent_products(sample_size=50000)
    return render_template(
        "index.html",
        top_products=top_products.to_html(classes="styled-table", index=False)
    )


@app.route("/run", methods=["POST"])
def run_algorithm():

    apriori_rules, apriori_time = run_apriori(basket)
    fpgrowth_rules, fpgrowth_time = run_fpgrowth(basket)

    algorithm = request.form["algorithm"]

    if algorithm == "apriori":
        rules = apriori_rules
        exec_time = apriori_time
    else:
        rules = fpgrowth_rules
        exec_time = fpgrowth_time

    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

    rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    rules = rules.sort_values(by="lift", ascending=False).head(10)

    recommendations = [
        f"If customer buys {row['antecedents']}, recommend {row['consequents']} (Lift: {round(row['lift'],2)})"
        for _, row in rules.iterrows()
    ]

    rule_labels = rules['antecedents'].tolist()
    rule_lifts = rules['lift'].tolist()

    return render_template(
        "results.html",
        tables=[rules.to_html(classes="styled-table", index=False)],
        exec_time=exec_time,
        algorithm=algorithm,
        recommendations=recommendations,
        apriori_time=apriori_time,
        fpgrowth_time=fpgrowth_time,
        rule_labels=rule_labels,
        rule_lifts=rule_lifts
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False) 