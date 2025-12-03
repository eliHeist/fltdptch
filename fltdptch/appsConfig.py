from django.urls import path, include

app_configs = [
	{ 'app_name': 'flights', 'url': 'flights_be/', 'namespace': 'flights' },

	{ 'app_name': 'accounts', 'url': 'accounts/', 'namespace': 'accounts' },

	{ 'app_name': 'frontend', 'url': '', 'namespace': 'frontend' },
    
]

def getAppUrls():
    urlpatterns = []
    for config in app_configs:
        urlpatterns.append(
            path(f"{config['url']}", include(f"{config['app_name']}.urls", namespace=config['namespace']))
        )
    return urlpatterns

def getAppNames():
    return [config['app_name'] for config in app_configs]
