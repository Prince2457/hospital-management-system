import os

if not os.path.exists("reports"):
    os.makedirs("reports")

filepath = os.path.join("reports", "test_report.csv")

with open(filepath, "w") as f:
    f.write("hello")