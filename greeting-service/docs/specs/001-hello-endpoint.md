# Spec 001: Hello Endpoint

## Intent
Expose a `GET /hello` endpoint that returns a greeting in the requested
language.

## Inputs
- Query parameter `name` is optional and defaults to `world`.
- Query parameter `name` must be 50 characters or fewer after trimming.
- Query parameter `lang` is optional and defaults to `en`.
- Supported `lang` values are `en`, `es`, and `fr`.

## Output
- `200` with JSON body `{"greeting": "<string>", "language": "<string>"}`.
- `400` when `name` is too long.
- `400` when `lang` is unsupported.
- `404` for any route other than `/hello` and `/health`.

## Acceptance Criteria
- Unit tests cover valid and invalid request combinations.
- Integration tests hit the running HTTP endpoint.
- Property tests confirm the response payload can be emitted as UTF-8 JSON.
- The spec compliance dataset includes at least 10 cases for this spec.

## Out Of Scope
- Authentication
- Persistence
- Rate limiting
- External API calls
