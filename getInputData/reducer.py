import sys
for data in sys.stdin:
    data = data.strip()
    sys.stdout.write("%s\n" % data)

