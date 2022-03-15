# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"\n(?P<cas>[0-9]{2,7}[-][0-9]{2}[-][0-9]{1})[ ]{1,}(?P<name>.*?(?=( \n|\n| A\n| B\n))){1}(?=(?P<cat>( A\n| B\n|\n){1}))"

test_str = ("'\n"
            "50-00-0  Formaldehyd  \n"
            "50-32-8  Benso(a)pyren  \n"
            "51-79-6 2-Etylkarbamat (uretan) B\n"
            "50-32-8  Benso(a)pyren  \n"
            "54-11-5 Nikotin \n"
            "50-32-8  Benso(a)pyren\n"
            "55-63-0 Nitroglycerin \n"
            "56-23-5 Koltetraklorid \n"
            "56-49-5 20-Metylkolantren \n"
            "(3-metylkolantren)\n"
            "A \n"
            "53-96-3 2-Acetamidofluoren A\n"
            "56-49-5 20-Metylkolantren \n\n\n"
            "(3-metylkolantren) \n\n"
            "A \n"
            "50-00-0  Formaldehyd  \n"
            "100-80-1 3-Vinyltoluen\n"
            "100-97-0 Hexametylentetramin\n"
            "101-14-4 4,4’-Diamino-3,3’-diklordifenylmetan \n"
            "(metylenbis(o-kloranilin)) \n\n"
            "101-68-8 4,4´-Metylendifenyldiisocyanat Se diisocyanater\n"
            "101-77-9 4,4’-Metylendianilin\n"
            "(4,4’-diaminodifenylmetan)\n"
            "101-84-8 Difenyleter\n"
            "102-71-6 Trietanolamin Se noasdsda\n")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):

    print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                        end=match.end(), match=match.group()))

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1

        print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=match.start(groupNum),
                                                                        end=match.end(groupNum),
                                                                        group=match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
