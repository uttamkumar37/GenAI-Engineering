package com.genai.rag;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.converter.BeanOutputConverter;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class RagService {

    private final ChatClient chatClient;
    private final VectorStore vectorStore;

    public RagService(ChatClient.Builder chatClientBuilder, VectorStore vectorStore) {
        this.chatClient = chatClientBuilder.build();
        this.vectorStore = vectorStore;
    }

    public RagAnswer answer(String question) {
        List<Document> hits = vectorStore.similaritySearch(
                SearchRequest.query(question).withTopK(4));

        String context = hits.stream()
                .map(Document::getContent)
                .collect(Collectors.joining("\n---\n"));

        BeanOutputConverter<RagAnswer> converter = new BeanOutputConverter<>(RagAnswer.class);

        String prompt = """
                Answer the question using only the context below.
                Context:
                %s

                Question: %s

                %s
                """.formatted(context, question, converter.getFormat());

        String raw = chatClient.prompt()
                .user(prompt)
                .call()
                .content();

        return converter.convert(raw);
    }
}
