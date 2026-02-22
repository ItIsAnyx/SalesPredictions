# Read Me First
The following was discovered as part of building this project:

* The original package name 'ru.morzevichka.api-gateway' is invalid and this project uses 'ru.morzevichka.api_gateway' instead.

# Getting Started

### Reference Documentation
For further reference, please consider the following sections:

* [Official Apache Maven documentation](https://maven.apache.org/guides/index.html)
* [Spring Boot Maven Plugin Reference Guide](https://docs.spring.io/spring-boot/4.0.3/maven-plugin)
* [Create an OCI image](https://docs.spring.io/spring-boot/4.0.3/maven-plugin/build-image.html)
* [Gateway](https://docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-mvc.html)
* [Spring Session for Spring Data Redis](https://docs.spring.io/spring-session/reference/)
* [OAuth2 Client](https://docs.spring.io/spring-boot/4.0.3/reference/web/spring-security.html#web.security.oauth2.client)

### Maven Parent overrides

Due to Maven's design, elements are inherited from the parent POM to the project POM.
While most of the inheritance is fine, it also inherits unwanted elements like `<license>` and `<developers>` from the parent.
To prevent this, the project POM contains empty overrides for these elements.
If you manually switch to a different parent and actually want the inheritance, you need to remove those overrides.

