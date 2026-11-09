import pytest
from app.geocoder import geocode_article, evaluate_article_location

def test_geocode_turkish_province():
    article = {
        "title": "İzmir barajlarında doluluk oranı kritik seviyenin altına indi",
        "description": "İZSU yetkilileri İzmir genelinde su tasarrufu çağrısı yaptı.",
        "source_feed": "Ege Haberleri"
    }
    lat, lon, label = geocode_article(article)
    assert lat is not None
    assert lon is not None
    assert "İzmir" in label

def test_geocode_basin_location():
    article = {
        "title": "Kızılırmak havzasında kuraklık alarmı verildi",
        "description": "DSİ nehir debisindeki düşüşü incelemeye aldı.",
        "source_feed": "Ulusal Basın"
    }
    lat, lon, label = geocode_article(article)
    assert lat is not None
    assert lon is not None
    assert label is not None

def test_geocode_homonym_protection():
    # 'mısır' (corn/maize) should not falsely geocode to Egypt (Mısır) in agricultural contexts
    article = {
        "title": "TMO mısır alım fiyatlarını ton başına 9500 TL olarak güncelledi",
        "description": "Çukurova'da mısır hasadı devam ediyor.",
        "source_feed": "Tarım Bülteni"
    }
    lat, lon, label = geocode_article(article)
    # Should resolve to Çukurova / Adana region, not Cairo / Egypt!
    if label:
        assert "Kahire" not in label
        assert "Mısır Ülkesi" not in label
