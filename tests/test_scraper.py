import pytest
from app.scraper import scrape_google_news_story

SAMPLE_STORY_HTML = """
<!DOCTYPE html>
<html>
<body>
<div class="W84tYb">
  <div class="N0NI1d"><a class="wEwyrc">Kathimerini</a></div>
  <h4><a href="./read/CBMikwFBVV95cUxOZERqOGtuOE10NXJUbW1QelZXRW1rRUpXVVp3Q3FkMFJaLVN1eHF3aGJjVHhiTnkxMVUzZUNiQ2hCREJMcnd0eGVISE04OU5Db2M2YVRHSmRxRVh5NlJTVkE3Wlc1NExvYzM0bWd4aWJZamxpVjMtUXEtQ2EzRW8wUDZ4c3JVMDhYTUhyOVJRWlBxd00?hl=el&gl=GR&ceid=GR%3Ael" class="DY5T1d">Το βαρύ «αποτύπωμα» της ανομβρίας</a></h4>
  <time datetime="2026-11-06T19:30:28Z">3 ημέρες πριν</time>
</div>
<div class="W84tYb">
  <div class="N0NI1d"><a class="wEwyrc">iefimerida.gr</a></div>
  <h4><a href="./read/CBMiekFVX3lxTE00U1ZUcl9VRS1LdjZoNWk2d2t6RWRZOGktbUxNZ00wYmtXX3VGRHdVRjZWYktFbGZDUi10NF85OXdBNWVtNzh1SkFFZ2JuUXdTc3kzZDRMNEJKY28wZ3dWRzhvdldLelV4TTJOMlpxU3NoRWFELUZpRGpn?hl=el&gl=GR&ceid=GR%3Ael" class="DY5T1d">Μελέτη για τα υπόγεια ύδατα στην Ελλάδα - Σε κακή κατάσταση το 28%</a></h4>
  <time datetime="2026-11-06T18:00:00Z">3 ημέρες πριν</time>
</div>
</body>
</html>
"""

def test_scrape_google_news_story_mock(monkeypatch):
    class MockResponse:
        status_code = 200
        text = SAMPLE_STORY_HTML

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    items = scrape_google_news_story(limit=10)
    assert len(items) == 2
    assert "ανομβρίας" in items[0]["title"]
    assert items[0]["author"] == "Kathimerini"
    assert items[0]["source_feed"] == "🇬🇷 Kathimerini"
    assert items[0]["link"].startswith("https://news.google.com/read/")
    assert items[0]["category_tr"] == "İklim & Kuraklık"
    assert items[0]["is_turkey"] == 0
