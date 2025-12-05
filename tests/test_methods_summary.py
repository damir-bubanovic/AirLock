from airlock.methods_summary import generate_methods_summary


def test_methods_summary_basic():
    text = generate_methods_summary(
        nox_rows=100,
        postcode_rows=200,
        matched_rows=180,
        unmatched_rows=20,
        match_rate=0.9,
    )

    assert "AirLock – Methods Summary" in text
    assert "Total NOx grid cells loaded: 100" in text
    assert "Total postcode records processed: 200" in text
    assert "Matched postcodes: 180" in text
    assert "Unmatched postcodes: 20" in text
    assert "Match rate: 90.00%" in text
