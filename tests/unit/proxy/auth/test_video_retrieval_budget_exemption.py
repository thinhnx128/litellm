import pytest

from litellm.proxy.auth.auth_checks import (
    _is_video_retrieval_route,
    route_skips_budget_checks,
)


@pytest.mark.parametrize(
    "route",
    [
        "/v1/videos/vid_abc123",
        "/videos/vid_abc123",
        "/v1/videos/vid_abc123/content",
        "/videos/vid_abc123/content",
        "/v1/videos/{video_id}",
        "/videos/{video_id}",
        "/v1/videos/{video_id}/content",
        "/videos/{video_id}/content",
    ],
)
def test_video_status_and_content_routes_skip_budget_checks(route: str):
    """
    Regression test for #51147: polling video status or downloading video content
    for an already-created video does not incur new spend and must be allowed
    even when the key or end-user budget is exhausted.
    """
    assert _is_video_retrieval_route(route) is True
    assert route_skips_budget_checks(route) is True


@pytest.mark.parametrize(
    "route",
    [
        "/v1/videos",
        "/videos",
        "/v1/videos/",
        "/videos/",
        "/v1/videos/vid_abc123/remix",
        "/videos/vid_abc123/remix",
        "/v1/videos/{video_id}/remix",
        "/videos/{video_id}/remix",
        "/v1/chat/completions",
    ],
)
def test_video_creation_and_remix_routes_enforce_budget_checks(route: str):
    """
    Video creation (POST /v1/videos) and remix (POST /v1/videos/{video_id}/remix)
    incur spend and must continue to enforce budget checks.
    """
    assert _is_video_retrieval_route(route) is False
    assert route_skips_budget_checks(route) is False
