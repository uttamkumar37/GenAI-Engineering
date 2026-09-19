package com.genai.mcpclient;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * UNCERTAINTY: at the time of writing, an official "MCP Java SDK" with stable class names could not be
 * confidently confirmed (modelcontextprotocol.io should be checked for the current io.modelcontextprotocol
 * artifact). To avoid inventing SDK class names, this talks to an MCP server directly over stdio using the
 * documented JSON-RPC 2.0 message shape (initialize -> tools/list -> tools/call), the same transport the
 * Topic 11 Python MCP server exposes. Swap this for the official SDK's client once its API is verified.
 */
public class McpJsonRpcClient implements AutoCloseable {

    private final Process serverProcess;
    private final OutputStream serverStdin;
    private final BufferedReader serverStdout;
    private final ObjectMapper mapper = new ObjectMapper();
    private final AtomicInteger requestId = new AtomicInteger(0);

    public McpJsonRpcClient(List<String> serverCommand) throws IOException {
        // e.g. List.of("python", "-m", "mcp_server_module") — the Topic 11 Python-built MCP server
        this.serverProcess = new ProcessBuilder(serverCommand)
                .redirectErrorStream(false)
                .start();
        this.serverStdin = serverProcess.getOutputStream();
        this.serverStdout = new BufferedReader(new InputStreamReader(serverProcess.getInputStream(), StandardCharsets.UTF_8));
    }

    public JsonNode initialize() throws IOException {
        return sendRequest("initialize", Map.of(
                "protocolVersion", "2024-11-05",
                "clientInfo", Map.of("name", "spring-ai-mcp-client", "version", "0.1.0"),
                "capabilities", Map.of()));
    }

    public JsonNode listTools() throws IOException {
        return sendRequest("tools/list", Map.of());
    }

    public JsonNode callTool(String toolName, Map<String, Object> arguments) throws IOException {
        return sendRequest("tools/call", Map.of("name", toolName, "arguments", arguments));
    }

    private JsonNode sendRequest(String method, Map<String, Object> params) throws IOException {
        ObjectNode request = mapper.createObjectNode();
        request.put("jsonrpc", "2.0");
        request.put("id", requestId.incrementAndGet());
        request.put("method", method);
        request.set("params", mapper.valueToTree(params));

        String line = mapper.writeValueAsString(request) + "\n";
        serverStdin.write(line.getBytes(StandardCharsets.UTF_8));
        serverStdin.flush();

        String responseLine = serverStdout.readLine();
        if (responseLine == null) {
            throw new IOException("MCP server closed stdout unexpectedly");
        }
        JsonNode response = mapper.readTree(responseLine);
        if (response.has("error")) {
            throw new IOException("MCP error: " + response.get("error"));
        }
        return response.get("result");
    }

    @Override
    public void close() {
        serverProcess.destroy();
    }
}
