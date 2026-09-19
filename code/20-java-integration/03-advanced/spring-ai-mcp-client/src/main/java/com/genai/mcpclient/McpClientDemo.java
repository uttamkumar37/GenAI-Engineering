package com.genai.mcpclient;

import com.fasterxml.jackson.databind.JsonNode;

import java.util.List;
import java.util.Map;

public class McpClientDemo {

    public static void main(String[] args) throws Exception {
        // connect, list tools, call a tool — the general MCP client pattern
        try (McpJsonRpcClient client = new McpJsonRpcClient(List.of("python", "-m", "topic11_mcp_server"))) {
            client.initialize();

            JsonNode tools = client.listTools();
            System.out.println("Available tools: " + tools);

            JsonNode result = client.callTool("search_documents", Map.of("query", "pgvector setup"));
            System.out.println("Tool result: " + result);
        }
    }
}
