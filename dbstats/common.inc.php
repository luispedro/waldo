<?php

require_once('abstractdb.php');

$DB = @mysql_pconnect('localhost', 'researchuser', 'r3NMYGccy7PLQp9b') or die('Unable to establish a database connection.' . "\n");
mysql_select_db('msdatabases');

// full database names and their abbreviations
$DATABASES = array(
			'MGI' => 'mgi',
			'eSLDB' => 'esldb',
			'LOCATE' => 'locate',
			'UniProt' => 'uniprot',
		);

// relative file locations to this script
$PREFIX = '../';

// associations of files with databases
$DB_FILES = array(
			'uniprot' => array(
				'general' => $PREFIX . 'uniprot_sprot.xml',
				),
			'esldb' => array(
				'mouse' => $PREFIX . 'eSLDB_Mus_musculus.txt',
				'human' => $PREFIX . 'eSLDB_Homo_sapiens.txt',
				),
			'locate' => array(
				'mouse' => $PREFIX . 'LOCATE_mouse_v6_20081121.xml',
				'human' => $PREFIX . 'LOCATE_human_v6_20081121.xml',
				),
			'mgi' => array(
				'ensembl' => $PREFIX . 'MRK_ENSEMBL.rpt',
				'citations' => $PREFIX . 'BIB_PubMed.rpt',
				'general' => $PREFIX . 'gene_association.mgi',
				),
		);
?>
