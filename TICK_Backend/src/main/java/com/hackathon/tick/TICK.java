package com.hackathon.tick;

import lombok.RequiredArgsConstructor;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@RequiredArgsConstructor
public class TICK {
    public static void main(String[] args) {
        SpringApplication.run(TICK.class, args);
    }
}
