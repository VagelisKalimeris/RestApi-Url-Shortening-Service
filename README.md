## Purpose
Service exposes following functionalities:
1. Shortens a given URL
2. Maintains database correlation with original url and user
3. Offers retrieval of original url by user


## Swagger
Run server and visit [this page][swagger].


## Design
Short url consists of service url plus postfix. Users can choose their own postfix, which is then verified to be 
unused.  
In case they do not select a custom postfix, the service generates a random and unused one. 

Url retrieval by user is currently offered instead of redirection. 

An intermediary retrieval cache is used, so subsequent lookups do not put load on the database, as long as they have 
not been evicted.


## Todos

- [ ] User authentication
- [ ] Concurrency
- [ ] Setup testing env and add cases
- [ ] Implement layer classes & use as dependencies
- [ ] Move db/cache dependencies to data layer
- [ ] Add `use_cahe=True/False` 


[swagger]: http://127.0.0.1:80/docs
