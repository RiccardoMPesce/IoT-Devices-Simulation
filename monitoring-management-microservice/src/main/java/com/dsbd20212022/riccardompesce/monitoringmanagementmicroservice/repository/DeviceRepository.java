package com.example.moneytransferrestapi.repository;

import org.springframework.data.repository.CrudRepository;

import com.example.moneytransferrestapi.model.Account;

public interface AccountRepository extends CrudRepository<Account, Integer> {

}