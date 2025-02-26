from django.conf import settings
from asgiref.sync import sync_to_async
from django.db import connection
from django.core.exceptions import DisallowedHost
from django_tenants.utils import get_tenant_domain_model
from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.urls import set_urlconf, clear_url_caches
from django_tenants.urlresolvers import get_subfolder_urlconf
from django_tenants.utils import (
    remove_www, get_public_schema_name,
    get_tenant_types,
    has_multi_type_tenants,
    get_tenant_domain_model,
    get_public_schema_urlconf,
    get_subfolder_prefix,
    get_tenant_model,

)
from django.http import Http404, HttpResponseNotFound
from django.core.handlers.asgi import ASGIRequest



class ProtocolTypeRouter:
    """
    Takes a mapping of protocol type names to other Application instances,
    and dispatches to the right one based on protocol name (or raises an error)

    `Adapted from: channels.routing (https://pypi.org/project/channels/)`
    
    PS: If you have channels in your installed app you can simply call it from
    here, it is all your choice.

    #### How to set it up on your asgi.py 
        
        ```
        application = ProtocolTypeRouter(
            "http": get_asgi_application()
            ## Other protocols here.
        )

        # in your setting, add this - ASGI_APPLICATION = "your_project.asgi.application"
        ```
   
    You must explicitly mention the key, `http` to route your asgi instances\
      on the ProtocolTypeRouter class.
    """

    def __init__(self, application_mapping):
        self.application_mapping = application_mapping

    async def __call__(self, scope, receive, send):
        if scope["type"] in self.application_mapping:
            application = self.application_mapping[scope["type"]]
            return await application(scope, receive, send)
        else:
            raise ValueError(
                "No application configured for scope type %r" % scope["type"]
            )


class CoreMiddleware:
    """
    Base class for implementing ASGI middleware.

    Note that subclasses of this are not self-safe; don't store state on
    the instance, as it serves multiple application instances. Instead, use
    scope.

    `Adapted from: channels.middleware (https://pypi.org/project/channels/)`


    """

    def __init__(self, inner):
        """
        Middleware constructor - just takes inner application.
        """
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """
        ASGI application; can insert things into the scope and run asynchronous
        code.
        """
        # Copy scope to stop changes going upstream
        scope = dict(scope)
        # Run the inner application along with the scope
        return await self.inner(scope, receive, send)


