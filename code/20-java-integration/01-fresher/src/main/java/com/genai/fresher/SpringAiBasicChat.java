package com.genai.fresher;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class SpringAiBasicChat {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiBasicChat.class, args);
    }

    // ChatClient.Builder is auto-configured by the OpenAI starter from application.yml properties
    @Bean
    ChatClient chatClient(ChatClient.Builder builder) {
        return builder.build();
    }
}

@RestController
class ChatController {

    private final ChatClient chatClient;

    ChatController(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    @GetMapping("/chat")
    String chat(@RequestParam(defaultValue = "What is the capital of France?") String question) {
        return chatClient.prompt()
                .user(question)
                .call()
                .content();
    }
}
