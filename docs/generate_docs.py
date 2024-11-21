import os
import json
from fastapi.openapi.utils import get_openapi
from app.__init__ import app

# Generate the OpenAPI schema
openapi_schema = get_openapi(
    title=app.title,
    version=app.version,
    openapi_version="3.0.0",  # Update to OpenAPI version 3.1.0
    description=app.description,
    routes=app.routes,
)


with open("docs\\swagger.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)

# Create the Swagger UI HTML content
swagger_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swagger UI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: 'swagger.json',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            });
            window.ui = ui;
        };
    </script>
</body>
</html>
"""

# Save the Swagger UI HTML content to a file
with open("docs\\index.html", "w") as f:
    f.write(swagger_html_content)

if __name__ == '__main__':
    print("Swagger documentation generated successfully.")
