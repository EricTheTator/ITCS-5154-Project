import os
import mailbox

def find_mbox_file(directory):
    """Finds the first .mbox file in a given directory."""
    for file in os.listdir(directory):
        if file.endswith(".mbox"):
            return os.path.join(directory, file)
    return None  # No MBOX file found

def extract_emails_from_mbox(mbox_file):
    """Extracts emails from an MBOX file and returns a list of cleaned email texts."""
    mbox = mailbox.mbox(mbox_file)
    emails = []

    for message in mbox:
        if message.is_multipart():
            content = ""
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    content += part.get_payload(decode=True).decode(errors="ignore")
        else:
            content = message.get_payload(decode=True).decode(errors="ignore")

        if content:
            emails.append(content.strip())

    return emails

# Set the directory where your MBOX files are stored
mbox_directory = "mbox_data"  # Adjust if needed

# Find the first MBOX file in the directory
mbox_file = find_mbox_file(mbox_directory)

if mbox_file:
    print(f"Using MBOX file: {mbox_file}")
    emails = extract_emails_from_mbox(mbox_file)

    # Print first 5 emails for review
    for i, email in enumerate(emails[:5]):
        print(f"===== EMAIL {i+1} =====\n{email}\n{'='*40}\n")
else:
    print("No MBOX files found in the directory!")
