import argparse
import sys
from get_papers.fetch_papers import fetch_papers, filter_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output.")
    
    args = parser.parse_args()
    
    if args.debug:
        print(f"Debug mode enabled. Query: {args.query}")
    
    try:
        papers = fetch_papers(args.query)
        filtered_papers = filter_papers(papers)
        
        if args.file:
            save_to_csv(filtered_papers, args.file)
            print(f"Results saved to {args.file}")
        else:
            for paper in filtered_papers:
                print(paper)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()