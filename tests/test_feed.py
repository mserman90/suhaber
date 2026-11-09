import pytest
import xml.etree.ElementTree as ET
from app.feed import generate_rss_2_xml, generate_atom_xml, generate_json_feed

@pytest.fixture
def sample_items():
    return [
        {
            "guid": "test:1",
            "title": "[Barajlar] Atatürk Barajı Su Seviyesi",
            "link": "https://example.com/haber1",
            "author": "DSİ",
            "source_feed": "DSİ Basın",
            "description": "<p>Atatürk Barajı su seviyesi yükseldi.</p>",
            "pub_date": "Wed, 06 Nov 2026 09:00:00 +0000",
            "pub_date_ts": 1730883600,
            "image_url": "https://example.com/dam.jpg"
        }
    ]

def test_generate_rss_2_xml(sample_items):
    xml_str = generate_rss_2_xml(
        feed_title="Su Haber Bülteni",
        feed_description="Test Açıklama",
        feed_link="https://example.com",
        self_rss_url="https://example.com/rss.xml",
        items=sample_items
    )
    assert "<?xml" in xml_str
    root = ET.fromstring(xml_str)
    assert root.tag == "rss"
    assert root.attrib.get("version") == "2.0"
    channel = root.find("channel")
    assert channel is not None
    title = channel.find("title")
    assert title.text == "Su Haber Bülteni"
    item = channel.find("item")
    assert item is not None
    assert item.find("title").text == sample_items[0]["title"]

def test_generate_atom_xml(sample_items):
    xml_str = generate_atom_xml(
        feed_title="Su Haber Bülteni Atom",
        feed_description="Test Açıklama",
        feed_link="https://example.com",
        self_atom_url="https://example.com/atom.xml",
        items=sample_items
    )
    assert "<?xml" in xml_str
    assert "http://www.w3.org/2005/Atom" in xml_str

def test_generate_json_feed(sample_items):
    data = generate_json_feed(
        feed_title="Su Haber JSON",
        feed_description="Test Açıklama",
        feed_link="https://example.com",
        self_json_url="https://example.com/feed.json",
        items=sample_items
    )
    assert data["version"] == "https://jsonfeed.org/version/1.1"
    assert data["title"] == "Su Haber JSON"
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == "test:1"
