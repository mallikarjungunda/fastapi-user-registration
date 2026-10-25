from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/users_api.feature")


@given("the API is ready", target_fixture="api_state")
def api_is_ready(client):
    return {
        "client": client,
        "response": None,
        "first_user_id": None,
    }


@when(
    parsers.parse(
        'I register a user named "{name}" with email "{email}" and password "{password}"'
    )
)
def register_user(api_state, name, email, password):
    response = api_state["client"].post(
        "/users",
        json={"name": name, "email": email, "password": password},
    )
    api_state["response"] = response
    if response.status_code == 201 and api_state["first_user_id"] is None:
        api_state["first_user_id"] = response.json()["id"]


@when("I list users")
def list_users(api_state):
    api_state["response"] = api_state["client"].get("/users")


@when(parsers.parse("I list users with offset {offset:d} and limit {limit:d}"))
def list_users_with_pagination(api_state, offset, limit):
    api_state["response"] = api_state["client"].get(
        "/users",
        params={"offset": offset, "limit": limit},
    )


@when("I get the first registered user")
def get_first_user(api_state):
    api_state["response"] = api_state["client"].get(
        f"/users/{api_state['first_user_id']}"
    )


@when(parsers.parse("I get user {user_id:d}"))
def get_user(api_state, user_id):
    api_state["response"] = api_state["client"].get(f"/users/{user_id}")


@when(parsers.parse('I update the first registered user\'s name to "{name}"'))
def update_first_user(api_state, name):
    api_state["response"] = api_state["client"].patch(
        f"/users/{api_state['first_user_id']}",
        json={"name": name},
    )


@when(parsers.parse('I update user {user_id:d}\'s name to "{name}"'))
def update_user(api_state, user_id, name):
    api_state["response"] = api_state["client"].patch(
        f"/users/{user_id}",
        json={"name": name},
    )


@when("I delete the first registered user")
def delete_first_user(api_state):
    api_state["response"] = api_state["client"].delete(
        f"/users/{api_state['first_user_id']}"
    )


@when(parsers.parse("I delete user {user_id:d}"))
def delete_user(api_state, user_id):
    api_state["response"] = api_state["client"].delete(f"/users/{user_id}")


@then(parsers.parse("the response status is {status:d}"))
def response_has_status(api_state, status):
    assert api_state["response"].status_code == status


@then(
    parsers.parse(
        'the response user has name "{name}" and email "{email}"'
    )
)
def response_user_has_fields(api_state, name, email):
    assert api_state["response"].json()["name"] == name
    assert api_state["response"].json()["email"] == email


@then("the response does not expose password fields")
def response_hides_password(api_state):
    response_body = api_state["response"].json()
    assert "password" not in response_body
    assert "password_hash" not in response_body


@then(parsers.parse('the response user names are "{names}"'))
def response_has_user_names(api_state, names):
    expected_names = [] if not names else names.split(",")
    assert [user["name"] for user in api_state["response"].json()] == expected_names


@then("the response body is empty")
def response_body_is_empty(api_state):
    assert api_state["response"].content == b""


@then(parsers.parse('the response error is "{message}"'))
def response_has_error(api_state, message):
    assert api_state["response"].json() == {"detail": message}
