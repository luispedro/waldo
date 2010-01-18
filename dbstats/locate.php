<?php

class LOCATE extends AbstractDB {

	public function populate() {
		return;
		$files = $this->getFiles();
		// go through both of them
		$count = 0;
		foreach ($files as $type => $file) {
			$fp = @fopen($file, 'r+') or die('Unable to open file ' . $file . ' for reading.' . "\n");

			$count = 0;
			while (($entry = $this->extractEntry($fp)) != null) {
				// get the next entry
				$entry = $this->extractEntry($fp);

				// pull out the ID
				$id = $this->extractID($entry);
				if (!$id) continue;

				// get the information
				$this->experimentalData($entry, $id, $type);
				$this->externalAnnotations($entry, $id);
				$this->predictions($entry, $id);
				$this->citations($entry, $id);

				$count++;
				if ($count % 1000 == 0) {
					echo $count . ' entries in ' . $type
						. ' done.' . "\n";
				}
			}
			fclose($fp);
		}
	}

	private function extractEntry($fp) {
		$retval = '';
		while (!feof($fp)) {
			$line = fgets($fp);
			$retval .= $line;
			if (strstr($line, '</LOCATE_protein>')) {
				return $retval;
			}
		}
		return null;
	}

	private function extractID($entry) {
		$pattern = '#<LOCATE_protein.*?uid="(.*?)".*?>#';
		$match = array();
		if (preg_match($pattern, $entry, $match) > 0) {
			return intval($match[1]);
		} else {
			return null;
		}
	}

	private function externalAnnotations($entry, $id) {
		$pattern = '#<xrefs>[\w\W\s\S]*?<\/xrefs>#';
		$match = array();
		if (preg_match($pattern, $entry, $match) == 0) {
			return null;
		}
		$pattern = '#<source source_id="(.*?)">[\w\s]*?<source_name>(.*?)<\/source_name>[\w\s]*?<accn>(.*?)<\/accn>[\w\s]*?<\/source>#';
		$matches = array();
		preg_match_all($pattern, $match[0], $matches);
		for ($i = 0; $i < count($matches[0]); $i++) {
			$query = 'INSERT INTO locate_external_annot ' .
				'(locate_id, source_id, source_name, accn)' .
				' VALUES (' . $id . ', ' . 
				intval($matches[1][$i]) . ', "' . 
				mysql_real_escape_string($matches[2][$i]) .
				'", "' .
				mysql_real_escape_string($matches[3][$i]) .
				'")';
/*
		$pattern = '#<externalannot>[\w\W\s\S]*?<\/externalannot>#';
		$match = array();
		if (preg_match($pattern, $entry, $match) == 0) {
			return null;
		}
		// we have the annotation
		// pull out the evidence, source name, and source id
		$pattern = '#<evidence>(.*?)<\/evidence>[\w\W\s\S]*?<source_name>(.*?)<\/source_name>[\w\W\s\S]*?<accn>(.*?)<\/accn>#';
		$matches = array();
		preg_match_all($pattern, $match[0], $matches);
		for ($i = 0; $i < count($matches[0]); $i++) {
			$query = 'INSERT INTO locate_external_annot ' .
				'(locate_id, evidence, source_name, ' .
				'source_id) VALUES (' . $id . ', "' . 
				mysql_real_escape_string($matches[1][$i]) .
				'", "' . 
				mysql_real_escape_string($matches[2][$i]) .
				'", "' .
				mysql_real_escape_string($matches[3][$i]) .
				'")';
*/
			mysql_query($query) or die($query . ":\n" . 
						mysql_error() . "\n");
		}
	}

	private function experimentalData($entry, $id, $type) {
		$pattern = '#<experimental_data>[\s\S\w\W]*?<\/experimental_data>#';
		$match = array();
		if (preg_match($pattern, $entry, $match) == 0) {
			return null;
		}
		// pull out images and coloc_images
		$pattern = '#(<images>[\w\W\s\S]*?<\/images>)[\w\W\s\S]*?(<coloc_images>[\w\W\s\S]*?<\/coloc_images>)#';
		$hit = array();
		preg_match($pattern, $match[0], $hit);
		
		// check if there was any content
		if (strstr($hit[1], 'no images')) {
			$hit[1] = null;
		}
		if (strstr($hit[2], 'no coloc_images')) {
			$hit[2] = null;
		}

		// make the query
		$query = 'INSERT INTO locate VALUES (' . $id . ', ' .
			($hit[1] ? '"' . $hit[1] . '", ' : 'NULL, ') .
			($hit[2] ? '"' . $hit[2] . '"' : 'NULL') . ', "' .
			$type . '")';
		mysql_query($query) or die($query . ":\n" . 
					mysql_error() . "\n");
	}

	private function predictions($entry, $id) {
		$pattern = '#<scl_prediction>[\w\W\s\S]*?<\/scl_prediction>#';
		$match = array();
		if (preg_match($pattern, $entry, $match) == 0) {
			return null;
		}
		$pattern = '#<source source_id="(.*?)">[\w\s]*?<method>(.*?)<\/method>[\w\s]*?<location>(.*?)<\/location>[\w\s]*?<goid>(.*?)<\/goid>[\w\s]*?<evaluation>(.*?)<\/evaluation>[\w\s]*?<\/source>#';
		$matches = array();
		preg_match_all($pattern, $match[0], $matches);
		for ($i = 0; $i < count($matches[0]); $i++) {
			$query = 'INSERT INTO locate_scl_predictions (' .
				'locate_id, source_id, method, location, ' .
				'goid, confidence) VALUES (' . $id . ', ' .
				intval($matches[1][$i]) . ', "' .
				mysql_real_escape_string($matches[2][$i]) .
				'", "' .
				mysql_real_escape_string($matches[3][$i]) .
				'", "' .
				mysql_real_escape_string($matches[4][$i]) .
				'", "' .
				mysql_real_escape_string($matches[5][$i]) .
				'")';
			mysql_query($query) or die($query . ":\n" .
						mysql_error() . "\n");
		}
	}

	private function citations($entry, $id) {
		$pattern = '#<literature>[\w\W\s\S]*?<\/literature>#';
		$match = array();
		if (preg_match($pattern, $entry, $match) == 0) {
			return null;
		}
		$pattern = '#<author>(.*?)<\/author>[\w\s]*?<title>(.*?)<\/title>[\w\s]*?<citation>(.*?)<\/citation>[\w\s\S\W]*?<source source_id="(.*?)">[\w\s]*?<source_name>(.*?)<\/source_name>[\w\s]*?<accn>(.*?)<\/accn>[\w\s]*?<\/source>#';
		$matches = array();
		preg_match_all($pattern, $match[0], $matches);
		for ($i = 0; $i < count($matches[0]); $i++) {
			$query = 'INSERT INTO locate_citations (' .
				'locate_id, author, title, citation_type, ' .
				'source_id, source_name, accn) VALUES (' .
				$id . ', "' . 
				mysql_real_escape_string($matches[1][$i]) .
				'", "' .
				mysql_real_escape_string($matches[2][$i]) .
				'", "' .
				mysql_real_escape_string($matches[3][$i]) .
				'", ' . intval($matches[4][$i]) . ', "' .
				mysql_real_escape_string($matches[5][$i]) .
				'", "' .
				mysql_real_escape_String($matches[6][$i]) .
				'")';
			mysql_query($query) or die($query . ":\n" . 
						mysql_error() . "\n");
		}
	}
}

?>
