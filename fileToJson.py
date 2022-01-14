# Modern way to open files. The closing in handled cleanly
with open('inventory.txt', mode='r') as in_file, \
     open('purchasing.txt', mode='w') as out_file:

    # A file is iterable
    # We can read each line with a simple for loop
    for line in in_file:

        # Tuple unpacking is more Pythonic and readable
        # than using indices
        ref, name, price, quantity, reorder = line.split()

        # Turn strings into integers
        quantity, reorder = int(quantity), int(reorder)

        if quantity <= reorder:
            # Use f-strings (Python 3) instead of concatenation
            out_file.write(f'{ref}\t{name}\n')