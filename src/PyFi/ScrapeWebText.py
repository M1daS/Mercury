


from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment
import urllib.request


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False

    return True






def init(link):
	html = urllib.request.urlopen(link).read()
	soup = BeautifulSoup(html, 'html.parser')
	# for link in soup.findAll('a', href=True):
	# 	del soup[link]


	texts = soup.findAll(text=True)


	visible_texts = filter(tag_visible, texts)

	xx =  u" ".join(t.strip() for t in visible_texts)
	return xx



# # item.text.strip()
# # output = soup.findAll('s')
# if element.name == 'div':
# if script.has_attr('some_attribute'):
# soup.find('h1', attrs={'class': 'name'})

