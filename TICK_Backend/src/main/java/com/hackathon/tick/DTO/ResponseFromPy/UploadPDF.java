package com.hackathon.tick.DTO.ResponseFromPy;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UploadPDF {
    private String pdf_id;
    private Integer total_pages;
}
