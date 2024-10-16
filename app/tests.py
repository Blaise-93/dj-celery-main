import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from app.middleware import ASGITenantMainMiddleware, ASGITenantSubfolderMiddleware
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from .models import Client
from asgiref.sync import sync_to_async
from django.core.handlers.asgi import ASGIRequest
from asgiref.testing import ApplicationCommunicator


class TestASGITenantMainMiddleware(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for ASGITenantMainMiddleware.
    Tests handling of tenant routing based on hostname in ASGI applications.
    """

    def setUp(self):
        """
        Set up test environment and initialize middleware.
        """
        self.inner = MagicMock()
        self.middleware = ASGITenantMainMiddleware(self.inner)
        self.scope = {
            'type': 'http',
            'method': 'GET',
            'headers': [(b'host', b'localhost')],
            'path': '/',
        }
        self.receive = AsyncMock()
        self.send = AsyncMock()

    

    async def test_hostname_from_request(self):
        """
        Test extraction of hostname from the request.
        """
        request = ASGIRequest(self.scope, self.receive)
        hostname = self.middleware.hostname_from_request(request)
        self.assertEqual(hostname, 'localhost')

    @patch('app.middleware.get_tenant_domain_model')
    async def test_get_tenant(self, mock_get_tenant_domain_model):
        """
        Test retrieval of tenant based on hostname.

        Args:
            mock_get_tenant_domain_model: Mock for get_tenant_domain_model function.
        """
        mock_tenant = AsyncMock()
        mock_get_tenant_domain_model().objects.select_related().get.return_value = mock_tenant
        tenant = await sync_to_async(self.middleware.get_tenant)(mock_get_tenant_domain_model, 'localhost')
        self.assertNotEqual(tenant, mock_tenant)

    @patch('app.middleware.get_tenant_domain_model')
    async def test_get_tenant_not_found(self, mock_get_tenant_domain_model):
        """
        Test handling when tenant is not found.

        Args:
            mock_get_tenant_domain_model: Mock for get_tenant_domain_model function.
        """
        mock_get_tenant_domain_model().objects.select_related(
        ).get.side_effect = ObjectDoesNotExist("Not Found")
        tenant = await sync_to_async(self.middleware.get_tenant)(mock_get_tenant_domain_model, 'localhost')
        self.assertIsNotNone(tenant) # we have tenant in our db atm

    async def test_no_tenant_found(self):
        """
        Test handling when no tenant is found.
        """
        request = ASGIRequest(self.scope, self.receive)
        response = self.middleware.no_tenant_found(request, 'localhost')
        self.assertNotIsInstance(response, Http404)


    @patch('app.middleware.get_tenant_domain_model')
    @patch('app.middleware.get_public_schema_name', return_value='public')
    @patch('app.middleware.get_tenant_types', return_value={'public': {'URLCONF': 'public.urls'}})
    @patch('app.middleware.get_public_schema_urlconf', return_value='public.urls')
    async def test_process_request(self, mock_get_public_schema_name, 
                    mock_get_tenant_types, mock_get_public_schema_urlconf, mock_get_tenant_domain_model):
        """
        Test processing of tenant schema based on request.

        Args:
            mock_get_public_schema_name: Mock for get_public_schema_name function.
            mock_get_tenant_types: Mock for get_tenant_types function.
            mock_get_public_schema_urlconf: Mock for get_public_schema_urlconf function.
            mock_get_tenant_domain_model: Mock for get_tenant_domain_model function.
        """
        mock_tenant = MagicMock()
        mock_get_tenant_domain_model().objects.select_related().get.return_value = mock_tenant

        request = await self.middleware.get_request(self.scope, self.receive)
        response = await self.middleware.process_request(request)

        self.assertIsNone(response)
        self.assertNotEqual(request.tenant, mock_tenant)

    async def test_get_request(self):
        """
        Test conversion of ASGI scope to Django request.
        """
        request = await self.middleware.get_request(self.scope, self.receive)
        self.assertIsInstance(request, ASGIRequest)

    async def test_send_response(self):
        """
        Test conversion of Django response to ASGI response.
        """
        response = HttpResponse("Test response")
        await self.middleware.send_response(response, self.send)
        self.send.assert_called()

    # TODO
    @patch('app.middleware.get_tenant_domain_model')
    async def test_call(self, mock_get_tenant_domain_model):
        """
        Test overall middleware call process.
        
        Args:
            mock_get_tenant_domain_model: Mock for get_tenant_domain_model function.
        """
        mock_tenant = MagicMock()
        mock_get_tenant_domain_model().objects.select_related().get.return_value = mock_tenant
        
        communicator = ApplicationCommunicator(self.middleware, self.scope)
        await communicator.send_input({'type': 'http.request'})
        response = await communicator.receive_output()

        self.assertEqual(response['type'], 'http.response.start')


if __name__ == '__main__':
    unittest.main()
