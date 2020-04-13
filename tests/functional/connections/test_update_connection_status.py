from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory


def test_update_connection_status(db, testapp):
    person_from = PersonFactory(first_name='Diana')
    person_to = PersonFactory(first_name='Harry')
    db.session.commit()

    connection = ConnectionFactory(
        from_person=person_from,
        to_person=person_to,
    )
    db.session.commit()

    connection_type = 'mother'
    expected_connection = {
        'id': connection.id,
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': connection_type,
    }
    payload = {
        'connection_type': connection_type,
    }
    res = testapp.put(f'/connections/{connection.id}', json=payload)

    assert res.status_code == HTTPStatus.OK
    result_connection = res.json

    assert expected_connection['from_person_id'] == result_connection['from_person_id']
    assert expected_connection['to_person_id'] == result_connection['to_person_id']
    assert expected_connection['connection_type'] == result_connection['connection_type']
