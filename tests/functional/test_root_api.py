from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/root_api.feature")


@given("the API is ready", target_fixture="api_state")
def api_is_ready(client):
    return {"client": client, "response": None}


@when("I request the root endpoint")
def request_root(api_state):
    api_state["response"] = api_state["client"].get("/")


@then("the response status is 200")
def root_response_is_successful(api_state):
    assert api_state["response"].status_code == 200


@then(parsers.parse('the response message is "{message}"'))
def root_response_has_greeting(api_state, message):
    assert api_state["response"].json() == {"message": message}
