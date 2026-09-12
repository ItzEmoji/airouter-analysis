# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///

import argparse
import requests
import csv
import sys

# Define the API endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/models"
# Fetch top 100 text-generation models from Hugging Face, sorted by downloads
HF_API_URL = "https://huggingface.co/api/models?pipeline_tag=text-generation&sort=downloads&direction=-1&limit=100"

# List of known proprietary model providers for categorization
PROPRIETARY_PROVIDERS = ["openai", "anthropic", "google", "cohere", "perplexity", "x-ai"]

def main():
    parser = argparse.ArgumentParser(description="Fetch top LLM models and pricing to CSV.")
    parser.add_argument("-o", "--out", help="Output CSV file. If omitted, prints to standard output.")
    args = parser.parse_args()

    csv_data = []
    header = ["Model ID", "Type", "Provider", "Input Price USD (1M Tokens)", "Output Price USD (1M Tokens)"]
    seen_models = set()

    # --- 1. Fetch OpenRouter Models ---
    try:
        print("Fetching OpenRouter data...", file=sys.stderr)
        response = requests.get(OPENROUTER_API_URL)
        response.raise_for_status() 
        data = response.json().get("data", [])
        
        for model in data:
            model_id = model.get("id", "")
            provider = model_id.split("/")[0] if "/" in model_id else model_id
            model_type = "Proprietary" if provider in PROPRIETARY_PROVIDERS else "Open"
            pricing = model.get("pricing", {})
            
            try:
                prompt_price_1m = float(pricing.get("prompt", 0)) * 1_000_000
                completion_price_1m = float(pricing.get("completion", 0)) * 1_000_000
            except (ValueError, TypeError):
                prompt_price_1m = 0.0
                completion_price_1m = 0.0

            csv_data.append([
                model_id, model_type, provider, 
                f"{prompt_price_1m:.4f}", f"{completion_price_1m:.4f}"
            ])
            seen_models.add(model_id)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OpenRouter data: {e}", file=sys.stderr)

    # --- 2. Fetch Hugging Face Models ---
    try:
        print("Fetching Hugging Face data...", file=sys.stderr)
        response = requests.get(HF_API_URL)
        response.raise_for_status()
        hf_data = response.json()
        
        for model in hf_data:
            model_id = model.get("id", "")
            
            # Skip if OpenRouter already provided this model
            if model_id in seen_models:
                continue
                
            provider = model_id.split("/")[0] if "/" in model_id else "huggingface"
            
            # HF models downloaded from the Hub are open weights and don't have token pricing
            csv_data.append([
                model_id, "Open", provider, "0.0000", "0.0000"
            ])
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Hugging Face data: {e}", file=sys.stderr)

    # --- Sort and Output ---
    # 1st key: Model Type -> 'Open' comes first (0), then 'Proprietary' (1)
    # 2nd key: Model ID -> Alphabetically
    csv_data.sort(key=lambda row: (0 if row[1] == "Open" else 1, row[0].lower()))
    
    if args.out:
        with open(args.out, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(csv_data)
        print(f"Success: Data saved to '{args.out}'.", file=sys.stderr)
    else:
        writer = csv.writer(sys.stdout, delimiter=",", lineterminator='\n')
        writer.writerow(header)
        writer.writerows(csv_data)

if __name__ == "__main__":
    main()
