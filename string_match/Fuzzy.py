from fuzzywuzzy import process


def string_match(sentence, string_list):
    extracted_string = process.extract(sentence, string_list)
    if extracted_string[0][1] < 40:
        return None
    return [extracted_string[0][0]]
    