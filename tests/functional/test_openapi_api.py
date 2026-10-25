from pytest_bdd import given, scenarios, then, when

scenarios("features/openapi_api.feature")


@given("the API is ready", target_fixture="api_state")
def api_is_ready(client):
    return {"client": client, "response": None}


@when("I request the OpenAPI document")
def request_openapi(api_state):
    api_state["response"] = api_state["client"].get("/openapi.json")


@then("the response status is 200")
def openapi_response_is_successful(api_state):
    assert api_state["response"].status_code == 200


@then("the OpenAPI document lists the root and users endpoints")
def openapi_lists_routes(api_state):
    paths = api_state["response"].json()["paths"]
    assert set(paths) >= {"/", "/users", "/users/{user_id}"}
    assert set(paths["/users"]) == {"get", "post"}
    assert set(paths["/users/{user_id}"]) == {"get", "patch", "delete"}
