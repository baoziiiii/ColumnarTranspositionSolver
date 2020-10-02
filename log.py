import datetime
output_file = 'log{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())


def fprint(line):
    with open(output_file, "a") as f:
        f.write(str(line)+'\n')
        print(line)

