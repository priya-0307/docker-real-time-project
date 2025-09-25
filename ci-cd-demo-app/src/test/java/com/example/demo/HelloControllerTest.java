package com.example.demo;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class HelloControllerTest {

    private final HelloController controller = new HelloController();

    @Test
    void testHelloEndpoint() {
        String response = controller.hello();
        assertThat(response).isEqualTo("Hello from Jenkins CI/CD Pipeline!");
    }

    @Test
    void testHealthEndpoint() {
        String response = controller.health();
        assertThat(response).isEqualTo("OK");
    }
}
