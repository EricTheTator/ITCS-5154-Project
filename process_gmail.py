import os
import mailbox
import re

def find_mbox_file(directory):
    """Finds the first .mbox file in a given directory."""
    for file in os.listdir(directory):
        if file.endswith(".mbox"):
            return os.path.join(directory, file)
    return None  # No MBOX file found

def clean_email_text(email_body):
    """Removes signatures, replies, and unnecessary warnings."""
    email_body = re.sub(r"(?i)--\s*\n.*$", "", email_body, flags=re.DOTALL)  # Signatures
    email_body = re.sub(r"(?i)On.*wrote:.*", "", email_body, flags=re.DOTALL)  # Replies
    email_body = re.sub(r"\[Caution: Email from External Sender.*?\]", "", email_body, flags=re.DOTALL)  # External warnings
    email_body = re.sub(r"\n+", "\n", email_body)  # Excess new lines
    return email_body.strip()

def process_large_mbox(mbox_file, limit=50, filter_questions=True):
    """Processes emails while filtering only VA-related questions."""
    mbox = mailbox.mbox(mbox_file)
    processed_count = 0
    email_texts = []

    print(f"Processing {mbox_file}... This may take a while for large files.")

    for message in mbox:
        if message.is_multipart():
            content = ""
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    content += part.get_payload(decode=True).decode(errors="ignore")
        else:
            content = message.get_payload(decode=True).decode(errors="ignore")

        content = clean_email_text(content)

        if filter_questions and "?" not in content:
            continue  # Skip if no question is detected

        if content.strip():
            email_texts.append(content.strip())
            processed_count += 1

        if processed_count >= limit:  # Stop after 'limit' emails
            break

    print(f"Finished processing {processed_count} emails.")

    # Save extracted emails to a text file for later analysis
    with open("extracted_questions.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(email_texts))

mbox_directory = "mbox_data"
mbox_file = find_mbox_file(mbox_directory)

if mbox_file:
    print(f"Using MBOX file: {mbox_file}")
    process_large_mbox(mbox_file, limit=50, filter_questions=True)  # Adjust limit as needed
else:
    print("No MBOX files found in the directory!")
