# fastapi-logto-demonstration

This is a minimal project to show how I successfully implemented logto authentification with FastAPI.

## Documentation

For additional context about this project, you can visit:

- [Logto Documentation](https://docs.logto.io/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [SwaggerUI Documentation](https://swagger.io/tools/swagger-ui/)

## Implementation

This project uses native FastAPI functions to implement Logto authentication without requiring a Python Logto client.
This approach relies heavily on FastAPI built-in functionalities, which offer robust and secure ways to handle
authentication and authorization. 

### Logto Authentication and the Concept of Resource

Logto introduces the concept of a 'Resource', which might be likened to an 'Audience' in other identity providers'
parlance. This 'Resource' plays a crucial role in how this project deals with authentication.

### Customizing Swagger UI and FastAPI Router

To fully incorporate this concept, I've made modifications to both FastAPI's router and Swagger UI. Specifically, I had
to create my own Swagger UI build and customize FastAPI's documentation router to correctly
handle full OAuth2 authentification process. Now, swagger integrated authentification process give full JWT token and not Opaque Token if you provide resource. [Reference](https://blog.logto.io/oidc-resource-and-jwt-access-token/)

### Session Control Token

The session control token has been implemented in line with the exemple provided in M2M  provided in the API Resource documentation of
Logto.

### Credits and Further Reading

I must also give credit to [Daniel ATkinson](https://github.com/danielatk) who first implemented the concept of '
Audience'. His work served as a valuable reference point during the development process. To further explore these topics
or to see the customized Swagger UI fork I've used, visit [my Github](https://github.com/yann-dubrana).