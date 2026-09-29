import requests
import bs4
import sys
from pathlib import Path
import json
import re
import os
from dotenv import load_dotenv

def fetch_advisories(url: str) -> bs4.BeautifulSoup:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f'Error GET Request: {e}')
        sys.exit(1)                                                                   
    return bs4.BeautifulSoup(response.text, 'html.parser').select('#content ul > li > p')

def is_non_vulnerable(safe_versions, MAJOR, MINOR, PATCH):
    for version in safe_versions:
        version_number = version.split('.')
        if int(version_number[0]) == int(MAJOR) and int(version_number[1]) == int(MINOR):
            if '+' in version_number[2]:
                version_number[2] = version_number[2].replace('+', '')
                if int(version_number[2]) <= int(PATCH):
                    return True
            elif int(version_number[2]) == int(PATCH):
                return True
    return False

def is_vulnerable(ranges, MAJOR, MINOR, PATCH):
    for r in ranges:
        if '-' in r:
            vulnerable_range = r.split('-')
            min_range = vulnerable_range[0].split('.')
            max_range = vulnerable_range[1].split('.')
            in_range = False
            if int(MAJOR) == int(min_range[0]):
                if int(MINOR) == int(min_range[1]):
                    if int(PATCH) >= int(min_range[2]):
                        in_range = True
                elif int(MINOR) > int(min_range[1]):
                    in_range = True
            elif int(MAJOR) > int(min_range[0]):
                in_range = True
            if in_range:
                if int(MAJOR) == int(max_range[0]):
                    if int(MINOR) == int(max_range[1]):
                        if int(PATCH) <= int(max_range[2]):
                            return True
                    elif int(MINOR) < int(max_range[1]):
                        return True
                elif int(MAJOR) < int(max_range[0]):
                    return True
        else:
            #non c'e un range ma solo una versione specifica vulnerabile
            vulnerable_version = r.split('.')
            if (int(vulnerable_version[0]) != int(MAJOR) or
                int(vulnerable_version[1]) != int(MINOR) or
                int(vulnerable_version[2]) != int(PATCH)):
                return False

    return False

def parse_advisory(advisory):
    data = advisory.getText(separator='\n', strip=True).splitlines()
    clean_advisory = {}
    clean_advisory['Description'] = data[0]
    links = advisory.find_all('a')
    for link in links:
        clean_advisory[link.getText()] = link.get('href')
    return clean_advisory

def compare_new_vulnerabilities(PATH, advisories):
    path = Path(PATH)
    if path.exists() and path.is_file() and path.stat().st_size > 0:
        try:
            json_file = path.read_text(encoding = 'utf-8')
            old_advisories = json.loads(json_file)
        except Exception as e:
            print(f'Error Reading json file: {e}')
            sys.exit(1)
        new_advisories = []
        for advisory in advisories:
            is_new = True
            for old_adv in old_advisories:
                if advisory['Description'] == old_adv['Description']:
                    is_new = False
                    break
            if is_new:
                new_advisories.append(advisory)
        if new_advisories:
            old_advisories.extend(new_advisories)
            updated_json = json.dumps(old_advisories, indent=4)
            path.write_text(updated_json, encoding='utf-8')
        return new_advisories
    try:
        json_str = json.dumps(advisories, indent=4)
        path.write_text(json_str, encoding='utf-8')
    except Exception as e:
        print(f'Error Creating File: {e}')
        sys.exit(1)
    return advisories

def telegram_notify(advisories):
    load_dotenv()
    TOKEN = os.environ.get('TG_BOT_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    if not TOKEN or not CHAT_ID:
        print(f'Error getting env variables')
        sys.exit(1)
    URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    for advisory in advisories:
        message = ''
        for key, value in advisory.items():
            message += f'{key}: {value}\n'
        payload = {
                'chat_id': CHAT_ID,
                'text': message
        }
        try:
            response = requests.post(URL, json=payload)
            if not response.json().get('ok'):
                print(f"Error Telegram: {response.json().get('description')}")
        except Exception as e:
            print(f'Network error: {e}')


if __name__ == '__main__':
    URL = 'https://nginx.org/en/security_advisories.html'
    JSON_FILE_PATH = 'path_to_json_file'
    MAJOR = '1'
    MINOR = '31'
    PATCH = '1'
    html_page = fetch_advisories(URL)
    vulnerabilities = []
    for raw_advisory in html_page:
        parsed_advisory = iter(raw_advisory.getText(separator='\n', strip=True).splitlines())
        for record in parsed_advisory:
            if 'not vulnerable' in record.lower():
                pattern = r"\d+\.\d+\.\d+\+?"
                safe_versions = re.findall(pattern, record)
                if is_non_vulnerable(safe_versions, MAJOR, MINOR, PATCH):
                    break
                pattern = r"\d+\.\d+\.\d+\+?(?:-\d+\.\d+\.\d+)?"
                unsafe_ranges = re.findall(pattern, next(parsed_advisory, None))
                if not is_vulnerable(unsafe_ranges, MAJOR, MINOR, PATCH):
                    break
                vulnerabilities.append(parse_advisory(raw_advisory))
                break
    new_vulnerabilities = compare_new_vulnerabilities(JSON_FILE_PATH, vulnerabilities)
    if new_vulnerabilities:
        telegram_notify(new_vulnerabilities)
