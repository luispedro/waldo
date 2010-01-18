<?php

class eSLDB extends AbstractDB {

	public function populate() {
		// get the stuff we need
		$db = $this->getDB();
		$files = $this->getFiles();

		// do the same thing with both files
		foreach ($files as $name => $file) {
			$fp = @fopen($file, 'r+') or die('Unable to open file ' . $file . ".\n");
			$count = -1;
			while (!feof($fp)) {
				$line = explode("\t", fgets($fp));
				$count++;
				if (count($line) < 5 || $count == 0) continue;
				$id = mysql_real_escape_string($line[0]);
				$ensemblid = mysql_real_escape_string($line[1]);
				$query = 'INSERT INTO esldb (esldbid, ' .
					'experimental_annot, ' .
					'similarity_annot, ' .
					'uniprot_fulltext_annot, ' .
					'uniprot_entry_id, ' .
					'uniprot_homologue_id, ' .
					'prediction, ' . 
					'db_type) VALUES ("' . $id . '", "' .
					mysql_real_escape_string($line[2]) .
					'", "' . 
					mysql_real_escape_string($line[5]) .
					'", "' .
					mysql_real_escape_string($line[3]) . 
					'", "' .
					mysql_real_escape_string($line[4]) .
					'", "' .
					mysql_real_escape_string($line[6]) .
					'", ' . 
					($line[7] != 'None' ? $line[7] : -1.0) . 
					', "' .
					$name . '")';
				mysql_query($query) or die($query . ':' . mysql_error() . "\n");
				// now insert the ensembl id
				$query = 'INSERT INTO db_to_ensembl VALUES("' .
					'esldb", ' . mysql_insert_id() . 
					', "' . 
					mysql_real_escape_string($line[1]) .
					'")';
				mysql_query($query) or die(mysql_error() . "\n");
				if ($count % 1000 == 0) {
					echo $count . ' eSLDB (' . $name . 
						') entries inserted.' . "\n";
				}
			}
			// close it up
			fclose($fp);
		}
	}

}

?>
