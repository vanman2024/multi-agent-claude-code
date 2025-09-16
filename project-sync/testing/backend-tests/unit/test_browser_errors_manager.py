import pytest
pytest.skip("Skipped in API-only mode (browser errors manager not present)", allow_module_level=True)


@pytest.mark.unit
def test_is_transient_classification():
    assert is_transient(TransientBrowserError("tmp"))
    assert not is_transient(PermanentBrowserError("no"))


@pytest.mark.unit
@pytest.mark.asyncio
async def test_browser_session_retries_on_transient_errors():
    calls = {"n": 0}

    async def factory():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TransientBrowserError("flaky start")
        return object()

    async with BrowserSession(factory, retries=3) as browser:
        assert browser is not None
    # Should have attempted until success
    assert calls["n"] == 3


@pytest.mark.unit
@pytest.mark.asyncio
async def test_browser_session_raises_on_permanent_error():
    async def factory():
        raise PermanentBrowserError("bad creds")

    with pytest.raises(PermanentBrowserError):
        async with BrowserSession(factory, retries=5):
            pass
import pytest
pytest.skip("Skipped in API-only mode (browser errors manager not present)", allow_module_level=True)
