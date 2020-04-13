# Six degrees of separation

Well, not sure what format is expected, so let's try with a simple way:

## Description

Endpoint name: `separation_degree`

`GET` endpoint with url path params:

`/separation_degree/<int:person_id>/<int:bacon_number>`

Returns a list of people who are connected within X (range 1-X) degrees of separation to a specified person.

For future references:
- `X` - degrees of separation
- `ID` - person id

Url params:
- `person_id`: int > 0, a valid existing id of a person in the database
- `bacon_number`: int > 0, represent "degrees of separation"

Returns:

```json
[
    {
        "person_id": "<int>",
        "bacon_number": "<int:1-X>"
    },
    ...
    {
        "person_id": "<int>",
        "bacon_number": "<int:1-X>"
    }
]
```

## In a kind of formal way
```yaml
  /get_separation_degree:
    get:
      summary: "Return a list of connected (degrees of separation) people within range 1-X to ID"
      consumes:
      - "pathparams"
      produces:
      - "application/json"
      parameters:
      - in: "urlparams"
        person_id: "integer > 0, a valid existing id of a person in the database"
        bacon_number: "integer > 0"
        required: true
      responses:
        200:
          description: "Successful operation"
        400:
          description: "Invalid input"
        404:
          description: "Person with specified id was not found"
```

## Potential challenges:
- Performance issues in case of big X number
- Async/Batch processing to calculate data after each new Person

## Possible implemenation:
- Precalculate and store after each new person
    - (+) Fastest response
    - (-) Eventual consistency
- Find value when a request is arrived
    - (-) Long response time
    - (+) Consistent

## Questions:

- How often this endpoint will be used (request per second/minute)? Is there any performance limitation?
- Do we need to include added persons immidiately (to X calculations) or it's possible to guarantee only "eventual consistency"?
- Is it possible to set up a max possible X to simplify validation/performance?
- Do we need additional parameters to determine X? Is it possible that we will need it in future? More types of connections? Excluding persons by some criteria or specified ids?
