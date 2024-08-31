import hashlib
import concurrent.futures
import time
import os

def md5_crack(md5_hash, wordlist_file, max_length=5):
    """
    Attempts to crack the given MD5 hash by using words from a wordlist file up to `max_length` character strings.
    
    :param md5_hash: The MD5 hash to crack.
    :param wordlist_file: Path to the file containing the wordlist.
    :param max_length: The maximum length of strings to try.
    :return: The original string if found, otherwise None.
    """
    def attempt_crack():
        try:
            with open(wordlist_file, 'r') as file:
                for line in file:
                    word = line.strip()  # Remove any leading/trailing whitespace
                    if len(word) > max_length:
                        continue  # Skip words longer than the maximum length
                    attempt_hash = hashlib.md5(word.encode()).hexdigest()  # Compute MD5 hash of the word
                    if attempt_hash == md5_hash:
                        return word  # Return the word if it matches the hash
        except FileNotFoundError:
            print(f"Error: The file {wordlist_file} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        start_time = time.time()
        future = executor.submit(attempt_crack)

        while not future.done():
            elapsed_time = time.time() - start_time
            print(f'Elapsed Time: {elapsed_time:.2f} seconds')
            time.sleep(1)  # Update every second

        result = future.result()
    return result

# Ensure the wordlist file is in the same directory as this script
current_directory = os.path.dirname(os.path.abspath(__file__))
wordlist_file = os.path.join(current_directory, 'wordlist.txt')

md5_hash = input("Enter the MD5 hash value: ").strip()

# Validate the MD5 hash length
if len(md5_hash) != 32:
    print("Invalid MD5 hash length. Please enter a valid 32-character MD5 hash.")
else:
    # Attempt to crack the MD5 hash
    result = md5_crack(md5_hash, wordlist_file)

    if result:
        print(f'The original string is: {result}')
    else:
        print('No match found.')

# Wait for user input before closing
input("Press Enter to exit...")
