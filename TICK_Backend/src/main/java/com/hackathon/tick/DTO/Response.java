package com.hackathon.tick.DTO;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Response {
    private String message;
    private String status;
    private Object data;
}
