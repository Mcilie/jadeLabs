import os 
key = os.getenv("OPENPERPLEX_KEY")

from openperplex import OpenperplexSync

client_sync = OpenperplexSync(key)

result = client_sync.search(
    query="Who is Aman Agrawal? What are his research interests? What has he accomplished?",
    date_context="2024-08-25",
    location="us",
    pro_mode=False,
    response_language="en",
    answer_type="text",
    verbose_mode=False,
    search_type="general",
    return_citations=False,
    return_sources=False,
    return_images=False
)

print(result)