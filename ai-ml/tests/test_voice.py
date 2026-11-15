import base64


def test_voice_tts_synthesis_success(client, auth_headers):
    """Test text-to-speech returns playable base64 audio and MIME type."""
    payload = {
        "text": "ನಿಮ್ಮ ಕೆಲಸವನ್ನು ನಾಯಕರು ಅನುಮೋದಿಸಿದ್ದಾರೆ.",
        "language": "kn"
    }
    response = client.post("/api/v1/ai/voice/tts", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "audio_base64" in data
    assert len(data["audio_base64"]) > 100
    assert "audio/" in data["mime_type"]

    # Verify base64 is valid
    decoded = base64.b64decode(data["audio_base64"])
    assert len(decoded) > 0


def test_voice_stt_provider_unavailable_when_unconfigured(client, auth_headers):
    """Test that when external Whisper STT provider is unconfigured, it returns HTTP 503."""
    dummy_wav = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    b64_dummy = base64.b64encode(dummy_wav).decode("utf-8")

    payload = {
        "audio_base64": b64_dummy,
        "language": "kn"
    }
    response = client.post("/api/v1/ai/voice/stt", json=payload, headers=auth_headers)
    # When no SPEECH_API_KEY is configured in env, must honestly return 503!
    assert response.status_code == 503
    err = response.json()
    assert err["success"] is False
    assert err["error"]["code"] == "PROVIDER_UNAVAILABLE"


def test_voice_tts_unsupported_language(client, auth_headers):
    """Test TTS rejects unsupported language codes with HTTP 400."""
    payload = {
        "text": "Hello world",
        "language": "fr"  # French is not supported (only en, kn, hi)
    }
    response = client.post("/api/v1/ai/voice/tts", json=payload, headers=auth_headers)
    assert response.status_code == 400

