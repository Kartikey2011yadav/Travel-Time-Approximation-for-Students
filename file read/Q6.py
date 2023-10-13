with open("text_file.txt", "r") as file:
    read_data = file.read()
    per_word = read_data.split()

    print('Total Words:', len(per_word))