SELECT :columnSet
FROM
  :tableName
WHERE 1 = 1 :filters
;

INSERT
INTO :tableName
  :columnSet
VALUES
  :valueSet
;

UPDATE :tableName
SET :fieldSet
WHERE 1 = 1 :filters
;

DELETE
FROM :tableName
WHERE 1 = 1 :filters
;
