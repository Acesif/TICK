package com.hackathon.tick.DTO;

import lombok.Builder;
import lombok.Data;

import java.util.Map;

@Builder
@Data
public class Response {
    private String message;
    private String status;
    private Map<String, Object> data;
}
