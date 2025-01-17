package com.hackathon.tick.DTO.ResponseFromPy;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SummarizePage {
    private String summary;
    private Integer page_number;
}
