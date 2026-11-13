#gpu list-- what we will monitor

import pandas as pd



gpu_products = [
    {"manufacturer": "NVIDIA", "model": "GeForce RTX 5090"},
    {"manufacturer": "NVIDIA", "model": "GeForce RTX 5080"},
    {"manufacturer" : "NVIDIA", "model": "GeForce RTX 5070"},
    {"manufacturer": "NVIDIA", "model": "GeForce RTX 5060"},
    {"manufacturer": "AMD", "model": "Radeon RX 9070 XT"},
    {"manufacturer": "AMD", "model": "Radeon RX 9070"},
    {"manufacturer": "AMD", "model": "Radeon RX 9060 XT"}
    ]

#convert the list into a pandas dataframe (table)
gpu_catalog = pd.DataFrame(gpu_products)

#display the gpu catalog
print(gpu_catalog)

# save the catalog as a csv file
gpu_catalog.to_csv("gpu_catalog.csv", index=False)

print("\nGPU catalog saved as gpu_catalog.csv")


