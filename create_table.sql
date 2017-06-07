drop table if exists `scrapy`.`cw`;
create table `scrapy`.`cw` (
  id          INT NOT NULL AUTO_INCREMENT,
  import_date DATE NOT NULL,
  sku         INT NOT NULL,
  name        VARCHAR(1000),
  price       DECIMAL(9,2),
  saved       DECIMAL(9,2),
  url         VARCHAR(1000),
  Primary key (id)
);
