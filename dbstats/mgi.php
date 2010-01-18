<?php

class MGI extends AbstractDB {

	public function populate() {
		return;
		// get the stuff we need first
		$files = $this->getFiles();
		$db = $this->getDB();

		// open all three files
		$general = @fopen($files['general'], 'r+') or die('Unable to open file ' . $files['general'] . ".\n");
		$citations = @fopen($files['citations'], 'r+') or die('Unable to open file ' . $files['citations'] . ".\n");
		$ensembl = @fopen($files['ensembl'], 'r+') or die('Unable to open file ' . $files['ensembl'] . ".\n");

		// first, let's add all the instances to the database
		// we'll do the ensembl IDs after
		$count = 0;
		while (!feof($general)) {
			$line = explode("\t", fgets($general));
			if (count($line) < 10) continue;
			$id = mysql_real_escape_string($line[1]);

			// insert!
			$query = 'INSERT INTO mgi (mgiid, goid, ' .
				'go_evidence_code, inferred_from, ' .
				'database_assigned_by, accession_ID) ' .
				'VALUES("' . $id . '", "' .
				mysql_real_escape_string($line[4]) . '", "' .
				mysql_real_escape_string($line[6]) . '", "' .
				mysql_real_escape_string($line[7]) . '", "' .
				mysql_real_escape_string($line[14]) . '", "' .
				mysql_real_escape_string($line[16]) . '")';	
			mysql_query($query) or die($query . ":\n" . 
						mysql_error() . "\n");
			$count++;
			if ($count % 1000 == 0) {
				echo $count . ' generals entered.' . "\n";
			}
		}
		fclose($general);

		// next: go through the pubmed file, adding the 
		// necessary IDs to the entries
		$count = 0;
		while (!feof($citations)) {
			$line = explode("\t", fgets($citations));
			$query = 'UPDATE mgi SET pubmedid = ' .
				intval($line[1]) . ' WHERE mgiid = "' .
				mysql_real_escape_string($line[0]) . '"';
			mysql_query($query) or die($query . ":\n" . 
						mysql_error() . "\n");
			$count++;
			if ($count % 1000 == 0) {
				echo $count . ' citations updated.' . "\n";
			}
		}
		fclose($citations);
		
		// lastly, run through the ensembl file and add those
		$count = 0;
		while (!feof($ensembl)) {
			$line = explode("\t", fgets($ensembl));
			// first, find the ID we want
			$query = 'SELECT entryid FROM mgi WHERE mgiid = "' .
				mysql_real_escape_string($line[0]) . '"';
			$result = mysql_query($query) or die($query . ":\n" . 
						mysql_error() . "\n");
			switch (mysql_affected_rows()) {
				case 0:
					// nothing exists...
					break;
				case 1:
					$row = mysql_fetch_array($result);
					$query = 'INSERT IGNORE INTO ' .
						'db_to_ensembl ' .
						'VALUES ("mgi", "' . 
						$row['entryid'] . '", "' .
		mysql_real_escape_string($line[count($line) - 1]) . '")';
					mysql_query($query) or die($query .
						":\n" . mysql_error() . "\n");
					$count++;
					break;
				default:
					// what the hell do we do here?
					while ($row = mysql_fetch_array($result)) {
						$query = 'INSERT IGNORE INTO' .
						' db_to_ensembl VALUES ( ' .
						'"mgi", "' . $row['entryid'] .
						'", "' . 
		mysql_real_escape_string($line[count($line) - 1]) . '")';
						mysql_query($query) or die(
							$query . ":\n" . 
							mysql_error() . "\n");
					}
					$count++;
					break;
			}
			if ($count % 1000 == 0) {
				echo $count . ' ensembl IDs stored.' . "\n";
			}
		}
		fclose($ensembl);
/*	
		// run through the general file, accessing citations
		// and ensembl as necessary for lookup
		$count = 0;
		while (!feof($general)) {
			$line = explode("\t", fgets($general));
			if (count($line) < 10) continue;
			$id = mysql_real_escape_string($line[1]);
			$ensemblid = $this->extractEnsembl($ensembl, $id);
			$pubmed = $this->extractPubmed($citations, $id);

			// perform the query
			$query = 'INSERT INTO mgi (mgiid, pubmedid, ' .
				'goid, go_evidence_code, inferred_from, ' .
				'database_assigned_by, accession_ID) ' .
				'VALUES ("' . $id . '", ' .
				($pubmed ? intval($pubmed) : 0) . ', "' .
				mysql_real_escape_string($line[4]) . '", "' .
				mysql_real_escape_string($line[6]) . '", "' . 
				mysql_real_escape_string($line[7]) . '", "' .
				mysql_real_escape_string($line[14]) . '", "' .
				mysql_real_escape_string($line[16]) . '")';
			mysql_query($query) or die(mysql_error() . "\n");

			// also, insert the ensembl ID
			if ($ensemblid) {
			$query = 'INSERT INTO db_to_ensembl VALUES ("mgi", "' .
				mysql_insert_id() . '", "' .
				mysql_real_escape_string($ensemblid) . '")';
			mysql_query($query) or die(mysql_error() . "\n");
			}

			$count++;
			if ($count % 1000 == 0) {
				echo $count . ' entries inserted.' . "\n";
			}
		}

		// all done! close everything up
		fclose($general);
		fclose($citations);
		fclose($ensembl);
		*/
	}

	private function extractEnsembl($fp, $id) {
		$retval = null;
		while (!feof($fp) && !$retval) {
			$line = explode("\t", fgets($fp));
			if ($line[0] == $id) {
				$retval = $line[count($line) - 1];
			}
		}
		rewind($fp);
		return $retval;
	}

	private function extractPubmed($fp, $id) {
		$retval = null;
		while (!feof($fp) && !$retval) {
			$line = explode("\t", fgets($fp));
			if ($line[0] == $id) {
				$retval = $line[1];
			}
		}
		rewind($fp);
		return $retval;
	}

}

?>
