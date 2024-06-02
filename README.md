## Purpose
Service exposes following functionalities:
1. Shortens a given URL
2. Maintains database correlation with original url and user
3. Offers retrieval of original url by user(instead of redirection)


## Swagger
Run server and visit [this page][swagger].


## Design
Short url consists of service url plus postfix. Users can choose their own postfix, which is then verified to be unused. 
In case they do not select a custom postfix, the service generates a random and unused one. 

Url retrieval by user is currently offered instead of redirection. Results get cached upon retrieval, so subsequent 
retrievals do not put load on the database, as long as cached results do not get evicted.


## Todos

- [ ] User authentication
- [ ] Concurrency
- [ ] Setup testing env and add cases
- [ ] Implement layer classes & use as dependencies
- [ ] Move db/cache dependencies to data layer
- [ ] Add `use_cahe=True/False` 


[swagger]: http://127.0.0.1:80/docs
