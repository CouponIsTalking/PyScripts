import BeautifulSoup
from BeautifulSoup import BeautifulSoup, Comment

def removeComments(htmlpage):
    soup = BeautifulSoup(htmlpage)
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()
        
    return str(soup)

def removeJS(htmlpage):
    soup = BeautifulSoup(htmlpage)
    scripts = soup('script')
    for script in scripts:
        script.extract()
        
    return str(soup)

def removeHeads(htmlpage):
    soup = BeautifulSoup(htmlpage)
    heads = soup('head')
    for head in heads:
        head.extract()
        
    return str(soup)

def removeCommentsAndJS(htmlpage):
    #htmlpage = removeComments(htmlpage)
    #htmlpage = removeJS(htmlpage)
    soup = BeautifulSoup(htmlpage)
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    scripts = soup('script')
    for script in scripts:
        script.extract()
    
    for comment in comments:
        comment.extract()
        
    return str(soup)
    

def getAllDivs(htmlpage):
    soup = BeautifulSoup(htmlpage)
    divs = soup('div');
    return divs;