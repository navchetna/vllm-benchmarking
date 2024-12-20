import os
import json
import pandas as pd

def collect_json_data(base_dir, output_csv):
    """
    Collects all JSON files ending with 'summary.json' in the directory tree,
    extracts their data, and writes it to a CSV file.

    Args:
        base_dir (str): The base directory to start searching from.
        output_csv (str): The path to the output CSV file.
    """
    data = []

    # Walk through the directory tree
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith("summary.json"):
                json_path = os.path.join(root, file)
                
                # Read and load the JSON file
                try:
                    with open(json_path, "r") as f:
                        json_data = json.load(f)
                        
                        # Add the data along with the file path
                        json_data["source_file"] = json_path
                        data.append(json_data)
                except Exception as e:
                    print(f"Error reading {json_path}: {e}")

    # Convert the list of dictionaries to a DataFrame
    if data:
        df = pd.DataFrame(data)
        data = df[["model", "mean_input_tokens", "mean_output_tokens","num_concurrent_requests", "results_ttft_s_quantiles_p90", "results_end_to_end_latency_s_quantiles_p90","results_mean_output_throughput_token_per_s", "results_num_completed_requests_per_min"]]
        # Save the DataFrame to a CSV file
        data.to_csv(output_csv, index=False)
        print(f"Data successfully written to {output_csv}")
    else:
        print("No summary.json files found.")

# Usage
if __name__ == "__main__":
    base_directory = "/root/kubernetes_files/llama_perf"  # Replace with your base directory
    output_csv_path = "llama3-8b-I.csv"          # Replace with your desired output CSV path
    collect_json_data(base_directory, output_csv_path)
