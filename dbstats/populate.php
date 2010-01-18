<?php

require_once('common.inc.php');

// include all the necessary files and populate the database
foreach ($DATABASES as $class => $name) {
	require_once($name . '.php');
	$obj = new $class($DB, $DB_FILES[$name]);
	$obj->populate();
}

?>
