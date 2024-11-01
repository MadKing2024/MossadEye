import requests
import json
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from bs4 import BeautifulSoup
import time
from colorama import Fore, Style, init
import os
from datetime import datetime
from tqdm import tqdm

class MossadEye:
    def __init__(self):
        init()
        self.print_banner()
        self.setup_directories()
        self.load_config()
        
    def setup_directories(self):
        dirs = ['reports', 'cache', 'data']
        for dir in dirs:
            os.makedirs(dir, exist_ok=True)

    def load_config(self):
        self.apis = {
            'numverify': os.getenv('NUMVERIFY_API_KEY', 'default_key'),
            'truecaller': os.getenv('TRUECALLER_API_KEY', 'default_key'),
            'eyecon': os.getenv('EYECON_API_KEY', 'default_key')
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def print_banner(self):
        banner = """
        ███╗   ███╗ ██████╗ ███████╗███████╗ █████╗ ██████╗     ███████╗██╗   ██╗███████╗
        ████╗ ████║██╔═══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗    ██╔════╝╚██╗ ██╔╝██╔════╝
        ██╔████╔██║██║   ██║███████╗███████╗███████║██║  ██║    █████╗   ╚████╔╝ █████╗  
        ██║╚██╔╝██║██║   ██║╚════██║╚════██║██╔══██║██║  ██║    ██╔══╝    ╚██╔╝  ██╔══╝  
        ██║ ╚═╝ ██║╚██████╔╝███████║███████║██║  ██║██████╔╝    ███████╗   ██║   ███████╗
        ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝     ╚══════╝   ╚═╝   ╚══════╝
                                    Version 1.0 - The All-Seeing Eye
        """
        print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")

    def analyze_target(self, number):
        print(f"\n{Fore.GREEN}[+] Initiating reconnaissance on target: {number}{Style.RESET_ALL}")
        
        with tqdm(total=100, desc="Gathering Intelligence") as pbar:
            results = {
                'timestamp': datetime.now().isoformat(),
                'target': number,
                'basic_info': self.get_basic_info(number),
                'social_media': self.check_social_media(number),
                'whatsapp_intel': self.gather_whatsapp_intel(number)
            }
            pbar.update(100)
        
        return results

    def check_whatsapp(self, number):
        clean_number = number.replace('+', '').replace(' ', '')
        url = f"https://wa.me/{clean_number}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return {
                    'exists': True,
                    'url': url,
                    'status': 'Active'
                }
            return {
                'exists': False,
                'url': url,
                'status': 'Not Found'
            }
        except Exception as e:
            return {
                'exists': False,
                'url': url,
                'status': f'Error: {str(e)}'
            }

    def check_telegram(self, number):
        clean_number = number.replace('+', '').replace(' ', '')
        url = f"https://t.me/{clean_number}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return {
                    'exists': True,
                    'url': url,
                    'status': 'Active'
                }
            return {
                'exists': False,
                'url': url,
                'status': 'Not Found'
            }
        except Exception as e:
            return {
                'exists': False,
                'url': url,
                'status': f'Error: {str(e)}'
            }

    def get_basic_info(self, number):
        try:
            parsed_number = phonenumbers.parse(number)
            return {
                'valid': phonenumbers.is_valid_number(parsed_number),
                'carrier': carrier.name_for_number(parsed_number, 'en'),
                'region': geocoder.description_for_number(parsed_number, 'en'),
                'timezones': timezone.time_zones_for_number(parsed_number),
                'number_type': str(phonenumbers.number_type(parsed_number))
            }
        except Exception as e:
            return {'error': str(e)}

    def check_social_media(self, number):
        platforms = {
            'whatsapp': self.check_whatsapp(number),
            'telegram': self.check_telegram(number)
        }
        return platforms

    def gather_whatsapp_intel(self, number):
        return {
            'profile_exists': self.check_wa_profile(number),
            'business_info': self.check_wa_business(number)
        }

    def check_wa_profile(self, number):
        url = f"https://wa.me/{number.replace('+', '')}"
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False

    def check_wa_business(self, number):
        url = f"https://wa.me/business/{number.replace('+', '')}"
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False

    def generate_report(self, results, number):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/MossadEye_report_{number}_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n{Fore.GREEN}[+] Intelligence report generated: {report_file}{Style.RESET_ALL}")
        self.print_summary(results)
        return report_file

    def print_summary(self, results):
        print(f"\n{Fore.YELLOW}=== Intelligence Summary ==={Style.RESET_ALL}")
        print(f"Target Number: {results['target']}")
        print(f"Region: {results['basic_info'].get('region', 'Unknown')}")
        print(f"Carrier: {results['basic_info'].get('carrier', 'Unknown')}")
        print(f"WhatsApp Status: {'Active' if results['whatsapp_intel']['profile_exists'] else 'Not Found'}")
