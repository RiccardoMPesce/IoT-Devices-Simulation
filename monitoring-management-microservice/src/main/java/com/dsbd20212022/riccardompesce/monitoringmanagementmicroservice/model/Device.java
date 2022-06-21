package com.dsbd20212022.riccardompesce.monitoringmanagementmicroservice.model;

import java.time.LocalDateTime;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "devices")
public class Device {
    @Id
    private String id;

    private String measure;

    private int publishQos;

    private boolean status;

    private LocalDateTime updateDatetime;

    private double decadingFactor;

    public String getId() {
        return id;
    }

    public String getMeasure() {
        return measure;
    }

    public int getPublishQos() {
        return publishQos;
    }

    public boolean isStatus() {
        return status;
    }

    public LocalDateTime getUpdateDatetime() {
        return updateDatetime;
    }

    public double getDecadingFactor() {
        return decadingFactor;
    }

    public void setId(String id) {
        this.id = id;
    }

    public void setMeasure(String measure) {
        this.measure = measure;
    }

    public void setPublishQos(int publishQos) {
        this.publishQos = publishQos;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public void setUpdateDatetime(LocalDateTime updateDatetime) {
        this.updateDatetime = updateDatetime;
    }

    public void setDecadingFactor(double decadingFactor) {
        this.decadingFactor = decadingFactor;
    }
}
