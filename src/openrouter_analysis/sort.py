
import argparse
import sys
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Sort a CSV file by a specific column.")
    parser.add_argument("-f", "--file", required=True, help="Input CSV file")
    parser.add_argument("-o", "--out", help="Output CSV file (optional). If omitted, prints to standard output.")
    parser.add_argument("-c", "--column", default="Output Price USD (1M Tokens)", help="Column to sort by")
    
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.file)
        # Sort values descending
        df_sorted = df.sort_values(by=args.column, ascending=False)

        if args.out:
            # Write to specific file
            df_sorted.to_csv(args.out, index=False)
            print(f"Success: Data sorted by '{args.column}' and saved to '{args.out}'.", file=sys.stderr)
        else:
            # Write to stdout for `> out.csv` redirection
            df_sorted.to_csv(sys.stdout, index=False)

    except FileNotFoundError:
        print(f"Error: The file '{args.file}' was not found.", file=sys.stderr)
        sys.exit(1)
    except KeyError:
        print(f"Error: The column '{args.column}' does not exist in the CSV file.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
