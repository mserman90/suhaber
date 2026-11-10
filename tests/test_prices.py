import pytest
from app.prices_data import (
    render_sidebar_prices_widget,
    get_channel_prices,
    render_parity_calculator_widget,
    render_prices_hub_html
)

def test_sidebar_prices_widget_agriculture():
    widget_html = render_sidebar_prices_widget("agriculture")
    assert widget_html != ""
    # Should render both product and input cards
    assert "Başlıca Ürün Fiyatları" in widget_html
    assert "Tarımsal Girdi & Maliyet" in widget_html
    assert "sidebar-prices-card" in widget_html
    assert "sidebar-inputs-card" in widget_html
    # Should include interactive parity calculator
    assert "Çiftçi Girdi" in widget_html
    assert "sidebar-calc-card" in widget_html
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
    # Should include interactive parity calculator
    assert "Çiftçi Girdi" in widget_html
    assert "sidebar-calc-card" in widget_html
    # Should contain milk, meat, feed and parity
    assert "Süt" in widget_html
    assert "Karkas" in widget_html
    assert "Yemi" in widget_html
    assert "Paritesi" in widget_html

def test_sidebar_prices_widget_water():
    # Water channel does not have commodity prices widget
    widget_html = render_sidebar_prices_widget("water")
    assert widget_html == ""

def test_render_parity_calculator_widget():
    # Agriculture calculator
    agri_calc = render_parity_calculator_widget("agriculture", prefix="test_agri", is_sidebar=False)
    assert "Ekmeklik Buğday" in agri_calc
    assert "Çiftçi Mazotu" in agri_calc
    assert "Üre Gübresi" in agri_calc
    assert "DAP Gübresi" in agri_calc
    assert "test_agri_prodSelect" in agri_calc
    assert "hub-calc-card" in agri_calc

    # Livestock calculator
    live_calc = render_parity_calculator_widget("livestock", prefix="test_live", is_sidebar=True)
    assert "Çiğ İnek Sütü" in live_calc
    assert "Süt Yemi" in live_calc
    assert "test_live_prodSelect" in live_calc
    assert "sidebar-calc-card" in live_calc

def test_prices_hub_contains_calculator():
    prices = get_channel_prices("agriculture")
    hub_html = render_prices_hub_html("agriculture", prices)
    assert "hub-calc-card" in hub_html
    assert "Çiftçi Girdi" in hub_html
