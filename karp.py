import plotly
import bs4
from urllib.request import urlopen as uReq
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

req = Request('http://www.nst.com.my/opinion/columnists/2018/05/365668/malaysia', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

page_soup = soup(webpage, 'html.parser')

[s.extract() for s in page_soup(['style', 'script', '[document]', 'head', 'title'])]

article = page_soup.getText()

print(article)
# d is the number of characters in input alphabet
d = 256
newText = ""
positive = 0
negative = 0

# pat  -> pattern
# txt  -> text
# q    -> A prime number

def filter(pat, txt, q):
    for r in range(len(pat)-1, -1, -1):
        global newText
        M = len(pat[r])
        N = len(txt)
        i = 0
        j = 0
        p = 0  # hash value for pattern
        t = 0  # hash value for txt
        h = 1
        k = 0
        cond = False

        if M > N:
            return -1
        if pat[r] == None or txt == None:
            return -1
        if pat[r] == "" or txt == "":
            return -1

        # The value of h would be "pow(d, M-1)%q"
        for i in range(M - 1):
            h = (h * d) % q

        # Calculate the hash value of pattern and first window
        # of text
        for i in range(M):
            p = (d * p + ord(pat[r][i].lower())) % q
            t = (d * t + ord(txt[i].lower())) % q

        # Slide the pattern over text one by one
        for i in range(N - M + 1):
                # Check the hash values of current window of text and
                # pattern if the hash values match then only check
                # for characters on by one
                if p == t:
                    # Check for characters one by one
                    for j in range(M):
                        if txt[i + j].lower() != pat[r][j].lower():
                            break
                    j += 1
                    # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
                    if j == M:
                        newText = txt[0:i] + txt[i + M - 1: N]
                        txt = newText
                        cond = True
                        N = (N+1)-M

                # Calculate hash value for next window of text: Remove
                # leading digit, add trailing digit
                if i < N - M:
                    t = (d * (t - ord(txt[i].lower()) * h) + ord(txt[i + M].lower())) % q
                    # We might get negative values of t, converting it to
                    # positive
                    if t < 0:
                        t = t + q
                if i >= N-M:
                    if cond == False:
                        del pat[r]


def compare(pat, txt, q, sentiment):
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0  # hash value for pattern
    t = 0  # hash value for txt
    h = 1
    global positive
    global negative

    if M > N:
        return -1
    if pat == None or txt == None:
        return -1
    if pat == "" or txt == "":
        return -1


    # The value of h would be "pow(d, M-1)%q"
    for i in range(M - 1):
        h = (h * d) % q

    # Calculate the hash value of pattern and first window
    # of text
    for i in range(M):
        p = (d * p + ord(pat[i].lower())) % q
        t = (d * t + ord(txt[i].lower())) % q

    # Slide the pattern over text one by one
    for i in range(N - M + 1):
        # Check the hash values of current window of text and
        # pattern if the hash values match then only check
        # for characters on by one
        if p == t:
            # Check for characters one by one
            for j in range(M):
                if txt[i + j].lower() != pat[j].lower():
                    break

            j += 1
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
            if j == M:
                print("Pattern found starting from index: " + str(i))
                print("Pattern matched: " + str(pat))
                if sentiment == True:
                    positive += 1
                if sentiment == False:
                    negative += 1
        # Calculate hash value for next window of text: Remove
        # leading digit, add trailing digit
        if i < N - M:
            t = (d * (t - ord(txt[i].lower()) * h) + ord(txt[i + M].lower())) % q

            # We might get negative values of t, converting it to
            # positive
            if t < 0:
                t = t + q


txt = ' ' + article + ' '

stopWords = "a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves"
stopWords = stopWords.split()
print(stopWords)
q = 977 # A prime number

for o in range(len(stopWords)):
    stopWords[o] = stopWords[o].replace(stopWords[o], ' ' + stopWords[o] + ' ')

for l in range(len(stopWords)):
    filter(stopWords, txt, q)
    txt = newText
print()
print()


print("POSITIVE:")
with open('C:/Users/ASUS/PycharmProjects/karp/positive.txt', 'r') as f:
    for line in f:
        line = line.replace('â€“', '')
        for word in line.split():
            word = word.replace(',', '')
            word = word.replace(word, ' '+word+' ')
            compare(word, newText, q, True)
print()


print("NEGATIVE:")
with open('C:/Users/ASUS/PycharmProjects/karp/negative.txt', 'r') as w:
    for line in w:
        line = line.replace('â€“', '')
        for word in line.split():
            word = word.replace(',', '')
            word = word.replace(word, ' '+word+' ')
            compare(word, newText, q, False)
print()
print()

print("Positive words count: "+ str(positive))
print("Negative words count: "+ str(negative))
print("Text after filtering stop words: "+ '"'+newText.strip()+'"')

sent = (positive + negative) * (15 / 100)

print(str(sent))

if positive-sent > negative:
    print("Article sentiment is positive!")
elif negative-sent > positive:
    print("Article sentiment is positive!")
else:
    print("Article sentiment is neutral")

