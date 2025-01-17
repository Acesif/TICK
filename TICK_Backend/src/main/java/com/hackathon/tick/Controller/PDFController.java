package com.hackathon.tick.Controller;

import com.hackathon.tick.DTO.Response;
import com.hackathon.tick.DTO.ResponseFromPy.SummarizePage;
import com.hackathon.tick.DTO.ResponseFromPy.UploadPDF;
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

        UploadPDF result = pdfService.uploadPDF(file);

        return Response.builder()
                .status("success")
                .message("File uploaded successfully")
                .data(result)
                .build();
    }

    @RequestMapping(value = "/summarize",
            method = RequestMethod.POST,
            consumes = MediaType.MULTIPART_FORM_DATA_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public Response summarizePDF(
            @RequestParam(name = "pdf_id") String pdf_id,
            @RequestParam(name = "page_number") Integer page_number
    ) {

        SummarizePage result = pdfService.summarizePage(pdf_id, page_number);

        return Response.builder()
                .status("success")
                .message("Page summarized successfully")
                .data(result)
                .build();
    }

}
