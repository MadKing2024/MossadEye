

from MossadEye import MossadEye
import argparse
from colorama import Fore, Style

def main():
    parser = argparse.ArgumentParser(description='MossadEye - Advanced Phone Intelligence Tool')
    parser.add_argument('number', help='Target phone number (e.g. +393401234567)')
    parser.add_argument('--silent', action='store_true', help='Run in silent mode')
    parser.add_argument('--output', help='Custom output file path')
    parser.add_argument('--deep-scan', action='store_true', help='Perform deep scanning')
    args = parser.parse_args()

    tool = MossadEye()
    
    if not args.silent:
        print(f"{Fore.YELLOW}[*] Initializing MossadEye...{Style.RESET_ALL}")
    
    results = tool.analyze_target(args.number)
    report_file = tool.generate_report(results, args.number)
    
    if not args.silent:
        print(f"{Fore.GREEN}[+] Operation completed successfully{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
