import pytest
from app.portal import generate_newspaper_portal_html, render_settings_modal_html

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

def test_agriculture_flashcards_and_calendar(sample_agri_items):
    """Verify Tarım Gündemi includes interactive agri flashcards and November planting calendar."""
    html = generate_newspaper_portal_html(
        items=sample_agri_items,
        last_updated="10.11.2026 12:00 UTC",
        rss_url="https://example.com/rss_tarim.xml",
        atom_url="https://example.com/atom_tarim.xml",
        json_url="https://example.com/feed_tarim.json",
        channel="agriculture"
    )
    assert 'Akıllı Tarım &amp; Çiftçi Rehberi' in html or 'Akıllı Tarım & Çiftçi Rehberi' in html
    assert 'Kasım Ayı Saha &amp; Ekim Takvimi' in html or 'Kasım Ayı Saha & Ekim Takvimi' in html
    assert 'Damla sulama' in html or 'Münavebe' in html

def test_livestock_flashcards_and_calendar():
    """Verify Hayvancılık Gündemi includes livestock flashcards and shelter calendar."""
    dummy_item = [{
        "id": 1, "title": "Besi Danası Rasyonu", "title_tr": "Besi Danası Rasyonu",
        "category_tr": "Besi", "source_feed": "Hayvancılık Basını", "pub_date": "10.11.2026",
        "link": "#", "image_url": "https://example.com/cow.jpg", "is_turkey": True, "is_academic": False
    }]
    html = generate_newspaper_portal_html(
        items=dummy_item,
        last_updated="10.11.2026 12:00 UTC",
        rss_url="https://example.com/rss_hayvancilik.xml",
        atom_url="https://example.com/atom_hayvancilik.xml",
        json_url="https://example.com/feed_hayvancilik.json",
        channel="livestock"
    )
    assert 'Modern Besi &amp; Sürü Yönetimi' in html or 'Modern Besi & Sürü Yönetimi' in html
    assert 'Kasım Ayı Barınak &amp; Besi Takvimi' in html or 'Kasım Ayı Barınak & Besi Takvimi' in html
    assert 'kolostrum' in html or 'asidoz' in html

def test_portal_startup_preferences_modal(sample_agri_items):
    """Verify that settings modal and startup preferences are rendered into portal."""
    modal_html = render_settings_modal_html()
    assert 'id="settingsModal"' in modal_html
    assert 'name="optStartupChannel"' in modal_html
    assert 'value="agriculture"' in modal_html
    assert 'value="water"' in modal_html
    assert 'value="livestock"' in modal_html
    assert 'name="optStartupTab"' in modal_html
    assert 'value="news"' in modal_html
    assert 'value="events"' in modal_html
    assert 'value="prices"' in modal_html

    # Check generated HTML contains top button and modal
    html = generate_newspaper_portal_html(
        items=sample_agri_items,
        last_updated="13.11.2026 10:00 UTC",
        rss_url="https://example.com/rss.xml",
        atom_url="https://example.com/atom.xml",
        json_url="https://example.com/feed.json",
        channel="agriculture"
    )
    assert 'id="portalSettingsBtn"' in html
    assert 'openPortalSettingsModal()' in html
    assert 'id="settingsModal"' in html
    assert 'initPortalStartupPreferences()' in html
    assert 'su_startup_prefs' in html


def test_portal_headline_photos_and_fallback(sample_agri_items):
    """Verify headline photos include zero-blank img tags, no-referrer policy, and SVG fallbacks."""
    html = generate_newspaper_portal_html(
        items=sample_agri_items,
        last_updated="13.11.2026 10:00 UTC",
        rss_url="https://example.com/rss.xml",
        atom_url="https://example.com/atom.xml",
        json_url="https://example.com/feed.json",
        channel="agriculture"
    )
    assert '<meta name="referrer" content="no-referrer">' in html
    assert 'class="hero-bg-img"' in html
    assert 'class="sub-bg-img"' in html
    assert 'class="card-bg-img"' in html
    assert 'handlePortalImageError(' in html
    assert 'PORTAL_FALLBACK_SVGS' in html
    assert 'data:image/svg+xml' in html

