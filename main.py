import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#load data set
try:
    data = pd.read_csv("sales_data.csv")
    data.columns = data.columns.str.strip()  # Remove leading/trailing spaces from column names
    print("\nDATA LOADED SUCCESSFULLY!!!\n")
except FileNotFoundError:
    print("sales_data.csv FILE NOT FOUND!!")
    exit()

#data cleaning
data.dropna(inplace = True)

#remove duplicate rows
data.drop_duplicates(inplace = True)

#calculation
data['Total_sales'] = data["Price"] * data["Quantity"]

#discount 
if "Discount" in data.columns:
    data["Final Amount"] = (
        data["Total_sales"] - (data["Total_sales"] * data["Discount"]/100)
    )
else:
    data["Final Amount"] = data["Total_sales"]

#dispay Data
print("==========E-COMMERCE SALES DATA ANALYSIS==========")
print(data)

#Statistics
total_orders = len(data)
total_revenue = data["Final Amount"].sum()
average_order_value = data["Final Amount"].mean()
highest_sale = data["Final Amount"].max()
lowest_sale = data["Final Amount"].min()

print("\n==========STATISTICS==========")
print(f"Total Orders: {total_orders}")
print(f"Total Revenue: ₹{total_revenue:.2f}")
print(f"Average Order Value: ₹{average_order_value:.2f}")
print(f"Highest Sale: ₹{highest_sale:.2f}")
print(f"Lowest Sale: ₹{lowest_sale:.2f}")

#Top product
top_products = (
    data.groupby("Product")["Quantity"].sum().sort_values(ascending = False)
)

print("==========TOP PRODUCTS==========")
for product, quantity in top_products.items():
    print(f"{product}: {quantity} units sold")

#category revenue
category_revenue = (
    data.groupby("Category")["Final Amount"].sum().sort_values(ascending = False)
)

print("\n==========CATEGORY REVENUE==========")
for category, revenue in category_revenue.items():
    print(f"{category}: ₹{revenue:.2f}")

#profit product
product_revenue = (
    data.groupby("Product")["Final Amount"].sum()
)

best_product = product_revenue.idxmax()

print("\nMost Profitable product: ",best_product)
print(f"{best_product}-->₹{product_revenue.max():.2f}")

#save to file
current_date = datetime.now().strftime("%d-%m-%Y")
with open(f"sales_report.txt","w",encoding = "utf-8") as file:
    file.write("==========E-COMMERCE SALES DATA ANALYSIS==========\n")
    file.write(f"Total Orders: {total_orders}\n")
    file.write(f"Total Revenue: ₹{total_revenue:.2f}\n")
    file.write(f"Average Order Value: ₹{average_order_value:.2f}\n")
    file.write(f"Highest Sale: ₹{highest_sale:.2f}\n")
    file.write(f"Lowest Sale: ₹{lowest_sale:.2f}\n\n")    
    file.write("=====TOP PRODUCTS=====\n")
    for product, quantity in top_products.items():
        file.write(f"{product}: {quantity} units sold\n")
    file.write("\n\n")
    file.write("=====CATEGORY WISE REVENUE=====\n")
    for category, revenue in category_revenue.items():
        file.write(f"{category}: ₹{revenue:.2f}\n")
    file.write("\n\n")
    file.write(f"MOST PROFITABLE PRODUCT: {best_product} --> ₹{product_revenue.max():.2f}")

    print("\nSALES REPORT SAVED SUCCESSFULLY!!!")

#chart 1-->PRODUCT SALES (BAR CHART)
plt.figure(figsize = (10,6))
top_products.plot(kind = "bar")
plt.title("TOP SELLING PRODUCT")
plt.xlabel("PRODUCTS")
plt.ylabel("UNITS SOLD")
plt.xticks(rotation = 25)
plt.tight_layout()
plt.savefig("top_selling_product_chart.png")

#chart 2-->CATEGORY REVENUE(PIE CHART)
plt.figure(figsize = (8,8))
category_revenue.plot(kind = "pie", autopct = "%1.1f%%")
plt.ylabel("")
plt.title("CATEGORY_WISE REVENUE CHART")
plt.tight_layout()
plt.savefig("category_revenue_chart.png")

#chart 3-->REVENUE DISTRIBUTION (LINE CHART)
plt.figure(figsize = (10,5))
data["Final Amount"].plot(kind = "line", marker = "o")
plt.title("REVENUE DISTURIBUTION PER UNIT")
plt.xlabel("ORDER NUMBER")
plt.ylabel("REVENUE(₹)")
plt.grid(True)
plt.savefig("revenue_distribution_chart.png")

plt.show()

print("==========ANALYSED SUCCESSFULLY!!!==========")
