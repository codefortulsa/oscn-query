import re
import sys

import oscn

test_for = re.compile(r"reappear", re.I | re.M)


def find_disp(html_doc):
    if test_for.search(html_doc):
        return True
    else:
        sys.stdout.write(".")
        sys.stdout.flush()

    return False


# define the Case attr to test and the function to use

cases = oscn.request.CaseList(
    county="tulsa", type="CF", year="2017", start=1001, stop=2000
)

for c in cases:
    docket = c.docket
    print(docket.text)
