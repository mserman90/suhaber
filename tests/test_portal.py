import pytest
from app.portal import generate_newspaper_portal_html

@pytest.fixture
def sample_agri_items():
    return [
        {
            "id": 1,
            "title": "Çukurova'da Buğday Hasadı Başladı",
            "title_tr": "Çukurova'da Buğday Hasadı Başladı",
            "title_en": "Wheat Harvest Began in Cukurova",
            "summary_tr": "Buğday veriminde bu yıl %15 artış bekleniyor.",
            "summary_en": "A 15% increase is expected in wheat yield.",
            "category_tr": "Bitkisel Üretim",
            "source_feed": "Tarım Basını",
            "author": "Tarım Muhabiri",
            "pub_date": "10.11.2026",
            "link": "https://example.com/agri1",
            "image_url": "https://example.com/wheat.jpg",
            "is_turkey": True,
            "is_academic": False
        }
    ]

@pytest.fixture
def sample_water_items():
    return [
        {
            "id": 2,
            "title": "Atatürk Barajı Doluluk Oranı",
            "title_tr": "Atatürk Barajı Doluluk Oranı",
            "title_en": "Ataturk Dam Storage Level",
            "summary_tr": "Baraj doluluk oranı %72 seviyesine ulaştı.",
            "summary_en": "Storage reached 72%.",
            "category_tr": "Su Kaynakları",
            "source_feed": "DSİ Basın",
            "author": "DSİ",
            "pub_date": "10.11.2026",
            "link": "https://example.com/water1",
            "image_url": "https://example.com/dam.jpg",
            "is_turkey": True,
            "is_academic": False
        }
    ]

def test_agriculture_portal_is_homepage(sample_agri_items, sample_water_items):
    """Verify Tarım Gündemi is configured with index.html as homepage."""
    html = generate_newspaper_portal_html(
        items=sample_agri_items,
        last_updated="10.11.2026 12:00 UTC",
        rss_url="https://example.com/rss_tarim.xml",
        atom_url="https://example.com/atom_tarim.xml",
        json_url="https://example.com/feed_tarim.json",
        channel="agriculture",
        water_count=1,
        agri_count=1,
        livestock_count=0,
        water_items=sample_water_items,
        agri_items=sample_agri_items
    )
    # Homepage check
    assert 'TARIM GÜNDEMİ' in html
    assert 'href="index.html" class="channel-tab-btn active" id="tabAgri"' in html
    assert 'href="su.html" class="channel-tab-btn "' in html or 'href="su.html" class="channel-tab-btn  "' in html or 'id="tabWater"' in html
    assert 'href="su.html"' in html
    assert 'href="hayvancilik.html"' in html

def test_water_portal_routes(sample_water_items, sample_agri_items):
    """Verify Su Gündemi points to su.html and links back to index.html for Tarım."""
    html = generate_newspaper_portal_html(
        items=sample_water_items,
        last_updated="10.11.2026 12:00 UTC",
        rss_url="https://example.com/rss.xml",
        atom_url="https://example.com/atom.xml",
        json_url="https://example.com/feed.json",
        channel="water",
        water_count=1,
        agri_count=1,
        livestock_count=0,
        water_items=sample_water_items,
        agri_items=sample_agri_items
    )
    assert 'SU GÜNDEMİ' in html
    assert 'href="su.html" class="channel-tab-btn active" id="tabWater"' in html
    assert 'href="index.html" class="channel-tab-btn "' in html
