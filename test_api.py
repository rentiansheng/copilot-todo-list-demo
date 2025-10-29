"""
Basic tests for the CMDB Tree API
"""

import pytest

def test_api_routes_exist():
    """Test that all required API routes are registered"""
    from main import app
    routes = [route.path for route in app.routes]
    
    # Check tree operation routes
    assert "/api/tree/{type}" in routes
    assert "/api/tree/{type}/move" in routes
    assert "/api/tree/{type}/copy" in routes
    assert "/api/tree/{tree_id}/{parent_obj_id}/{parent_inst_id}/list" in routes
    
    # Check service binding routes
    assert "/api/tree/service/inst/bind" in routes
    assert "/api/tree/service/inst/unbind" in routes
    
    # Check model routes
    assert "/api/model/tree/object" in routes
    assert "/api/model/tree/object/list" in routes

def test_app_starts():
    """Test that the FastAPI app can be imported and initialized"""
    from main import app
    assert app is not None
    assert app.title == "CMDB Tree API"

def test_routes_count():
    """Test that expected number of routes are registered"""
    from main import app
    # Should have at least the main API routes plus docs routes
    assert len(app.routes) >= 10

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
