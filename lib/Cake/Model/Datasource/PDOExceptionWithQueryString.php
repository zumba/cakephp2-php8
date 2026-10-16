<?php

class PDOExceptionWithQueryString extends PDOException {

	public string $queryString = "";

/**
 * Bound parameters of the failed query, displayed by the pdo_error view.
 *
 * @var array|null
 */
	public $params = null;

/**
 * Wrapper for PDOException to avoid creating dynamic property.
 *
 * @param PDOException $e Source exception.
 */
	public function __construct(PDOException $e) {
		parent::__construct($e->getMessage(), 0, $e->getPrevious());

		$this->errorInfo = $e->errorInfo;
		$this->code = $e->code;
	}
}
