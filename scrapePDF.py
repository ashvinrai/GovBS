import PyPDF2
import urllib.request
import textract

print('Beginning file download')

url = 'https://portal.ct.gov/-/media/Office-of-the-Governor/Executive-Orders/Lamont-Executive-Orders/Executive-Order-No-7C.pdf'
urllib.request.urlretrieve(url, 'temp.pdf')

text = textract.process("temp.pdf")

lines = text.decode("utf8").lower().split("\n")

lines = list(filter(lambda line: line != "", lines ))

lines = list(filter(lambda line: line != ' ', lines ))

pdfLineLength = len(lines)

def getSchoolClosingScore(lines):
    schoolPhrases = [" educational institutions ", " educational settings ", " school ", " college ", " universities ", " university ", " class "]
    recommendPhrases = [" recommend ", " advise ", " request "]
    requireSomePhrases = [" some ", " secondary ", " primary ", " on campus ", " age "]
    requireAll = [" required ", " all ", " cancelation ", " cancellation "]
    score = 0
    for phrase in schoolPhrases:
        matched = [line for line in lines if phrase in line]
        for match in matched:
            i = lines.index(match)
            start = i - 5 if i - 5 >= 0 else 0
            end = i + 5 if i + 5 <= pdfLineLength else pdfLineLength
            searchZone = lines[start:end]
            for rPhrase in recommendPhrases:
                recommendMatch = [line for line in searchZone if rPhrase in line]
                if len(recommendMatch) > 0:
                    return 1

            for rsphrase in requireSomePhrases:
                rsMatch = [line for line in searchZone if rsphrase in line]
                if len(rsMatch) > 0:
                    print(rsphrase)
                    print(rsMatch)
                    return 2

            for raphrase in requireAll:
                ramatch = [line for line in searchZone if raphrase in line]
                if len(ramatch) > 0:
                    return 3

    return score

print(getSchoolClosingScore(lines))

# print(' PDF')

# pdfFileObj = open('temp.pdf', "rb")
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)



# print(pdfReader.getPage(1).extractText().replace("\n", ""))