class ASGITenantMainMiddleware(CoreMiddleware):
    """
    Middleware to handle multi-tenancy for ASGI applications. 
    
    This middleware selects the appropriate tenant 
    based on the request's hostname and ensures the request uses the correct database schema.

    Attributes:
        TENANT_NOT_FOUND_EXCEPTION (Exception): Exception raised when no tenant is found.
        
        inner (callable): The next ASGI application or middleware in the chain.

    Methods:
        hostname_from_request(request): Extracts the hostname from the request.
        
        get_tenant(domain_model, hostname): Retrieves the tenant based on the hostname.
        
        __call__(scope, receive, send): Processes incoming ASGI requests.
        
        process_request(request): Processes the tenant schema based on the request.
        
        get_request(scope, receive): Converts ASGI scope to Django request.
        
        send_response(response, send): Converts Django response to ASGI response.
        
        no_tenant_found(request, hostname): Handles the case when no tenant is found.
        
        setup_url_routing(request, force_public): Sets up the correct URL 
        configuration based on the tenant.
    """

    TENANT_NOT_FOUND_EXCEPTION = Http404

    def __init__(self, inner):
        """
        Initializes the middleware with the next ASGI application or 
        middleware in the chain.

        Args:
            inner (callable): The next ASGI application or middleware 
            in the chain.
        """
        super().__init__(inner)

    @staticmethod
    def hostname_from_request(request):
        """
        Extracts the hostname from the request.

        Args:
            request (ASGIRequest): The Django request object.

        Returns:
            str: The hostname extracted from the request.
        """
        return remove_www(request.get_host().split(':')[0])

    def get_tenant(self, domain_model, hostname):
        """
        Retrieves the tenant based on the hostname.

        Args:
            domain_model (Model): The domain model.
            hostname (str): The hostname extracted from the request.

        Returns:
            Tenant: The tenant associated with the hostname, 
            or None if not found.
        """
        try:
            domain = domain_model.objects.select_related(
                'tenant').get(domain=hostname)
            return domain.tenant
        except Exception as e:
            print(f"Error fetching tenant: {e}")
            return None

    async def __call__(self, scope, receive, send):
        """
        Processes incoming ASGI requests.

        Args:
            scope (dict): The ASGI scope dictionary.
            receive (callable): The receive callable.
            send (callable): The send callable.
        """
        if scope['type'] == 'http':
            request = await self.get_request(scope, receive)
            response = await self.process_request(request)
            if isinstance(response, HttpResponse):
                await self.send_response(response, send)
            else:
                await self.inner(scope, receive, send)
        else:
            await self.inner(scope, receive, send)

    async def process_request(self, request):
        """
        Processes the tenant schema based on the request.

        Args:
            request (ASGIRequest): The Django request object.

        Returns:
            HttpResponse: The response object if the tenant is processed, 
            or HttpResponseNotFound if not.
        """
        connection.set_schema_to_public()
        try:
            hostname = self.hostname_from_request(request)
        except DisallowedHost:
            return HttpResponseNotFound()

        domain_model = get_tenant_domain_model()
        try:
            tenant = await sync_to_async(self.get_tenant)(domain_model, hostname)
        except domain_model.DoesNotExist:
            self.no_tenant_found(request, hostname)
            return HttpResponseNotFound()

        tenant.domain_url = hostname
        request.tenant = tenant
        connection.set_tenant(request.tenant)
        self.setup_url_routing(request)

    async def get_request(self, scope, receive):
        """
        Converts ASGI scope to Django request.

        Args:
            scope (dict): The ASGI scope dictionary.
            receive (callable): The receive callable.

        Returns:
            ASGIRequest: The Django request object.
        """
        return ASGIRequest(scope, receive)

    async def send_response(self, response, send):
        """
        Converts Django response to ASGI response.

        Args:
            response (HttpResponse): The Django response object.
            send (callable): The send callable.
        """
        headers = [
            (b"content-type", response["Content-Type"].encode("latin-1"))]
        for key, value in response.items():
            headers.append([key.encode("latin-1"), value.encode("latin-1")])
        await send({
            "type": "http.response.start",
            "status": response.status_code,
            "headers": headers,
        })
        await send({
            "type": "http.response.body",
            "body": response.content,
            "more_body": False,
        })

    def no_tenant_found(self, request, hostname):
        """
        Handles the case when no tenant is found.

        Args:
            request (ASGIRequest): The Django request object.
            hostname (str): The hostname extracted from the request.
        """
        if hasattr(settings, 'SHOW_PUBLIC_IF_NO_TENANT_FOUND') and \
                settings.SHOW_PUBLIC_IF_NO_TENANT_FOUND:
            self.setup_url_routing(request=request, force_public=True)
        else:
            raise self.TENANT_NOT_FOUND_EXCEPTION(
                f'No tenant for hostname "{hostname}"')

    @staticmethod
    def setup_url_routing(request, force_public=False):
        """
        Sets up the correct URL configuration based on the tenant.

        Args:
            request (ASGIRequest): The Django request object.
            force_public (bool): Whether to force the public schema
              URL configuration.
        """
        public_schema_name = get_public_schema_name()
        if has_multi_type_tenants():
            tenant_types = get_tenant_types()
            if (not hasattr(request, 'tenant') or
                    ((force_public or request.tenant.schema_name == public_schema_name) and
                     'URLCONF' in tenant_types[public_schema_name])):
                request.urlconf = get_public_schema_urlconf()
            else:
                tenant_type = request.tenant.get_tenant_type()
                request.urlconf = tenant_types[tenant_type]['URLCONF']
            set_urlconf(request.urlconf)
        else:
            if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and (
                    force_public or request.tenant.schema_name == public_schema_name):
                request.urlconf = settings.PUBLIC_SCHEMA_URLCONF


