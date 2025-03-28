from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)
def callGemini(text: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=text,
    )
    return response.text

def create_and_fill_file(file_path, data):
    """
    Creates a file and fills it with the provided data.

    Args:
        file_path (str): The path to the file to create.
        data (str or bytes): The data to write to the file. If 'data' is a string,
                             it will be written as text. If 'data' is bytes, it will
                             be written as binary data.
    """
    try:
        # Open the file in write mode ('w' for text, 'wb' for binary)
        if isinstance(data, str):
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            print(f"File '{file_path}' created and filled successfully (text).")
        elif isinstance(data, bytes):
            with open(file_path, 'wb') as file:
                file.write(data)
            print(f"File '{file_path}' created and filled successfully (binary).")

        else:
          print("Error: data must be a string or bytes object.")

    except FileNotFoundError:
        print(f"Error: Could not create file at '{file_path}'. Check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_files_in_folder(folder_path):
    """
    Reads and prints the content of each file in the specified folder.

    Args:
        folder_path (str): The path to the folder.
    """
    try:
        # Get a list of all files in the folder
        files = os.listdir(folder_path)

        for filename in files:
            file_path = os.path.join(folder_path, filename)

            # Check if it's a file (not a subdirectory)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # print(f"--- Content of {filename} ---")
                        # print(content)
                        # print("-" * 20)  # Separator for readability
                        text = """Corecteaza aceasta rezolvare a elevului. Fisierul atasat contine subiectul si baremul. Raspunsul doresc sa contina doar numele exercitiului si punctajul aferent:
                                ITEM	PUNCTAJ POSIBIL
                                1.1	    4
                                1.2	    4
                                1.3	    4
                                1.4	    4
                                1.5	    4
                                2.1.a	6
                                2.1.b	6
                                2.1.c	10
                                2.1.d	6
                                2.2	    6
                                2.3	    6
                                3.1	    10
                                3.2	    10
                                3.3.a	2
                                3.3.b	8

                                Nota: La subiectul 1(cel cu grila) spune pentru fiecare exercitiu daca elevul a ales corect sau gresit
                                Rezolvarea data de elev este:
                                """ + content
                        resp = callGemini(text)
                        create_and_fill_file(f"Rezultate/Gemini{an}/{filename}",resp)

                except UnicodeDecodeError:
                    print(f"--- Cannot decode {filename} as utf-8, skipping ---") #Handles non-text files.
                except FileNotFoundError:
                    print(f"--- File {filename} not found (shouldn't happen) ---")
                except Exception as e:
                    print(f"--- An error occurred while reading {filename}: {e} ---")

    except FileNotFoundError:
        print(f"--- Folder '{folder_path}' not found. ---")
    except NotADirectoryError:
        print(f"--- '{folder_path}' is not a valid folder. ---")
    except Exception as e:
        print(f"--- An unexpected error occurred: {e} ---")

an = ""
while(an not in ["2021","2022"]):
    an = input("Introdu an: ")

myfile = client.files.upload(file=f"subiect-barem{an}.pdf")
print(f"{myfile=}")
read_files_in_folder(an)