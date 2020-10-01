## File usage
When given a base64 string without casing it will output the printable plaintext possabilites for each chunk (Generally 1/2). As well as the most likely combination of all combined.


## Technical overview
Because base64 works in chunks of 4 b64 chars each chunk can be treated independently from each other, reducing the bruteforce possibilities from n^2 (Checking 2 cases for each letter) to 2^4 * (n/4) (The 16 case possabilities for each 4 chunk * number of chunks). These are sorted with the lower values first as they contain more common characters
