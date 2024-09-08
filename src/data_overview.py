import pandas as pd

rest_data = pd.read_csv('data/summary_150_10_10000.csv')
grpc_data = pd.read_csv('data/summary_150_10_10000_grpc.csv')
tum_live_errors_data = pd.read_csv('./data/TUM-Live Service errors-data-2024-08-11 23_35_47.csv')
general_errors_data = pd.read_csv('./data/Errors-data-2024-08-11 23_48_43.csv')

rest_data = rest_data[rest_data['elapsed'] > 100]
grpc_data = grpc_data[grpc_data['elapsed'] > 100]

def print_overview(df, name):
    print(f"Overview of {name}:")
    print(f"Number of records: {len(df)}")
    print("Columns and data types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isnull().sum())
    print("\nDescriptive statistics:")
    print(df.describe(include='all'))
    print("\n" + "="*50 + "\n")

print_overview(rest_data, "REST Data")
print_overview(grpc_data, "gRPC Data")
print_overview(tum_live_errors_data, "TUM-Live Service Errors Data")
print_overview(general_errors_data, "General Errors Data")