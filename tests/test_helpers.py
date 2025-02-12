"""Tests for utility/helper functions."""

from pytest import raises

from music_assistant.common.helpers import uri, util
from music_assistant.common.models import media_items
from music_assistant.common.models.errors import MusicAssistantError


def test_version_extract():
    """Test the extraction of version from title."""
    test_str = "Bam Bam (feat. Ed Sheeran) - Karaoke Version"
    title, version = util.parse_title_and_version(test_str)
    assert title == "Bam Bam"
    assert version == "Karaoke Version"


def test_uri_parsing():
    """Test parsing of URI."""
    # test regular uri
    test_uri = "spotify://track/123456789"
    media_type, provider, item_id = uri.parse_uri(test_uri)
    assert media_type == media_items.MediaType.TRACK
    assert provider == "spotify"
    assert item_id == "123456789"
    # test spotify uri
    test_uri = "spotify:track:123456789"
    media_type, provider, item_id = uri.parse_uri(test_uri)
    assert media_type == media_items.MediaType.TRACK
    assert provider == "spotify"
    assert item_id == "123456789"
    # test public play/open url
    test_uri = "https://open.spotify.com/playlist/5lH9NjOeJvctAO92ZrKQNB?si=04a63c8234ac413e"
    media_type, provider, item_id = uri.parse_uri(test_uri)
    assert media_type == media_items.MediaType.PLAYLIST
    assert provider == "spotify"
    assert item_id == "5lH9NjOeJvctAO92ZrKQNB"
    # test filename with slashes as item_id
    test_uri = "filesystem://track/Artist/Album/Track.flac"
    media_type, provider, item_id = uri.parse_uri(test_uri)
    assert media_type == media_items.MediaType.TRACK
    assert provider == "filesystem"
    assert item_id == "Artist/Album/Track.flac"
    # test invalid uri
    with raises(MusicAssistantError):
        uri.parse_uri("invalid://blah")
