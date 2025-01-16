package com.hackathon.tick.Controller;

import com.hackathon.tick.DTO.Response;
import com.hackathon.tick.Gateway.PDFService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.util.Map;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/pdf")
public class PDFController {

    private final PDFService pdfService;

    @RequestMapping(value = "/upload",
            method = RequestMethod.POST,
            consumes = MediaType.MULTIPART_FORM_DATA_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public Response uploadPDF(@RequestParam(name = "file") MultipartFile file) {

        var result = pdfService.uploadPDF(file);

        return Response.builder()
                .status("success")
                .message("File uploaded successfully")
                .data(result)
                .build();
    }

}
