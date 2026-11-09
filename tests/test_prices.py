import pytest
from app.prices_data import render_sidebar_prices_widget, get_channel_prices

def test_sidebar_prices_widget_agriculture():
    widget_html = render_sidebar_prices_widget("agriculture")
    assert widget_html != ""
    # Should render both product and input cards
    assert "Başlıca Ürün Fiyatları" in widget_html
    assert "Tarımsal Girdi & Maliyet" in widget_html
    assert "sidebar-prices-card" in widget_html
    assert "sidebar-inputs-card" in widget_html
    # Should contain key products and inputs
    assert "Buğday" in widget_html
    assert "Çiftçi Mazotu" in widget_html or "Mazot" in widget_html
    assert "Gübre" in widget_html

def test_sidebar_prices_widget_livestock():
    widget_html = render_sidebar_prices_widget("livestock")
    assert widget_html != ""
    # Should render both product and input cards
    assert "Hayvansal Ürün & Karkas" in widget_html
    assert "Yem & Besleme Girdileri" in widget_html
    assert "sidebar-prices-card" in widget_html
    assert "sidebar-inputs-card" in widget_html
    # Should contain milk, meat, feed and parity
    assert "Süt" in widget_html
    assert "Karkas" in widget_html
    assert "Yemi" in widget_html
    assert "Paritesi" in widget_html

def test_sidebar_prices_widget_water():
    # Water channel does not have commodity prices widget
    widget_html = render_sidebar_prices_widget("water")
    assert widget_html == ""
