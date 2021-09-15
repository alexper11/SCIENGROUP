"file key.txt must be created, add API KEY in first line and INST TOKEN in second line of the file"
def read_key():
    with open("scopus/key.txt") as key:
        lines = [line.rstrip() for line in key]

    return lines[0], lines[1]
 