from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests, json
from django.views.decorators.csrf import csrf_exempt

def get_dynamics_data(request):
    # Authentication details
    client_id = '4ee4b905-1072-4847-ad0e-18789ec52916'
    client_secret = 'jXr8Q~wx2TxkdmQQeQk.2aaeNzuPrNA~176Y1a1s'
    tenant_id = '1a55aa79-6752-4642-8503-6d82888db1d0'
    resource = 'https://usnconeboxax1aos.cloud.onebox.dynamics.com/'

    # Get OAuth token
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': resource
    }
    token_r = requests.post(token_url, data=token_data)
    access_token = token_r.json().get('access_token')

    # Fetch data from Dynamics 365
    dynamics_url = 'https://usnconeboxax1aos.cloud.onebox.dynamics.com/data/MyCars'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    dynamics_response = requests.get(dynamics_url, headers=headers, verify=False)
    
    data = dynamics_response.json()

    return JsonResponse(data, safe=False)


@csrf_exempt
def create_dynamics_data(request):
    if request.method == 'POST':
        # Authentication details
        client_id = '4ee4b905-1072-4847-ad0e-18789ec52916'
        client_secret = 'jXr8Q~wx2TxkdmQQeQk.2aaeNzuPrNA~176Y1a1s'
        tenant_id = '1a55aa79-6752-4642-8503-6d82888db1d0'
        resource = 'https://usnconeboxax1aos.cloud.onebox.dynamics.com/'

        # Get OAuth token
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': resource
        }
        token_r = requests.post(token_url, data=token_data)
        access_token = token_r.json().get('access_token')

        # Fetch data from Dynamics 365
        dynamics_url = 'https://usnconeboxax1aos.cloud.onebox.dynamics.com/data/MyCars'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Extract data from the POST request
        data = request.GET
        
        # Create data to be sent to Dynamics 365
        data_to_create = {       
                'CarId': data.get('CarId'),
                'BrandName': data.get('BrandName'),
                'Color': data.get('Color')           
        }

        dynamics_response = requests.post(dynamics_url, headers=headers, json=data_to_create, verify=False)

        if dynamics_response.status_code == 201:  # Created
            return JsonResponse({'message': 'Data created successfully'}, status=201)
        else:
            return JsonResponse({'error': 'Failed to create data'}, status=dynamics_response.status_code)

    # Return error response for unsupported methods
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_dynamics_data(request, dataAreaId, CarId):
    if request.method == 'DELETE':
        # Authentication details
        client_id = '4ee4b905-1072-4847-ad0e-18789ec52916'
        client_secret = 'jXr8Q~wx2TxkdmQQeQk.2aaeNzuPrNA~176Y1a1s'
        tenant_id = '1a55aa79-6752-4642-8503-6d82888db1d0'
        resource = 'https://usnconeboxax1aos.cloud.onebox.dynamics.com/'

        # Get OAuth token
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': resource
        }

        try:
            token_r = requests.post(token_url, data=token_data)
            access_token = token_r.json().get('access_token')

            # Dynamics 365 URL for the specific car_id
            dynamics_url = f"https://usnconeboxax1aos.cloud.onebox.dynamics.com/data/MyCars(dataAreaId='{dataAreaId}',CarId='{CarId}')"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            # Perform DELETE request to Dynamics 365
            dynamics_response = requests.delete(dynamics_url, headers=headers,verify=False)          

            if dynamics_response.status_code == 204:  # No content (successful deletion)
                return JsonResponse({'message': 'Data deleted successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Failed to delete data'}, status=dynamics_response.status_code)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_dynamics_data(request, dataAreaId, CarId):
    if request.method == 'PUT':
        # Authentication details
        client_id = '4ee4b905-1072-4847-ad0e-18789ec52916'
        client_secret = 'jXr8Q~wx2TxkdmQQeQk.2aaeNzuPrNA~176Y1a1s'
        tenant_id = '1a55aa79-6752-4642-8503-6d82888db1d0'
        resource = 'https://usnconeboxax1aos.cloud.onebox.dynamics.com/'

        # Get OAuth token
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': resource
        }

        try:
            token_r = requests.post(token_url, data=token_data)
            access_token = token_r.json().get('access_token')

            # Dynamics 365 URL for the specific car_id
            dynamics_url = f"https://usnconeboxax1aos.cloud.onebox.dynamics.com/data/MyCars(dataAreaId='{dataAreaId}',CarId='{CarId}')"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Extract data from the PUT request body
            data = json.loads(request.body)  
            print(data)

        
            # Perform PUT request to Dynamics 365
            dynamics_response = requests.put(dynamics_url, headers=headers, json=data, verify=False)          

            if dynamics_response.status_code == 204:  # No content (successful update)
                return JsonResponse({'message': 'Data updated successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Failed to update data'}, status=dynamics_response.status_code)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)