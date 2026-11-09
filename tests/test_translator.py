import pytest
from app.translator import (
    clean_html_and_metadata,
    strip_publisher_suffix,
    is_genuinely_turkish,
    categorize_article,
    categorize_agriculture_article,
    categorize_livestock_article
)

def test_clean_html_and_metadata():
    raw = "<p>Konya Ovası'nda <b>yeraltı su seviyesi</b> kritik eşikte.&nbsp;</p>"
    clean = clean_html_and_metadata(raw)
    assert clean == "Konya Ovası'nda yeraltı su seviyesi kritik eşikte."
    assert "<p>" not in clean
    assert "&nbsp;" not in clean

def test_strip_publisher_suffix():
    title = "Baraj doluluk oranları açıklandı - AA"
    assert strip_publisher_suffix(title) == "Baraj doluluk oranları açıklandı"

    title_yt = "Su Verimliliği Raporu || The Gist - YouTube"
    assert "YouTube" not in strip_publisher_suffix(title_yt)

def test_is_genuinely_turkish():
    assert is_genuinely_turkish("Devlet Su İşleri yeni sulama kanalını hizmete açtı") is True
    assert is_genuinely_turkish("Konya Ovası'nda buğday hasadı tamamlandı") is True
    assert is_genuinely_turkish("Water resources management in Colorado river basin") is False
    assert is_genuinely_turkish("Die Wasserwirtschaft und Grundwasserbericht") is False

def test_categorize_article():
    cat = categorize_article("Atatürk Barajı doluluk oranı açıklandı", "Barajda su seviyesi yükseldi.")
    assert cat in ["Barajlar & Göller", "Su Kaynakları"]

def test_categorize_agriculture_article():
    cat = categorize_agriculture_article("Buğday ve Arpa tohumculuk destekleri açıklandı", "TMO alım fiyatları")
    assert cat in ["Tahıllar & Bakliyat", "Tarımsal Destekler & Borsa", "Tohum & Gübre"]

def test_categorize_livestock_article():
    cat = categorize_livestock_article("Ulusal Süt Konseyi çiğ süt tavsiye fiyatını belirledi", "Süt üreticileri")
    assert cat in ["Süt Endüstrisi & USK", "Büyükbaş & Besicilik"]
