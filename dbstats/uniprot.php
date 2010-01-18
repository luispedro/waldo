<?php

class UniProt extends AbstractDB {

	public function populate() {
		return;
		$db = $this->getDB();
		$files = $this->getFiles();

		// open the file and start parsing out the entries
		$fp = @fopen($files['general'], 'r+') or die('Unable to open file ' . $files['general'] . ".\n");
		$count = 0;
		while (!feof($fp)) {
			$entry = $this->extractEntry($fp);

			// perform voodoo regex on this entry
			// to get the info we want out of it
			$id = $this->extractName($entry);
			$this->insertAccessions($entry, $id);
			$this->insertCitations($entry, $id);
			$this->insertComments($entry, $id);
		//	$this->insertDBReferences($entry, $id);

			$count++;
			if ($count % 1000 == 0) {
				echo $count . ' entries added.' . "\n";
			}
		}

		// all done!
		fclose($fp);
	}

	private function extractEntry($fp) {
		$retval = '';
		while (!feof($fp)) {
			$line = fgets($fp);
			$retval .= $line;
			if (strstr($line, '</entry>')) {
				// all done!
				return $retval;
			}
		}
	}

	private function extractName($entry) {
		$pattern = '#<name>(.*?)<\/name>#';
		$match = array();
		if (preg_match($pattern, $entry, $match) > 0) {
			return mysql_real_escape_string($match[1]);
		} else {
			die("Unable to extract name from:\n" . $entry . "\n");
		}
	}

	private function insertAccessions($entry, $id) {
		$pattern = '#<accession>(.*?)<\/accession>#';
		$matches = array();
		if (preg_match_all($pattern, $entry, $matches) > 0) {
			foreach ($matches[1] as $match) {
				$query = 'INSERT INTO uniprot_accessions ' .
					'VALUES ("' . $id . '", "' .
					mysql_real_escape_string($match) . '")';
				mysql_query($query) or die($query .
					": \n" . mysql_error() . "\n");
			}
		}
	}

	private function insertComments($entry, $id) {
		$pattern = '#<comment type=\"(.*?)\">[\s\S\w\W]*?<\/comment>#';
		$matches = array();
		if (preg_match_all($pattern, $entry, $matches) > 0) {
			for ($i = 0; $i < count($matches); $i++) {
				// build the query
				$query = 'INSERT INTO uniprot_comments ' .
					'(uniprot_id, comment_type, ' .
					'`fulltext`) ' .
					'VALUES ("' . $id . '", "' .
					mysql_real_escape_string($matches[1][$i]) .
					'", "' . 
					mysql_real_escape_string($matches[0][$i]) .
					'")';
				mysql_query($query) or die($query . 
					": \n" . mysql_error() . "\n");
			}
		} /*else {
			echo 'No comments found for entry ' . $id . "\n";
		}*/
	}

	private function insertDBReferences($entry, $id) {
		
	}

	private function insertCitations($entry, $id) {
		$pattern = '#<reference key=\"(.*?)\">[\s\S\w\W]*?<citation[\s\S\w\W]*?type=\"(.*?)\"[\s\S\w\W]*?<title>(.*?)<\/title>[\s\S\w\W]*?<\/reference>#';
		$matches = array();
		if (preg_match_all($pattern, $entry, $matches) > 0) {
			for ($i = 0; $i < count($matches[0]); $i++) {
				$query = 'INSERT INTO uniprot_citations ' .
					'VALUES ("' . $id . '", ' .
					$matches[1][$i] . ', "' .
					mysql_real_escape_string($matches[2][$i]) . '", "' .
					mysql_real_escape_string($matches[3][$i]) . '", "' .
					mysql_real_escape_string($matches[0][$i]) . '")';
				mysql_query($query) or die($query . ":\n" . 
							mysql_error() . "\n");
			}
		} /*else {
			echo 'No citations found for entry ' . $id . "\n";
		}*/
	}
}

?>
