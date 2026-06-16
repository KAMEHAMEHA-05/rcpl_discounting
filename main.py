import pandas as pd
from collections import defaultdict

df_customsize = pd.read_excel(
    "customSizeData__15-06-2026.xlsx",
    engine="calamine"
)
df_customsize = df_customsize.to_dict(orient="records")

df_productrate = pd.read_excel(
    "Product_rate 300426.xlsx",
    engine="calamine"
)
df_productrate = df_productrate.to_dict(orient="records")

df_ups = pd.read_excel(
    "UpsRatio.xlsx",
    engine="calamine"
)
df_ups = df_ups.to_dict(orient="records")

# df_final = pd.read_excel(
#     "FinalResult.xlsx",
#     engine="calamine"
# )


# print(df_customsize.head())
# print("-"*100)
# print(df_productrate.head())
# print("-"*100)
# print(df_ups.head())
# print("-"*100) 
# print(df_final.head())

customsize = defaultdict(list)
for row in df_customsize:
    
    key = (row["Media"], row["Std. Qty"])
    value = {
        k: v
        for k, v in row.items()
        if k not in ["Media", "Std. Qty"]
    }

    customsize[key].append(value)

ups = defaultdict(list)
for row in df_ups:
    
    key = (row["Media"], row["Product Size"], row["Ref. Size for Rate"])
    value = row["Ups"]

    ups[key]=value

final_db = []

for row in df_productrate:

    product_title = row["Product Title"]
    rate = row["Rate"]
    media_type = row["Media Type"]
    product_size = row["Product Size"]
    product_quantity = row["Product Quantity"]

    key_customsize = (media_type, product_quantity)
    value_customsize = customsize.get(key_customsize, [])
    if value_customsize:
        ref_size = value_customsize[0].get("Ref. Size for Rate")
        key_ups = (media_type, product_size, ref_size)
        value_ups = ups.get(key_ups)
        if value_ups:
            for item in value_customsize:
                if(item["Ups From"] <= value_ups <= item["Ups To"]):
                    pkg_cost_per_up = item["Pkg. Cost per Up"]
                    discount_rate = item["Basic Discount %"]
                    total_pkg_cost = pkg_cost_per_up * value_ups
                    interim_rate = rate - total_pkg_cost
                    discount_amount = (interim_rate * discount_rate) / 100 
                    final_rate = interim_rate - discount_amount

                    final_db.append({
                        "Product Title": product_title,
                        "Media Type": media_type,
                        "Product Size": product_size,
                        "Product Quantity": product_quantity,
                        "Ref. Size for Rate": ref_size,
                        "Ups": value_ups,
                        "Ref. Size Rate": rate,
                        "New Interim Rate": interim_rate,
                        "Pkg. Cost per Up": pkg_cost_per_up,
                        "Total Pkg. Cost": total_pkg_cost,
                        "Discount %": discount_rate,
                        "Discount Amount": discount_amount,
                        "Final Rate": final_rate
                    })


column_order = [
    "Product Title",
    "Media Type",
    "Product Size",
    "Product Quantity",
    "Ref. Size for Rate",
    "Ups",
    "Ref. Size Rate",
    "New Interim Rate",
    "Pkg. Cost per Up",
    "Total Pkg. Cost",
    "Discount %",
    "Discount Amount",
    "Final Rate",
]

#df_final = pd.concat([df_final, pd.DataFrame(final_db)], ignore_index=True)
df_final = pd.DataFrame(final_db, columns=column_order)
df_final.to_excel("FinalResult.xlsx", index=False)




