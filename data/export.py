from sys import stderr
import fitz

doc = fitz.open("2.pdf")
for idx, page in enumerate(doc):
    tabs = page.find_tables()
    if tabs.tables:
        data = tabs[0].extract()

        for i in range(0 if idx == 0 else 1, len(data)):
            print('"' + '","'.join(data[i]) + '"')

        stderr.write("Page : " + str(idx) + " extracted\n")
