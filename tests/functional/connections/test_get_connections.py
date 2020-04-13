from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory


def test_get_connections(db, testapp):
    # TODO: id is not available after create, so let's specify
    # it directly. Oh, dirty
    person_from = PersonFactory(id=100, first_name='Diana')
    person_to = PersonFactory(id=200, first_name='Harry')
    ConnectionFactory(
        from_person=person_from,
        to_person=person_to,
    )
    db.session.commit()

    expected_connection = {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'friend',
    }
    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK
    assert len(res.json) == 1
    result_connection = res.json[0]

    assert expected_connection['from_person_id'] == result_connection['from_person_id']
    assert expected_connection['to_person_id'] == result_connection['to_person_id']
    assert expected_connection['connection_type'] == result_connection['connection_type']
