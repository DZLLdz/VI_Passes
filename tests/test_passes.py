# import json
# import pytest
# from models import Passes
#
#
# def test_send_data(test_client, sample_user):
#     data = {
#         "data": {
#             "users_id": f"{sample_user.id}",
#             "coords_id": "1",
#             "images": [],
#             "beautyTitle": "пер.",
#             "title": "Title1",
#             "other_titles": "Title2",
#             "connect": [],
#             "level": {
#                 "winter": "threeA",
#                 "spring": "oneB",
#                 "summer": "twoA",
#                 "autumn": "z1"
#             }
#         }
#     }
#     data_json = json.dumps(data)
#
#     response = test_client.post('/api/sendData',
#                                 data=data_json,
#                                 content_type='application/json')
#     assert response.status_code == 200
#
#     try:
#         response_json = response.get_json()
#     except ValueError:
#         pytest.fail("Response data is not valid JSON")
#
#     assert 'message' in response_json
#
#
# def test_get_pass(test_client, sample_pass):
#     response = test_client.get(f'/api/submitData/{sample_pass.id}')
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert data['data']['beautyTitle'] == sample_pass.beautyTitle
#
#
# def test_get_passes_for_mail(test_client, sample_user, sample_pass):
#     response = test_client.get(f'/api/passes/{sample_user.email}')
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert len(data['data']) == 1
#     assert data['data'][0]['beautyTitle'] == sample_pass.beautyTitle
#
#
# def test_post_pass(test_client):
#     data = {
#         "data": {
#             "users_id": 1,
#             "coords_id": 1,
#             "images": [],
#             "beautyTitle": "Test",
#             "title": "Test Title",
#             "other_titles": "Other Titles",
#             "connect": [],
#             "level": {
#                 "winter": "oneA",
#                 "spring": "oneB",
#                 "summer": "twoA",
#                 "autumn": "z1"
#             }
#         }
#     }
#     response = test_client.post('/api/sendData', json=data)
#     assert response.status_code == 200
#     response_data = response.get_json()
#     assert response_data['message'] == 'Data submitted successfully'
#
#
# def test_patch_pass(test_client, sample_pass):
#     data = {
#         "data": {
#             "beautyTitle": "Updated Title",
#             "level": {
#                 "winter": "twoA",
#                 "spring": "oneB",
#                 "summer": "twoB",
#                 "autumn": "z1"
#             }
#         }
#     }
#     response = test_client.patch(f'/api/submitData/{sample_pass.id}', json=data)
#     assert response.status_code == 200
#     updated_pass = Passes.query.get(sample_pass.id)
#     assert updated_pass.beautyTitle == "Updated Title"
