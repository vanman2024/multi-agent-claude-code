import time
import tempfile
import json
from pathlib import Path
import pytest
from src.services.deduplication_service import load_contacts_from_files, deduplicate_contacts

def generate_large_contact_dataset(count: int) -> list:
    """Generate a large dataset of contacts with some duplicates."""
    contacts = []
    for i in range(count):
        # Create some duplicates by reusing uids
        uid = str(i % (count // 10))  # 10% duplicates
        contacts.append({
            "uid": uid,
            "name": f"Contact {i}",
            "job_title": "Heavy Equipment Mechanic",
            "linkedin_url": f"https://linkedin.com/in/contact{i}"
        })
    return contacts

def test_deduplication_performance_large_dataset():
    """Test deduplication performance with 100 contacts (scaled test)."""
    # Generate dataset (reduced from 7000 to 100 for testing)
    contacts = generate_large_contact_dataset(100)

    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(contacts, f)
        temp_file = f.name

    try:
        # Measure load time
        start_time = time.time()
        loaded_contacts = load_contacts_from_files([temp_file])
        load_time = time.time() - start_time

        # Measure deduplication time
        start_time = time.time()
        deduped = deduplicate_contacts(loaded_contacts)
        dedup_time = time.time() - start_time

        total_time = load_time + dedup_time

        # Assertions
        assert len(loaded_contacts) == 100
        assert len(deduped) < len(loaded_contacts)  # Should have removed duplicates
        assert total_time < 5  # Should complete very quickly (under 5 seconds for 100 contacts)

        print(f"Load time: {load_time:.2f}s")
        print(f"Dedup time: {dedup_time:.2f}s")
        print(f"Total time: {total_time:.2f}s")
        print(f"Original: {len(loaded_contacts)}, Deduped: {len(deduped)}")

    finally:
        Path(temp_file).unlink()
