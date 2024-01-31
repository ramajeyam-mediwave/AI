from bs4 import BeautifulSoup

source_html = """
<span class="ratingsDisplay">
    <a class="ratingNumber" href="https://www.youtube.com/watch?v=oHg5SJYRHA0" target="_blank" rel="noopener">
        <span class="ratingsContent">Hello</span>
    </a>
</span>
"""

soup = BeautifulSoup(source_html, "lxml")
my_ratings = getattr(soup.find('span', {"class": "ratingsContent"}), "text", None)
print(my_ratings)
