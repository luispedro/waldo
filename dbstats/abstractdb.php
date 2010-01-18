<?php

abstract class AbstractDB {

	private $db;
	private $files;

	public function __construct($db, $files) {
		$this->db = $db;
		$this->files = $files;
	}

	public function getFiles() {
		return $this->files;
	}

	public function getDB() {
		return $this->db;
	}

	public abstract function populate();
}

?>
