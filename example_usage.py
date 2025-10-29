#!/usr/bin/env python3
"""
Example usage of the CMDB Tree API.
This script demonstrates how to use the API endpoints.
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def main():
    """Example API usage"""
    
    # 1. Create a tree object model (e.g., "host")
    print("\n1. Creating tree object model 'host'...")
    response = requests.post(
        f"{BASE_URL}/api/model/tree/object",
        json={
            "bk_obj_id": "host",
            "bk_obj_name": "主机",
            "properties": {
                "description": "主机对象模型"
            }
        }
    )
    print_response(response, "Create Object Model")
    
    # 2. List object models
    print("\n2. Listing object models...")
    response = requests.post(
        f"{BASE_URL}/api/model/tree/object/list",
        json={
            "page": 1,
            "page_size": 20
        }
    )
    print_response(response, "List Object Models")
    
    # 3. Create a root tree node
    print("\n3. Creating root tree node...")
    response = requests.post(
        f"{BASE_URL}/api/tree/host",
        json={
            "bk_inst_name": "根节点",
            "properties": {
                "ip": "192.168.1.1",
                "description": "根主机"
            }
        }
    )
    print_response(response, "Create Root Node")
    root_inst_id = response.json()['data']['bk_inst_id']
    
    # 4. Create a child node
    print("\n4. Creating child node...")
    response = requests.post(
        f"{BASE_URL}/api/tree/host",
        json={
            "bk_inst_name": "子节点1",
            "parent_obj_id": "host",
            "parent_inst_id": root_inst_id,
            "properties": {
                "ip": "192.168.1.2",
                "description": "子主机1"
            }
        }
    )
    print_response(response, "Create Child Node")
    child_inst_id = response.json()['data']['bk_inst_id']
    
    # 5. List children
    print("\n5. Listing children of root node...")
    response = requests.post(
        f"{BASE_URL}/api/tree/host/host/{root_inst_id}/list",
        json={
            "page": 1,
            "page_size": 20
        }
    )
    print_response(response, "List Children")
    
    # 6. Update a node
    print("\n6. Updating child node...")
    response = requests.put(
        f"{BASE_URL}/api/tree/host",
        json={
            "bk_inst_id": child_inst_id,
            "bk_inst_name": "子节点1（已更新）",
            "properties": {
                "ip": "192.168.1.10"
            }
        }
    )
    print_response(response, "Update Node")
    
    # 7. Create another child for moving
    print("\n7. Creating another child node for testing move...")
    response = requests.post(
        f"{BASE_URL}/api/tree/host",
        json={
            "bk_inst_name": "子节点2",
            "parent_obj_id": "host",
            "parent_inst_id": root_inst_id,
            "properties": {
                "ip": "192.168.1.3"
            }
        }
    )
    print_response(response, "Create Another Child")
    child2_inst_id = response.json()['data']['bk_inst_id']
    
    # 8. Move node (move child2 to be under child1)
    print("\n8. Moving child2 under child1...")
    response = requests.post(
        f"{BASE_URL}/api/tree/host/move",
        json={
            "bk_inst_id": child2_inst_id,
            "target_parent_obj_id": "host",
            "target_parent_inst_id": child_inst_id
        }
    )
    print_response(response, "Move Node")
    
    # 9. Copy a node
    print("\n9. Copying a node...")
    response = requests.post(
        f"{BASE_URL}/api/tree/host/copy",
        json={
            "bk_inst_id": child_inst_id,
            "target_parent_obj_id": "host",
            "target_parent_inst_id": root_inst_id,
            "new_inst_name": "子节点1的副本"
        }
    )
    print_response(response, "Copy Node")
    
    # 10. Create a service object and bind
    print("\n10. Creating service object model...")
    response = requests.post(
        f"{BASE_URL}/api/model/tree/object",
        json={
            "bk_obj_id": "service",
            "bk_obj_name": "服务",
            "properties": {
                "description": "服务对象模型"
            }
        }
    )
    print_response(response, "Create Service Object Model")
    
    # 11. Create a service instance
    print("\n11. Creating service instance...")
    response = requests.post(
        f"{BASE_URL}/api/tree/service",
        json={
            "bk_inst_name": "Web服务",
            "properties": {
                "port": 80,
                "protocol": "http"
            }
        }
    )
    print_response(response, "Create Service Instance")
    service_inst_id = response.json()['data']['bk_inst_id']
    
    # 12. Bind service to host
    print("\n12. Binding service to host...")
    response = requests.post(
        f"{BASE_URL}/api/tree/service/inst/bind",
        json={
            "service_obj_id": "service",
            "service_inst_id": service_inst_id,
            "target_obj_id": "host",
            "target_inst_id": root_inst_id
        }
    )
    print_response(response, "Bind Service")
    
    # 13. Unbind service from host
    print("\n13. Unbinding service from host...")
    response = requests.post(
        f"{BASE_URL}/api/tree/service/inst/unbind",
        json={
            "service_obj_id": "service",
            "service_inst_id": service_inst_id,
            "target_obj_id": "host",
            "target_inst_id": root_inst_id
        }
    )
    print_response(response, "Unbind Service")
    
    # 14. Delete a node (soft delete)
    print("\n14. Deleting a node (soft delete)...")
    response = requests.delete(
        f"{BASE_URL}/api/tree/host",
        json={
            "bk_inst_id": child2_inst_id
        }
    )
    print_response(response, "Delete Node")
    
    print("\n" + "="*60)
    print("Example completed! Check http://localhost:8000/docs for full API documentation.")
    print("="*60)

if __name__ == "__main__":
    print("CMDB Tree API Usage Example")
    print("Make sure the API server is running on http://localhost:8000")
    print("Start the server with: uvicorn main:app --reload")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            main()
        else:
            print("Server is running but returned unexpected status")
    except requests.exceptions.ConnectionError:
        print("\nError: Cannot connect to API server.")
        print("Please start the server first with: uvicorn main:app --reload")
    except Exception as e:
        print(f"\nError: {e}")
