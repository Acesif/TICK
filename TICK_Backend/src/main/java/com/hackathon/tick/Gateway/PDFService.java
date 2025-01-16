package com.hackathon.tick.Gateway;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@Service
public class PDFService {

    public Map<String, Object> uploadPDF(MultipartFile file) {
        Map<String, Object> result = new HashMap<>();
        result.put("status", "success");
        result.put("message", "File uploaded successfully");
        result.put("file", 1);
        return result;
    }
}
