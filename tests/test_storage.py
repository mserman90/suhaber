import pytest
from pathlib import Path
from app.storage import Storage

def test_storage_lifecycle(tmp_path: Path):
    db_file = tmp_path / "test_feed.db"
    storage = Storage(db_file)

    sample_items = [
        {
            "guid": "test:item:1",
            "title": "İlk Haber",
            "link": "https://example.com/1",
            "author": "Yazar",
            "source_feed": "Kaynak",
            "description": "Açıklama",
            "image_url": "https://example.com/img.jpg",
            "pub_date": "Wed, 06 Nov 2026 09:00:00 +0000",
            "pub_date_ts": 1730883600,
            "raw_date_str": "06 Nov 2026",
            "title_tr": "İlk Türkçe Haber",
            "summary_tr": "Türkçe Özet",
            "category_tr": "Su Kaynakları"
        }
    ]

    # Save
    inserted = storage.save_items(sample_items, default_channel="water")
    assert inserted == 1
    assert storage.count_items() == 1

    # Retrieve
    items = storage.get_items(limit=10, channel="water")
    assert len(items) == 1
    assert items[0]["title_tr"] == "İlk Türkçe Haber"

    # Meta
    storage.set_meta("test_key", "test_value")
    assert storage.get_meta("test_key") == "test_value"

    # Prune & Vacuum
    storage.prune_items(max_items_per_channel=10)
    assert storage.count_items() == 1
