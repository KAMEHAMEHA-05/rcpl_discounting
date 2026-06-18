from pandas import DataFrame, read_excel
from collections import defaultdict
from tqdm import tqdm
from sys import argv

def extract_code(product_title):
    return "-".join(product_title.split("-")[2:8])


def process_data(customsize_path = "CustomSizeData.xlsx", productrate_path = "ProductRate.xlsx", ups_path = "ProductWiseUps.xlsx", final_path = "FinalResult.xlsx", error_path = "Error.xlsx"):
    
    df_customsize = read_excel(
        customsize_path,
        engine="calamine"
    )
    df_customsize = df_customsize.to_dict(orient="records")

    df_productrate = read_excel(
        productrate_path,
        engine="calamine"
    )
    df_productrate = df_productrate.to_dict(orient="records")

    df_ups = read_excel(
        ups_path,
        engine="calamine"
    )
    df_ups = df_ups.to_dict(orient="records")

    customsize = defaultdict(list)
    for row in df_customsize:
        
        key = (row["Media"], row["Std. Qty"], row["Ref. Size for Rate"])
        value = {
            k: v
            for k, v in row.items()
            if k not in {"Media", "Std. Qty", "Ref. Size for Rate"}
        }

        customsize[key].append(value)

    ups = defaultdict(list)
    for row in df_ups:
        
        key = (row["Media"], row["Product Size"])
        value = {
            k: v
            for k, v in row.items()
            if k not in {"Media", "Product Size"}
        }

        ups[key]=value

    productrate = defaultdict(list)
    for row in df_productrate:

        product_title = row["Product Title"]
        product_size = row["Product Size"]

        code = extract_code(product_title)
        key = (code, product_size)
        value = {"Product Title": product_title, "Rate": row["Rate"]}

        productrate[key] = value



    final_db = []
    error_db = []

    for row in tqdm(df_productrate):

        media_type = row["Media Type"]
        product_size = row["Product Size"]

        key_ups = (media_type, product_size)
        value_ups = ups.get(key_ups)

        if value_ups:
            ref_size = value_ups.get("Ref. Size for Rate")
            ups_value = value_ups.get("Ups")
            product_title = row["Product Title"]
            code = extract_code(product_title)
            #print("Code:", code)
            key_productrate = (code, ref_size)
            value_productrate = productrate.get(key_productrate)
            if not value_productrate: 
                error_db.append({
                    "Product Title": product_title,
                    "Status": "N"
                })
                continue

            rate = value_productrate.get("Rate")
            if(rate == 0):
                error_db.append({
                    "Product Title": product_title,
                    "Status": "0"
                })
                continue

            total_rate = rate * ups_value
            min_title = value_productrate.get("Product Title")

            product_quantity = row["Product Quantity"]
            key_customsize = (media_type, product_quantity, ref_size)
            value_customsize = customsize.get(key_customsize, [])

            pkg_cost_per_up = 0
            discount_rate = 0

            if value_customsize:
                for item in value_customsize:
                    if(item["Ups From"] <= ups_value <= item["Ups To"]):
                        pkg_cost_per_up = item["Pkg. Cost per Up"]
                        discount_rate = item["Basic Discount %"]
                        break

            total_pkg_cost = pkg_cost_per_up * ups_value
            interim_rate = total_rate - total_pkg_cost
            discount_amount = (interim_rate * discount_rate) / 100 
            final_rate = interim_rate - discount_amount

            final_db.append({
                "Product Title": product_title,
                "Min Product Title": min_title,
                "Media Type": media_type,
                "Product Size": product_size,
                "Product Quantity": product_quantity,
                "Ref. Size for Rate": ref_size,
                "Ups": ups_value,
                "Ref. Size Rate": rate,
                "Total Ups Value": total_rate,
                "Pkg. Cost per Up": pkg_cost_per_up,
                "Total Pkg. Cost": total_pkg_cost,
                "New Interim Rate": interim_rate,
                "Discount %": discount_rate,
                "Discount Amount": discount_amount,
                "Final Rate": final_rate,
                "Rounded Final Rate": round(final_rate, 0)
            })


    column_order_result = [
        "Product Title",
        "Min Product Title",
        "Media Type",
        "Product Size",
        "Product Quantity",
        "Ref. Size for Rate",
        "Ups",
        "Ref. Size Rate",
        "Total Ups Value",
        "Pkg. Cost per Up",
        "Total Pkg. Cost",
        "New Interim Rate",
        "Discount %",
        "Discount Amount",
        "Final Rate",
        "Rounded Final Rate"
    ]

    column_order_error = [
        "Product Title",
        "Status"
    ]

    df_final = DataFrame(final_db, columns=column_order_result)
    df_final.to_excel(final_path, index=False)

    df_error = DataFrame(error_db, columns=column_order_error)
    df_error.to_excel(error_path, index=False)


if __name__ == "__main__":

    args = argv[1:]

    process_data(*args)




