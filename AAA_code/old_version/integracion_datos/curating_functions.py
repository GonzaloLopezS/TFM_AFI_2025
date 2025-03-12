import re

def remove_note(text):
    return re.sub(r"\[Note \d+\]", "", text) #revisar Note y note