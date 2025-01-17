package com.hackathon.tick.Gateway;

import com.hackathon.tick.DTO.ResponseFromPy.SummarizePage;
import com.hackathon.tick.DTO.ResponseFromPy.UploadPDF;
import com.hackathon.tick.Utils.MultipartToFile;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

@Service
@RequiredArgsConstructor
public class PDFService {

    private final MultipartToFile multipartToFile;
    private final RestTemplate restTemplate;

    public UploadPDF uploadPDF(MultipartFile file) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        InputStreamResource fileAsResource = multipartToFile.convertMultipartToFile(file);

        body.add("file", fileAsResource);

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        ResponseEntity<UploadPDF> response = restTemplate.postForEntity(
                "http://0.0.0.0:8000/upload-pdf",
                requestEntity,
                UploadPDF.class
        );
        return response.getBody();
    }

    public SummarizePage summarizePage(String pdf_id, Integer page_number) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("pdf_id", pdf_id);
        body.add("page_number", page_number.toString());

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        ResponseEntity<SummarizePage> response = restTemplate.postForEntity(
                "http://0.0.0.0:8000/summarize",
                requestEntity,
                SummarizePage.class
        );
        return response.getBody();
    }
}
