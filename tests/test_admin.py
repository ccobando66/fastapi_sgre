from .base_module import *

def test_get_user_by_cedula():
    cedula = '1012432366'
    response = client.get(f'http://localhost:8000/admin/whoami',
                          headers={'Authorization':f'Bearer {token}'}
                          )
    
    data = response.json()
    assert response.status_code == 200
    assert cedula in data['user']['cedula'] 
    
    
    
def test_repeat_again_admin():
    cedula = '1012432366'
    response = client.post('http://localhost:8000/admin/',
                           json={'user_cedula':cedula},
                           headers={'Authorization':f'Bearer {token}'}
                           )
    
    assert response.status_code == 400
    assert response.json() == {"detail": f"{cedula} ya esta registrado en el sistema o esta registrado con otro rol"}

def test_set_user_in_admin():
    cedula = '1012432365'
    response = client.post('http://localhost:8000/admin/',
                           json={'user_cedula':cedula},
                           headers={'Authorization':f'Bearer {token}'}
                           )
    data = response.json() 
    assert response.status_code == 200
    assert cedula in data['user']['cedula']
    
    

def test_try_delete_admin_on_db_doesnot_exists():
    cedula = "1012432364"
    response = client.delete(f'http://localhost:8000/admin/{cedula}/admin',
                               headers={'Authorization':f'Bearer {token}'}
                            )
    assert response.status_code == 404


def test_unlock_user_from_admin():
    cedula = '1012432365'
    response = client.put(f'http://localhost:8000/admin/{cedula}/admin/unlock',
                            headers={'Authorization':f'Bearer {token}'}
                         )
    data = response.json()
    assert response.status_code == 200
    assert cedula in data['cedula']
    

def test_lock_user_from_admin():
    cedula = '1012432365'
    response = client.put(f'http://localhost:8000/admin/{cedula}/admin/lock',
                            headers={'Authorization':f'Bearer {token}'}
                         )
    data = response.json()
    assert response.status_code == 200
    assert cedula in data['cedula']
    
    

