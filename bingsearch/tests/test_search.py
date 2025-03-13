from bingsearch import search

results = search("python programming", num_results=5)
for result in results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
    print(f"Description: {result.description}\n")
