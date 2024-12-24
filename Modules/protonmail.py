import requests
import re
import datetime


def header():
    print("Welcome to Proton Intelligence Tool.")


def extract_timestamp(source_code):
    timestamp = re.findall(r':(\d{10}):', source_code)
    return int(timestamp[0]) if timestamp else None


def extract_key_and_length(source_code):
    key_line = source_code.split('\n')[1]
    key_parts = key_line.split(':')
    try:
        key_type = key_parts[2]
        key_length = key_parts[3]
    except IndexError:
        key_type = key_length = None
    return key_type, key_length


def check_email(email):
    response=[]
    url = f"https://api.protonmail.ch/pks/lookup?op=index&search={email}"
    result=[]
    response = requests.get(url)
    if response.text.startswith('info:1:1'):
        email_domain = email.split("@")[1]
        if email_domain in ["protonmail.com", "protonmail.ch", "proton.me"]:
            result.append("This is a Protonmail address.")
        else:
            result.append("This is a Protonmail custom domain.")

        data = response.text.split('\n')
        uid_line = data[2]
        email_in_brackets = re.findall(r'<(.*?)>', uid_line)
        if email_in_brackets:
            actual_email = email_in_brackets[0]
            if actual_email != email:
                result.append(f"Catch-All detected, this is the main email --> {actual_email}")

        timestamp = extract_timestamp(response.text)
        if timestamp is not None:
            creation_date = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            result.append(f"PGP Key Date and Creation Time: {creation_date}")
        else:
            result.append("Problem parsing Key Creation Date.")

        key_type, key_length = extract_key_and_length(response.text)
        if key_type is not None:
            if key_type != "22":
                result.append(f"Encryption Standard : RSA {key_length}-bit")
            else:
                result.append("Encryption Standard : ECC Curve25519")
        else:
            result.append("Problem parsing Encryption Standard.")
    else:
        result.append("Not a Protonmail custom domain!")
    return result


if __name__ == "__main__":
    header()
    email = input("Enter the proton email address to check its validity: ")
    print(check_email(email))
