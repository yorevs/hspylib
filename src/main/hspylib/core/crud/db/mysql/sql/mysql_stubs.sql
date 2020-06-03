SELECT
  $columns
  FROM
    $tablename
  WHERE
    1 = 1
    $filters
;

INSERT
  INTO $tablename
    ($columns)
  VALUES
    ($valueset)
;

UPDATE $tablename
  SET $fielset
  WHERE
    1 = 1
    $filters
;

DELETE
  FROM $tablename
  WHERE
    1 = 1
    $filters
;
