from unicodedata import normalize

def latin2CamelCase(st):
    assert(len(st) > 0)
    string = st.decode('latin-1')
    encoded_str = normalize('NFKD', string).encode('ascii','ignore')
    return camelCase(encoded_str)

def camelCase(st):
    assert(len(st) > 0)
    output = ''.join(x for x in st.title() if x.isalpha())
    return output[0].lower() + output[1:]
