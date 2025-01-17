package com.hackathon.tick.Utils;

import org.springframework.core.io.InputStreamResource;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@Component
public class MultipartToFile {

    public InputStreamResource convertMultipartToFile(MultipartFile file) {
        try {
            return new InputStreamResource(file.getInputStream()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }

                @Override
                public long contentLength() {
                    return file.getSize();
                }
            };
        } catch (IOException e) {
            e.fillInStackTrace();
        }
        return null;
    }
}
