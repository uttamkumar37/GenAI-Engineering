package com.genai.rag;

import java.util.List;

// structured-output target: mirrors the Python Topic 08 pipeline's answer schema
public record RagAnswer(String answer, List<String> citedSources, double confidence) {
}
