# p31
# http://www.feedparser.org
import feedparser
import re

def getwords(html):
    # Remove all the HTML tags
    txt = re.compile(r'<[^>]>').sub('', html)
    
    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    
    # Convert to lowercase
    return [word.lower() for word in words if word != '']

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
    # Parse the feed
    d = feedparser.parse(url)
    wc={}
    
    # Loop over all the entries
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
            
        # Extract a list of words
        words = getwords(e.title + ' ' + summary)
    
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
            
    # http://stackoverflow.com/questions/29068485/attributeerror-object-has-no-attribute-title
    return getattr(d.feed, 'title', 'Unknown title'), wc

apcount = {}
wordcounts={}
feedlist=[]
for feedurl in file('feedlist.txt'):
    feedlist.append(feedurl)
    title,wc=getwordcounts(feedurl)
    wordcounts[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word,0)
        if count > 1:
            apcount[word]+=1
           
# determine which words to use for each blog        
wordlist=[]
MIN_PERCENTAGE = 0.1
MAX_PERCENTAGE = 0.5

for w, bc in apcount.items():
    frac=float(bc)/len(feedlist)
    if frac > MIN_PERCENTAGE and frac < MAX_PERCENTAGE:
        wordlist.append(w)
        
# create a text file containing term-document matrix for each blog
out = file('blogdata.txt', 'w')
out.write('Blog')

for word in wordlist:
    out.write('\t%s' % word)
    
out.write('\n')

for blog, wc in wordcounts.items():
    # deal with the unicode outside th ascii range
    blog = blog.encode('ascii', 'ignore')
    out.write(blog)
    
    for word in wordlist:
        if word in wc:
            out.write('\t%d '% wc[word])
        else:
            out.write('\t0')
    out.write('\n')