class ASGITenantSubfolderMiddleware(ASGITenantMainMiddleware):
    """
    Middleware to handle subfolder-based multi-tenancy for ASGI applications.
    This middleware selects the appropriate tenant based on the request's subfolder.
    """

    TENANT_NOT_FOUND_EXCEPTION = Http404

    def __init__(self, inner):
        super().__init__(inner)
        if not get_subfolder_prefix():
            raise ImproperlyConfigured(
                '"TenantSubfolderMiddleware" requires "TENANT_SUBFOLDER_PREFIX" '
                "present and non-empty in settings"
            )

    @staticmethod
    def extract_subfolder_from_request(request):
        """
        Extracts the subfolder from the request URL.

        Args:
            request (ASGIRequest): The Django request object.

        Returns:
            str: The subfolder extracted from the request URL.
        """
        path = request.path.split('/')
        return path[1] if len(path) > 1 else None

    async def process_request(self, request):
        """
        Processes the tenant schema based on the request subfolder.

        Args:
            request (ASGIRequest): The Django request object.

        Returns:
            HttpResponse: The response object if the tenant is processed,
                          or HttpResponseNotFound if not.
        """
        # Short circuit if tenant is already set by another middleware.
        if hasattr(request, "tenant"):
            return

        connection.set_schema_to_public()
        urlconf = None
        tenant_model = get_tenant_model()
        domain_model = get_tenant_domain_model()
        hostname = self.hostname_from_request(request)
        subfolder_prefix_path = f"/{get_subfolder_prefix()}/"

        # if public specific
        if not request.path.startswith(subfolder_prefix_path):
            try:
                tenant = await sync_to_async(tenant_model.objects.get)(schema_name=get_public_schema_name())
            except tenant_model.DoesNotExist:
                raise self.TENANT_NOT_FOUND_EXCEPTION(
                    "Unable to find public tenant")
            self.setup_url_routing(request, force_public=True)
        #  if tenant specific
        else:
            path_chunks = request.path[len(subfolder_prefix_path):].split("/")
            tenant_subfolder = path_chunks[0]
            try:
                tenant = await sync_to_async(self.get_tenant)(
                    domain_model=domain_model, hostname=tenant_subfolder)
            except domain_model.DoesNotExist:
                return self.no_tenant_found(request, tenant_subfolder)

            except domain_model.DoesNotExist:
                return HttpResponseNotFound()
            tenant.domain_subfolder = tenant_subfolder
            urlconf = get_subfolder_urlconf(tenant)
    

        tenant.domain_url = hostname
        request.tenant = tenant
        connection.set_tenant(request.tenant)
        clear_url_caches()  # Required to remove previous tenant prefix from cache, if present

        if urlconf:
            request.urlconf = urlconf
            set_urlconf(urlconf)

        return None

    async def __call__(self, scope, receive, send):
        """
        Processes incoming ASGI requests.

        Args:
            scope (dict): The ASGI scope dictionary.
            receive (callable): The receive callable.
            send (callable): The send callable.
        """
        if scope['type'] == 'http':
            request = await self.get_request(scope, receive)
            response = await self.process_request(request)
            if response is not None:
                await self.send_response(response, send)
            else:
                await self.inner(scope, receive, send)
        else:
            await self.inner(scope, receive, send)

    def no_tenant_found(self, request, hostname):
        """
        Handles the case when no tenant is found.

        Args:
            request (ASGIRequest): The Django request object.
            hostname (str): The hostname extracted from the request.
        """
        raise self.TENANT_NOT_FOUND_EXCEPTION(
            'No tenant for subfolder "%s"' % hostname)
