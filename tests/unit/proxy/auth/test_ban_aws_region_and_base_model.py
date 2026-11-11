import pytest

from litellm.proxy.auth.auth_utils import (
    _BANNED_REQUEST_BODY_PARAMS,
    is_request_body_safe,
)


@pytest.mark.parametrize("banned_param", ["aws_region_name", "base_model"])
def test_aws_region_name_and_base_model_rejected_by_default(banned_param: str):
    """
    Regression test for #51185: client-supplied aws_region_name and base_model
    must be rejected by default so callers cannot override the deployment
    configured AWS region or cost calculation model.
    """
    assert banned_param in _BANNED_REQUEST_BODY_PARAMS
    with pytest.raises(ValueError, match=f"Rejected Request: {banned_param} is not allowed in request body"):
        is_request_body_safe(
            request_body={"model": "claude-sonnet", banned_param: "override-value"},
            general_settings={},
            llm_router=None,
            model="claude-sonnet",
        )


@pytest.mark.parametrize("param_name", ["aws_region_name", "base_model"])
def test_aws_region_name_and_base_model_allowed_when_global_opt_in_enabled(param_name: str):
    """
    When general_settings.allow_client_side_credentials is True, client-supplied
    aws_region_name and base_model are permitted.
    """
    assert (
        is_request_body_safe(
            request_body={"model": "claude-sonnet", param_name: "override-value"},
            general_settings={"allow_client_side_credentials": True},
            llm_router=None,
            model="claude-sonnet",
        )
        is True
    )
